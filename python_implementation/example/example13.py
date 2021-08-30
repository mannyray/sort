import commonExample
import math
import sys
sys.path.insert(0,'..')
import generate
import constants
import intersection
import sort
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
from os import path
import numpy as np

xcoords = [constants.width]
ycoords = [0]

gif_file="example13"
saveGif = False


def updateCoords(xCor,yCor,frameNumber):
    lastFrame = False
    for i in range(0,len(xCor)):
        xCor[i] = xCor[i] - constants.step_size
        if xCor[i] + constants.orange_width < 0:
            xCor[i] = constants.width

    if xCor[0] <= 200:
        lastFrame = True

    return lastFrame, xCor, yCor

def drawImage13(image,draw,xcoords,ycoords,index):
    original = Image.open('assets/orange.jpg')
    image.paste(original, box=(xcoords[index],ycoords[index]))

xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal,xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise,xBoxTrackerTotal,yBoxTrackerTotal,boxWidthTrackerTotal,boxHeightTrackerTotal,objectTypeTrackerTotal,boxIdTrackerTotal,trackedTotal = commonExample.common_run(updateCoords,gif_file,xcoords,ycoords,saveToGif=saveGif)


#noisy measurements
#xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise

measurementsTotal = []
for frame in range(0,len(xBoxCoordinateTotalNoise)):
    measurements = []
    for i in range(0,len(xBoxCoordinateTotalNoise[frame])):
        measurements.append(sort.measurement(xBoxCoordinateTotalNoise[frame][i],yBoxCoordinateTotalNoise[frame][i],
            boxWidthTotalNoise[frame][i],boxHeightTotalNoise[frame][i],objectTypeTotalNoise[frame][i]))
    measurementsTotal.append(measurements)

trackedTotal = []
Tracker = sort.tracker()

trackedTotal2 = []
Tracker_every_second = sort.tracker()

trackedTotal3 = []
Tracker_every_third = sort.tracker()

trackedTotal4 = []
Tracker_every_fourth = sort.tracker()

trackedTotal5 = []
Tracker_every_fifth = sort.tracker()

for time in range(0, len(measurementsTotal)):
    Tracker.predictPhase(time)
    Tracker.updatePhase(measurementsTotal[time],time)
    tracked = Tracker.getTracked()
    trackedTotal.append(tracked)

    if time % 2 == 0:
        Tracker_every_second.predictPhase(time)
        Tracker_every_second.updatePhase(measurementsTotal[time],time)
        tracked = Tracker_every_second.getTracked()
        trackedTotal2.append(tracked)
    else:
        trackedTotal2.append(None)

    if time % 3 == 0:
        Tracker_every_third.predictPhase(time)
        Tracker_every_third.updatePhase(measurementsTotal[time],time)
        tracked = Tracker_every_third.getTracked()
        trackedTotal3.append(tracked)
    else:
        trackedTotal3.append(None)

    if time % 4 == 0:
        Tracker_every_fourth.predictPhase(time)
        Tracker_every_fourth.updatePhase(measurementsTotal[time],time)
        tracked = Tracker_every_fourth.getTracked()
        trackedTotal4.append(tracked)
    else:
        trackedTotal4.append(None)

    if time % 5 == 0:
        Tracker_every_fifth.predictPhase(time)
        Tracker_every_fifth.updatePhase(measurementsTotal[time],time)
        tracked = Tracker_every_fifth.getTracked()
        trackedTotal5.append(tracked)
    else:
        trackedTotal5.append(None)


plot_title = "Comparing when decreasing frequency of when measurements arrive"
plot_file_title = "example13_comparison.png"

iou = []
iou2 = []
iou3 = []
iou4 = []
iou5 = []

time1 = []
time2 = []
time3 = []
time4 = []
time5 = []

for i in range(0,len(xBoxCoordinateTotalNoise)):
    if len(trackedTotal[i]) == 0 or len(xBoxCoordinateTotal[i]) == 0:
        continue

    iou.append(intersection.IOU(trackedTotal[i][0].position[0],trackedTotal[i][0].position[1],trackedTotal[i][0].width,trackedTotal[i][0].height,
        xBoxCoordinateTotal[i][0],yBoxCoordinateTotal[i][0],boxWidthTotal[i][0],boxHeightTotal[i][0]))
    time1.append(i)
        
    if i % 2 == 0:
        iou2.append(intersection.IOU(trackedTotal2[i][0].position[0],trackedTotal2[i][0].position[1],trackedTotal2[i][0].width,trackedTotal2[i][0].height,
            xBoxCoordinateTotal[i][0],yBoxCoordinateTotal[i][0],boxWidthTotal[i][0],boxHeightTotal[i][0]))
        time2.append(i)

    if i % 3 == 0:
        iou3.append(intersection.IOU(trackedTotal3[i][0].position[0],trackedTotal3[i][0].position[1],trackedTotal3[i][0].width,trackedTotal3[i][0].height,
            xBoxCoordinateTotal[i][0],yBoxCoordinateTotal[i][0],boxWidthTotal[i][0],boxHeightTotal[i][0]))
        time3.append(i)

    if i % 4 == 0:
        iou4.append(intersection.IOU(trackedTotal4[i][0].position[0],trackedTotal4[i][0].position[1],trackedTotal4[i][0].width,trackedTotal4[i][0].height,
            xBoxCoordinateTotal[i][0],yBoxCoordinateTotal[i][0],boxWidthTotal[i][0],boxHeightTotal[i][0]))
        time4.append(i)

    if i % 5 == 0:
        iou5.append(intersection.IOU(trackedTotal5[i][0].position[0],trackedTotal5[i][0].position[1],trackedTotal5[i][0].width,trackedTotal5[i][0].height,
            xBoxCoordinateTotal[i][0],yBoxCoordinateTotal[i][0],boxWidthTotal[i][0],boxHeightTotal[i][0]))
        time5.append(i)


line1, = plt.plot(time1,iou,label='Measurement every second',color='red')
#line3, = plt.plot([0,max(time1)],[sum(iou)/len(iou), sum(iou)/len(iou)], color='red', label='Average')
line2, = plt.plot(time2,iou2,label='Measurement every 2nd second',color='blue')
#line4, = plt.plot([0,max(time1)],[sum(iou2)/len(iou2), sum(iou2)/len(iou2)], color='blue', label='Average')
line5, = plt.plot(time3,iou3,label='Measurement every 3rd second',color='green')
#line6, = plt.plot([0,max(time1)],[sum(iou3)/len(iou3), sum(iou3)/len(iou3)], color='green', label='Average')
line7, = plt.plot(time4,iou4,label='Measurement every 4th second', color='orange')
line9, = plt.plot(time5,iou5,label='Measurement every 5th second', color ='black')
plt.xlabel('frame number')
plt.ylabel('Intersection Over Union')
plt.title(plot_title)
#plt.legend(handles=[line1,line3,line2,line4,line5,line6])
plt.legend(handles=[line1,line2,line5,line7,line9])
plt.ylim(top=1)
plt.ylim(bottom=0)
plt.savefig(path.join("output",plot_file_title))
plt.close()
