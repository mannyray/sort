import commonExample
import math
import sys
sys.path.insert(0,'..')
import generate
import constants

xcoords = [constants.width,constants.width + 300,constants.width + 600]
ycoords = [400,400,400]

gif_file="example3"

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

        yCor[i] = 400 + int(200.0*math.sin(2.0*math.pi/(float(i)*20.0+10.0)*float(frameNumber)))
    return lastFrame, xCor, yCor

commonExample.common_run(updateCoords,gif_file,xcoords,ycoords)
