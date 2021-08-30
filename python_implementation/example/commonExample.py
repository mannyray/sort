import sys
sys.path.insert(0,'..')
import generate
import math
import sort
import os
import numpy as np
from numpy import random
from PIL import Image, ImageDraw, ImageFont
import constants

def generateMeasurements(xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise):
    measurementsTotal = []
    for frame in range(0,len(xBoxCoordinateTotalNoise)):
        measurements = []
        for i in range(0,len(xBoxCoordinateTotalNoise[frame])):
            measurements.append(sort.measurement(xBoxCoordinateTotalNoise[frame][i],yBoxCoordinateTotalNoise[frame][i],
                boxWidthTotalNoise[frame][i],boxHeightTotalNoise[frame][i],objectTypeTotalNoise[frame][i]))
        measurementsTotal.append(measurements)
    return measurementsTotal

def trackMeasurements(measurementsTotal,trackerArguments):
    trackedTotal = []
    Tracker = sort.tracker()

    if "sensorNoise" in trackerArguments:
        Tracker.set_sensorNoise(trackerArguments["sensorNoise"])

    if "processNoise" in trackerArguments:
        Tracker.set_processNoise(trackerArguments["processNoise"])

    if "function" in trackerArguments:
        Tracker.set_predictFunction(trackerArguments["function"],trackerArguments["jacobian"])


    if "minimumIOU" in trackerArguments:
        Tracker.set_minimumIOU(trackerArguments["minimumIOU"])

    if "secondaryMinimumIOU" in trackerArguments:
        Tracker.set_secondaryMinimumIOU(trackerArguments["seconddaryMinimumIOU"])
        
    if "newShapeWeight" in trackerArguments:
        Tracker.set_newShapeWeight(trackerArguments["newShapeWeight"])

    if "threshold" in trackerArguments:
        Tracker.set_threshold(trackerArguments["threshold"])

    for frame in range(0,len(measurementsTotal)):
        Tracker.predictPhase(frame)
        Tracker.updatePhase(measurementsTotal[frame],frame)
        tracked = Tracker.getTracked()
        trackedTotal.append(tracked)
    return trackedTotal

def generateBoxesFromTrackedData(trackedTotal):
    xBoxTrackerTotal = []
    yBoxTrackerTotal = []
    boxWidthTrackerTotal = []
    boxHeightTrackerTotal = []
    boxIdTrackerTotal = []
    boxCovarianceTrackerTotal = []
    objectTypeTrackerTotal = []
    print("Drawing tracking data");
    for frame in range(0,len(trackedTotal)):
        print("drawing tracking "+str(frame)+"/"+str(len(trackedTotal)))
        tracked = trackedTotal[frame]
        xBoxTracker = []
        yBoxTracker = []
        boxWidthTracker= []
        boxHeightTracker = []
        boxIdTracker = []
        objectTypeTracker = []
        for i in range(0,len(tracked)):
            boxIdTracker.append(tracked[i].name)
            xBoxTracker.append(tracked[i].position[0][0])
            yBoxTracker.append(tracked[i].position[1][0])
            boxWidthTracker.append(tracked[i].width)
            boxHeightTracker.append(tracked[i].height)
            objectTypeTracker.append(tracked[i].objectType)
        boxIdTrackerTotal.append(boxIdTracker)
        xBoxTrackerTotal.append(xBoxTracker)
        yBoxTrackerTotal.append(yBoxTracker)
        boxWidthTrackerTotal.append(boxWidthTracker)
        boxHeightTrackerTotal.append(boxHeightTracker)
        objectTypeTrackerTotal.append(objectTypeTracker)
    return xBoxTrackerTotal, yBoxTrackerTotal, boxWidthTrackerTotal, boxHeightTrackerTotal, objectTypeTrackerTotal, boxIdTrackerTotal

def common_run(updateCoords,gif_file,xcoords,ycoords,boundBoxNoNoise=None,boundBoxNoise=None,drawImage=None,adjustMeasurementFrames=None,trackerArguments={},saveToGif=True,saveData=False,setTime=False,appendTime=0):

    if boundBoxNoise == None:
        boundBoxNoise = generate.boundBoxNoiseStandard

    if boundBoxNoNoise == None:
        boundBoxNoNoise = generate.boundBoxNoNoiseStandard

    if drawImage == None:
        drawImage = generate.drawImageStandard

    random.seed(1)

    xcoordTotal,ycoordTotal,frameCount = generate.generateCoordinates(xcoords, ycoords,updateCoords)
    xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal = generate.generateBoundingBox(xcoordTotal,ycoordTotal,boundBoxNoNoise)
    xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise = generate.generateBoundingBox(xcoordTotal,ycoordTotal,boundBoxNoise)

    if adjustMeasurementFrames != None:
        xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal,xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise =  adjustMeasurementFrames(xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal,xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise)

    if saveToGif == True:
        frames = generate.generateFrames(xcoordTotal,ycoordTotal,generate.cleanBackground,drawImage)

    measurementsTotal = generateMeasurements(xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise)

    trackedTotal = trackMeasurements(measurementsTotal,trackerArguments)
    xBoxTrackerTotal,yBoxTrackerTotal,boxWidthTrackerTotal,boxHeightTrackerTotal,objectTypeTrackerTotal,boxIdTrackerTotal = generateBoxesFromTrackedData(trackedTotal)

    if saveToGif == True:
        generate.drawBoxes(frames,xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,(100,100,100))
        generate.drawBoxes(frames,xBoxTrackerTotal,yBoxTrackerTotal,boxWidthTrackerTotal,boxHeightTrackerTotal,(0,150,0),objectTypeTrackerTotal,boxIdTrackerTotal)

        frameLengthOfMovement = constants.orange_width/constants.step_size
        duration=(math.floor(frameCount/frameLengthOfMovement)*constants.seconds_to_cross*1000)/frameCount
        if setTime == True:
            generate.addTime(frames,duration,appendTime)
        generate.saveToGif(frames,gif_file,duration)

    if saveData == True:
        output_folder = 'output_text'
        if not os.path.exists(output_folder):
            os.makedirs('output_text')
    	
    
        f = open(output_folder+"/"+gif_file+"_measurements.txt","w")
        for frame in range(0,len(measurementsTotal)):
            f.write("frame "+str(frame)+"\n")
            for j in range(0,len(measurementsTotal[frame])):
                str_to_write = "measure " + str(measurementsTotal[frame][j].x[0]) + " " + str(measurementsTotal[frame][j].y[0]) + " " + str(measurementsTotal[frame][j].width[0]) + " " + str(measurementsTotal[frame][j].height[0]) + " "+str(measurementsTotal[frame][j].objectType) +"\n"
                f.write(str_to_write)
        f.close()

        f = open(output_folder+"/"+gif_file+"_actual_tracked.txt","w")
        for frame in range(0,len(trackedTotal)):
            f.write("frame "+str(frame)+"\n")
            for j in range(0,len(trackedTotal[frame])):
                string = ""
                if trackedTotal[frame][j].objectType == None:
                    string = "None"
                str_to_write = "measure "+ str(trackedTotal[frame][j].position[0][0]) + " "+str(trackedTotal[frame][j].position[1][0])+" "+str(trackedTotal[frame][j].width)+" "+str(trackedTotal[frame][j].height) + " "+string+" "+str(trackedTotal[frame][j].name)+"\n"
                f.write(str_to_write)
        f.close()

    return xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal,xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise,xBoxTrackerTotal,yBoxTrackerTotal,boxWidthTrackerTotal,boxHeightTrackerTotal,objectTypeTrackerTotal,boxIdTrackerTotal,trackedTotal
