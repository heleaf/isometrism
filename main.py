#main
#   - main file that runs isometrism 

import math
import numpy as np
from cmu_112_graphics import *
from threedimfunctions import *
from newbasis import *
from cube import *
from button import *

def appStarted(app):
    initialize3D(app)
    initializeTitlePage(app)

    resetDrawCubeFloor(app, init=True)
    resetFurniture(app)

    resetView(app, init=True) 
    app.showCamera = True

    initializeButtons(app)
    initializeHelpScreenButtons(app)

    app.helpScreen = False

def keyPressed(app, event): 
    #skip past title screen
    if event.key == '1': app.title = False

    #toggle help screen
    if event.key == 'h':
        if app.title:
            app.title = False
        app.helpScreen = not app.helpScreen

    #step by step rotation of room
    if not app.helpScreen and not app.title and not app.view:
        if event.key == 'r':
            rotateAll(app,  angle=10)
        elif event.key == 't':
            rotateAll(app,  angle=-10)

    #camera/view window movement commands
    if (not app.helpScreen and not app.title and app.rotationAngle==0 
    and not app.rotateC and not app.rotateCC): 
        if event.key == 'v': #toggle view mode
            app.view = not app.view
        elif event.key == 'w': #move camera up (incr z)
            app.cameraOrigin += np.array([0,0,5])
            resetView(app)
        elif event.key == 'a': #move camera left (decr y)
            app.cameraOrigin += np.array([0,-5,0])
            resetView(app)
        elif event.key == 's': #move camera down (decr z)
            app.cameraOrigin += np.array([0,0,-5])
            resetView(app)
        elif event.key == 'd': #move camera right (incr y)
            app.cameraOrigin += np.array([0,5,0])
            resetView(app)
        elif event.key == 'z': #move camera forward (incr x)
            app.cameraOrigin += np.array([5,0,0])
            resetView(app)
        elif event.key == 'x': #move camera backwards (decr x)
            app.cameraOrigin += np.array([-5,0,0])
            resetView(app)
        elif event.key == 'c': #toggle camera visibility
            app.showCamera = not app.showCamera
        elif event.key == 'f': #change camera view (clockwise)
            app.viewIndex = (app.viewIndex + 1)%len(app.cameraBasisAlts)
            app.cameraBasis = app.cameraBasisAlts[app.viewIndex]
            app.cameraImageCoords = app.cameraImageAlts[app.viewIndex]
        elif event.key == 'g': #change camera view (counterclockwise)
            app.viewIndex = (app.viewIndex - 1)%len(app.cameraBasisAlts)
            app.cameraBasis = app.cameraBasisAlts[app.viewIndex]
            app.cameraImageCoords = app.cameraImageAlts[app.viewIndex]

def mousePressed(app, event): 
    if app.title:
        #show help screen upon entering the app
        if (app.titleButton.mouseOver(app,event) or 
        app.subtitleButton.mouseOver(app,event)): 
            app.title = False
            app.helpScreen = True
    else:
        #toggle help screen
        if app.helpButton.mouseOver(app, event):  
            app.helpScreen = not app.helpScreen
        
        #toggle view screen
        elif app.viewButton.mouseOver(app, event) and not app.helpScreen: 
            app.view = not app.view

        #clicked create room button 
        elif (app.roomButton.mouseOver(app, event) 
        and not app.view and not app.helpScreen and not app.drawCubeFloor):
            app.drawCubeFloor = True

        #creating floor
        elif (app.drawCubeFloor and not app.rotateC and not app.rotateCC 
        and app.rotationAngle==0 and not isinstance(app.COFloor, Cube)):
            makeCubeFloor(app, event)

        #creating walls
        elif (isinstance(app.COFloor, Cube) and app.cubeWallHeight == None 
        and not app.rotateC and not app.rotateCC and app.rotationAngle==0):
            makeCubeWalls(app, event)

        #clear all room and furniture
        elif (app.clearButton.mouseOver(app,event) and not app.helpScreen 
        and not app.view ):
            resetDrawCubeFloor(app)
            resetFurniture(app)

        #toggle clockwise room rotation
        elif (app.leftTurnButton.mouseOver(app, event) 
        and not app.view and not app.helpScreen and app.drawCubeFloor):
            app.rotateC = not app.rotateC
            app.rotateCC = False
            if not app.rotateC:
                while app.rotationAngle!=0:
                    rotateAll(app, angle=10)
                app.showCamera = True
        
        #toggle counterclockwise room rotation
        elif (app.rightTurnButton.mouseOver(app, event) and 
        not app.view and not app.helpScreen and app.drawCubeFloor):
            app.rotateCC = not app.rotateCC
            app.rotateC = False
            if not app.rotateCC:
                while app.rotationAngle!=0:
                    rotateAll(app, angle=-10)
                app.showCamera = True

        #toggle camera + pink view window visibility in edit/view modes
        elif (app.cameraButton.mouseOver(app, event) and not app.helpScreen):
            app.showCamera = not app.showCamera

        #change camera viewing direction (90 degrees clockwise)
        elif app.cameraLeftButton.mouseOver(app,event) and not app.helpScreen:
            app.viewIndex = (app.viewIndex + 1)%len(app.cameraBasisAlts)
            app.cameraBasis = app.cameraBasisAlts[app.viewIndex]
            app.cameraImageCoords = app.cameraImageAlts[app.viewIndex]
        
        #change camera viewing direction (90 degrees counterclockwise)
        elif app.cameraRightButton.mouseOver(app,event) and not app.helpScreen:
            app.viewIndex = (app.viewIndex - 1)%len(app.cameraBasisAlts)
            app.cameraBasis = app.cameraBasisAlts[app.viewIndex]
            app.cameraImageCoords = app.cameraImageAlts[app.viewIndex]

        #furniture creation and rotation  
        elif (not app.view and app.drawCubeFloor and isinstance(app.CORW, Cube) 
        and not app.rotateC and not app.rotateCC and app.rotationAngle==0):
            handleFurnitureCreationAndRotation(app, event)

def mouseDragged(app, event):
    #updates newly created furniture to be where the user's mouse is 
    if (not app.view and app.drawCubeFloor and isinstance(app.CORW, Cube)
        and app.rotationAngle==0 and app.newFurniture!=None):

        o = graph2Vecs(app, [[event.x, event.y]], z=app.COFloor.height)[0]

        length2 = app.newFurniture.length
        width2 = app.newFurniture.width
        height2 = app.newFurniture.height
        tth2 = app.newFurniture.tth
        lth2 = app.newFurniture.lth

        if app.chairButton.isPressed:
            app.newFurniture = Chair(length2, width2, height2, origin=o, 
                                    tableThickness=tth2, legThickness=lth2)

        elif app.tableButton.isPressed:
            app.newFurniture = Table(length2, width2, height2, origin=o, 
                                    tableThickness=tth2, legThickness=lth2)
        
        elif app.bedButton.isPressed:
            app.newFurniture = Bed(length2, width2, height2, origin=o)
        
        elif app.lampButton.isPressed: 
            app.newFurniture = Lamp(length2, width2, height2, origin=o, 
                                    tableThickness=tth2, legThickness=lth2)

def mouseReleased(app, event):
    #creates furniture where user releases if a furniture button was pressed 
    if (not app.view and not app.rotateC and not app.rotateCC 
         and app.drawCubeFloor and isinstance(app.CORW, Cube)
         and (app.chairButton.isPressed or 
              app.tableButton.isPressed or 
              app.bedButton.isPressed or 
              app.lampButton.isPressed)):
        
        #first push any potential out-of-bounds furniture inside room 
        ox2, oy2, oz2 = fitFurnitureInFloor(app, app.newFurniture, app.COFloor)

        l2, w2, h2 = app.newFurniture.length, app.newFurniture.width, \
                     app.newFurniture.height
        tth2, lth2 = app.newFurniture.tth, app.newFurniture.lth

        if app.chairButton.isPressed:
            app.newFurniture = Chair(l2,w2,h2, origin=(ox2,oy2,oz2), 
                                    tableThickness=tth2, legThickness=lth2)
        elif app.tableButton.isPressed: 
            app.newFurniture = Table(l2,w2,h2, origin=(ox2,oy2,oz2), 
                                    tableThickness=tth2, legThickness=lth2)

        elif app.bedButton.isPressed:
            app.newFurniture = Bed(l2,w2,h2, origin=(ox2,oy2,oz2))
        
        elif app.lampButton.isPressed:
            app.newFurniture = Lamp(l2,w2,h2, origin=(ox2,oy2,oz2), 
                                    tableThickness=tth2, legThickness=lth2)

        #furniture is not dropped into room if it collides w/ existing furniture
        for furniture in app.furniture:
            if (app.newFurniture.isCollide(furniture) or 
                furniture.isCollide(app.newFurniture)):
                app.newFurniture = None
                for button in app.furnitureButtons:
                    button.isPressed = False
                return 

        #furniture did not collide w/ any existing furniture -> add it!
        app.furniture.append(app.newFurniture)
        app.newFurniture = None

        #reset button status
        for button in app.furnitureButtons:
            button.isPressed = False

def mouseMoved(app, event): 
    #show user a preview of their floor while they make their floor
    if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==2:
        makeCubeFloor(app, event, floatFloor=True)
    #show user a preview of their walls while they make their walls
    elif app.cubeFloorVecs.shape[0]==8 and app.cubeWallHeight==None:
        makeCubeWalls(app, event, floatWalls=True)

    #hovering over titles changes their color
    if app.title:
        if (app.titleButton.mouseOver(app,event) or 
        app.subtitleButton.mouseOver(app,event)):
            app.textColor = 'pink'
        else: 
            app.textColor = 'black'
    
    else:
        #hovering over buttons changes their colors
        for button in app.buttons:
            if button.mouseOver(app,event):
                button.fillColor = 'pink'
                button.lineColor = 'red'
            else:
                button.fillColor = 'white'
                button.lineColor = 'black'

def timerFired(app):
    if app.title: #rotation animation on title screen 
        for furniture in app.titleObjs:
            furniture.rotateSelf(app, 5, app.titleFloor.center)
    #clockwise rotation (triggered via clockwise rotation button)
    elif (app.rotateC and not app.view and not app.helpScreen 
    and app.drawCubeFloor and isinstance(app.CORW, Cube)):
        rotateAll(app, angle=10)
    #counterclockwise rotation (triggered via counterclockwise rotation button)
    elif (app.rotateCC and not app.view and not app.helpScreen 
    and app.drawCubeFloor and isinstance(app.CORW, Cube)):
        rotateAll(app, angle=-10)

def redrawAll(app, canvas):
    if app.helpScreen: drawHelpScreen(app, canvas)

    elif app.title: drawTitleScreen(app, canvas)
        
    elif app.view: drawViewScreen(app, canvas)
        
    else: drawEditScreen(app, canvas)
    
def main():
    runApp(width=600, height=650)

main()