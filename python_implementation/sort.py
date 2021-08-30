import numpy as np
import hungarian
import intersection
import ddekf
from scipy import linalg 
import math
from copy import copy, deepcopy


class trackedObject:
    def __init__(self,position,width,height,velocity,velocity_covariance,time,name,objectType = None ):
        self.position = position
        self.velocity = velocity
        self.velocity_covariance = velocity_covariance
        self.velocity_covariance_sqrt = np.linalg.cholesky(velocity_covariance).transpose()
        self.last_update = time
        self.name = name
        self.objectType = objectType
        self.last_predict = time
        self.width = width
        self.height = height


class measurement():
    def __init__(self,x,y,width,height,objectType = None,percentage=None):
        self.x = x
        self.y = y
        self.position = np.array([x,y])
        self.percentage = percentage
        self.objectType = objectType
        self.width = width
        self.height = height

class tracker:
   
    def __init__(self,sensorNoise=np.array([[1,0],[0,1]]),processNoise=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]),predictFunction=None,predictFunctionJacobian=None,minimumIOU=0.001,newShapeWeight=1.0/10.0,threshold=4,initialVelocity=np.array([[0,0]]).transpose(),initialCovariance=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])):

        self.trackedObjectsByType = {}
        self.processNoise = processNoise
        self.sensorNoise = sensorNoise
        self.processNoiseSqrt = np.linalg.cholesky(self.processNoise).transpose()
        self.sensorNoiseSqrt = np.linalg.cholesky(self.sensorNoise).transpose()
        self.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]])
        self.minimum_IOU = minimumIOU
        self.threshold = threshold
        self.candidateCount = 0
        self.newShapeWeight = newShapeWeight

        if predictFunction == None:
            self.predictFunction = self.predictFunctionDefault
        else:
            self.predictFunction = predictFunction

        if predictFunctionJacobian == None:
            self.predictFunctionJacobian = self.predictFunctionJacobianDefault
        else:
            self.predictFunctionJacobian = predictFunctionJacobian

        self.initialCovariance = initialCovariance
        self.initialVelocity = initialVelocity

    def get_sensorNoise(self):
        return copy.copy(self.sensorNoise)

    def set_minimumIOU(self,iou):
        self.minimum_IOU = iou
        
    def set_threshold(self,threshold):
        self.threshold = threshold

    def set_sensorNoise(self,sensorNoise):
        self.sensorNoise = sensorNoise
        self.sensorNoiseSqrt = np.linalg.cholesky(self.sensorNoise).transpose()

    def get_processNoise(self):
        return copy.copy(self.processNoise)

    def set_processNoise(self,processNoise):
        self.processNoise = processNoise
        self.processNoiseSqrt = np.linalg.cholesky(self.processNoise).transpose()

    def set_predictFunction(self,function,jacobian):
        self.predictFunction = function
        self.predictFunctionJacobian = jacobian

    def set_newShapeWeight(self,weight):
        assert 0 <= weight and weight <= 1
        self.newShapeWeight = weight

    def predictFunctionDefault(self,state,t):
        position = state[0:2]
        velocity = state[2:4]
        position_next = position + velocity
        velocity_next = velocity
        result = [position_next[0], position_next[1], velocity_next[0], velocity_next[1]] 
        return np.array( result )

    def predictFunctionJacobianDefault(self,velocity,t):
        return np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]]) 
    
    def getTracked(self):
        resultArray = []
        for key in self.trackedObjectsByType:
            for trackedObject in self.trackedObjectsByType[key]:
                resultArray.append(deepcopy(trackedObject))
        return resultArray

    def getNorm(self, vector):
        result = 0
        for i in vector:
            result = result + vector[i]*vector[i]
        return result


    def predictPhase(self,time):
        for key in self.trackedObjectsByType:
            for i in range(0,len(self.trackedObjectsByType[key])):

                time_since_last_predict = time - self.trackedObjectsByType[key][i].last_predict

                if time_since_last_predict > 0:

                    state = np.array([self.trackedObjectsByType[key][i].position[0],self.trackedObjectsByType[key][i].position[1],
                            self.trackedObjectsByType[key][i].velocity[0]*time_since_last_predict,
                            self.trackedObjectsByType[key][i].velocity[1]*time_since_last_predict])


                    estimate, covariance_sqrt = ddekf.predictPhase(self.predictFunction, self.predictFunctionJacobian,time,
                        self.trackedObjectsByType[key][i].velocity_covariance_sqrt,state,self.processNoiseSqrt)


                    self.trackedObjectsByType[key][i].velocity = estimate[2:4]*(1.0/time_since_last_predict)
                    self.trackedObjectsByType[key][i].velocity_covariance_sqrt = covariance_sqrt
                    self.trackedObjectsByType[key][i].position = estimate[0:2]
                    self.trackedObjectsByType[key][i].last_predict = time


    def updatePhase(self,measurements,time):
        measurementByType = {}
        for measurement in measurements:
            if measurement.objectType not in measurementByType:
                measurementByType[measurement.objectType] = []
            measurementByType[measurement.objectType].append(measurement)

        for key in measurementByType:
            if key not in self.trackedObjectsByType:
                self.trackedObjectsByType[key] = []
            self.updatePhaseByObject(measurementByType[key],time,key)


        #identify objects that are too OLD
        for key in self.trackedObjectsByType:
            indexToPop = []
            for i in range(0,len(self.trackedObjectsByType[key])):
                if self.threshold < ( time - self.trackedObjectsByType[key][i].last_update ):
                    indexToPop.append(i)
            for index in sorted(indexToPop,reverse=True):
                del self.trackedObjectsByType[key][index]

    def updatePhaseByObject(self,measurements,time,key):
        
        for i in range(0,len(measurements)):
            if len(self.trackedObjectsByType[key]) == 0:
                self.candidateCount = self.candidateCount + 1
                self.trackedObjectsByType[key].append( 
                    trackedObject(measurements[i].position,measurements[i].width,
                    measurements[i].height,self.initialVelocity,
                    self.initialCovariance,time,"id-"+str(self.candidateCount),measurements[i].objectType))
                continue
            IOUTrackedObjectsToMeasurement = []
            for k in range(0,len(self.trackedObjectsByType[key])):
                iou = intersection.IOU(measurements[i].x,measurements[i].y,measurements[i].width,measurements[i].height,
                    self.trackedObjectsByType[key][k].position[0],self.trackedObjectsByType[key][k].position[1],
                    self.trackedObjectsByType[key][k].width,self.trackedObjectsByType[key][k].width);
                IOUTrackedObjectsToMeasurement.append(iou) 
            if max(IOUTrackedObjectsToMeasurement) < self.minimum_IOU: 
                self.candidateCount = self.candidateCount + 1
                self.trackedObjectsByType[key].append( 
                    trackedObject(measurements[i].position,measurements[i].width,
                    measurements[i].height,self.initialVelocity,
                    self.initialCovariance,time,"id-"+str(self.candidateCount),measurements[i].objectType))

        #more measurements than objects:
        #it means that there are two objects are really close together
        local_minimum_IOU = self.minimum_IOU
        while True:
            if local_minimum_IOU > 1:
                break
            if len(measurements) > len(self.trackedObjectsByType[key]):
                local_minimum_IOU = local_minimum_IOU + 0.1
                for i in range(0,len(measurements)):
                    IOUTrackedObjectsToMeasurement = []
                    for k in range(0,len(self.trackedObjectsByType[key])):
                        iou = intersection.IOU(measurements[i].x,measurements[i].y,measurements[i].width,measurements[i].height,
                            self.trackedObjectsByType[key][k].position[0],self.trackedObjectsByType[key][k].position[1],
                            self.trackedObjectsByType[key][k].width,self.trackedObjectsByType[key][k].width);
                        IOUTrackedObjectsToMeasurement.append(iou) 
                    if max(IOUTrackedObjectsToMeasurement) < local_minimum_IOU:
                        self.candidateCount = self.candidateCount + 1
                        self.trackedObjectsByType[key].append( 
                            trackedObject(measurements[i].position,measurements[i].width,
                            measurements[i].height,self.initialVelocity,
                            self.initialCovariance,time,"id-"+str(self.candidateCount),measurements[i].objectType))
            else:
                break

        #compute IOU
        candidateCount = len(self.trackedObjectsByType[key])
        candidateIDs = []
        for k in range(0,len(self.trackedObjectsByType[key])):
            candidateIDs.append(self.trackedObjectsByType[key][k])

        candidateOptions = [] 
        maxCandidate = 0
        for k in range(0,len(self.trackedObjectsByType[key])):
            optionsForKthObject = []
            for i in range(0,len(measurements)):
                iou = intersection.IOU(measurements[i].x,measurements[i].y,measurements[i].width,measurements[i].height,
                    self.trackedObjectsByType[key][k].position[0][0],self.trackedObjectsByType[key][k].position[1][0],
                    self.trackedObjectsByType[key][k].width,self.trackedObjectsByType[key][k].width)
                optionsForKthObject.append(iou)
                maxCandidate = max(maxCandidate,iou)
            candidateOptions.append(optionsForKthObject)

        #append dummy objects
        dummyCount = 0
        if len(measurements) > len(self.trackedObjectsByType[key]):
            dummyCount = len(measurements) - len(self.trackedObjectsByType[key])
            for i in range(0,dummyCount):
                candidateOptions.append([0]*len(measurements))
                candidateIDs.append("dummy"+str(i))
        candidateCount = candidateCount + dummyCount
        
        for k in range(0,len(self.trackedObjectsByType[key])):
            for i in range(0,len(measurements)):
                candidateOptions[k][i] = maxCandidate - candidateOptions[k][i]
        
        extraCount = 0
        if candidateCount > len(measurements):
            extraCount = candidateCount - len(measurements)
            for row in range(0,candidateCount):
                for i in range(0,extraCount):
                    candidateOptions[row].append(maxCandidate+1)

        selection = hungarian.hungarianAlgorithm(candidateCount,candidateIDs,candidateOptions)

        if selection == None:
            return

        #after matching boxes using hungarian algorithm
        #only matching stuff as some trackedObjects might be missing measurements
        for i in range(0,len(selection) - dummyCount):
            if (selection[i][1] >= len(measurements)):#other case
                continue
            
            #if the matched measurement's objectType does not match with the trackedObject's objectType
            #we ignore this matching
            if (measurements[selection[i][1]].objectType != self.trackedObjectsByType[key][i].objectType):
                continue
        
            state = np.array([self.trackedObjectsByType[key][i].position[0],self.trackedObjectsByType[key][i].position[1],
                    self.trackedObjectsByType[key][i].velocity[0],self.trackedObjectsByType[key][i].velocity[1]])
            measurement = np.array([measurements[selection[i][1]].position[0],measurements[selection[i][1]].position[1]])

            estimate,covariance_sqrt = ddekf.updatePhase( self.sensorNoiseSqrt, self.trackedObjectsByType[key][i].velocity_covariance_sqrt,
                self.measurementMatrix,state,measurement) 

            self.trackedObjectsByType[key][i].velocity = estimate[2:4]
            self.trackedObjectsByType[key][i].position = estimate[0:2]
            self.trackedObjectsByType[key][i].velocity_covariance_sqrt = covariance_sqrt

            self.trackedObjectsByType[key][i].width = int(float(self.trackedObjectsByType[key][i].width)*(1.0 - self.newShapeWeight) +  float(measurements[selection[i][1]].width)*(self.newShapeWeight))
            self.trackedObjectsByType[key][i].height = int(float(self.trackedObjectsByType[key][i].height)*(1.0 - self.newShapeWeight) +  float(measurements[selection[i][1]].height)*(self.newShapeWeight))
            self.trackedObjectsByType[key][i].last_update = time
            self.trackedObjectsByType[key][i].last_predict = time
