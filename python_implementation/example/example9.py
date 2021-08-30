import commonExample
import math
import sys
sys.path.insert(0,'..')
import generate
import constants
import numpy as np
import intersection
from matplotlib import pyplot as plt
from numpy import random
from os import path

saveGif = True

xcoords = [constants.width]
ycoords = [400]

gif_file="example9"

def updateCoords(xCor,yCor,frameNumber):
    lastFrame = False
    turnBack = False
    if frameNumber > constants.width/constants.step_size:
        turnBack = True
    if xCor[0] > constants.width + 10:
        lastFrame = True
    for i in range(0,len(xCor)):
        if turnBack == False:
            xCor[i] = xCor[i] - constants.step_size
        else:
            xCor[i] = xCor[i] + constants.step_size

        yCor[i] = 400 + int(300.0*math.sin(2.0*math.pi/(10.0)*float(frameNumber)))
    return lastFrame, xCor, yCor


def predictFunction9(state,t):
    position = state[0:2]
    velocity = state[2:4]
    if t > constants.width/constants.step_size:
        velocity[0] = constants.step_size
    else:
        velocity[0] = constants.step_size*(-1)
    velocity[1] = int(60.0*math.pi*math.cos(2.0*math.pi/(10.0)*float(t)))
 
    position_next = position + velocity#position#position + velocity
    velocity_next = velocity
    result = [position_next[0], position_next[1], velocity_next[0], velocity_next[1]]
    return np.array( result ) 

def predictFunctionJacobian9(state,t):
#    jacobian = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,#int(60.0*math.pi*math.cos(2.0*math.pi/(10.0)*float(t)))]])
    jacobian = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,int(12.0*math.pi*math.pi*math.cos(2.0*math.pi/(10.0)*float(t)))]])
    return jacobian


def boundBoxNoise9(x,y,index):
    center = 25
    multiplier = 5 
    arr = random.normal(size=(4,1))*multiplier
    return x+center+arr[0], y+center+arr[1], constants.orange_width - center*2+arr[2], constants.orange_width - center*2.5 + arr[3],None

tracker_arguments = {}
tracker_arguments["function"] = predictFunction9
tracker_arguments["jacobian"] = predictFunctionJacobian9

xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal,xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise,xBoxTrackerTotal,yBoxTrackerTotal,boxWidthTrackerTotal,boxHeightTrackerTotal,objectTypeTrackerTotal,boxIdTrackerTotal,trackedTotal = commonExample.common_run(updateCoords,gif_file,xcoords,ycoords,trackerArguments=tracker_arguments,saveToGif=saveGif,boundBoxNoise=boundBoxNoise9)

gif_file="example9_2"

xBoxCoordinateTotal2,yBoxCoordinateTotal2,boxWidthTotal2,boxHeightTotal2,objectTypeTotal2,xBoxCoordinateTotalNoise2,yBoxCoordinateTotalNoise2,boxWidthTotalNoise2,boxHeightTotalNoise2,objectTypeTotalNoise2,xBoxTrackerTotal2,yBoxTrackerTotal2,boxWidthTrackerTotal2,boxHeightTrackerTotal2,objectTypeTrackerTotal2,boxIdTrackerTotal2,trackedTotal2 = commonExample.common_run(updateCoords,gif_file,xcoords,ycoords,saveToGif=saveGif,boundBoxNoise=boundBoxNoise9)


plot_title = "Comparing when switching models"
plot_file_title = "example9_comparison.png"

iou = []
iou2 = []

for i in range(30,len(xBoxCoordinateTotalNoise)-30):
    iou.append(intersection.IOU(xBoxCoordinateTotal[i][0],yBoxCoordinateTotal[i][0],boxWidthTotal[i][0],boxHeightTotal[i][0],
        xBoxTrackerTotal[i][0],yBoxTrackerTotal[i][0],boxWidthTrackerTotal[i][0],boxHeightTrackerTotal[i][0]))
    iou2.append(intersection.IOU(xBoxCoordinateTotal2[i][0],yBoxCoordinateTotal2[i][0],boxWidthTotal2[i][0],boxHeightTotal2[i][0],
        xBoxTrackerTotal2[i][0],yBoxTrackerTotal2[i][0],boxWidthTrackerTotal2[i][0],boxHeightTrackerTotal2[i][0]))

line1, = plt.plot(iou,label='Custom model',color='red')
line3, = plt.plot([0,len(iou)],[sum(iou)/len(iou), sum(iou)/len(iou)], color='red', label='Average')
line2, = plt.plot(iou2,label='Default model',color='blue')
line4, = plt.plot([0,len(iou2)],[sum(iou2)/len(iou2), sum(iou2)/len(iou2)], color='blue', label='Average')
plt.xlabel('frame number')
plt.ylabel('Intersection Over Union')
plt.title(plot_title)
plt.legend(handles=[line1,line3,line2,line4])
plt.ylim(top=1)
plt.ylim(bottom=0)
plt.savefig(path.join("output",plot_file_title))
plt.close()

