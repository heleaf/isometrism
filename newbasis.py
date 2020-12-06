import math
import numpy as np
from cmu_112_graphics import *
from threedimfunctions import *
from cube import *
from button import *

def initialize3D(app):
    app.rotationAngle = 0

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
    e3 = app.cameraOrigin + np.array([-imageLength/2, -imageDistance, imageHeight/2])
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

    #in the view
    app.COFloorImageCoords = None
    app.CORWImageCoords = None
    app.COLWImageCoords = None

    app.rotationAngle = 0

def resetFurniture(app):
    app.furniture = dict()
    #first arr = floating furniture
    #second arr = stationary furniture 
    #third arr = rendered arrays of cube coordinates
    app.furniture['Chair'] = [[], [], []]
    app.newChair = None

    app.furniture['Table'] = [[], [], []]
    app.newTable = None

    #arrays of (start, end) 1d coordinates that are occupied
    app.occupiedX = []
    app.occupiedY = []

def appStarted(app):
    initialize3D(app)
    resetDrawCubeFloor(app, init=True)

    #cut out later
    app.fv = Cube(200,200,10, (50,50,0))
    app.rw = Cube(10,200,200, (40,50,0))
    app.lw = Cube(200,10,200, (50,40,0))
    app.test = [app.fv, app.rw, app.lw]
    
    app.classCube = Cube(50,100,150, (100,100,0))
    app.misc = []
    app.tempMisc = []

    app.makeCubes = False
    app.tracker = 0
    #expand makeCubes to makeFurniture

    #### perspective rendering 
    initializeView(app) 
    app.showCamera = True

    app.lwImageCoords = perspectiveRender(app, app.cameraBasis, app.lw.vecs)
    app.floorImageCoords = perspectiveRender(app, app.cameraBasis, app.fv.vecs)
    app.ccImageCoords = perspectiveRender(app, app.cameraBasis, app.classCube.vecs)
    app.rwImageCoords = perspectiveRender(app, app.cameraBasis, app.rw.vecs)
    app.miscImageCoords = []

    #########
    resetFurniture(app)
    o = (120,60)
    app.chairButton = Button(o, 60,50, padding = 10)
    setButtonIcon(app, app.chairButton, 'Chair')

    o = (200,60)
    app.tableButton = Button(o, 60,50, padding =10)
    setButtonIcon(app, app.tableButton, 'Table')
    
    #testing out rendering
    app.customRoom = False

def setButtonIcon(app, button, iconName): #iconName = str, #button = specific app button 
    ovec = graph2Vecs(app,[button.origin])[0]
    button.setIcon(ovec, iconName)
    iconCoords = []
    for cube in button.icon.cubes:
        coords = vecs2Graph(app, cube.vecs)
        iconCoords.append(coords)
    button.iconCoords = iconCoords

def perspectiveRender(app, cameraBasis, cubeVectors): 
    #takes in: cameraOrigin(vector), 
    #          cameraBasis (matrix w/ columns as vectors of camera's basis)
    #          cubeVectors (matrix w/ vectors as rows)
    #returns:  matrix of coordinates to render (coordinates as rows)

    #get new basis of cubeVectors (matrix w/ vectors as columns)
    cameraViewCubeVecs = np.linalg.inv(cameraBasis) @ cubeVectors.T

    imgCoords = np.zeros((8,2)) #8 rows of (x,y) coordinates for Tkinter
    for i in range(cameraViewCubeVecs.shape[1]): # in terms of columns
        divisor = cameraViewCubeVecs[:,i][2] #the third element in the column of a vector
        cameraViewCubeVecs[:,i] *= 1/(divisor) #scale down to get points in the image plane 
        imgCoords[i] = -cameraViewCubeVecs[:2, i] #get the first two components (pixel addresses)

    return imgCoords

def rotateCube(app, cube, angle, rotAxis=(0,0,1)): 
    #rotates all the vectors in a cube around an axis
    newCube = np.empty((0,3))
    for vec in cube:
        if vec[0]==vec[1]==vec[2]==0:
            rotatedVec = vec
        else:
            rotatedVec = rotateVec(app, vec, 10, rotAxis)
        newCube = np.append(newCube, [rotatedVec], axis=0)
    return newCube

def toggleMakeCubes(app):
    app.makeCubes = not app.makeCubes 
    app.misc = [] 
    app.tracker = 0
    app.miscImageCoords = []
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
    if event.key == '1': toggleMakeCubes(app)
    elif event.key == '2': changeAxisAngles(app)
    elif event.key == '4': 
        resetDrawCubeFloor(app)
        resetFurniture(app)
    elif event.key == 'h': 
        #help screen
        pass
    elif event.key == 'r':
        app.showCamera = False
        app.rotationAngle = (app.rotationAngle+10)%360
        #print(app.rotationAngle)
        for cube in app.misc:
            cube.vecs = rotateCube(app, cube.vecs, 10)
            cube.origin = cube.vecs[0]
        for cube in [app.fv, app.lw, app.rw]:
            cube.vecs = rotateCube(app, cube.vecs, 10)
            cube.origin = cube.vecs[0]
        #for i in range(len(app.table.cubes)):
        #    app.table.cubes[i].vecs = rotateCube(app, app.table.cubes[i].vecs, 10)
        #    app.table.cubes[i].origin = app.table.cubes[i].vecs[0]
        #for i in range(len(app.chair.cubes)):
        #    app.chair.cubes[i].vecs = rotateCube(app, app.chair.cubes[i].vecs, 10)
        #    app.chair.cubes[i].origin = app.chair.cubes[i].vecs[0]
        if app.cubeFloorVecs.shape[0]==8:
            app.cubeFloorVecs = rotateCube(app, app.cubeFloorVecs, 10)
            app.cubeFloorCoords = vecs2Graph(app, app.cubeFloorVecs)
            app.COFloor.vecs = rotateCube(app, app.COFloor.vecs, 10)
        if app.rightCubeWallCoords.shape[0]==8:
            app.rightCubeWallVecs = rotateCube(app, app.rightCubeWallVecs, 10)
            app.rightCubeWallCoords = vecs2Graph(app, app.rightCubeWallVecs)
            app.leftCubeWallVecs = rotateCube(app, app.leftCubeWallVecs, 10)
            app.leftCubeWallCoords = vecs2Graph(app, app.leftCubeWallVecs)

        for chair in app.furniture['Chair'][1]:
            for cube in chair.cubes:
                cube.vecs = rotateCube(app, cube.vecs, 10)

        for table in app.furniture['Table'][1]:
            for cube in table.cubes:
                cube.vecs = rotateCube(app, cube.vecs, 10)

    elif event.key == 'v':   app.view = not app.view  #toggle view
    elif not app.view and app.rotationAngle == 0 and event.key == 'c': app.showCamera = not app.showCamera

    #move camera around 
    elif event.key == 'w': pass
    elif event.key == 'a': pass
    elif event.key == 's': pass
    elif event.key == 'd': pass 
    elif event.key == 'x': 
        app.viewIndex = (app.viewIndex + 1)%2
        app.cameraBasis = app.cameraBasisAlts[app.viewIndex]
        app.cameraImageCoords = app.cameraImageAlts[app.viewIndex]

        if app.drawCubeFloor and app.rightCubeWallVecs.shape[0]==8:
            app.COFloorImageCoords = perspectiveRender(app, app.cameraBasis, app.COFloor.vecs)
            app.CORWImageCoords = perspectiveRender(app, app.cameraBasis, app.CORW.vecs)
            app.COLWImageCoords = perspectiveRender(app, app.cameraBasis, app.COLW.vecs)

            for i in range(len(app.furniture['Chair'][1])):
                chair = app.furniture['Chair'][1][i]
                chairImageCoords = []
                for cube in chair.cubes:
                    coords = perspectiveRender(app, app.cameraBasis, cube.vecs)
                    chairImageCoords.append(coords)
                app.furniture['Chair'][2][i] = chairImageCoords
            
            
            for i in range(len(app.furniture['Table'][1])):
                table = app.furniture['Table'][1][i]
                tableImageCoords = []
                for cube in table.cubes:
                    coords = perspectiveRender(app, app.cameraBasis, cube.vecs)
                    tableImageCoords.append(coords)
                app.furniture['Table'][2][i] = tableImageCoords

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
        #assert(app.COFloor.vecs.all() == app.cubeFloorVecs.all())
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

    app.COFloorImageCoords = perspectiveRender(app, app.cameraBasis, app.COFloor.vecs)
    app.CORWImageCoords = perspectiveRender(app, app.cameraBasis, app.CORW.vecs)
    app.COLWImageCoords = perspectiveRender(app, app.cameraBasis, app.COLW.vecs)

    #app.CORW.width

def mousePressed(app, event): 
    if app.drawCubeFloor and app.cubeFloorCoords.shape[0]<8 and app.rotationAngle==0:
        makeCubeFloor(app, event)
    elif app.cubeFloorCoords.shape[0]==8 and app.cubeWallHeight==None:
        makeCubeWalls(app, event)

    if app.makeCubes and app.rotationAngle==0:
        origin = graph2Vecs(app, [[event.x, event.y]], z=app.fv.height)[0]
        app.newCube = Cube(30, 30, 30, origin)
        app.tempMisc.append(app.newCube)

    if not app.view and app.drawCubeFloor and app.rightCubeWallVecs.shape[0]==8 and app.rotationAngle==0:
        chox, choy = app.chairButton.origin
        chw, chh = app.chairButton.w, app.chairButton.h

        tx, ty = app.tableButton.origin
        tw, th = app.tableButton.w, app.tableButton.h

        origin = graph2Vecs(app, [[event.x, event.y]], z=app.fv.height)[0]
        if chox-chw/2<=event.x<=chox+chw/2 and choy-chh/2 <= event.y <=choy+chh/2:
            app.chairButton.isPressed = True
            length = width = min(app.COFloor.length/8, app.COFloor.width/8)
            height = length*2.5
            app.newChair = Chair(length, width, height, origin=origin, legThickness=min(2,length*0.2))
            app.furniture['Chair'][0].append(app.newChair)#
            print('add chair!')
            print(app.furniture)
        elif tx-tw/2<=event.x<=tx+tw/2 and ty-th/2<=event.y<=ty+th/2:
            app.tableButton.isPressed = True
            length = app.COFloor.length/6
            width = length*2
            height = length*1.5
            app.newTable = Table(length, width, height, origin=origin, legThickness=min(2,length*0.2))
            app.furniture['Table'][0].append(app.newTable)
            print('add table!')
            print(app.furniture)

    #for debugging, print the vector
    c = np.array([[event.x, event.y]])
    v = graph2Vecs(app, c)[0]
    print(v)

def mouseDragged(app, event):
    if app.makeCubes and app.rotationAngle==0:
        origin = graph2Vecs(app, [[event.x, event.y]], z=app.fv.height)[0]
        app.newCube = Cube(30, 30, 30, origin) #<-- make this furniture in general
        #app.tempMisc.append(app.newCube)
        if app.tempMisc != []:
            app.tempMisc[-1] = app.newCube
    if (not app.view and app.drawCubeFloor and app.rightCubeWallVecs.shape[0]==8 
        and app.rotationAngle==0):
        o = graph2Vecs(app, [[event.x, event.y]], z=app.fv.height)[0]
        if app.chairButton.isPressed:
            length = app.newChair.length
            width = app.newChair.width 
            height = app.newChair.height
            tth = app.newChair.tth
            lth = app.newChair.lth
            app.newChair = Chair(length, width, height, origin=o, tableThickness=tth, legThickness=lth)
            app.furniture['Chair'][0][-1] = app.newChair
        elif app.tableButton.isPressed:
            length = app.newTable.length
            width = app.newTable.width
            height = app.newTable.height 
            tth = app.newTable.tth
            lth = app.newTable.lth
            app.newTable = Table(length, width, height, origin=o, tableThickness=tth, legThickness=lth) 
            app.furniture['Table'][0][-1] = app.newTable

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
        and app.rotationAngle == 0):
        if app.chairButton.isPressed:
            #constrain to room boundaries 
            ox,oy,oz = fitFurnitureInFloor(app, app.newChair, app.COFloor)

            l,w,h = app.newChair.length, app.newChair.width, app.newChair.height
            tth, lth = app.newChair.tth, app.newChair.lth

            app.newChair = Chair(l,w,h, origin=(ox,oy,oz), tableThickness=tth, legThickness=lth)

            #make sure there is no overlap (collision detection)
            for i in range(len(app.occupiedX)):
                startX = min(app.occupiedX[i])
                endX = max(app.occupiedX[i])
                startY = min(app.occupiedY[i])
                endY = max(app.occupiedY[i])
                if ((startX < ox < endX or startX < ox+l < endX) and
                    (startY < oy < endY or startY < oy+w < endY)):
                    print('nope')
                    app.furniture['Chair'][0].pop()
                    app.newChair = None
                    app.chairButton.isPressed = False
                    return 

            #passing collision detection
            app.occupiedX.append([ox, ox+app.newChair.length])
            app.occupiedY.append([oy, oy+app.newChair.width])
        
            app.furniture['Chair'][1].append(app.newChair)
            app.furniture['Chair'][0].pop()
            chairImageCoords = []
            for cube in app.newChair.cubes:
                coords = perspectiveRender(app, app.cameraBasis, cube.vecs)
                chairImageCoords.append(coords)
            app.furniture['Chair'][2].append(chairImageCoords)
            app.newChair = None
            app.chairButton.isPressed = False

        elif app.tableButton.isPressed: 
            ox,oy,oz = fitFurnitureInFloor(app, app.newTable, app.COFloor)
            l,w,h = app.newTable.length, app.newTable.width, app.newTable.height
            tth, lth = app.newTable.tth, app.newTable.lth

            app.newTable = Table(l,w,h, origin=(ox,oy,oz), tableThickness=tth, legThickness=lth)

            #make sure there is no overlap (collision detection)
            for i in range(len(app.occupiedX)):
                startX = min(app.occupiedX[i])
                endX = max(app.occupiedX[i])
                startY = min(app.occupiedY[i])
                endY = max(app.occupiedY[i])
                if ((startX < ox < endX or startX < ox+l < endX) and
                    (startY < oy < endY or startY < oy+w < endY)):
                    print('nope')
                    app.furniture['Table'][0].pop()
                    app.newTable = None
                    app.tableButton.isPressed = False
                    return 

            #passing collision detection
            app.occupiedX.append([ox, ox+app.newTable.length])
            app.occupiedY.append([oy, oy+app.newTable.width])
        
            app.furniture['Table'][1].append(app.newTable)
            app.furniture['Table'][0].pop()
            tableImageCoords = []
            for cube in app.newTable.cubes:
                coords = perspectiveRender(app, app.cameraBasis, cube.vecs)
                tableImageCoords.append(coords)
            app.furniture['Table'][2].append(tableImageCoords)

            app.newTable = None
            app.tableButton.isPressed = False

    if (app.makeCubes and app.rotationAngle == 0):
        ox,oy,oz = fitFurnitureInFloor(app, app.newCube, app.fv)
        app.newCube = Cube(30,30,30, (ox,oy,oz))
  
        imc = perspectiveRender(app, app.cameraBasis, app.newCube.vecs)
        app.miscImageCoords.append(imc)
        app.misc.append(app.newCube)
        app.tempMisc.pop()

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

    t = topFaceCoords = vecs2Graph(app, topFaceVecs)
    lf = leftFrontFaceCoords = vecs2Graph(app, leftFrontFaceVecs)
    rf = rightFrontFaceCoords = vecs2Graph(app, rightFrontFaceVecs)
    lb = leftBackFaceCoords = vecs2Graph(app, leftBackFaceVecs)
    rb = rightBackFaceCoords = vecs2Graph(app, rightBackFaceVecs)

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

    if app.view:
        #here's our view window
        canvas.create_rectangle(0,0,app.width, app.height, fill='pink')
        
        if (isinstance(app.COFloorImageCoords, np.ndarray) 
            and app.COFloorImageCoords.all() != None):

            for furniture in app.furniture['Chair'][2]:
                for cubeCoords in furniture:
                    drawCube(app, canvas, cubeCoords, color = 'orange')

            for furniture in app.furniture['Table'][2]:
                for cubeCoords in furniture:
                    drawCube(app, canvas, cubeCoords, color = 'orange')

            drawCube(app, canvas, app.COFloorImageCoords, color = 'red')
            drawCube(app, canvas, app.CORWImageCoords, color = 'red')
            drawCube(app, canvas, app.COLWImageCoords, color = 'red')

            
        '''
        drawCube(app, canvas, app.ccImageCoords, color = 'orange')

        drawCube(app, canvas, app.lwImageCoords, color = 'purple')
        drawCube(app, canvas, app.floorImageCoords, color = 'purple')
        drawCube(app, canvas, app.rwImageCoords, color = 'purple')
        '''
        #not working :(
        for imc in app.miscImageCoords: #wait yo this is working dawg
            drawCube(app, canvas, imc)
    
    else:
        if app.showCamera:
            #image face (view window)
            #imageCoord = app.cameraImageAlts
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
        chox, choy = app.chairButton.origin
        chw, chh = app.chairButton.w, app.chairButton.h
        chc = app.chairButton.color
        canvas.create_rectangle(chox-chw/2, choy-chh/2, chox+chw/2, choy+chh/2, fill=chc)
        for coords in app.chairButton.iconCoords:
            drawCube(app, canvas, coords)

        tox, toy = app.tableButton.origin
        tw, th = app.tableButton.w, app.tableButton.h
        tc = app.tableButton.color
        canvas.create_rectangle(tox-tw/2, toy-th/2, tox+tw/2, toy+th/2, fill=tc)
        for coords in app.tableButton.iconCoords:
            drawCube(app, canvas, coords) 


        #draw table
        #for cube in app.table.cubes:
        #    coords = vecs2Graph(app, cube.vecs)
        #    drawCube(app, canvas, coords)

        #draw chair
        #for cube in app.chair.cubes:
        #    coords = vecs2Graph(app, cube.vecs)
        #    drawCube(app, canvas, coords)
    
        '''
        #draw the room 
        for c in app.test: #walls, floor 
            c = vecs2Graph(app, c.vecs)
            drawCube(app, canvas, c, 'purple')
        '''
        #cubes? 
        for cube in app.misc:
            c = vecs2Graph(app, cube.vecs)
            drawCube(app, canvas, c, 'orange')

        #hovering cubes
        for cube in app.tempMisc:
            c = vecs2Graph(app, cube.vecs)
            drawCube(app, canvas, c, 'red')
        '''
        #classcube
        coords = vecs2Graph(app, app.classCube.vecs)
        drawCube(app, canvas, coords, color = 'orange')
        '''
        ox, oy = app.origin

        #walls (static)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8 and app.rightCubeWallCoords.shape[0]==8:
            drawCube(app, canvas, app.rightCubeWallCoords, 'red')
            drawCube(app, canvas, app.leftCubeWallCoords, 'red')
            
            #renderCube(app, canvas, app.COLW)
            #renderCube(app, canvas, app.CORW)
        
        #walls (moving)
        elif app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8 and app.cubeWallHeight==None:
            #print(app.tempRightCubeWallCoords)
            drawCube(app, canvas, app.tempRightCubeWallCoords, 'red')
            drawCube(app, canvas, app.tempLeftCubeWallCoords, 'red')

        #cube floor (static)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8:
            drawCube(app, canvas, app.cubeFloorCoords, 'red')
            #renderCube(app, canvas, app.COFloor)
        #cube floor (moving)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==2:
            drawCube(app, canvas, app.tempCubeFloorCoords, 'red')

        #draw furniture
        if app.newChair!=None:
            for cube in app.newChair.cubes:
                coords = vecs2Graph(app, cube.vecs)
                drawCube(app, canvas, coords, color='red')
        for chair in app.furniture['Chair'][1]:
            for cube in chair.cubes:
                coords = vecs2Graph(app, cube.vecs)
                drawCube(app, canvas, coords, color='orange') 

        if app.newTable!=None:
            for cube in app.newTable.cubes:
                coords = vecs2Graph(app, cube.vecs)
                drawCube(app, canvas, coords, color='red')
        for table in app.furniture['Table'][1]:
            for cube in table.cubes:
                coords = vecs2Graph(app, cube.vecs)
                drawCube(app, canvas, coords, color='orange')  

def main():
    runApp(width=600, height=600)

main()