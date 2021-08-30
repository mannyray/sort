import commonExample
import math
import sys
sys.path.insert(0,'..')
import generate
import constants

gif_file="example5"

frequency = 30.0
frameNumber = -1
xcoords = [1100 + int(100.0*math.sin(2.0*math.pi/frequency*(float(frameNumber) + float(0)*15.0 ) )), 1100 + int(100.0*math.sin((2.0*math.pi/frequency)*(float(frameNumber) + float(1)*15.0 ) ))]
ycoords = [ 500 + int(100.0*math.cos(2.0*math.pi/frequency*(float(frameNumber) + float(0)*15.0 ))), 500 + int(100.0*math.cos((2.0*math.pi/frequency)*(float(frameNumber) + float(1)*15.0 ))) ]


def updateCoords(xCor,yCor,frameNumber):
    lastFrame = False
    for i in range(0,len(xCor)):
        xCor[i] = 1100 + int(100.0*math.sin((2.0*math.pi/frequency)*(float(frameNumber) + float(i)*15.0 ) ))
        yCor[i] = 500 + int(100.0*math.cos((2.0*math.pi/frequency)*(float(frameNumber) + float(i)*15.0 )))

    if frameNumber == 200:
       lastFrame = True
    return lastFrame, xCor, yCor

commonExample.common_run(updateCoords,gif_file,xcoords,ycoords)

