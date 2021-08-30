import commonExample
import math
import sys
sys.path.insert(0,'..')
import generate
import constants
from numpy import random
import intersection
from PIL import Image, ImageDraw, ImageFont

gif_file="example7"


xcoords = [constants.width,constants.width,constants.width,100,400,700,1000,1300]
ycoords = [50,350,700,constants.height, constants.height, constants.height, constants.height, constants.height]

def updateCoords(xCor,yCor,frameNumber):
    lastFrame = False
    turnBackHorizontal = False
    turnBackVertical = False
    if frameNumber > constants.width/constants.step_size:
        turnBackHorizontal = True
    if frameNumber > constants.height/constants.step_size:
        turnBackVertical = True
    if yCor[3] > constants.height + 10:
        lastFrame = True
    for i in range(0,len(xCor)):
        if i < 3:
            if turnBackHorizontal == False:
                xCor[i] = xCor[i] - constants.step_size
            else:
                xCor[i] = xCor[i] + constants.step_size
        else:
            if turnBackVertical == False:
                yCor[i] = yCor[i] - constants.step_size
            else:
                yCor[i] = yCor[i] + constants.step_size
    return lastFrame, xCor, yCor

def drawImage7(image,draw,xcoords,ycoords,index):
    if index == 0:
        original = Image.open('assets/orange.jpg')
    elif index == 1:
        original = Image.open('assets/apple.jpg')
    elif index == 2:
        original = Image.open('assets/watermellon.jpg')
    elif index == 3:
        original = Image.open('assets/orange.jpg')
    elif index == 4:
        original = Image.open('assets/apple.jpg')
    elif index == 5:
        original = Image.open('assets/watermellon.jpg')
    elif index == 6:
        original = Image.open('assets/apple.jpg')
    elif index == 7:
        original = Image.open('assets/watermellon.jpg')
    
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    image.paste(original, box=(xcoords[index],ycoords[index]))
    draw.text((xcoords[index]+constants.orange_width/2,ycoords[index]+constants.orange_width/2),str(index+1),fill=(0,0,0), font=font)

def boundBoxNoNoise7(x,y,index):
    center = 25
    objectType = None
    if index == 0:
        objectType = "orange"
    if index == 1:
        objectType = "apple"
    if index == 2:
        objectType = "watermellon"
    if index == 3:
        objectType = "orange"
    if index == 4:
        objectType = "apple"
    if index == 5:
        objectType = "watermellon"
    elif index == 6:
        objectType = "apple"
    elif index == 7:
        objectType = "watermellon"
    return x+center, y+center, constants.orange_width - center*2, constants.orange_width - center*2.5,objectType

def boundBoxNoise7(x,y,index):
    multiplier = 10
    x,y,w,h,objectType = boundBoxNoNoise7(x,y,index)
    arr = random.normal(size=(4,1))*multiplier
    return x+arr[0], y+arr[1], w+arr[2], h+arr[3], objectType

commonExample.common_run(updateCoords,gif_file,xcoords,ycoords,boundBoxNoise=boundBoxNoise7,boundBoxNoNoise=boundBoxNoNoise7,drawImage=drawImage7,saveData=True)
