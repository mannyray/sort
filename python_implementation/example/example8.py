import commonExample
import math
import sys
import numpy as np
sys.path.insert(0,'..')
import generate
import constants
import intersection
from numpy import random
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from os import path

xBoxCoordinateTotalCollection = []
yBoxCoordinateTotalCollection = []
boxWidthTotalCollection = []
boxHeightTotalCollection = []
objectTypeTotalCollection = []
xBoxCoordinateTotalNoiseCollection = []
yBoxCoordinateTotalNoiseCollection = []
boxWidthTotalNoiseCollection = []
boxHeightTotalNoiseCollection = []
objectTypeTotalNoiseCollection = []
xBoxTrackerTotalCollection = []
yBoxTrackerTotalCollection = []
boxWidthTrackerTotalCollection = []
boxHeightTrackerTotalCollection = []
objectTypeTrackerTotalCollection = []
boxIdTrackerTotalCollection = []

messages = []

for whichNoiseHigher in range(0,2):
    for multiplierForSensorNoise in range(1,3): 

        saveGif = False
        gif_file="example8_1"+str(multiplierForSensorNoise)+"_"+str(whichNoiseHigher)

        xcoords = [ 100 ]
        ycoords = [ 200 ]

        tracker_arguments = {}
        
        plot_file_title = path.join("output","example8_")
        plot_title = ""
        if whichNoiseHigher == 0:
            plot_file_title = plot_file_title + "more_sensor_noise_"+str(multiplierForSensorNoise)+".png"
            plot_title = 'Assume high sensor noise.' 
            tracker_arguments["sensorNoise"] = 100*np.array([[1,0],[0,1]])
            tracker_arguments["processNoise"] = 0.1*np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
        else:
            plot_file_title = plot_file_title + "more_process_noise_"+str(multiplierForSensorNoise)+".png"
            plot_title = 'Assume high process noise.' 
            tracker_arguments["sensorNoise"] = 0.1*np.array([[1,0],[0,1]])
            tracker_arguments["processNoise"] = 100*np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])


        if multiplierForSensorNoise > 1:
            plot_title = plot_title + "\nExtra noisy measurements"
        else:
            plot_title = plot_title + "\nRegular noise measurements"

        messages.append(plot_title)

        def boundBoxNoise8(x,y,index):
            center = 25
            multiplier = 10*multiplierForSensorNoise*multiplierForSensorNoise
            arr = random.normal(size=(4,1))*multiplier
            return x+center+arr[0], y+center+arr[1], constants.orange_width - center*2+arr[2], constants.orange_width - center*2.5 + arr[3],None

        def updateCoords(xCor,yCor,frameNumber):
            lastFrame = False
            for i in range(0,len(xCor)):
                    xCor[i] = xCor[i] + constants.step_size
            if xCor[0] > constants.width/2:
                lastFrame = True
            return lastFrame, xCor, yCor

        xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal,xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise,xBoxTrackerTotal,yBoxTrackerTotal,boxWidthTrackerTotal,boxHeightTrackerTotal,objectTypeTrackerTotal,boxIdTrackerTotal,trackedTotal = commonExample.common_run(updateCoords,gif_file,xcoords,ycoords,trackerArguments=tracker_arguments,saveToGif=saveGif,boundBoxNoise=boundBoxNoise8)

        xBoxCoordinateTotalCollection.append(xBoxCoordinateTotal)
        yBoxCoordinateTotalCollection.append(yBoxCoordinateTotal)
        boxWidthTotalCollection.append(boxWidthTotal)
        boxHeightTotalCollection.append(boxHeightTotal)
        objectTypeTotalCollection.append(objectTypeTotal)
        xBoxCoordinateTotalNoiseCollection.append(xBoxCoordinateTotalNoise)
        yBoxCoordinateTotalNoiseCollection.append(yBoxCoordinateTotalNoise)
        boxWidthTotalNoiseCollection.append(boxWidthTotalNoise)
        boxHeightTotalNoiseCollection.append(boxHeightTotalNoise)
        objectTypeTotalNoiseCollection.append(objectTypeTotalNoise)
        xBoxTrackerTotalCollection.append(xBoxTrackerTotal)
        yBoxTrackerTotalCollection.append(yBoxTrackerTotal)
        boxWidthTrackerTotalCollection.append(boxWidthTrackerTotal)
        boxHeightTrackerTotalCollection.append(boxHeightTrackerTotal)
        objectTypeTrackerTotalCollection.append(objectTypeTrackerTotal)
        boxIdTrackerTotalCollection.append(boxIdTrackerTotal)

        iou = []
        iou2 = []

        for i in range(0,len(xBoxCoordinateTotalNoise)):
            iou.append(intersection.IOU(xBoxCoordinateTotalNoise[i][0],yBoxCoordinateTotalNoise[i][0],boxWidthTotalNoise[i][0],boxHeightTotalNoise[i][0],
                xBoxTrackerTotal[i][0],yBoxTrackerTotal[i][0],boxWidthTrackerTotal[i][0],boxHeightTrackerTotal[i][0]))
            iou2.append(intersection.IOU(xBoxCoordinateTotal[i][0],yBoxCoordinateTotal[i][0],boxWidthTotal[i][0],boxHeightTotal[i][0],
                xBoxTrackerTotal[i][0],yBoxTrackerTotal[i][0],boxWidthTrackerTotal[i][0],boxHeightTrackerTotal[i][0]))

        line1, = plt.plot(iou,label='Between estimated location and measurement',color='red')
        line3, = plt.plot([0,len(iou)],[sum(iou)/len(iou), sum(iou)/len(iou)], color='red', label='Average')
        line2, = plt.plot(iou2,label='Between estimated location and true location',color='blue')
        line4, = plt.plot([0,len(iou2)],[sum(iou2)/len(iou2), sum(iou2)/len(iou2)], color='blue', label='Average')
        plt.xlabel('frame number')
        plt.ylabel('Intersection Over Union')
        plt.title(plot_title)
        plt.legend(handles=[line1,line3,line2,line4])
        plt.ylim(top=1) 
        plt.ylim(bottom=0)
        plt.savefig(plot_file_title)
        plt.close()


xBoxCoordinateTotalGlobal = []
yBoxCoordinateTotalGlobal = []
for frame in range(0,len(xBoxCoordinateTotal)):
    xBoxCoordinateTotalGlobal_local = []
    yBoxCoordinateTotalGlobal_local = []
    for i in range(0,4):
        yAddition = 0
        xAddition = 0
        if i%2 == 0:
            yAddition = 400 
        if i >= 2:
            xAddition = 400
        xBoxCoordinateTotalGlobal_local.append(xBoxCoordinateTotal[frame][0] + xAddition)
        yBoxCoordinateTotalGlobal_local.append(yBoxCoordinateTotal[frame][0] + yAddition)
    xBoxCoordinateTotalGlobal.append(xBoxCoordinateTotalGlobal_local)
    yBoxCoordinateTotalGlobal.append(yBoxCoordinateTotalGlobal_local)


def drawImage8(image,draw,xcoords,ycoords,index):
    original = Image.open('assets/orange.jpg')
    image.paste(original, box=(xcoords[index],ycoords[index]))

gif_file = 'example8'
frames = generate.generateFrames(xBoxCoordinateTotalGlobal,yBoxCoordinateTotalGlobal,generate.cleanBackground,drawImage8)

for index in range(0,len(xBoxCoordinateTotalCollection)):

    yAddition = 0
    xAddition = 0
    if index%2 == 0:
        yAddition = 400 
    if index >= 2:
        xAddition = 400

    for i in range(0,len(xBoxCoordinateTotalNoiseCollection[index])):
        xBoxCoordinateTotalNoiseCollection[index][i][0][0] = xBoxCoordinateTotalNoiseCollection[index][i][0][0] + xAddition
        yBoxCoordinateTotalNoiseCollection[index][i][0][0] = yBoxCoordinateTotalNoiseCollection[index][i][0][0] + yAddition
        xBoxTrackerTotalCollection[index][i][0] = xBoxTrackerTotalCollection[index][i][0] + xAddition
        yBoxTrackerTotalCollection[index][i][0] = yBoxTrackerTotalCollection[index][i][0] + yAddition
        xBoxCoordinateTotalCollection[index][i][0] = xBoxCoordinateTotalCollection[index][i][0] + xAddition
        yBoxCoordinateTotalCollection[index][i][0] = yBoxCoordinateTotalCollection[index][i][0] + yAddition

    generate.drawBoxes(frames,xBoxCoordinateTotalNoiseCollection[index],yBoxCoordinateTotalNoiseCollection[index],boxWidthTotalNoiseCollection[index],boxHeightTotalNoiseCollection[index],(100,100,100))
    generate.drawBoxes(frames,xBoxCoordinateTotalCollection[index],yBoxCoordinateTotalCollection[index],boxWidthTotalCollection[index],boxHeightTotalCollection[index],(150,0,0))
    generate.drawBoxes(frames,xBoxTrackerTotalCollection[index],yBoxTrackerTotalCollection[index],boxWidthTrackerTotalCollection[index],boxHeightTrackerTotalCollection[index],(0,150,0),objectTypeTrackerTotalCollection[index],boxIdTrackerTotalCollection[index])

generate.saveToGif(frames,gif_file,70)
