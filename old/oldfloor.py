import numpy as np
import math
from threedimfunctions import *
def makeFloor(app, event): 
    if app.floorCoords.shape[0] == 0: #rows
        leftTopCoord = np.array([[event.x, event.y]])
        app.floorCoords = np.append(app.floorCoords, leftTopCoord, axis=0)
        for i in range(4):
            app.tempFloorCoords = np.append(app.tempFloorCoords, 
                                            leftTopCoord, axis=0)
    elif app.floorCoords.shape[0] == 1: #rows
        rightBotCoord = np.array([[event.x, event.y]])

        tempCoords = np.append(app.floorCoords, rightBotCoord, axis=0)
        tempVecs = graph2Vecs(app, tempCoords)

        leftTopVec, rightBotVec = tempVecs[0], tempVecs[1]

        #finding [x,y,z] of rightTopCoord 
        xRT = rightBotVec[0]
        yRT = leftTopVec[1]
        zRT = 0 
        rightTopVec = np.array([[xRT,yRT,zRT]])

        #finding [x,y,z] of leftBotCoord 
        xLB = leftTopVec[0] # rightBotVec[0]
        yLB = rightBotVec[1] #+ leftTopVec[1]
        zLB = 0
        leftBotVec = np.array([[xLB, yLB, zLB]])

        tempVecs2 = np.append(rightTopVec, leftBotVec, axis=0)
        tempCoords2 = vecs2Graph(app, tempVecs2)

        rightTopCoord, leftBotCoord = [tempCoords2[0]], [tempCoords2[1]]
        
        app.floorCoords = np.append(app.floorCoords,leftBotCoord, axis=0)
        app.floorCoords = np.append(app.floorCoords,rightTopCoord, axis=0)
        app.floorCoords = np.append(app.floorCoords,rightBotCoord, axis=0) 

        app.floorVecs = graph2Vecs(app, app.floorCoords) #store for rotation adjustment later
        #print(f'floor: \n{app.floorCoords}')
        #app.rightWallCoords = np.array([app.floorCoords[2], app.floorCoords[3]])
        #print(app.rightWallCoords)

def floatFloor(app, event): 
    rightBotCoord = np.array([[event.x, event.y]])

    tempCoords = np.append(app.floorCoords, rightBotCoord, axis=0)
    tempVecs = graph2Vecs(app, tempCoords)

    leftTopVec, rightBotVec = tempVecs[0], tempVecs[1]

    #finding [x,y,z] of rightTopCoord 
    xRT = rightBotVec[0]
    yRT = leftTopVec[1]
    zRT = 0 
    rightTopVec = np.array([[xRT,yRT,zRT]])

    #finding [x,y,z] of leftBotCoord 
    xLB = leftTopVec[0] # rightBotVec[0]
    yLB = rightBotVec[1] #+ leftTopVec[1]
    zLB = 0
    leftBotVec = np.array([[xLB, yLB, zLB]])

    tempVecs2 = np.append(rightTopVec, leftBotVec, axis=0)
    tempCoords2 = vecs2Graph(app, tempVecs2)

    rightTopCoord, leftBotCoord = tempCoords2[0], tempCoords2[1]

    app.tempFloorCoords[1] = leftBotCoord
    app.tempFloorCoords[2] = rightTopCoord
    app.tempFloorCoords[3] = rightBotCoord 