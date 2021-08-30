import commonExample
import math
import sys
sys.path.insert(0,'..')
import generate
import constants
import intersection

gif_file="example6"

xcoords = [ -600,-300,0,constants.width,constants.width + 300, constants.width + 600,  -600,-300,0,constants.width,constants.width + 300, constants.width + 600]
ycoords = [ 200,200,200,199,199,199,500,500,500,499,499,499]

def updateCoords(xCor,yCor,frameNumber):
    lastFrame = False
    for i in range(0,len(xCor)):
        if yCor[i] == 199:
            xCor[i] = xCor[i] - constants.step_size
        elif yCor[i] == 200 :
            xCor[i] = xCor[i] + constants.step_size
        elif yCor[i] == 499:
            xCor[i] = xCor[i] - constants.step_size
        elif yCor[i] == 500 :
            xCor[i] = xCor[i] + constants.step_size

    if xCor[0] > constants.width:
        lastFrame = True
    return lastFrame, xCor, yCor

def adjustMeasurementFrames6(xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal,
    xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise):

    for i in range(50,len(xBoxCoordinateTotal)-30):
        minXRight = xBoxCoordinateTotal[i][3]
        maxXRight = xBoxCoordinateTotal[i][5]
        indexToDelete = []
        for x in range(0,3):
            if intersection.IOU(minXRight,199,maxXRight - minXRight,199+constants.orange_width,
                    xBoxCoordinateTotal[i][x],yBoxCoordinateTotal[i][x],boxWidthTotal[i][x],boxHeightTotal[i][x]) > 0:
                if xBoxCoordinateTotal[i][x] + 100  < minXRight:
                    boxWidthTotal[i][x] = minXRight - xBoxCoordinateTotal[i][x]
                    boxWidthTotalNoise[i][x] = minXRight - xBoxCoordinateTotalNoise[i][x]
                elif xBoxCoordinateTotal[i][x] + boxWidthTotal[i][x] > maxXRight + 100:
                    boxWidthTotal[i][x] = boxWidthTotal[i][x] - ( maxXRight - xBoxCoordinateTotal[i][x] )
                    xBoxCoordinateTotal[i][x] = maxXRight + xBoxCoordinateTotal[i][x]*0
                    
                    boxWidthTotalNoise[i][x] = boxWidthTotalNoise[i][x] - ( maxXRight - xBoxCoordinateTotalNoise[i][x] )
                    xBoxCoordinateTotalNoise[i][x] = maxXRight + xBoxCoordinateTotalNoise[i][x]*0
                else:
                    indexToDelete.append(x)
        offset = 0 
        for index in indexToDelete:
            del objectTypeTotal[i][index - offset]
            del objectTypeTotalNoise[i][index - offset]
            del xBoxCoordinateTotalNoise[i][index - offset]
            del yBoxCoordinateTotalNoise[i][index - offset]
            del boxWidthTotalNoise[i][index - offset]
            del boxHeightTotalNoise[i][index - offset]
            del xBoxCoordinateTotal[i][index - offset]
            del yBoxCoordinateTotal[i][index - offset]
            del boxWidthTotal[i][index - offset]
            del boxHeightTotal[i][index - offset]
            offset = offset + 1

    return xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal,        xBoxCoordinateTotalNoise,yBoxCoordinateTotalNoise,boxWidthTotalNoise,boxHeightTotalNoise,objectTypeTotalNoise


commonExample.common_run(updateCoords,gif_file,xcoords,ycoords,adjustMeasurementFrames=adjustMeasurementFrames6)




