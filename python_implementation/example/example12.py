import commonExample
import math
import sys
sys.path.insert(0,'..')
import generate
import constants
from PIL import Image, ImageDraw, ImageFont

xcoords = [constants.width]
ycoords = [0]

gif_file="example12"
saveGif = False

tracker_arguments = {}


def updateCoords(xCor,yCor,frameNumber):
    lastFrame = False
    for i in range(0,len(xCor)):
        xCor[i] = xCor[i] - constants.step_size
        if xCor[i] + constants.orange_width < 0:
            xCor[i] = constants.width

    if xCor[0] <= constants.width - int(constants.width/2):
        lastFrame = True

    return lastFrame, xCor, yCor

def drawImage12(image,draw,xcoords,ycoords,index):
    original = Image.open('assets/orange.jpg')
    image.paste(original, box=(xcoords[index],ycoords[index]))


def adjustMeasurementFrames12(xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal,
    xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise):

    for i in range(40,len(xBoxCoordinateTotal)):
        xBoxCoordinateTotal[i] = []
        yBoxCoordinateTotal[i] = []
        boxWidthTotal[i] = []
        boxHeightTotal[i] = []
        objectTypeTotal[i] = []
        xBoxCoordinateTotalNoise[i] = []
        yBoxCoordinateTotalNoise[i] = []
        boxWidthTotalNoise[i] = []
        boxHeightTotalNoise[i] = []
        objectTypeTotalNoise[i] = []

    return xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal,xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise

tracker_arguments["threshold"] = 4
xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal,xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise,xBoxTrackerTotal,yBoxTrackerTotal,boxWidthTrackerTotal,boxHeightTrackerTotal,objectTypeTrackerTotal,boxIdTrackerTotal,trackedTotal = commonExample.common_run(updateCoords,gif_file,xcoords,ycoords,trackerArguments=tracker_arguments,saveToGif=saveGif,adjustMeasurementFrames=adjustMeasurementFrames12)

tracker_arguments["threshold"] = 8
xBoxCoordinateTotal2,yBoxCoordinateTotal2,boxWidthTotal2,boxHeightTotal2,objectTypeTotal2,xBoxCoordinateTotalNoise2,yBoxCoordinateTotalNoise2,boxWidthTotalNoise2,boxHeightTotalNoise2,objectTypeTotalNoise2,xBoxTrackerTotal2,yBoxTrackerTotal2,boxWidthTrackerTotal2,boxHeightTrackerTotal2,objectTypeTrackerTotal2,boxIdTrackerTotal2,trackedTotal2 = commonExample.common_run(updateCoords,gif_file,xcoords,ycoords,trackerArguments=tracker_arguments,saveToGif=saveGif,adjustMeasurementFrames=adjustMeasurementFrames12)

tracker_arguments["threshold"] = 12
xBoxCoordinateTotal3,yBoxCoordinateTotal3,boxWidthTotal3,boxHeightTotal3,objectTypeTotal3,xBoxCoordinateTotalNoise3,yBoxCoordinateTotalNoise3,boxWidthTotalNoise3,boxHeightTotalNoise3,objectTypeTotalNoise3,xBoxTrackerTotal3,yBoxTrackerTotal3,boxWidthTrackerTotal3,boxHeightTrackerTotal3,objectTypeTrackerTotal3,boxIdTrackerTotal3,trackedTotal3 = commonExample.common_run(updateCoords,gif_file,xcoords,ycoords,trackerArguments=tracker_arguments,saveToGif=saveGif,adjustMeasurementFrames=adjustMeasurementFrames12)


xBoxCoordinateTotalGlobal = []
yBoxCoordinateTotalGlobal = []
for frame in range(0,len(xBoxCoordinateTotal)):
    xBoxCoordinateTotalGlobal_local = []
    yBoxCoordinateTotalGlobal_local = []
    for i in range(0,3):
        yAddition = 0
        xAddition = 0
        if i == 1:
            yAddition = 400
        if i == 2:
            yAddition = 800
        if len(xBoxCoordinateTotal[frame]) > 0:
            xBoxCoordinateTotalGlobal_local.append(xBoxCoordinateTotal[frame][0] + xAddition)
            yBoxCoordinateTotalGlobal_local.append(yBoxCoordinateTotal[frame][0] + yAddition)
    xBoxCoordinateTotalGlobal.append(xBoxCoordinateTotalGlobal_local)
    yBoxCoordinateTotalGlobal.append(yBoxCoordinateTotalGlobal_local)

frames = generate.generateFrames(xBoxCoordinateTotalGlobal,yBoxCoordinateTotalGlobal,generate.cleanBackground,drawImage12)



yAddition = 0
xAddition = 0

for i in range(0,len(xBoxCoordinateTotal)):
    if len(xBoxCoordinateTotalNoise[i]) > 0:
        xBoxCoordinateTotalNoise[i][0][0] = xBoxCoordinateTotalNoise[i][0][0] + xAddition
        yBoxCoordinateTotalNoise[i][0][0] = yBoxCoordinateTotalNoise[i][0][0] + yAddition
    if len(xBoxTrackerTotal[i]) > 0:
        xBoxTrackerTotal[i][0] = xBoxTrackerTotal[i][0] + xAddition
        yBoxTrackerTotal[i][0] = yBoxTrackerTotal[i][0] + yAddition

generate.drawBoxes(frames,xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,(100,100,100))
generate.drawBoxes(frames,xBoxTrackerTotal,yBoxTrackerTotal,boxWidthTrackerTotal,boxHeightTrackerTotal,(0,150,0),objectTypeTrackerTotal,boxIdTrackerTotal)

yAddition = 400
xAddition = 0

for i in range(0,len(xBoxCoordinateTotal2)):
    if len(xBoxCoordinateTotalNoise2[i]) > 0:
        xBoxCoordinateTotalNoise2[i][0][0] = xBoxCoordinateTotalNoise2[i][0][0] + xAddition
        yBoxCoordinateTotalNoise2[i][0][0] = yBoxCoordinateTotalNoise2[i][0][0] + yAddition
    if len(xBoxTrackerTotal2[i]) > 0:
        xBoxTrackerTotal2[i][0] = xBoxTrackerTotal2[i][0] + xAddition
        yBoxTrackerTotal2[i][0] = yBoxTrackerTotal2[i][0] + yAddition

generate.drawBoxes(frames,xBoxCoordinateTotalNoise2,yBoxCoordinateTotalNoise2,boxWidthTotalNoise2,boxHeightTotalNoise2,(100,100,100))
generate.drawBoxes(frames,xBoxTrackerTotal2,yBoxTrackerTotal2,boxWidthTrackerTotal2,boxHeightTrackerTotal2,(0,150,0),objectTypeTrackerTotal2,boxIdTrackerTotal2)

yAddition = 800
xAddition = 0

for i in range(0,len(xBoxCoordinateTotal3)):
    if len(xBoxCoordinateTotalNoise3[i]) > 0:
        xBoxCoordinateTotalNoise3[i][0][0] = xBoxCoordinateTotalNoise3[i][0][0] + xAddition
        yBoxCoordinateTotalNoise3[i][0][0] = yBoxCoordinateTotalNoise3[i][0][0] + yAddition
    if len(xBoxTrackerTotal3[i]) > 0:
        xBoxTrackerTotal3[i][0] = xBoxTrackerTotal3[i][0] + xAddition
        yBoxTrackerTotal3[i][0] = yBoxTrackerTotal3[i][0] + yAddition

generate.drawBoxes(frames,xBoxCoordinateTotalNoise3,yBoxCoordinateTotalNoise3,boxWidthTotalNoise3,boxHeightTotalNoise3,(100,100,100))
generate.drawBoxes(frames,xBoxTrackerTotal3,yBoxTrackerTotal3,boxWidthTrackerTotal3,boxHeightTrackerTotal3,(0,150,0),objectTypeTrackerTotal3,boxIdTrackerTotal3)


generate.saveToGif(frames,gif_file,150)


