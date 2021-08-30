import commonExample
import sys
sys.path.insert(0,'..')
import generate
import constants

xcoords = [0,300,600,900,1200,1500,1800]
ycoords = [100,100,100,100,100,100,100]

gif_file="example1"

def updateCoords(xCor,yCor,frameNumber):
    lastFrame = False
    for i in range(0,len(xCor)):
        xCor[i] = xCor[i] - constants.step_size
        if xCor[i] + constants.orange_width < 0:
            xCor[i] = constants.width

    if xCor[0] == 0:
        lastFrame = True

    return lastFrame, xCor, yCor

commonExample.common_run(updateCoords,gif_file,xcoords,ycoords,saveData=True,setTime=True)

