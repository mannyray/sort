import commonExample
import math
import sys
sys.path.insert(0,'..')
import generate
import constants
import intersection
from numpy import random
from matplotlib import pyplot as plt
from os import path

gif_file="example4"

xcoords = [constants.width,constants.width,constants.width]
ycoords = [50,350,700]

def boundBoxNoise4(x,y,index):
    center = 25
    multiplier = 0
    if y == 50:
        multiplier = 10
    if y == 350:
        multiplier = 25
    if y == 700:
        multiplier = 55
    arr = random.normal(size=(4,1))*multiplier
    return x+center+arr[0], y+center+arr[1], constants.orange_width - center*2+arr[2], constants.orange_width - center*2.5 + arr[3],None

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
    return lastFrame, xCor, yCor

xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal,xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise,xBoxTrackerTotal,yBoxTrackerTotal,boxWidthTrackerTotal,boxHeightTrackerTotal,objectTypeTrackerTotal,boxIdTrackerTotal,trackedTotal = commonExample.common_run(updateCoords,gif_file,xcoords,ycoords,boundBoxNoise=boundBoxNoise4 )


iou = []
iou2 = []
iou3 = []
for i in range(20,len(xBoxCoordinateTotalNoise)-30):
    print(i)
    iou.append(intersection.IOU(xBoxCoordinateTotal[i][0],yBoxCoordinateTotal[i][0],boxWidthTotal[i][0],boxHeightTotal[i][0],
        xBoxTrackerTotal[i][0],yBoxTrackerTotal[i][0],boxWidthTrackerTotal[i][0],boxHeightTrackerTotal[i][0]))
    iou2.append(intersection.IOU(xBoxCoordinateTotal[i][1],yBoxCoordinateTotal[i][1],boxWidthTotal[i][1],boxHeightTotal[i][1],
        xBoxTrackerTotal[i][1],yBoxTrackerTotal[i][1],boxWidthTrackerTotal[i][1],boxHeightTrackerTotal[i][1]))
    iou3.append(intersection.IOU(xBoxCoordinateTotal[i][2],yBoxCoordinateTotal[i][2],boxWidthTotal[i][2],boxHeightTotal[i][2],
        xBoxTrackerTotal[i][2],yBoxTrackerTotal[i][2],boxWidthTrackerTotal[i][2],boxHeightTrackerTotal[i][2]))

line1, = plt.plot(iou,label='IOU between top orange and its tracker',color='red')
#line3, = plt.plot([0,len(iou)],[sum(iou)/len(iou), sum(iou)/len(iou)], color='red', label='Average')
line2, = plt.plot(iou2,label='IOU between middle orange and its tracker',color='blue')
#line4, = plt.plot([0,len(iou2)],[sum(iou2)/len(iou2), sum(iou2)/len(iou2)], color='blue', label='Average')
line5, = plt.plot(iou3,label='IOU between bottom orange and its tracker',color='green')
#line6, = plt.plot([0,len(iou3)],[sum(iou3)/len(iou3), sum(iou3)/len(iou3)], color='green', label='Average')
plt.xlabel('frame number')
plt.ylabel('Intersection Over Union')
plt.title('Comparing effect of increasing measurement noise\non tracking capability')
plt.legend(handles=[line1,line2,line5])#[line1,line3,line2,line4,line5,line6])
plt.ylim(top=1)
plt.ylim(bottom=0)
plt.savefig(path.join("output",'example_4_IOU_comparison'))
plt.close()



