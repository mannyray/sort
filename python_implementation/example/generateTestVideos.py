import commonExample
import sys
sys.path.insert(0,'..')
import generate
import constants

xcoordsFirstTrain = [0,300,600,900,1200,1500,1800,2100,2400,2700,3000,3300,3600,3900,4200,4500]
firstTrainLength = len(xcoordsFirstTrain)

xcoordsSecondTrain = [-300,-600,-900,-1200,-1500,-1800,-2100,-2400,-2700,-3000,-3300,-3600,-3900,-4200,-4500]
secondTrainLength = len(xcoordsSecondTrain)

xcoordsThirdTrain = [0,300,600,900,1200,1500,1800,2100,2400,2700,3000,3300,3600,3900,4200,4500]
for i in range(0,len(xcoordsThirdTrain)):
    xcoordsThirdTrain[i] = xcoordsThirdTrain[i] + constants.width
thirdTrainLength = len(xcoordsThirdTrain)

gif_file="big_gif"

xcoords = xcoordsFirstTrain
xcoords.extend(xcoordsSecondTrain)
xcoords.extend(xcoordsThirdTrain)

ycoords = [100]*len(xcoords)


def updateCoords(xCor,yCor,frameNumber):

    print(frameNumber)

    lastFrame = False
    firstTrain = xCor[firstTrainLength-1] > -300
    secondTrain = (not firstTrain) and xCor[firstTrainLength+secondTrainLength-1]<constants.width
    thirdTrain = firstTrain == False and secondTrain == False

    print(str(firstTrain) + " " + str(secondTrain) + " " +str(thirdTrain))
    
    if firstTrain:
        for i in range(0,firstTrainLength):
            xCor[i] = xCor[i] - constants.step_size
    if secondTrain:
        for i in range(firstTrainLength,firstTrainLength+secondTrainLength):
            xCor[i] = xCor[i] + constants.step_size
    if thirdTrain:
        for i in range(secondTrainLength+firstTrainLength,firstTrainLength+secondTrainLength+thirdTrainLength):
            xCor[i] = xCor[i] - constants.step_size

    if xCor[len(xCor)-1] < -3000:
        lastFrame = True
    #if frameNumber == 10:
    #    lastFrame = True
    return lastFrame, xCor, yCor



def updateCoords2(xCor,yCor,frameNumber):

    print(frameNumber)

    lastFrame = False
    firstTrain = xCor[firstTrainLength-1] > -300
    secondTrain = (not firstTrain) and xCor[firstTrainLength+secondTrainLength-1]<constants.width
    thirdTrain = firstTrain == False and secondTrain == False

    print(str(firstTrain) + " " + str(secondTrain) + " " +str(thirdTrain))
    
    if firstTrain:
        for i in range(0,firstTrainLength):
            xCor[i] = xCor[i] - constants.step_size
    if secondTrain:
        for i in range(firstTrainLength,firstTrainLength+secondTrainLength):
            xCor[i] = xCor[i] + constants.step_size
    if thirdTrain:
        for i in range(secondTrainLength+firstTrainLength,firstTrainLength+secondTrainLength+thirdTrainLength):
            xCor[i] = xCor[i] - constants.step_size

    if xCor[len(xCor)-1] < -3000:
        lastFrame = True
    if frameNumber == 99:
        lastFrame = True

    return lastFrame, xCor, yCor


xcoordsLocal = xcoords.copy()
ycoordsLocal = ycoords.copy()
frameNumberLocal = 0
xTotal = []
yTotal = []
while True:
    print("test "+str(frameNumberLocal))
    lastFrameLocal,xcoordsLocal,ycoordsLocal = updateCoords(xcoordsLocal,ycoordsLocal,frameNumberLocal)
    frameNumberLocal = frameNumberLocal + 1
    xTotal.append(xcoordsLocal.copy())
    yTotal.append(ycoordsLocal.copy())
    if lastFrameLocal:
        break

print(len(xTotal))
print(len(ycoordsLocal))

for i in range(0,18):
    appendTime = 90*(i*100)#89.10891089108911*(i*100) 
    commonExample.common_run(updateCoords2,gif_file+str(i),xTotal[i*100],yTotal[i],saveData=True,setTime=True,appendTime=appendTime)




