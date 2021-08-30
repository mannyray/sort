import commonExample
import sys
sys.path.insert(0,'..')
import generate
import constants

xcoords = [constants.width, constants.width + 300, constants.width + 600]
ycoords = [100,100,100]

gif_file="example2"

step_size=10
orange_width = 300

def updateCoords(xCor,yCor,frameNumber):
    lastFrame = False
    turnBack = False
    if frameNumber > constants.width/constants.step_size:
        turnBack = True
    if xCor[0] > 1805:
        lastFrame = True
    for i in range(0,len(xCor)):
        if turnBack == False:
            xCor[i] = xCor[i] - constants.step_size
        else:
            xCor[i] = xCor[i] + constants.step_size
    return lastFrame, xCor, yCor

commonExample.common_run(updateCoords,gif_file,xcoords,ycoords)
