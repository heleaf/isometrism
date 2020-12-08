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

def initializeView(app): #perspective rendering
    app.view = False
    app.cameraOrigin = np.array([0,30,60]) #change this to be something based on where the room is
    #app.cameraOrigin = np.array([100,0,30])
    imageDistance = 35
    imageLength = 80
    imageHeight = 80

    #be able to move the camera (then recalculate all imageCoordsFront)
    #generate the camera based on where the player's room is built
    #imageLength = imageHeight = 100

    #front facing (push forward on x)
    imageTopLeft = app.cameraOrigin + np.array([imageDistance, imageLength/2, imageHeight/2])
    imageTopRight = imageTopLeft + np.array([0,-imageLength, 0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([0,-imageLength,-imageHeight])
    app.cameraImageCoords = app.imageCoordsFront = vecs2Graph(app, [imageTopLeft, imageTopRight, imageBotRight, imageBotLeft])

    a1 = np.array([0,imageLength/app.width,0])
    a2 = np.array([0,0,imageHeight/app.height])
    a3 = imageTopLeft 
    app.cameraBasis = np.array([a1,a2,a3]).T #basis of camera vectors as columns 

    #right facing (flipped)
    b1 = np.array([imageLength/app.width,0,0])
    b2 = np.array([0,0,imageHeight/app.height])
    b3 = app.cameraOrigin + np.array([imageLength/2, imageDistance, imageHeight/2])

    #app.cameraBasis = np.array([b1,b2,b3]).T 
    #gibbirish
    '''
    c1 = np.array([imageLength/app.width,0,0])
    c2 = np.array([0,0,imageHeight/app.height])
    c3 = app.cameraOrigin + np.array([-imageLength/2, imageDistance, imageHeight/2])

    app.cameraBasis = np.array([c1,c2,c3]).T
    '''

    #this right facing is better, i think
    d1 = np.array([-imageLength/app.width,0,0])
    d2 = np.array([0,0,imageHeight/app.height])
    d3 = app.cameraOrigin + np.array([-imageLength/2, imageDistance, imageHeight/2])
    

    imageTopLeft = d3
    imageTopRight = imageTopLeft + np.array([imageLength,0,0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([imageLength, 0, -imageHeight])
    app.imageCoordsRight = vecs2Graph(app, [imageTopLeft, imageTopRight, imageBotRight, imageBotLeft]) 
    #imageTopLeft = app.cameraOrigin + np.array([imageDistance, imageLength/2, imageHeight/2]
    #app.cameraBasis = np.array([d1,d2,d3]).T

    e1 = np.array([imageLength/app.width,0,0])
    e2 = np.array([0,0,imageHeight/app.height])
    e3 = app.cameraOrigin + np.array([imageLength/2, imageDistance, imageHeight/2]) 

    #f1 = np.array([0,imageLength/app.width, 0])
    #f2 = np.array([0,0,])
    #f3 
    #app.cameraBasis = np.array([e1,e2,e3]).T


    app.cameraBasisAlts = [np.array([a1,a2,a3]).T, np.array([d1,d2,d3]).T]
    app.cameraImageAlts = [app.imageCoordsFront, app.imageCoordsRight]
    app.viewIndex = 0

    #app.cameraBasis = np.array([b1,b2,b3]).T

    #left facing (push forward on y)
    '''
    imageTopLeft = app.cameraOrigin + np.array([imageLength/2, -imageDistance, imageHeight/2])
    a1 = np.array([imageLength/app.width, 0,0])
    a2 = np.array([0,0,imageHeight/app.height])
    a3 = imageTopLeft
    '''
    #app.cameraBasis = np.array([a1,a2,a3]).T 
    #app.cameraBasisAlts.append(np.array([a1,a2,a3]))
    #imageTopRight = imageTopLeft + np.array([-imageLength, 0,0])
    #imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    #imageBotRight = imageTopLeft + np.array([-imageLength, 0, -imageHeight])

def resetDrawCubeFloor(app, init=False):
    if init:
        app.drawCubeFloor = False
    else:
        app.drawCubeFloor = not app.drawCubeFloor

    app.cubeFloorVecs = np.empty((0,3))
    app.cubeFloorCoords = np.empty((0,2))

    #hovering floor
    app.tempCubeFloorVecs = np.empty((0,3))
    app.tempCubeFloorCoords = np.empty((0,2))

    app.cubeWallHeight = None

    app.leftCubeWallCoords = np.empty((0,2))
    app.rightCubeWallCoords = np.empty((0,2))
    app.leftCubeWallVecs = np.empty((0,3))
    app.rightCubeWallVecs = np.empty((0,3))

    #hovering walls
    app.tempLeftCubeWallCoords = np.empty((0,2))
    app.tempRightCubeWallCoords = np.empty((0,2))
    app.tempLeftCubeWallVecs = np.empty((0,3))
    app.tempRightCubeWallVecs = np.empty((0,3))

    #objects 
    app.COFloor = None
    app.COLW = None
    app.CORW = None 

    app.rotationAngle = 0

def resetFurniture(app):
    app.furniture = []
    app.newFurniture = None

    #arrays of (start, end) 1d coordinates that are occupied
    app.occupiedX = []
    app.occupiedY = []

def appStarted(app):
    initialize3D(app)
    app.rotationAngle = 0
    app.rotate = False
    resetDrawCubeFloor(app, init=True)

    #### perspective rendering 
    initializeView(app) 
    app.showCamera = True

    #########
    resetFurniture(app)
    o = (140,60)
    app.roomButton = Button(o, 60,50, padding=10)
    setButtonIcon(app, app.roomButton, 'Room')

    o = (220,60)
    app.chairButton = Button(o, 60,50, padding = 10)
    setButtonIcon(app, app.chairButton, 'Chair')

    o = (300,60)
    app.tableButton = Button(o, 60,50, padding =10)
    setButtonIcon(app, app.tableButton, 'Table')
    
    #testing out rendering
    app.customRoom = False
    app.helpScreen = True

    app.cubeTest = Cube(30,30,30,(100,100,0))
    app.tableTest = Table(30,30,30,(200,200,0))
    app.chairTest = Chair(30,30,30,(300,300,0))

def setButtonIcon(app, button, iconName): #iconName = str, #button = specific app button 
    ovec = graph2Vecs(app,[button.origin])[0]
    button.setIcon(ovec, iconName)
'''
def changeAxisAngles(app):
    #try shifting origin? 
    #app.origin = (app.origin[0]+20, app.origin[1]+20)
    #try changing initial angles? 
    app.xAxisInitAngle-=10
    app.yAxisInitAngle+=10
    app.xAxisAngle = deg2Rad(app.xAxisInitAngle+app.rotationAngle)
    app.yAxisAngle = deg2Rad(app.yAxisInitAngle+app.rotationAngle)
def changeOrigin(app): pass
    #move the center of the room to the origin point 
'''
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
    if event.key == 'h': 
        app.helpScreen = not app.helpScreen #help screen
    elif event.key == '1': toggleMakeCubes(app)
    elif event.key == '2': changeAxisAngles(app)
    elif event.key == '3' and not app.view and not app.helpScreen: 
        app.rotate = not app.rotate
        if not app.rotate:
            while app.rotationAngle!=0:
                rotateAll(app)
            app.showCamera = True
    elif event.key == 'r' and not app.view and not app.helpScreen:
        app.cubeTest.rotateSelf(app, 10, center=app.cubeTest.center)
        app.tableTest.rotateSelf(app,10, center=app.tableTest.center)
        app.chairTest.rotateSelf(app, 10, center=app.chairTest.center)

        app.showCamera = False
        app.rotationAngle = (app.rotationAngle+10)%360
        
        if app.cubeFloorVecs.shape[0]==8:
            app.COFloor.rotateSelf(app, 10, center=app.COFloor.center)
        if app.rightCubeWallCoords.shape[0]==8:
            app.CORW.rotateSelf(app, 10, center=app.COFloor.center)
            app.COLW.rotateSelf(app, 10, center=app.COFloor.center)

        for furniture in app.furniture:
            furniture.rotateSelf(app, 10, center=app.COFloor.center)

    elif event.key == 'v':   app.view = not app.view  #toggle view
    elif not app.view and app.rotationAngle == 0 and event.key == 'c': app.showCamera = not app.showCamera
    #move camera around ?
    elif event.key == 'w': pass
    elif event.key == 'a': pass
    elif event.key == 's': pass
    elif event.key == 'd': pass 
    elif event.key == 'x': #change camera view 
        app.viewIndex = (app.viewIndex + 1)%len(app.cameraBasisAlts)
        app.cameraBasis = app.cameraBasisAlts[app.viewIndex]
        app.cameraImageCoords = app.cameraImageAlts[app.viewIndex]

        if app.drawCubeFloor and app.rightCubeWallVecs.shape[0]==8:
            app.COFloorImageCoords = perspectiveRender(app, app.cameraBasis, app.COFloor.vecs)
            app.CORWImageCoords = perspectiveRender(app, app.cameraBasis, app.CORW.vecs)
            app.COLWImageCoords = perspectiveRender(app, app.cameraBasis, app.COLW.vecs)

def rotateAll(app):
    app.showCamera = False
    app.rotationAngle = (app.rotationAngle+10)%360
    
    if app.cubeFloorVecs.shape[0]==8:
        app.COFloor.rotateSelf(app, 10, center=app.COFloor.center)
    if app.rightCubeWallCoords.shape[0]==8:
        app.CORW.rotateSelf(app, 10, center=app.COFloor.center)
        app.COLW.rotateSelf(app, 10, center=app.COFloor.center)

    for furniture in app.furniture:
        furniture.rotateSelf(app, 10, center=app.COFloor.center)

def timerFired(app):
    if app.rotate:
        rotateAll(app)

def makeCubeFloor(app, event, thickness=10):
    th = np.array([0,0,thickness]) #thickness of the floor, arbitrary for now 
    if app.cubeFloorVecs.shape[0] == 0: #rows
        firstPoint = np.array([event.x, event.y])
        e1 = graph2Vecs(app, [firstPoint])[0]
        app.cubeFloorVecs = np.append(app.cubeFloorVecs, [e1], axis=0)
        app.cubeFloorVecs = np.append(app.cubeFloorVecs, [e1+th], axis=0)
        for i in range(4):
            app.tempCubeFloorVecs = np.append(app.tempCubeFloorVecs, [e1], axis=0)
            app.tempCubeFloorVecs = np.append(app.tempCubeFloorVecs, [e1+th], axis=0)
        app.tempCubeFloorCoords = vecs2Graph(app, app.tempCubeFloorVecs) 

    elif app.cubeFloorVecs.shape[0] == 2: #rows 
        secondPoint = np.array([event.x, event.y])
        e2 = graph2Vecs(app, [secondPoint])[0]
        e1 = app.cubeFloorVecs[0]

        e3 = np.array([e2[0], e1[1], 0])
        e4 = np.array([e1[0], e2[1], 0])
        for vec in [e2, e3, e4]:
            app.cubeFloorVecs = np.append(app.cubeFloorVecs, [vec], axis=0)
            app.cubeFloorVecs = np.append(app.cubeFloorVecs, [vec+th], axis=0)

        app.cubeFloorCoords = vecs2Graph(app, app.cubeFloorVecs)
        for vec in [e2, e3, e2, e3]:
            app.tempRightCubeWallVecs = np.append(app.tempRightCubeWallVecs, [vec], axis=0)
            app.tempRightCubeWallVecs = np.append(app.tempRightCubeWallVecs, [vec + np.array([-10,0,0])], axis=0)
            #rw
        for vec in [e1, e3, e2, e3]:
            app.tempLeftCubeWallVecs = np.append(app.tempLeftCubeWallVecs, [vec], axis=0)
            app.tempLeftCubeWallVecs = np.append(app.tempLeftCubeWallVecs, [vec + np.array([0,-10,0])], axis=0)
            #lw 
        
        l = abs(e1[0]-e2[0])
        w = abs(e1[1]-e2[1])
        h = thickness 
        print(l,w,h)
        
        app.COFloor = Cube(l,w,h,e3)
        print('madeit')

def floatCubeFloor(app, event):
    th = np.array([0,0,10]) #arbitrary thickness
    e2 = graph2Vecs(app, np.array([[event.x, event.y]]))[0]
    e1 = app.cubeFloorVecs[0]
    e3 = np.array([e2[0], e1[1], 0])
    e4 = np.array([e1[0], e2[1], 0])
    vecs2Add = [e2, e2+th, e3, e3+th, e4, e4+th]
    for i in range(2, 8):
        app.tempCubeFloorVecs[i] = vecs2Add[i-2]
    #print(app.tempCubeFloorVecs)
    app.tempCubeFloorCoords = vecs2Graph(app, app.tempCubeFloorVecs) 

def floatCubeWalls(app, event):
    h = app.cubeFloorCoords[3][1]-event.y
    
    rwVecs = [app.cubeFloorVecs[2], app.cubeFloorVecs[4]] 

    for i in range(len(rwVecs)):
        app.tempRightCubeWallVecs[i] = rwVecs[i]
        app.tempRightCubeWallVecs[i+2] = rwVecs[i] + np.array([0,0,h])
        app.tempRightCubeWallVecs[i+4] = rwVecs[i] + np.array([[-10,0,0]])
        app.tempRightCubeWallVecs[i+6] = rwVecs[i] + np.array([[-10,0,h]])
    
    app.tempRightCubeWallCoords = vecs2Graph(app, app.tempRightCubeWallVecs)

    lwVecs = [app.cubeFloorVecs[0], app.cubeFloorVecs[4]]
    for i in range(len(lwVecs)):
        app.tempLeftCubeWallVecs[i] = lwVecs[i]
        app.tempLeftCubeWallVecs[i+2] = lwVecs[i] + np.array([0,0,h])
        app.tempLeftCubeWallVecs[i+4] = lwVecs[i] + np.array([0,-10,0])
        app.tempLeftCubeWallVecs[i+6] = lwVecs[i] + np.array([0,-10,h])

    app.tempLeftCubeWallCoords = vecs2Graph(app, app.tempLeftCubeWallVecs)

def makeCubeWalls(app, event):
    app.cubeWallHeight = app.cubeFloorCoords[3][1]-event.y
    
    #replace magic nums with custom height
    for vec in [app.cubeFloorVecs[2], app.cubeFloorVecs[4]]:
        app.rightCubeWallVecs = np.append(app.rightCubeWallVecs, [vec], axis=0)
        app.rightCubeWallVecs = np.append(app.rightCubeWallVecs, [vec + np.array([0,0,app.cubeWallHeight])], axis=0)
        app.rightCubeWallVecs = np.append(app.rightCubeWallVecs, [vec + np.array([-10,0,0])], axis=0)
        app.rightCubeWallVecs = np.append(app.rightCubeWallVecs, [vec + np.array([-10,0,app.cubeWallHeight])], axis=0) 

        app.tempRightCubeWallVecs = np.append(app.tempRightCubeWallVecs, [vec], axis=0)
        app.tempRightCubeWallVecs = np.append(app.tempRightCubeWallVecs, [vec + np.array([-10,0,0])], axis=0)
        app.tempRightCubeWallVecs = np.append(app.tempRightCubeWallVecs, [vec], axis=0)
        app.tempRightCubeWallVecs = np.append(app.tempRightCubeWallVecs, [vec + np.array([-10,0,0])], axis=0)  

    app.rightCubeWallCoords = vecs2Graph(app, app.rightCubeWallVecs)

    for vec in [app.cubeFloorVecs[0], app.cubeFloorVecs[4]]:
        app.leftCubeWallVecs = np.append(app.leftCubeWallVecs, [vec], axis=0)
        app.leftCubeWallVecs = np.append(app.leftCubeWallVecs, [vec + np.array([0,0,app.cubeWallHeight])], axis=0)
        app.leftCubeWallVecs = np.append(app.leftCubeWallVecs, [vec + np.array([0,-10,0])], axis=0)
        app.leftCubeWallVecs = np.append(app.leftCubeWallVecs, [vec + np.array([0,-10,app.cubeWallHeight])], axis=0)

        app.tempLeftCubeWallVecs = np.append(app.tempLeftCubeWallVecs, [vec], axis=0)
        app.tempLeftCubeWallVecs = np.append(app.tempLeftCubeWallVecs, [vec + np.array([0,-10,0])], axis=0)
        app.tempLeftCubeWallVecs = np.append(app.tempLeftCubeWallVecs, [vec], axis=0)
        app.tempLeftCubeWallVecs = np.append(app.tempLeftCubeWallVecs, [vec + np.array([0,-10,0])], axis=0)  

    app.leftCubeWallCoords = vecs2Graph(app, app.leftCubeWallVecs)

    #making Cube objects of walls for rendering 
    rl = app.COFloor.height
    rw = app.COFloor.width
    rh = app.cubeWallHeight
    rx,ry,rz = app.COFloor.origin[0]-rl, app.COFloor.origin[1], 0 

    app.CORW = Cube(rl, rw, rh, (rx, ry, rz))
    
    ll = app.COFloor.length
    lw = app.COFloor.height
    lh = app.cubeWallHeight
    lx,ly,lz = app.COFloor.origin[0], app.COFloor.origin[1]-lw, 0
    app.COLW = Cube(ll, lw, lh, (lx,ly,lz))

    #app.COFloorImageCoords = perspectiveRender(app, app.cameraBasis, app.COFloor.vecs)
    #app.CORWImageCoords = perspectiveRender(app, app.cameraBasis, app.CORW.vecs)
    #app.COLWImageCoords = perspectiveRender(app, app.cameraBasis, app.COLW.vecs)

    #app.CORW.width

def mousePressed(app, event): 
    '''
    if app.drawCubeFloor and app.cubeFloorCoords.shape[0]<8 and app.rotationAngle==0:
        makeCubeFloor(app, event)
    elif app.cubeFloorCoords.shape[0]==8 and app.cubeWallHeight==None:
        makeCubeWalls(app, event)
    '''
    rox, roy = app.roomButton.origin
    rw, rh = app.roomButton.w, app.roomButton.h
    if rox-rw/2 <= event.x <= rox+rw/2 and roy-rh/2 <= event.y <= roy+rh/2:
        resetDrawCubeFloor(app)
        resetFurniture(app)

    elif app.drawCubeFloor and app.cubeFloorCoords.shape[0]<8 and app.rotationAngle==0:
        makeCubeFloor(app, event)

    elif app.cubeFloorCoords.shape[0]==8 and app.cubeWallHeight==None:
        makeCubeWalls(app, event)

    elif not app.view and app.drawCubeFloor and app.rightCubeWallVecs.shape[0]==8 and app.rotationAngle==0:

        chox, choy = app.chairButton.origin
        chw, chh = app.chairButton.w, app.chairButton.h

        tx, ty = app.tableButton.origin
        tw, th = app.tableButton.w, app.tableButton.h

        origin = graph2Vecs(app, [[event.x, event.y]], z=app.COFloor.height)[0]
        if chox-chw/2<=event.x<=chox+chw/2 and choy-chh/2 <= event.y <=choy+chh/2:
            app.chairButton.isPressed = True
            length = width = min(app.COFloor.length/8, app.COFloor.width/8)
            height = length*2.5
            app.newFurniture = Chair(length, width, height, origin=origin, legThickness=min(2,length*0.2))
            print('add chair!')
        elif tx-tw/2<=event.x<=tx+tw/2 and ty-th/2<=event.y<=ty+th/2:
            app.tableButton.isPressed = True
            length = app.COFloor.length/6
            width = length*2
            height = length*1.5
            app.newFurniture = Table(length, width, height, origin=origin, legThickness=min(2,length*0.2))
            print('add table!')

        else:
            for i in range(len(app.furniture)):
                furniture = app.furniture[i]

                #making hitBox
                l,w,h = furniture.length, furniture.width, furniture.height
                
                #get leftX from this 
                leftVec = furniture.origin + np.array([l,0,0])
                leftCoord = vecs2Graph(app, [leftVec])[0]
                leftX = leftCoord[0]

                #get rightX from this 
                rightVec = furniture.origin + np.array([0,w,0])
                rightCoord = vecs2Graph(app, [rightVec])[0]
                rightX = rightCoord[0]

                #topY from this 
                topVec = furniture.origin + np.array([0,0,h])
                topCoord = vecs2Graph(app, [topVec])[0]
                topY = topCoord[1]
                
                #botY from this 
                botVec = furniture.origin + np.array([l,w,0])
                botCoord = vecs2Graph(app, [botVec])[0]
                botY = botCoord[1]

                if leftX <= event.x <= rightX and topY <= event.y <= botY:
                    furniture.isClicked = True
                    print('im clicked')
            
            #resetting
            for i in range(len(app.furniture)):
                furniture = app.furniture[i]

                if furniture.isClicked:
                    furniture.rotateSelf(app, 10, furniture.center)

                    furnitureImageCoords = []
                    
                    for furniture2 in app.furniture:
                        if furniture!=furniture2 and (furniture.isCollide(furniture2) or furniture2.isCollide(furniture)):
                            furniture.rotateSelf(app, -10, furniture.center)
                            furniture.isClicked = False
                            return

                furniture.isClicked = False

    #for debugging, print the vector
    c = np.array([[event.x, event.y]])
    v = graph2Vecs(app, c)[0]
    print(v)

def mouseDragged(app, event):
    if (not app.view and app.drawCubeFloor and app.rightCubeWallVecs.shape[0]==8 
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

    if (not app.view and app.drawCubeFloor and app.rightCubeWallVecs.shape[0]==8 
        and app.rotationAngle == 0 and (app.chairButton.isPressed or app.tableButton.isPressed)):
        ox2, oy2, oz2 = fitFurnitureInFloor(app, app.newFurniture, app.COFloor)
        l2, w2, h2 = app.newFurniture.length, app.newFurniture.width, app.newFurniture.height
        tth2, lth2 = app.newFurniture.tth, app.newFurniture.lth

        if app.chairButton.isPressed:
            app.newFurniture = Chair(l2,w2,h2, origin=(ox2,oy2,oz2), tableThickness=tth2, legThickness=lth2)
        elif app.tableButton.isPressed: 
            app.newFurniture = Table(l2,w2,h2, origin=(ox2,oy2,oz2), tableThickness=tth2, legThickness=lth2)
        
        for furniture in app.furniture:
            if app.newFurniture.isCollide(furniture) or furniture.isCollide(app.newFurniture):
                print('no :o')
                app.newFurniture = None
                app.chairButton.isPressed = False
                app.tableButton.isPressed = False
                return 
    
        app.furniture.append(app.newFurniture)

        app.newFurniture = None
        app.tableButton.isPressed = False
        app.chairButton.isPressed = False

def mouseMoved(app, event): 
    if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==2:
        floatCubeFloor(app, event)
    elif app.cubeFloorVecs.shape[0]==8 and app.cubeWallHeight==None:
        floatCubeWalls(app, event)

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

    elif app.view:
        #here's our view window
        canvas.create_rectangle(0,0,app.width, app.height, fill='pink')
        
        if isinstance(app.CORW, Cube):
            for furniture in app.furniture:
                furniture.drawImageCoords(app, canvas, color='black')

            for cube in [app.COFloor, app.CORW, app.COLW]:
                cube.drawImageCoords(app, canvas, color='black')
    
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
            canvas.create_oval(x-r, y-r, x+r, y+r, fill = 'red')
        
        #buttons
        for button in [app.roomButton, app.chairButton, app.tableButton]:
            box, boy = button.origin
            bw, bh = button.w, button.h
            bc = button.color
            canvas.create_rectangle(box-bw/2, boy-bh/2, box+bw/2, boy+bh/2, fill=bc)
            if button.icon!=None:
                for cube in button.icon:
                    cube.draw(app, canvas, 'black')

        ox, oy = app.origin

        #walls (static)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8 and app.rightCubeWallCoords.shape[0]==8:
            app.CORW.draw(app, canvas, 'black')
            app.COLW.draw(app, canvas, 'black')
            #renderCube(app, canvas, app.COLW)
            #renderCube(app, canvas, app.CORW)
        
        #walls (moving)
        elif app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8 and app.cubeWallHeight==None:
            drawCube(app, canvas, app.tempRightCubeWallCoords, 'red')
            drawCube(app, canvas, app.tempLeftCubeWallCoords, 'red')

        #cube floor (static)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8:
            app.COFloor.draw(app, canvas, 'black')
            #renderCube(app, canvas, app.COFloor)

        #cube floor (moving)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==2:
            drawCube(app, canvas, app.tempCubeFloorCoords, 'red')

        #draw furniture
        if app.newFurniture!=None:
            app.newFurniture.draw(app, canvas, 'red')
        for furniture in app.furniture:
            furniture.draw(app, canvas, 'black')
            #hitBoxCoords = vecs2Graph(app, furniture.hitBox.vecs)
            #drawCube(app, canvas, hitBoxCoords, 'pink')

def main():
    runApp(width=600, height=600)