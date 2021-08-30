import sys
import math
from PIL import Image, ImageDraw, ImageFont
import os
import copy
import numpy as np
import constants
from numpy import random
import os.path
from os import path
import time

def generateCoordinates(xcoordsInitial,ycoordsInitial,updateCoordinateFunction):
    xcoordTotal = [xcoordsInitial]
    ycoordTotal = [ycoordsInitial]

    xcoords = xcoordsInitial[:]
    ycoords = ycoordsInitial[:]

    frame = 0
    while True:
        lastFrame, xcoords, ycoords = updateCoordinateFunction(xcoords, ycoords, frame)

        xcoordTotal.append(xcoords[:])
        ycoordTotal.append(ycoords[:])

        frame = frame + 1
        if lastFrame:
            break
    return xcoordTotal, ycoordTotal,frame

def adjustBasedOnBounding(x,y,w,h,width,height):
    inBounding = True
    if x + w < 0:
        inBounding = False
    if x < 0:
        w = w + x
        x = x * 0
    if x > width:   
        inBounding = False
    if x + w > width:
        w = width - x
    if y + h < 0:
        inBounding = False
    if y < 0:
        h = h + y
        y = y * 0
    if y > height:
        inBounding = False
    if y + h > height:
        h = height - y  


    identifyingDistance = 150
    if w < identifyingDistance and  (abs( x - 0 ) < identifyingDistance or abs(x - width) < identifyingDistance):
        inBounding = False
    if h < identifyingDistance and  (abs( y - 0 ) < identifyingDistance or abs(y - height) < identifyingDistance):
        inBounding = False

    return x,y,w,h,inBounding
        

def generateBoundingBox(xcoordTotal,ycoordTotal,boundingBoxFunction):
    xBoxCoordinateTotal = []
    yBoxCoordinateTotal = []
    boxWidthTotal = []
    boxHeightTotal = []
    objectTypeTotal = []
    for frame in range(0,len(xcoordTotal)):
        xBoxCoordinate = []
        yBoxCoordinate = []
        boxWidth = []
        boxHeight = []
        objectTypeSingle = []
        for i in range(0,len(xcoordTotal[frame])):
            x,y,w,h,objectType = boundingBoxFunction(xcoordTotal[frame][i],ycoordTotal[frame][i],i)
            x,y,w,h,inBounding = adjustBasedOnBounding(x,y,w,h,constants.width,constants.height)
            if inBounding == False:
                continue
            xBoxCoordinate.append(x)
            yBoxCoordinate.append(y)
            boxWidth.append(w)
            boxHeight.append(h)
            objectTypeSingle.append(objectType)
        xBoxCoordinateTotal.append(xBoxCoordinate)
        yBoxCoordinateTotal.append(yBoxCoordinate)
        boxWidthTotal.append(boxWidth)
        boxHeightTotal.append(boxHeight)
        objectTypeTotal.append(objectTypeSingle)
    return xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,objectTypeTotal
        
def generateFrames(xcoordTotal,ycoordTotal,backgroundDraw,drawItem):
    print("Generating jpgs")
    for frame in range(0,len(xcoordTotal)):
        #draw clean background
        image, draw = backgroundDraw()

        #draw all the objects
        for i in range(0,len(xcoordTotal[frame])):
            drawItem(image,draw,xcoordTotal[frame],ycoordTotal[frame],i)

        image.save('test'+str(frame)+'.jpg')
        print("Generating frame "+str(frame)+"/"+str(len(xcoordTotal)))

    imgs = []
    for i in range(0,frame):
        imgs.append("test"+str(i)+".jpg")

    frames = []
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    for i in range(0,len(xcoordTotal)):
        os.remove("test"+str(i)+".jpg")

    return frames

def saveToGif(frames,name,duration):
    if path.exists("output") == False:
        os.mkdir("output")
    for i in range(0,(len(frames))):
        frames[i] = frames[i].resize((int(constants.width/2),int(constants.height/2)),Image.ANTIALIAS)
    frames[0].save(path.join("output",name+'.gif'),format='GIF',append_images=frames[1:],duration=duration,save_all=True,loop=0)

def boundBoxNoiseStandard(x,y,index):
    center = 25
    arr = random.normal(size=(4,1))*7
    return x+center+arr[0], y+center+arr[1], constants.orange_width - center*2+arr[2], constants.orange_width - center*2.5 + arr[3],None

def boundBoxNoNoiseStandard(x,y,index):
        center = 25
        return x+center, y+center, constants.orange_width - center*2, constants.orange_width - center*2.5,None

def addTime(frames,timeBetweenEachFrameInMilli,offset=0):
    rollingTimeSum = offset
    for frame in range(0,len(frames)):
        draw = ImageDraw.Draw(frames[frame])
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",60)
        seconds=(rollingTimeSum/1000.0)%60.0
        seconds = int(seconds)
        minutes=(rollingTimeSum/(1000.0*60.0))%60.0
        minutes = int(minutes)
        hours=(rollingTimeSum/(1000.0*60.0*60.0))%24.0
        hours = int(hours)
        residue = rollingTimeSum - (float(hours*60*60*1000) + float(minutes*60*1000) + float(seconds * 1000))
        str_time = "%02d:%02d:%02d:%03d"%(hours,minutes,seconds,residue)
        draw.text((constants.width/2-200,constants.height/2-100),str_time,fill=(0,0,0),font=font)
        rollingTimeSum = rollingTimeSum + timeBetweenEachFrameInMilli
    return frames


def drawBoxes(frames,xBoxCoordinateTotal,yBoxCoordinateTotal,boxWidthTotal,boxHeightTotal,color,objectTypeTotal=None,IDs = None, covariances = None):
    for frame in range(0,len(frames)): 
        draw = ImageDraw.Draw(frames[frame])
        for box in range(0,len(xBoxCoordinateTotal[frame])):
            draw.rectangle((xBoxCoordinateTotal[frame][box],yBoxCoordinateTotal[frame][box],
                boxWidthTotal[frame][box]+xBoxCoordinateTotal[frame][box],
                boxHeightTotal[frame][box]+yBoxCoordinateTotal[frame][box]), outline = color,width=5)
            if IDs != None:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
                draw.text((xBoxCoordinateTotal[frame][box],yBoxCoordinateTotal[frame][box]),IDs[frame][box],fill=(0,0,0), font=font)
                if objectTypeTotal[frame][box] != None:
                    draw.text((xBoxCoordinateTotal[frame][box],yBoxCoordinateTotal[frame][box]+20),objectTypeTotal[frame][box],fill=(0,0,0), font=font)
                else:
                    draw.text((xBoxCoordinateTotal[frame][box],yBoxCoordinateTotal[frame][box]+20),"unclassified object type",fill=(0,0,0), font=font)
    return frames

def drawImageStandard(image,draw,xcoords,ycoords,index):
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    original = Image.open('assets/orange.jpg')
    image.paste(original, box=(xcoords[index],ycoords[index]))
    draw.text((xcoords[index]+constants.orange_width/2,ycoords[index]+constants.orange_width/2),str(index+1),fill=(0,0,0), font=font)


def cleanBackground():
    image = Image.new( 'RGB', ( constants.width, constants.height ) )
    draw = ImageDraw.Draw(image)
    draw.rectangle ((0,0,constants.width,constants.height), fill = (255,255,255) )
    return image, draw
