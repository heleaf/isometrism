import math
import numpy as np
from cmu_112_graphics import *
from threedimfunctions import *
from cube import *
from button import *

def initialize3D(app):
    app.origin = (app.width/2, app.height/2)

    app.xAxisInitAngle = 200
    app.yAxisInitAngle = 340

    app.xAxisAngle = deg2Rad(app.xAxisInitAngle)
    app.yAxisAngle = deg2Rad(app.yAxisInitAngle)

def initializeTitlePage(app):
    app.title = True

    ovec = graph2Vecs(app, [[app.width/2, app.height*0.4]])[0]
    fl = fw = app.width*0.3
    fh = 15

    app.titleFloor = Cube(fl, fw, fh, ovec)

    rh = app.height*0.3
    rovec = np.array(ovec) + np.array([-fh,0,0])
    app.titleRW = Cube(fh, fw, rh, rovec)

    lovec = np.array(ovec) + np.array([0,-fh,0])
    app.titleLW = Cube(fl, fh, rh, lovec)

def resetView(app, init=False): #perspective rendering   
    if init:
        app.view = False
        app.cameraOrigin = np.array([0,30,60]) 
        app.viewIndex = 0
    makeCameraBases(app, app.cameraOrigin)
    app.cameraBasis = app.cameraBasisAlts[app.viewIndex]
    app.cameraImageCoords = app.cameraImageAlts[app.viewIndex]

def makeCameraBases(app, cameraOrigin=np.array([0,30,60]), imageDistance=35, imageLength=80, imageHeight=80):

    #front facing 
    f1 = np.array([0,imageLength/app.width,0])
    f2 = np.array([0,0,imageHeight/app.height])
    f3 = cameraOrigin + np.array([imageDistance, imageLength/2, imageHeight/2]) 
   
    imageTopLeft = f3
    imageTopRight = imageTopLeft + np.array([0,-imageLength, 0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([0,-imageLength,-imageHeight])
    app.imageCoordsFront = vecs2Graph(app, [imageTopLeft, imageTopRight, imageBotRight, imageBotLeft])

    #right facing
    r1 = np.array([imageLength/app.width,0,0])
    r2 = np.array([0,0,imageHeight/app.height])
    r3 = cameraOrigin + np.array([imageLength/2, -imageDistance, imageHeight/2]) 

    imageTopLeft = r3
    imageTopRight = imageTopLeft + np.array([-imageLength, 0,0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([-imageLength, 0, -imageHeight])
    app.imageCoordsRight = vecs2Graph(app, [imageTopLeft, imageTopRight, imageBotRight, imageBotLeft])

    #back facing
    b1 = np.array([0,-imageLength/app.width, 0])
    b2 = np.array([0,0,imageHeight/app.height])
    b3 = cameraOrigin + np.array([-imageLength/2, -imageDistance, imageHeight/2])

    imageTopLeft = b3
    imageTopRight = imageTopLeft + np.array([0,imageLength,0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([0, imageLength, -imageHeight])
    app.imageCoordsBack = vecs2Graph(app, [imageTopLeft, imageTopRight, imageBotRight, imageBotLeft])

    #left facing
    l1 = np.array([-imageLength/app.width,0,0])
    l2 = np.array([0,0,imageHeight/app.height])
    l3 = cameraOrigin + np.array([-imageLength/2, imageDistance, imageHeight/2])
    
    imageTopLeft = l3
    imageTopRight = imageTopLeft + np.array([imageLength,0,0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([imageLength, 0, -imageHeight])
    app.imageCoordsLeft = vecs2Graph(app, [imageTopLeft, imageTopRight, imageBotRight, imageBotLeft]) 

    #f - front
    #r - right 
    #b - back
    #l - left

    app.cameraBasisAlts = [np.array([f1,f2,f3]).T, np.array([r1,r2,r3]).T, np.array([b1,b2,b3]).T, np.array([l1,l2,l3]).T]
    app.cameraImageAlts = [app.imageCoordsFront, app.imageCoordsRight, app.imageCoordsBack, app.imageCoordsLeft]

def initializeButtons(app):
    o = (80,60)
    app.roomButton = Button(o, 60,50, padding=10, iconName='Room', 
                                        ovec=True, app=app)

    o = (160,60)
    app.chairButton = Button(o, 60,50, padding = 10, iconName='Chair', 
                                        ovec=True, app=app)

    o = (240,60)
    app.tableButton = Button(o, 60,50, padding =10, iconName='Table', 
                                        ovec=True, app=app)

    o = (80, app.height-90)
    app.cameraButton = Button(o, 60,60, padding=10, iconName='Camera', 
                                        ovec=True, app=app)
                                        
    o = (80+50, app.height-80)
    app.cameraLeftButton = Button(o,20,40, padding=5, iconName = 'Left Arrow')

    o = (80+50+20, app.height-80)
    app.cameraRightButton = Button(o,20,40,padding=5, iconName = 'Right Arrow')

    
    #o = (app.width-100-180, app.height-80)
    #o = (70, app.height/2)
    #o = (app.width-70-50, app.height-80-50)
    #o = (app.width-70-50, 50)
    o = (app.width/2 - 20, app.height-80)
    app.leftTurnButton = Button(o, 40,40, padding=10, iconName='Left Turn')

    #o = (app.width-100-120, app.height-80)
    #o = (app.width-70, app.height-80-50)
    #o = (app.width-70, 50)
    o = (app.width/2 +20, app.height-80)
    app.rightTurnButton = Button(o, 40,40, padding=10, iconName='Right Turn')

    o = (app.width-70-50, app.height-80)
    app.viewButton = Button(o, 40,40, padding=10, iconName='Eye')

    o = (app.width-70, app.height-80)
    app.helpButton = Button(o, 40,40, padding=10, iconName='Help')

    #make a titlePageButton

    app.buttons = [app.roomButton, app.chairButton, app.tableButton, 
                   app.leftTurnButton, app.rightTurnButton, app.cameraButton, app.cameraLeftButton, app.cameraRightButton, app.viewButton, 
                   app.helpButton]
    app.editButtons = [app.roomButton, app.chairButton, app.tableButton, 
                       app.leftTurnButton, app.rightTurnButton, app.cameraButton, app.cameraLeftButton, app.cameraRightButton, app.viewButton] 
    app.furnitureButtons = [app.chairButton, app.tableButton]

def resetDrawCubeFloor(app, init=False):
    if init:
        app.drawCubeFloor = False
    else:
        app.drawCubeFloor = not app.drawCubeFloor

    app.cubeFloorVecs = np.empty((0,3))
    app.cubeFloorCoords = np.empty((0,2))

    app.cubeWallHeight = None

    #objects 
    app.COFloor = None
    app.COLW = None
    app.CORW = None 

    app.tempCOFloor = None
    app.tempCOLW = None
    app.tempCORW = None

    app.rotationAngle = 0
    app.rotateC = False
    app.rotateCC = False

def resetFurniture(app):
    app.furniture = []
    app.newFurniture = None

    #arrays of (start, end) 1d coordinates that are occupied
    app.occupiedX = []
    app.occupiedY = []

def appStarted(app):
    initialize3D(app)
    initializeTitlePage(app)

    resetDrawCubeFloor(app, init=True)

    #### perspective rendering 
    resetView(app, init=True) 
    app.showCamera = True

    #########
    resetFurniture(app)
    initializeButtons(app)

    app.helpScreen = False

    app.cubeTest = Cube(30,30,30,(100,100,0))
    app.tableTest = Table(30,30,30,(200,200,0))
    app.chairTest = Chair(30,30,30,(300,300,0))

def rotateRenderedWalls(app):
    app.CORW.vecs = rotateCube(app, app.CORW.vecs, 10)

    #print('after')
    #print(app.CORW.rightBackFaceVecs) #[0, 2, 3, 6]
    #print(app.CORW.vecs)
    print(app.rightCubeWallCoords)
    
    maxVal = max(app.rightCubeWallCoords[:,0])
    minVal = min(app.rightCubeWallCoords[:,0])
    #print(val)
    
    if maxVal == app.rightCubeWallCoords[-1][0]: #good for detecting initial turn 
        print('we need right back')
    elif minVal!=app.rightCubeWallCoords[-1][0]: #good for detecting end of turn
        print('we still need right back')
    else:
        print('nope')

    app.COLW.vecs = rotateCube(app, app.COLW.vecs, 10)

def keyPressed(app, event): 
    if event.key == '1':
        app.title = False
    elif event.key == 'h':
        app.helpScreen = not app.helpScreen
    elif event.key == 'r' and not app.helpScreen and not app.title and not app.view:
        rotateAll(app,  angle=10)
    elif event.key == 't' and not app.helpScreen and not app.title and not app.view:
        rotateAll(app,  angle=-10)
    elif event.key == 'v' and not app.title:
        app.view = not app.view
    elif event.key == 'w': #move camera up
        app.cameraOrigin += np.array([0,0,5])
        resetView(app)
    elif event.key == 'a': #move camera left (decr y)
        app.cameraOrigin += np.array([0,-5,0])
        resetView(app)
    elif event.key == 's': #move camera down
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
    elif event.key == 'c':
        app.showCamera = not app.showCamera
    elif event.key == 'f': #change camera view (clockwise)
        app.viewIndex = (app.viewIndex + 1)%len(app.cameraBasisAlts)
        app.cameraBasis = app.cameraBasisAlts[app.viewIndex]
        app.cameraImageCoords = app.cameraImageAlts[app.viewIndex]
    elif event.key == 'g': #change camera view (counterclockwise)
        app.viewIndex = (app.viewIndex - 1)%len(app.cameraBasisAlts)
        app.cameraBasis = app.cameraBasisAlts[app.viewIndex]
        app.cameraImageCoords = app.cameraImageAlts[app.viewIndex]

def rotateAll(app, angle=10):
    app.showCamera = False
    app.rotationAngle = (app.rotationAngle+angle)%360
    if isinstance(app.COFloor, Cube):
        app.COFloor.rotateSelf(app, angle, center=app.COFloor.center)
    if isinstance(app.CORW, Cube): 
        app.CORW.rotateSelf(app, angle, center=app.COFloor.center)
        app.COLW.rotateSelf(app, angle, center=app.COFloor.center)
    for furniture in app.furniture:
        furniture.rotateSelf(app, angle, center=app.COFloor.center)

def timerFired(app):
    if app.rotateC and not app.view and not app.helpScreen and app.drawCubeFloor and isinstance(app.CORW, Cube):
        rotateAll(app, angle=10)
    elif app.rotateCC and not app.view and not app.helpScreen and app.drawCubeFloor and isinstance(app.CORW, Cube):
        rotateAll(app, angle=-10)

def makeCubeFloor(app, event, thickness=10, floatFloor=False):
    if floatFloor: #modify temp floor
        e1 = app.cubeFloorVecs[0] #(origin + [length, 0,0])
        e2 = graph2Vecs(app, np.array([[event.x, event.y]]))[0] #(origin + [0,width,0])
        e3 = np.array([e2[0], e1[1], 0]) #(origin)

        length = (e1 - e3)[0] #origin + [length,0,0] - origin 
        width = (e2 - e3)[1] #origin + [0,width,0] - origin 
        height = thickness
        app.tempCOFloor = Cube(length, width, height, e3)

    else: #set actual floor
        th = np.array([0,0,thickness]) #thickness of the floor 
        if app.cubeFloorVecs.shape[0] == 0: #rows
            firstPoint = np.array([event.x, event.y])
            e1 = graph2Vecs(app, [firstPoint])[0]
            app.cubeFloorVecs = np.append(app.cubeFloorVecs, [e1], axis=0)
            app.cubeFloorVecs = np.append(app.cubeFloorVecs, [e1+th], axis=0)

        elif app.cubeFloorVecs.shape[0] == 2: #rows 
            secondPoint = np.array([event.x, event.y])
            e1 = app.cubeFloorVecs[0]
            e2 = graph2Vecs(app, [secondPoint])[0]
            e3 = np.array([e2[0], e1[1], 0])
            e4 = np.array([e1[0], e2[1], 0])
            for vec in [e2, e3, e4]:
                app.cubeFloorVecs = np.append(app.cubeFloorVecs, [vec], axis=0)
                app.cubeFloorVecs = np.append(app.cubeFloorVecs, [vec+th], axis=0)
            app.cubeFloorCoords = vecs2Graph(app, app.cubeFloorVecs)

            l = abs(e1[0]-e2[0])
            w = abs(e1[1]-e2[1])
            h = thickness 
            print(l,w,h)
            
            app.COFloor = Cube(l,w,h,e3)

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

def mousePressed(app, event): 
    if app.helpButton.mouseOver(app, event): 
        app.helpScreen = not app.helpScreen
    
    elif app.viewButton.mouseOver(app, event) and not app.helpScreen: 
        app.view = not app.view

    elif (app.roomButton.mouseOver(app, event) 
    and not app.view and not app.helpScreen):
        resetDrawCubeFloor(app)
        resetFurniture(app)

    elif (app.drawCubeFloor and not app.rotateC and not app.rotateCC 
    and app.rotationAngle==0 and not isinstance(app.COFloor, Cube)):
        makeCubeFloor(app, event)

    elif (isinstance(app.COFloor, Cube) and app.cubeWallHeight == None 
    and not app.rotateC and not app.rotateCC and app.rotationAngle==0):
        makeCubeWalls(app, event)

    elif (app.leftTurnButton.mouseOver(app, event) 
    and not app.view and not app.helpScreen and app.drawCubeFloor):
        app.rotateC = not app.rotateC
        app.rotateCC = False
        if not app.rotateC:
            while app.rotationAngle!=0:
                rotateAll(app, angle=10)
            app.showCamera = True
    
    elif (app.rightTurnButton.mouseOver(app, event) and 
    not app.view and not app.helpScreen and app.drawCubeFloor):
        app.rotateCC = not app.rotateCC
        app.rotateC = False
        if not app.rotateCC:
            while app.rotationAngle!=0:
                rotateAll(app, angle=-10)
            app.showCamera = True

    elif (app.cameraButton.mouseOver(app, event) 
    and not app.view and not app.helpScreen):
        app.showCamera = not app.showCamera

    elif (not app.view and app.drawCubeFloor and isinstance(app.CORW, Cube) 
    and not app.rotateC and not app.rotateCC and app.rotationAngle==0):
        origin = graph2Vecs(app, [[event.x, event.y]], z=app.COFloor.height)[0]
        if app.chairButton.mouseOver(app, event):
            app.chairButton.isPressed = True
            length = width = min(app.COFloor.length/8, app.COFloor.width/8)
            height = length*2.5
            app.newFurniture = Chair(length, width, height, 
            origin=origin, legThickness=min(2,length*0.2))
            print('add chair!')
        elif app.tableButton.mouseOver(app, event):
            app.tableButton.isPressed = True
            length = app.COFloor.length/6
            width = min((min(app.COFloor.width, app.COFloor.length), length*2))
            height = length*1.5
            app.newFurniture = Table(length, width, height, 
            origin=origin, legThickness=min(2,length*0.2))
            print('add table!')
        else:

            #check which furniture is clicked
            for i in range(len(app.furniture)):
                furniture = app.furniture[i]
                if furniture.mouseInHitbox(app, event):
                    furniture.isClicked = True
                    print('im clicked')
            
            #rotating furniture if possible
            for i in range(len(app.furniture)):
                furniture = app.furniture[i]

                if furniture.isClicked:
                    furniture.rotateSelf(app, 10, furniture.center)

                    #backtracking: rotate back if it collides with a wall.
                    if (furniture.isCollide(app.CORW) 
                    or furniture.isCollide(app.COLW)):
                        furniture.rotateSelf(app, -10, furniture.center)
                        furniture.isClicked = False
                        return
                    
                    #or if it collides with other furniture. 
                    for furniture2 in app.furniture:
                        if (furniture!=furniture2 and 
                        (furniture.isCollide(furniture2) 
                        or furniture2.isCollide(furniture))):
                            furniture.rotateSelf(app, -10, furniture.center)
                            furniture.isClicked = False
                            return

                furniture.isClicked = False

    #for debugging, print the vector
    #c = np.array([[event.x, event.y]])
    #v = graph2Vecs(app, c)[0]
    #print(v)

def mouseDragged(app, event):
    if (not app.view and app.drawCubeFloor and isinstance(app.CORW, Cube)#app.rightCubeWallVecs.shape[0]==8 
        and app.rotationAngle==0 and app.newFurniture!=None):
        o = graph2Vecs(app, [[event.x, event.y]], z=app.COFloor.height)[0]

        length2 = app.newFurniture.length
        width2 = app.newFurniture.width
        height2 = app.newFurniture.height
        tth2 = app.newFurniture.tth
        lth2 = app.newFurniture.lth

        if app.chairButton.isPressed:
            app.newFurniture = Chair(length2, width2, height2, origin=o, tableThickness=tth2, legThickness=lth2)

        elif app.tableButton.isPressed:
            app.newFurniture = Table(length2, width2, height2, origin=o, tableThickness=tth2, legThickness=lth2)

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

def mouseReleased(app, event):

    if (not app.view and not app.rotateC and not app.rotateCC 
         and app.drawCubeFloor and isinstance(app.CORW, Cube)
         and (app.chairButton.isPressed or app.tableButton.isPressed)):
        ox2, oy2, oz2 = fitFurnitureInFloor(app, app.newFurniture, app.COFloor)
        l2, w2, h2 = app.newFurniture.length, app.newFurniture.width, app.newFurniture.height
        tth2, lth2 = app.newFurniture.tth, app.newFurniture.lth

        if app.chairButton.isPressed:
            app.newFurniture = Chair(l2,w2,h2, origin=(ox2,oy2,oz2), 
                                    tableThickness=tth2, legThickness=lth2)
        elif app.tableButton.isPressed: 
            app.newFurniture = Table(l2,w2,h2, origin=(ox2,oy2,oz2), 
                                    tableThickness=tth2, legThickness=lth2)
        
        for furniture in app.furniture:
            if (app.newFurniture.isCollide(furniture) or 
                furniture.isCollide(app.newFurniture)):
                app.newFurniture = None
                for button in app.furnitureButtons:
                    button.isPressed = False
                return 
    
        app.furniture.append(app.newFurniture)
        app.newFurniture = None
        for button in app.furnitureButtons:
            button.isPressed = False

def mouseMoved(app, event): 
    if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==2:
        makeCubeFloor(app, event, floatFloor=True)
    elif app.cubeFloorVecs.shape[0]==8 and app.cubeWallHeight==None:
        makeCubeWalls(app, event, floatWalls=True)
    
    for button in app.buttons:
        if button.mouseOver(app,event):
            button.fillColor = 'pink'
            button.lineColor = 'red'
        else:
            button.fillColor = 'white'
            button.lineColor = 'black'

def drawCube(app, canvas, cubeCoords, color='black'):
    for i in range(cubeCoords.shape[0]):
        p1 = cubeCoords[i]
        for j in range(cubeCoords.shape[0]):
            p2 = cubeCoords[j]
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)

def drawCubeOutline(app, canvas, cube, color='black'):
    topFaceVecs = []
    for i in cube.topFaceVecs:
        topFaceVecs.append(cube.vecs[i])
    
    leftFrontFaceVecs = []
    for i in cube.leftFrontFaceVecs:
        leftFrontFaceVecs.append(cube.vecs[i])
    
    rightFrontFaceVecs = []
    for i in cube.rightFrontFaceVecs:
        rightFrontFaceVecs.append(cube.vecs[i])

    leftBackFaceVecs = []
    for i in cube.leftBackFaceVecs:
        leftBackFaceVecs.append(cube.vecs[i])
    
    rightBackFaceVecs = []
    for i in cube.rightBackFaceVecs:
        rightBackFaceVecs.append(cube.vecs[i])

    botFaceVecs = []
    for i in cube.botFaceVecs:
        botFaceVecs.append(cube.vecs[i])

    t = topFaceCoords = vecs2Graph(app, topFaceVecs)
    lf = leftFrontFaceCoords = vecs2Graph(app, leftFrontFaceVecs)
    rf = rightFrontFaceCoords = vecs2Graph(app, rightFrontFaceVecs)
    lb = leftBackFaceCoords = vecs2Graph(app, leftBackFaceVecs)
    rb = rightBackFaceCoords = vecs2Graph(app, rightBackFaceVecs)
    b = botFaceCoords = vecs2Graph(app, botFaceVecs)

    for r in [t,lf,rf,lb,rb,b]:
        canvas.create_line(r[0][0], r[0][1], r[1][0], r[1][1], fill=color)
        canvas.create_line(r[1][0],r[1][1], r[3][0], r[3][1], fill=color)
        canvas.create_line(r[3][0], r[3][1], r[2][0], r[2][1], fill=color)
        canvas.create_line(r[2][0],r[2][1], r[0][0], r[0][1], fill=color)
        #canvas.create_polygon(r[0][0], r[0][1], r[1][0], r[1][1], r[3][0], r[3][1], r[2][0], r[2][1], fill=None, outline=color)

    #canvas.create_polygon(t[0][0], t[0][1], t[1][0], t[1][1], t[3][0], t[3][1], t[2][0], t[2][1],fill=None)

def renderCube(app, canvas, cube):
    topFaceVecs = []
    for i in cube.topFaceVecs:
        topFaceVecs.append(cube.vecs[i])
    
    leftFrontFaceVecs = []
    for i in cube.leftFrontFaceVecs:
        leftFrontFaceVecs.append(cube.vecs[i])
    
    rightFrontFaceVecs = []
    for i in cube.rightFrontFaceVecs:
        rightFrontFaceVecs.append(cube.vecs[i])

    leftBackFaceVecs = []
    for i in cube.leftBackFaceVecs:
        leftBackFaceVecs.append(cube.vecs[i])
    
    rightBackFaceVecs = []
    for i in cube.rightBackFaceVecs:
        rightBackFaceVecs.append(cube.vecs[i])

    botFaceVecs = []
    for i in cube.botFaceVecs:
        botFaceVecs.append(cube.vecs[i])

    t = topFaceCoords = vecs2Graph(app, topFaceVecs)
    lf = leftFrontFaceCoords = vecs2Graph(app, leftFrontFaceVecs)
    rf = rightFrontFaceCoords = vecs2Graph(app, rightFrontFaceVecs)
    lb = leftBackFaceCoords = vecs2Graph(app, leftBackFaceVecs)
    rb = rightBackFaceCoords = vecs2Graph(app, rightBackFaceVecs)
    b = botFaceCoords = vecs2Graph(app, botFaceVecs)

    #print(rightBackFaceVecs)
    
    #if rb[1][1]>rb[0][1] and rb[2][0]>rb[0][0]:
    #    canvas.create_polygon(t[0][0], t[0][1], t[1][0], t[1][1], t[3][0], t[3][1], t[2][0], t[2][1],fill='yellow')
    #    canvas.create_polygon(rf[0][0], rf[0][1], rf[1][0], rf[1][1], rf[3][0], rf[3][1], rf[2][0], rf[2][1],fill='red') 
    #    canvas.create_polygon(rb[0][0], rb[0][1], rb[1][0], rb[1][1], rb[3][0], rb[3][1], rb[2][0], rb[2][1],fill='orange')
    #else:
    canvas.create_polygon(t[0][0], t[0][1], t[1][0], t[1][1], t[3][0], t[3][1], t[2][0], t[2][1],fill='yellow')
    canvas.create_polygon(lf[0][0], lf[0][1], lf[1][0], lf[1][1], lf[3][0], lf[3][1], lf[2][0], lf[2][1],fill='orange')
    canvas.create_polygon(rf[0][0], rf[0][1], rf[1][0], rf[1][1], rf[3][0], rf[3][1], rf[2][0], rf[2][1],fill='red') 

def redrawAll(app, canvas):
    if app.helpScreen:
        canvas.create_text(app.width/2, 30, text='isometrism')
        canvas.create_text(app.width/2, 60, text='controls:')
        canvas.create_text(app.width/2, 120, text='v - toggle between edit and view screens')
        canvas.create_text(app.width/2, 150, text='4 - reset room (click 3x to set room corners)')
        canvas.create_text(app.width/2, 180, text='r - rotate room')
        canvas.create_text(app.width/2, 210, text='c - toggle camera and its image plane')
        canvas.create_text(app.width/2, 240, text='x - change the camera image plane')
        canvas.create_text(app.width/2, 270, text='click & drag chairs/tables into your room from top left buttons')
        canvas.create_text(app.width/2, 300, text='h - toggle help screen')

        app.cubeTest.draw(app, canvas)
        app.chairTest.draw(app, canvas)
        app.tableTest.draw(app, canvas)

        app.helpButton.draw(app, canvas, app.helpButton.fillColor, app.helpButton.lineColor)

    elif app.title:
        app.titleFloor.draw(app, canvas, 'black')
        app.titleRW.draw(app, canvas, 'black')
        app.titleLW.draw(app, canvas, 'black')
        app.helpButton.draw(app, canvas, app.helpButton.fillColor, app.helpButton.lineColor)

    elif app.view:
        if app.showCamera:
            canvas.create_rectangle(0,0,app.width, app.height, fill='pink')
        
        if isinstance(app.CORW, Cube):
            for furniture in app.furniture:
                furniture.drawImageCoords(app, canvas, color='black')

            for cube in [app.COFloor, app.CORW, app.COLW]:
                cube.drawImageCoords(app, canvas, color='black')

        app.viewButton.draw(app, canvas, app.viewButton.fillColor, app.viewButton.lineColor)
        app.helpButton.draw(app, canvas, app.helpButton.fillColor, app.helpButton.lineColor)
        app.cameraButton.draw(app, canvas, app.cameraButton.fillColor, app.cameraButton.lineColor)
    
    else:
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

        #walls (static)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8 and isinstance(app.CORW, Cube):#app.rightCubeWallCoords.shape[0]==8:
            app.CORW.draw(app, canvas, 'black')
            app.COLW.draw(app, canvas, 'black')
            #renderCube(app, canvas, app.COLW)
            #renderCube(app, canvas, app.CORW)
        
        #walls (moving)
        elif app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8 and app.cubeWallHeight==None and isinstance(app.tempCORW, Cube):
            app.tempCORW.draw(app, canvas, 'red')
            app.tempCOLW.draw(app, canvas, 'red')

        #cube floor (static)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8:
            app.COFloor.draw(app, canvas, 'black')
            #renderCube(app, canvas, app.COFloor)

        #cube floor (moving)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==2 and isinstance(app.tempCOFloor, Cube):
            app.tempCOFloor.draw(app, canvas, 'red')

        #draw furniture
        if app.newFurniture!=None:
            app.newFurniture.draw(app, canvas, 'red')
        for furniture in app.furniture:
            furniture.draw(app, canvas, 'black')
            #hitBoxCoords = vecs2Graph(app, furniture.hitBox.vecs)
            #drawCube(app, canvas, hitBoxCoords, 'pink')

        #buttons
        for button in app.editButtons+[app.helpButton]:
            button.draw(app, canvas, button.fillColor, button.lineColor)

def main():
    runApp(width=600, height=600)