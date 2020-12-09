#newbasis
#   - helper functions that run in main.py organized into 5 categories:
#       1. INITIALIZATION FUNCTIONS 
#          (functions only called 1x in appStarted)
#       2. CAMERA BASIS FUNCTIONS 
#          (functions that handle the view mode's camera perspectives)
#       3. ROOM CREATION FUNCTIONS
#          (functions that handle floor/wall creation, and room rotation)
#       4. FURNITURE SPECIFIC FUNCTIONS 
#          (functions that handle furniture creation, rotation, & collision)
#       5. DRAW FUNCTIONS 
#          (draw functions for each of the screens in the app)

import math
import numpy as np
from cmu_112_graphics import *
from threedimfunctions import *
from cube import *
from button import *


################ 1. INITIALIZATION FUNCTIONS ################
#specifies visualization parameters for 3D vector coordinate system
def initialize3D(app): 
    app.origin = (app.width/2, app.height/2)

    #x axis is the left hand side axis
    app.xAxisAngle = deg2Rad(200) 

    #y axis is the right hand side axis 
    app.yAxisAngle = deg2Rad(340)

    #z axis is simply a vertical axis 

#initializes title page variables and objects 
def initializeTitlePage(app): 
    app.title = True

    ovec = graph2Vecs(app, [[app.width/2, app.height*0.38]])[0]
    fl = fw = app.width*0.3
    fh = 15
    app.titleFloor = Cube(fl, fw, fh, ovec)

    rh = app.height*0.3
    rovec = np.array(ovec) + np.array([-fh,0,0])
    app.titleRW = Cube(fh, fw, rh, rovec)

    lovec = np.array(ovec) + np.array([0,-fh,0])
    app.titleLW = Cube(fl, fh, rh, lovec)

    lampO = np.array(ovec) + np.array([0,fw*0.7,fh])
    app.titleLamp = Lamp(fl*0.15,fl*0.15, rh*0.6, lampO)
    
    bedO = np.array(ovec) + np.array([0,0,fh])
    app.titleBed = Bed(fl*0.3, fw*0.6, rh*0.3, bedO)

    chairO = np.array(ovec) + np.array([fl*0.4, fw*0.6, fh])
    app.titleChair = Chair(fl*0.2, fl*0.2, rh*0.4, chairO)

    tableO = np.array(ovec) + np.array([fl*0.7, fw*0.2, fh])
    app.titleTable = Table(fl*0.2, fw*0.7, rh*0.2, tableO)

    cubeO = np.array(ovec) + np.array([fl*0.3, -fh, rh*0.5])
    app.titleCube = Cube(fl*0.4, fh, rh*0.3,cubeO)

    app.titleObjs = [app.titleFloor, app.titleRW, app.titleLW, 
                    app.titleLamp, app.titleBed, app.titleChair, 
                    app.titleTable, app.titleCube]

    app.titleText = 'ISOMETRISM'
    app.subtitleText = 'a 2.5d room planner'
    app.textColor = 'black'

#creates the buttons used in the title, help, edit, and view screens 
def initializeButtons(app):
    #o specifies the origin of a button 

    o = (80,60)
    app.roomButton = Button(o, 60,50, padding=10, iconName='Room', 
                                        ovec=True, app=app)

    o = (160,60)
    app.chairButton = Button(o, 60,50, padding = 10, iconName='Chair', 
                                        ovec=True, app=app)

    o = (240,60)
    app.tableButton = Button(o, 60,50, padding =10, iconName='Table', 
                                        ovec=True, app=app)

    o = (320, 60)
    app.bedButton = Button(o, 60,50, padding=10, iconName='Bed', 
                                        ovec=True, app=app)

    o = (400, 60)
    app.lampButton = Button(o, 60,50, padding=10, iconName='Lamp', 
                                        ovec=True, app=app)

    o = (80, app.height-90)
    app.cameraButton = Button(o, 60,60, padding=10, iconName='Camera', 
                                        ovec=True, app=app)
                                        
    o = (80+50, app.height-90)
    app.cameraLeftButton = Button(o,20,60, padding=5, iconName = 'Left Arrow')

    o = (80+50+20, app.height-90)
    app.cameraRightButton = Button(o,20,60,padding=5, iconName = 'Right Arrow')

    o = (app.width/2 - 20, app.height-80)
    app.leftTurnButton = Button(o, 40,40, padding=10, iconName='Left Turn')

    o = (app.width/2 +20, app.height-80)
    app.rightTurnButton = Button(o, 40,40, padding=10, iconName='Right Turn')

    o = (app.width-70-50, app.height-80)
    app.viewButton = Button(o, 40,40, padding=10, iconName='Eye')

    o = (app.width-70, app.height-80)
    app.helpButton = Button(o, 40,40, padding=10, iconName='Help')

    o = (app.width-80, 60)
    app.clearButton = Button(o, 60,50, padding=10, iconName='Clear')

    o = (app.width/2, app.height-190)
    app.titleButton = Button(o, app.width-120, 80, padding=10, 
                                fillColor='black', lineColor='white')

    o = (app.width/2, app.height-100)
    app.subtitleButton = Button(o, app.width-200, 50, padding=10, 
                                fillColor='black', lineColor='white')

    app.buttons = [app.roomButton, app.chairButton, app.tableButton, 
                   app.bedButton, app.lampButton,
                   app.leftTurnButton, app.rightTurnButton, 
                   app.cameraButton, app.cameraLeftButton, 
                   app.cameraRightButton, app.viewButton, 
                   app.helpButton, app.clearButton]

    app.titleButtons = [app.titleButton, app.subtitleButton]

    app.viewButtons = [app.cameraButton, app.cameraLeftButton, 
                       app.cameraRightButton, app.viewButton, app.helpButton]

    app.editButtons = [app.roomButton, app.chairButton, 
                       app.tableButton, app.bedButton, app.lampButton,
                       app.leftTurnButton, app.rightTurnButton, 
                       app.cameraButton, app.cameraLeftButton, 
                       app.cameraRightButton, app.viewButton, 
                       app.clearButton] 

    app.furnitureButtons = [app.chairButton, app.tableButton, 
                            app.bedButton, app.lampButton]

#creates the buttons displayed in the help screen (no functionality, just icons)
def initializeHelpScreenButtons(app):
    w = app.width/8
    o = (w, 100)
    hRoom = Button(o, 50,40, padding=10, iconName='Room', ovec=True, app=app)
    o = (w, 150)
    hChair = Button(o, 50,40, padding=10, iconName='Chair', ovec=True, app=app)
    o = (w, 200)
    hClear = Button(o,40,40,padding=10, iconName='Clear')
    o = (w, 250)
    hLT = Button(o, 40,40, padding=10, iconName='Left Turn')
    o = (w,300)
    hRT = Button(o, 40,40, padding=10, iconName='Right Turn')
    o = (w,350)
    hView = Button(o, 40,40, padding=10, iconName='Eye')
    o = (w,400)
    hCam = Button(o, 40,40, padding=5, iconName = 'Camera', ovec=True, app=app)
    o = (w-10,450)
    hCamL = Button(o, 20,40,padding=5, iconName= 'Left Arrow')
    hCamR = Button((w+10,450), 20,40,padding=5, iconName='Right Arrow')
    o = (w,500)
    hHelp = Button(o,40,40,padding=10,iconName='Help')

    app.hScreenButtons = [hRoom,hChair,hClear,hLT,hRT,
                          hView,hCam,hCamL,hCamR,hHelp]


################ 2. CAMERA BASIS FUNCTIONS ################
#calculates perspective rendering coords of objects in all 4 camera directions
def resetView(app, init=False):  
    if init: #starting parameters
        app.view = False
        app.cameraOrigin = np.array([0,30,60]) 
        app.viewIndex = 0

    #creates camera bases in the 4 directions of the room 
    makeCameraBases(app, app.cameraOrigin)

    #current camera basis the user is on
    app.cameraBasis = app.cameraBasisAlts[app.viewIndex]

    #coordinates of the edit window's pink screen (corresponds to camera basis)
    app.cameraImageCoords = app.cameraImageAlts[app.viewIndex]

#1. creates camera bases in 4 camera directions 
#   - each basis has v1, v2, v3
#   - v1 draws the horizontal components of perspective rendered object coords 
#     from the image's top left corner
#   - v2 draws the vertical components of perspective rendered object coords
#     from the image's top left corner 
#   - v3 is the vector from the camera's origin to the image's top left corner
#2. calculates coords of the view window in the edit screen for each basis
def makeCameraBases(app, cameraOrigin=np.array([0,30,60]), 
                    imageDistance=35, imageLength=80, imageHeight=80):

    #front facing basis (faces positive x axis direction)
    f1 = np.array([0,imageLength/app.width,0])
    f2 = np.array([0,0,imageHeight/app.height])
    f3 = cameraOrigin + np.array([imageDistance, imageLength/2, imageHeight/2]) 
   
    imageTopLeft = f3
    imageTopRight = imageTopLeft + np.array([0,-imageLength, 0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([0,-imageLength,-imageHeight])

    app.imageCoordsFront = vecs2Graph(app, [imageTopLeft, imageTopRight, 
                                            imageBotRight, imageBotLeft])

    #right facing basis (faces negative y axis direction)
    r1 = np.array([imageLength/app.width,0,0])
    r2 = np.array([0,0,imageHeight/app.height])
    r3 = cameraOrigin + np.array([imageLength/2, -imageDistance, imageHeight/2]) 

    imageTopLeft = r3
    imageTopRight = imageTopLeft + np.array([-imageLength, 0,0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([-imageLength, 0, -imageHeight])
    app.imageCoordsRight = vecs2Graph(app, [imageTopLeft, imageTopRight, 
                                            imageBotRight, imageBotLeft])

    #back facing basis (faces negative x axis direction)
    b1 = np.array([0,-imageLength/app.width, 0])
    b2 = np.array([0,0,imageHeight/app.height])
    b3 = cameraOrigin + np.array([-imageLength/2, -imageDistance, imageHeight/2])

    imageTopLeft = b3
    imageTopRight = imageTopLeft + np.array([0,imageLength,0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([0, imageLength, -imageHeight])
    app.imageCoordsBack = vecs2Graph(app, [imageTopLeft, imageTopRight, 
                                            imageBotRight, imageBotLeft])

    #left facing basis (faces positive y axis direction)
    l1 = np.array([-imageLength/app.width,0,0])
    l2 = np.array([0,0,imageHeight/app.height])
    l3 = cameraOrigin + np.array([-imageLength/2, imageDistance, imageHeight/2])
    
    imageTopLeft = l3
    imageTopRight = imageTopLeft + np.array([imageLength,0,0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([imageLength, 0, -imageHeight])
    app.imageCoordsLeft = vecs2Graph(app, [imageTopLeft, imageTopRight, 
                                            imageBotRight, imageBotLeft]) 

    #creates an list of all camera bases
    #   - each camera basis is now a matrix with basis vectors as columns 
    app.cameraBasisAlts = [np.array([f1,f2,f3]).T, np.array([r1,r2,r3]).T, 
                           np.array([b1,b2,b3]).T, np.array([l1,l2,l3]).T]

    #creates a list of coords for drawing the view window in the edit screen 
    #   - order corresponds to each camera basis 
    app.cameraImageAlts = [app.imageCoordsFront, app.imageCoordsRight, 
                           app.imageCoordsBack, app.imageCoordsLeft]



################ 3. ROOM CREATION FUNCTIONS ################
#resets parameters for creating a room 
def resetDrawCubeFloor(app, init=False):
    if init:
        app.drawCubeFloor = False
    else:
        app.drawCubeFloor = not app.drawCubeFloor

    app.cubeFloorVecs = np.empty((0,3))
    app.cubeFloorCoords = np.empty((0,2))

    app.cubeWallHeight = None

    #variables that will be assigned cube objects later 
    app.COFloor = None
    app.COLW = None
    app.CORW = None 

    app.tempCOFloor = None
    app.tempCOLW = None
    app.tempCORW = None

    #rotation parameters of the room 
    app.rotationAngle = 0
    app.rotateC = False
    app.rotateCC = False

#creates permanent (mousePressed) and floating (mouseMoved) floor cubes
def makeCubeFloor(app, event, thickness=10, floatFloor=False):
    if floatFloor: #modify temp floor objects (changes w/ mouse movement)
        e1 = app.cubeFloorVecs[0] #origin + [length,0,0]
        e2 = graph2Vecs(app, [[event.x, event.y]])[0] #origin + [0,width,0]
        e3 = np.array([e2[0], e1[1], 0]) #origin

        length = (e1 - e3)[0] #origin + [length,0,0] - origin 
        width = (e2 - e3)[1] #origin + [0,width,0] - origin 
        height = thickness
        app.tempCOFloor = Cube(length, width, height, e3)

    else: #set actual floor object
        th = np.array([0,0,thickness]) #height of the floor cube

        if app.cubeFloorVecs.shape[0] == 0: #rows (vectors) set so far
            firstPoint = np.array([event.x, event.y])
            e1 = graph2Vecs(app, [firstPoint])[0]

            #sets bottom leftmost vector of floor (and vector right above it)
            app.cubeFloorVecs = np.append(app.cubeFloorVecs, [e1], axis=0)
            app.cubeFloorVecs = np.append(app.cubeFloorVecs, [e1+th], axis=0)

        elif app.cubeFloorVecs.shape[0] == 2: #rows (vectors) set so far
            secondPoint = np.array([event.x, event.y])
            e1 = app.cubeFloorVecs[0] #bottom leftmost floor vec
            e2 = graph2Vecs(app, [secondPoint])[0] #bottom rightmost floor vec
            e3 = np.array([e2[0], e1[1], 0]) #origin 
            e4 = np.array([e1[0], e2[1], 0]) #origin + [l,0,0] + [0,w,0]
            for vec in [e2, e3, e4]:
                app.cubeFloorVecs = np.append(app.cubeFloorVecs, [vec], axis=0)
                app.cubeFloorVecs = np.append(app.cubeFloorVecs, [vec+th], axis=0)
            app.cubeFloorCoords = vecs2Graph(app, app.cubeFloorVecs)

            #calculating floor length, width, height
            length = abs(e1[0]-e2[0])
            width = abs(e1[1]-e2[1])
            height = thickness 
            
            app.COFloor = Cube(length,width,height,e3)

#creates permanent (mousePressed) and floating (mouseMoved) wall cubes
def makeCubeWalls(app, event, floatWalls=False):
    h = app.cubeFloorCoords[3][1]-event.y
    rl, rw, rh = app.COFloor.height, app.COFloor.width, h
    rx, ry, rz = app.COFloor.origin[0]-rl, app.COFloor.origin[1], 0  
    ll, lw, lh = app.COFloor.length, app.COFloor.height, h
    lx, ly, lz = app.COFloor.origin[0], app.COFloor.origin[1]-lw, 0 

    if floatWalls: #assign to temp walls
        app.tempCORW = Cube(rl, rw, rh, (rx, ry, rz))
        app.tempCOLW = Cube(ll, lw, lh, (lx,ly,lz))
    else: #set as actual walls and height
        app.cubeWallHeight = h
        app.CORW = Cube(rl, rw, rh, (rx, ry, rz))
        app.COLW = Cube(ll, lw, lh, (lx,ly,lz))

#rotate all room elements around the center of the room (center of the floor)
def rotateAll(app, angle=10):
    app.showCamera = False #hide camera
    app.rotationAngle = (app.rotationAngle+angle)%360 #update rotation tracker
    if isinstance(app.COFloor, Cube): #rotate floor if it exists
        app.COFloor.rotateSelf(app, angle, center=app.COFloor.center)
    if isinstance(app.CORW, Cube): #rotate walls if they exist
        app.CORW.rotateSelf(app, angle, center=app.COFloor.center)
        app.COLW.rotateSelf(app, angle, center=app.COFloor.center)
    for furniture in app.furniture: #rotate furniture
        furniture.rotateSelf(app, angle, center=app.COFloor.center)




################ 4. FURNITURE SPECIFIC FUNCTIONS ################
#resets parameters for user-created furniture 
def resetFurniture(app):
    app.furniture = []
    app.newFurniture = None

#creates furniture if a button was clicked. otherwise, checks for rotation
def handleFurnitureCreationAndRotation(app, event): 
    #track where mouse clicked was in terms of the 3D vector system
    origin = graph2Vecs(app, [[event.x, event.y]], 
                        z=app.COFloor.height)[0]

    #creating furniture based on which button was pressed 
    #furniture scales according to floor/wall sizes
    if app.chairButton.mouseOver(app, event):
        app.chairButton.isPressed = True
        length = width = min(app.COFloor.length/8, app.COFloor.width/8)
        height = length*2.5
        app.newFurniture = Chair(length, width, height, 
        origin=origin, legThickness=min(2,length*0.2))

    elif app.tableButton.mouseOver(app, event):
        app.tableButton.isPressed = True
        length = app.COFloor.length/6
        width = min((min(app.COFloor.width, 
                        app.COFloor.length), length*2))
        height = length*1.5
        app.newFurniture = Table(length, width, height, 
        origin=origin, legThickness=min(2,length*0.2))

    elif app.bedButton.mouseOver(app, event):
        app.bedButton.isPressed = True
        length = app.COFloor.length/6
        width = min((min(app.COFloor.width, 
                    app.COFloor.length), length*2))
        height = length*1.2
        app.newFurniture = Bed(length, width, height, origin=origin)

    elif app.lampButton.mouseOver(app, event):
        app.lampButton.isPressed = True
        length = width = min(app.COFloor.length/10, 
                            app.COFloor.width/10)
        height = app.CORW.height*0.6
        app.newFurniture = Lamp(length, width, height, 
        origin=origin, legThickness=min(2,length*0.2))

    #if no furniture button was clicked, 
    # check if any existing furniture in the room was clicked
    else: rotateFurniture(app, event)

#handles furniture rotation and possible collision w/ walls or other furniture
def rotateFurniture(app, event):

    #check if any furniture was clicked (if so, change its status)
    for i in range(len(app.furniture)):
        furniture = app.furniture[i]
        if furniture.mouseInHitbox(app, event):
            furniture.isClicked = True
    
    #rotate furniture if they were marked as clicked
    for i in range(len(app.furniture)):
        furniture = app.furniture[i]
        if furniture.isClicked:
            furniture.rotateSelf(app, 10, furniture.center)

            #if rotated furniture collides with a wall, 
            # rotate it back & reset clicked status
            if (furniture.isCollide(app.CORW) 
            or furniture.isCollide(app.COLW)):
                furniture.rotateSelf(app, -10, furniture.center)
                furniture.isClicked = False
                return
            
            #if rotated furniture collides w/ other furniture,
            # rotated it back & reset clicked status
            for furniture2 in app.furniture:
                if (furniture!=furniture2 and 
                (furniture.isCollide(furniture2) 
                or furniture2.isCollide(furniture))):
                    furniture.rotateSelf(app, -10, furniture.center)
                    furniture.isClicked = False
                    return

        #reset clicked status
        furniture.isClicked = False

#returns the appropriate furniture 'origin' vector 
# to correct for furniture dropped outside the room's bounds
def fitFurnitureInFloor(app, furniture, floor):
    #correcting x component
    if (furniture.origin[0] + furniture.length > floor.origin[0] + floor.length
    ):
        ox = floor.origin[0] + floor.length - furniture.length 
    elif (furniture.origin[0]<floor.origin[0]):
        ox = floor.origin[0]
    else: ox = furniture.origin[0]

    #correcting y component of vector
    if (furniture.origin[1] + furniture.width > floor.origin[1] + floor.width
    ): 
        oy = floor.origin[1] + floor.width - furniture.width
    elif (furniture.origin[1]<floor.origin[1]):
        oy = floor.origin[1]
    else: oy = furniture.origin[1]

    #correcting z component of vector 
    oz = floor.height

    return ox,oy,oz




################ 5. DRAW FUNCTIONS ################
def drawHelpScreen(app, canvas):
    canvas.create_text(app.width/2, 50, text='ISOMETRISM', font='Courier 20')

    for button in app.hScreenButtons:
        button.draw(app,canvas,button.fillColor, button.lineColor)

    #keyboard shortcuts 
    f = 'Courier 15 bold'
    w = app.width/5
    canvas.create_text(w,250, text='r', font=f)
    canvas.create_text(w,300, text='t', font=f)
    canvas.create_text(w,350, text='v', font=f)
    canvas.create_text(w,400, text='c', font=f)
    canvas.create_text(w,450, text='f g', font=f)
    canvas.create_text(w,500, text='h', font=f)

    #button functionality
    f2 = 'Courier 12'
    w2 = app.width/4
    canvas.create_text(w2, 100, font=f2, anchor=W,
        text='start a room. click 3x to set floor & walls.')
    canvas.create_text(w2, 140, font=f2, anchor=W,
        text='drag & drop furniture into your room.')
    canvas.create_text(w2,160, font=f2, anchor=W,
        text='click inside furniture to rotate furniture.')
    canvas.create_text(w2,200, font=f2, anchor=W,
        text='clear room and all furniture.')
    canvas.create_text(w2,250, font=f2, anchor=W,
        text='toggle clockwise room rotation.')
    canvas.create_text(w2,300, font=f2, anchor=W,
        text='toggle counterclockwise room rotation.')
    canvas.create_text(w2,350, font=f2, anchor=W,
        text='toggle between edit mode and perspective viewing mode.')
    canvas.create_text(w2,390, font=f2, anchor=W,
        text='toggle camera visibility in edit and view mode.')
    canvas.create_text(w2,410, font=f2, anchor=W,
        text='wasdxz keys move camera in edit and view mode.')
    canvas.create_text(w2,450, font=f2, anchor=W,
        text='rotate camera view window in edit and view mode.')
    canvas.create_text(w2,500, font=f2, anchor=W,
        text='toggle help screen.')

    app.helpButton.draw(app, canvas, app.helpButton.fillColor, 
                                    app.helpButton.lineColor)

def drawTitleScreen(app, canvas):
    #rotating room and furniture
    for obj in app.titleObjs:
        obj.draw(app,canvas,'black')

    ox,oy = app.titleButton.origin
    canvas.create_text(ox,oy, text=app.titleText, font='Courier 80', 
                                                    fill=app.textColor)

    ox,oy = app.subtitleButton.origin
    canvas.create_text(ox,oy, text=app.subtitleText, font='Courier 30', 
                                                    fill=app.textColor)

def drawViewScreen(app, canvas): 
    if app.showCamera: #pink tinted view window
        canvas.create_rectangle(0,0,app.width, app.height, fill='pink')
    
    if isinstance(app.CORW, Cube):
        for furniture in app.furniture:
            furniture.drawImageCoords(app, canvas, color='black')

        for cube in [app.COFloor, app.CORW, app.COLW]:
            cube.drawImageCoords(app, canvas, color='black')

    for button in app.viewButtons:
        button.draw(app, canvas, button.fillColor, button.lineColor)

def drawEditScreen(app, canvas):
    if app.showCamera:
        #image face (view window)
        x0,y0 = app.cameraImageCoords[0]
        x1,y1 = app.cameraImageCoords[1]
        x2,y2 = app.cameraImageCoords[2]
        x3,y3 = app.cameraImageCoords[3]
        canvas.create_polygon(x0,y0,x1,y1,x2,y2,x3,y3, fill='pink')

        camCoord = vecs2Graph(app, [app.cameraOrigin])[0]
        x,y = camCoord
        r = 3
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = 'red', width=0)

    ox, oy = app.origin

    #draw walls (static, set by mousePressed)
    if (app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8 
                           and isinstance(app.CORW, Cube)):
        app.CORW.draw(app, canvas, 'black')
        app.COLW.draw(app, canvas, 'black')

    #draw walls (moving, set by mouseMoved)
    elif (app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8 
    and app.cubeWallHeight==None and isinstance(app.tempCORW, Cube)):
        app.tempCORW.draw(app, canvas, 'red')
        app.tempCOLW.draw(app, canvas, 'red')

    #draw floor (static, set by mousePressed)
    if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8:
        app.COFloor.draw(app, canvas, 'black')

    #cube floor (moving, set by mouseMoved)
    if (app.drawCubeFloor and app.cubeFloorVecs.shape[0]==2 
    and isinstance(app.tempCOFloor, Cube)):
        app.tempCOFloor.draw(app, canvas, 'red')

    #draw furniture
    if app.newFurniture!=None:
        app.newFurniture.draw(app, canvas, 'red')
    for furniture in app.furniture:
        furniture.draw(app, canvas, 'black')

    #buttons
    for button in app.editButtons+[app.helpButton]:
        button.draw(app, canvas, button.fillColor, button.lineColor)