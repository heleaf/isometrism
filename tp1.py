from cmu_112_graphics import *
#import module_manager
#module_manager.review()

import numpy as np #, scipy, math
import math

#from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
#class MyApp(App):
def appStarted(self): 
    self.circs = np.empty((0,2)) #shape, 0 rows, 2 cols (2d arr)
    self.rect = np.array([[self.width/4, self.height/8], 
                            [3*self.width/4, 7*self.height/8]])
    self.xWidth = abs(((self.width/4) - (3*self.width/4)))
    #4 points 
    self.rect2 = np.array([[self.width/4, self.height/8], 
                            [self.width/4, 6*self.height/8],
                            [3*self.width/4, 2*self.height/8],
                            [3*self.width/4, 7*self.height/8]])
    print(f'width: {self.xWidth}')
    self.r = 5
    self.incr = False
    self.counter = 0
    self.drawFloor = False
    self.floorCoords = np.empty((0,2))
    self.tempFloorCoords = np.empty((0,2))

    self.debugFloorCoords = np.array(
        [[106., 343.],
        [233., 442.],
        [360., 343.],
        [487., 442.]]
    )

def appStopped(self): pass

def keyPressed(self, event):
    if event.key == '1':
        self.drawFloor = not self.drawFloor 
        self.floorCoords = np.empty((0,2))
        self.tempFloorCoords = np.empty((0,2)) 
        print(f'self.drawfloor: {self.drawFloor}')

def keyReleased(self, event): pass
       
def mousePressed(self, event): 
    #2d arr
    print(self.floorCoords.shape[0])
    if not self.drawFloor:
        newCirc = np.array([[event.x, event.y]]) 
        self.circs = np.append(self.circs, newCirc, axis=0) #add a row 
        print(newCirc)
    elif self.floorCoords.shape[0] == 0: #rows
        leftTopCoord = np.array([[event.x, event.y]])
        self.floorCoords = np.append(self.floorCoords, leftTopCoord, axis=0)
        for i in range(4):
            self.tempFloorCoords = np.append(self.tempFloorCoords, 
                                            leftTopCoord, axis=0)
        print(self.floorCoords)
        print(self.tempFloorCoords)
    elif self.floorCoords.shape[0] == 1: #rows
        rightBotCoord = np.array([[event.x, event.y]])

        margin = (self.floorCoords[0][0]-event.x)/3
        rightTopCoord = np.array([[event.x+margin, self.floorCoords[0][1]]])
        leftBotCoord = np.array([[self.floorCoords[0][0]-margin, event.y]])

        self.floorCoords = np.append(self.floorCoords,leftBotCoord, axis=0)
        self.floorCoords = np.append(self.floorCoords,rightTopCoord, axis=0)
        self.floorCoords = np.append(self.floorCoords,rightBotCoord, axis=0) 
        print(f'floor: \n{self.floorCoords}')

def mouseReleased(self, event): pass
    #self.messages.append(f'mouseReleased at {(event.x, event.y)}')

def mouseMoved(self, event): 
    if self.drawFloor and self.floorCoords.shape[0]==1:
        rightBotCoord = np.array([[event.x, event.y]])
        margin = (self.tempFloorCoords[0][0]-event.x)/3
        rightTopCoord = np.array([[event.x+margin, self.tempFloorCoords[0][1]]])
        leftBotCoord = np.array([[self.tempFloorCoords[0][0]-margin, event.y]])
        self.tempFloorCoords[1] = leftBotCoord
        self.tempFloorCoords[2] = rightTopCoord
        self.tempFloorCoords[3] = rightBotCoord

def mouseDragged(self, event): pass
    #self.messages.append(f'mouseDragged at {(event.x, event.y)}')

def sizeChanged(self): pass
    #self.messages.append(f'sizeChanged to {(self.width, self.height)}')

def timerFired(self): 
    pass

def redrawAll(self, canvas): 
    #floor 
    if self.drawFloor and self.floorCoords.shape[0]==1:
        c0,d0 = self.tempFloorCoords[0]
        c1,d1 = self.tempFloorCoords[1]
        c2,d2 = self.tempFloorCoords[2]
        c3,d3 = self.tempFloorCoords[3]
        canvas.create_polygon(c1,d1,c0,d0,c2,d2,c3,d3, fill = 'yellow')

    elif self.drawFloor and self.floorCoords.shape[0]==4: 
        c0,d0 = self.floorCoords[0]
        c1,d1 = self.floorCoords[1]
        c2,d2 = self.floorCoords[2]
        c3,d3 = self.floorCoords[3]
        canvas.create_polygon(c1,d1,c0,d0,c2,d2,c3,d3, fill = 'yellow')

    #debugFloor
    x0,y0 = self.debugFloorCoords[0]
    x1,y1 = self.debugFloorCoords[1]
    x2,y2 = self.debugFloorCoords[2]
    x3,y3 = self.debugFloorCoords[3]
    canvas.create_polygon(x1,y1,x0,y0,x2,y2,x3,y3, fill = 'green')

def main():
    runApp(width=600, height=600)
    #printArrays()

main()
