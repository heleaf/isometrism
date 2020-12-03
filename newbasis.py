import math
import numpy as np
from cmu_112_graphics import *
from threedimfunctions import *
from oldfloor import *
from cube import *

def initialize(app):
    app.rotationAngle = 0

    app.xRotationAngle = 0
    app.yRotationAngle = 0

    app.origin = (app.width/2, app.height/2)

    app.xAxisInitAngle = 200
    app.yAxisInitAngle = 340

    app.xAxisAngle = deg2Rad(app.xAxisInitAngle+app.rotationAngle)
    app.yAxisAngle = deg2Rad(app.yAxisInitAngle+app.rotationAngle)

    app.CUBE = np.array([[10,10,0],
                        [60,10,0],
                        [10,60,0],
                        [10,10,50],
                        [60,60,0],
                        [60,10,50],
                        [10,60,50],
                        [60,60,50]])
    app.CUBEPOINTS = vecs2Graph(app, app.CUBE)
    app.showUnitCube = False

    app.xAxisVec = np.array([100,0,0])
    app.yAxisVec = np.array([0,100,0])

    app.drawCubeFloor = False
    app.cubeFloorVecs = np.empty((0,3))
    app.tempCubeFloorVecs = np.empty((0,3))
    app.cubeFloorCoords = np.empty((0,2))

    app.cubeWallHeight = None
    app.leftCubeWallCoords = np.empty((0,2))
    app.rightCubeWallCoords = np.empty((0,2))
    app.tempLeftCubeWallCoords = np.empty((0,2))
    app.tempRightCubeWallCoords = np.empty((0,2))

    app.sampleCubeFloorVecs = np.array([[287.7097569,   39.75633592,  0.        ],
                                    [287.7097569,   39.75633592,  10.        ],
                                    [ 43.73894914, 301.26997008,   0.        ],
                                    [ 43.73894914, 301.26997008,  10.        ],
                                    [ 43.73894914,  39.75633592,   0.        ],
                                    [ 43.73894914, 39.75633592,  10.        ],
                                    [287.7097569,  301.26997008,   0.        ],
                                    [287.7097569,  301.26997008, 10.        ]])
    
    app.sampleCubeFloorCoords = vecs2Graph(app, app.sampleCubeFloorVecs)

    app.sampleCubeRWVecs = np.array([[ 43.73894914, 301.26997008,   0.        ],
                                [ 43.73894914, 301.26997008, 138.        ],
                                [ 33.73894914, 301.26997008,   0.        ],
                                [ 33.73894914, 301.26997008, 138.        ],
                                [ 43.73894914,  39.75633592,   0.        ],
                                [ 43.73894914,  39.75633592, 138.        ],
                                [ 33.73894914, 39.75633592,   0.        ],
                                [ 33.73894914, 39.75633592, 138.        ]])
    app.sampleCubeRWCoords = vecs2Graph(app, app.sampleCubeRWVecs)

    app.sampleCubeLWVecs = np.array([[287.7097569,   39.75633592,   0.        ],
                                    [287.7097569,   39.75633592, 138.        ],
                                    [287.7097569,   29.75633592,   0.        ],
                                    [287.7097569,   29.75633592, 138.        ],
                                    [ 43.73894914,  39.75633592,   0.        ],
                                    [ 43.73894914,  39.75633592, 138.        ],
                                    [ 43.73894914,  29.75633592,   0.        ],
                                    [ 43.73894914,  29.75633592, 138.        ]])
    app.sampleCubeLWCoords = vecs2Graph(app, app.sampleCubeLWVecs)

    app.sampleCubeVecs = np.array([[100, 70,  10],
                                [150, 70,  10],
                                [100, 120,  10],
                                [100,  70,  60],
                                [150, 120,  10],
                                [150,  70,  60],
                                [100, 120,  60],
                                [150, 120,  60]])
    app.sampleCubeCoords = vecs2Graph(app, app.sampleCubeVecs)

def appStarted(app):
    initialize(app)

    app.fv = Cube(200,200,10, (50,50,0))
    app.rw = Cube(10,200,200, (40,50,0))
    app.lw = Cube(200,10,200, (50,40,0))
    app.test = [app.fv, app.rw, app.lw]
    
    app.view = False
    #app.misc = []
    app.classCube = Cube(50,100,150, (100,100,0))
    app.classCube2 = Cube(50,100,150, (0,100,0))
    app.misc = [app.classCube, app.classCube2]
    app.tempMisc = []

    app.makeCubes = False
    app.tracker = 0

    #### perspective rendering 
    app.cameraOrigin = np.array([130,280,60])
    imageDistance = 100
    imageLength = 120
    imageHeight = 120
    app.imageTopLeft = app.cameraOrigin + np.array([imageLength/2,imageHeight/2,imageDistance])
    #app.imageTopLeft = np.array([200,250,80])
    #app.imageTopRight = np.array([])


    #these things change based on your rotation // image view (camera origin may change too / stay the same?)
    a1 = np.array([-(app.width/imageLength),0,0]) #--> "right" direction on the image plane
    a2 = np.array([0,0,-(app.height/imageHeight)]) #--> "down" direction on the image plane 
    a3 = app.imageTopLeft - app.cameraOrigin #vector from camera to the top left corner of image plane
    #a3 = app.cameraOrigin - app.imageTopLeft
    app.cameraBasis = np.array([a1,a2,a3]) #put basis vecs in as rows, then transpose so they are cols
    #app.cameraBasis = cameraBasis
    #print(a1, a2, a3)
    #print(app.cameraBasis)
    #print(app.cameraBasis.T)

    app.lwImageCoords = perspectiveRender(app, app.cameraBasis.T, app.lw.vecs)
    app.floorImageCoords = perspectiveRender(app, app.cameraBasis.T, app.fv.vecs)
    app.ccImageCoords = perspectiveRender(app, app.cameraBasis.T, app.classCube.vecs)
    app.rwImageCoords = perspectiveRender(app, app.cameraBasis.T, app.rw.vecs)
    app.miscImageCoords = []

    app.unitCubeCoords = perspectiveRender(app, app.cameraBasis.T, app.CUBE)
    #print(app.floorImageCoords)
    #print(app.lwImageCoords)
    #for coord in app.lwImageCoords: 
    #    app.uhhh = np.append(app.uhhh, [coord+np.array([app.width, app.height*1.2])], axis=0)

    #for i in range(1):
        #R2D = np.array([[math.cos(math.pi), -math.sin(math.pi)],
        #                [math.sin(math.pi),  math.cos(math.pi)]])

        #R2D = np.array([[1, 0],
        #                [0,-1]])

        #print(app.lwImageCoords)
        #for i in range(app.lwImageCoords.shape[0]):
        #    app.lwImageCoords[i] = R2D @ app.lwImageCoords[i] 
        #    app.lwImageCoords[i] += np.array([app.width, app.height])

        #for i in range(app.rwImageCoords.shape[0]):
        #    app.rwImageCoords[i] = R2D @ app.rwImageCoords[i]
        #    app.rwImageCoords[i] += np.array([app.width,app.height])
        
        #for i in range(app.floorImageCoords.shape[0]):
        #    app.floorImageCoords[i] = R2D @ app.floorImageCoords[i]
        #   app.floorImageCoords[i] += np.array([app.width, app.height])
        #print(app.floor)
        #app.lwImageCoords = R2D @ app.lwImageCoords
        #app.floorImageCoords = R2D @ app.lwImageCoords
        #app.rwImageCoords = R2D @ app.lwImageCoords
        #for coord in app.rwImageCoords: 
        #    app.uhhh2 = np.append(app.uhhh2, [coord+np.array([app.width, app.height*1.2])], axis=0)

def perspectiveRender(app, cameraBasis, cubeVectors): 
    #takes in: cameraOrigin(vector), 
    #          cameraBasis (matrix w/ columns as vectors of camera's basis)
    #          cubeVectors (matrix w/ vectors as rows)
    #returns matrix of coordinates to render (coordinates as rows)

    #get new basis of cubeVectors (matrix w/ vectors as columns)
    cameraViewCubeVecs = np.linalg.inv(cameraBasis) @ cubeVectors.T

    imageCoords = np.zeros((2,8))
    #print(cameraViewCubeVecs.shape[1])
    for i in range(cameraViewCubeVecs.shape[1]): # in terms of columns
        col = cameraViewCubeVecs[:,i] #a cube vector 
        divisor = col[2] 
        cameraViewCubeVecs[:,i] /= divisor #scale down to get points in the image plane 
        imageCoords[:, i] = cameraViewCubeVecs[:2, i] #use first two components only 
    
    return imageCoords.T

def rotateCube(app, cube, angle, rotAxis=(0,0,1)):
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
    app.misc = [app.classCube, app.classCube2] 
    app.tracker = 0
    app.miscImageCoords = []
def changeAxisAngles(app):

    #try shifting origin? 
    #app.origin = (app.origin[0]+20, app.origin[1]+20)
    #works 
    #try changing initial angles? 
    app.xAxisInitAngle-=10
    app.yAxisInitAngle+=10
    app.xAxisAngle = deg2Rad(app.xAxisInitAngle+app.rotationAngle)
    app.yAxisAngle = deg2Rad(app.yAxisInitAngle+app.rotationAngle)
    #works 
def resetDrawCubeFloor(app):
    app.drawCubeFloor = not app.drawCubeFloor
    app.cubeFloorVecs = np.empty((0,3))
    app.tempCubeFloorVecs = np.empty((0,3))
    app.cubeFloorCoords = np.empty((0,2))
    app.tempCubeFloorCoords = np.empty((0,2))

    app.cubeWallHeight = None
    app.leftCubeWallCoords = np.empty((0,2))
    app.rightCubeWallCoords = np.empty((0,2))
    app.leftCubeWallVecs = np.empty((0,3))
    app.rightCubeWallVecs = np.empty((0,3))

    app.tempLeftCubeWallCoords = np.empty((0,2))
    app.tempRightCubeWallCoords = np.empty((0,2))
    app.tempLeftCubeWallVecs = np.empty((0,3))
    app.tempRightCubeWallVecs = np.empty((0,3))
def rotateSamples(app):
    #sample cube floor
    app.sampleCubeFloorVecs = rotateCube(app, app.sampleCubeFloorVecs, 10)
    app.sampleCubeFloorCoords = vecs2Graph(app, app.sampleCubeFloorVecs) 

    app.sampleCubeRWVecs = rotateCube(app, app.sampleCubeRWVecs, 10)
    app.sampleCubeRWCoords = vecs2Graph(app, app.sampleCubeRWVecs)

    app.sampleCubeLWVecs = rotateCube(app, app.sampleCubeLWVecs, 10)
    app.sampleCubeLWCoords = vecs2Graph(app, app.sampleCubeLWVecs)
    
    #sample cube
    app.sampleCubeVecs = rotateCube(app, app.sampleCubeVecs, 10)
    app.sampleCubeCoords = vecs2Graph(app, app.sampleCubeVecs) 

def keyPressed(app, event): 

    if event.key == '1': toggleMakeCubes(app)
    elif event.key == '2': changeAxisAngles(app)
    elif event.key == '4': resetDrawCubeFloor(app)
    elif event.key == 'h': app.showUnitCube = not app.showUnitCube  #toggle unit cube
        
    elif event.key == 'r':
        for cube in app.misc[2:]:
            cube.vecs = rotateCube(app, cube.vecs, 10)
            pass
        for cube in [app.fv, app.lw, app.rw]:
            cube.vecs = rotateCube(app, cube.vecs, 10)
            pass
        app.classCube.vecs = rotateCube(app, app.classCube.vecs, 10)

        #rotating cUbE
        app.CUBE = rotateCube(app, app.CUBE, 10)
        rotateSamples(app)
        
        #for reference, rotating the "axes" of the cube objs
        rotatedXAxisVec = rotateVec(app, app.xAxisVec, 10, [0,0,1])
        rotatedYAxisVec = rotateVec(app, app.yAxisVec, 10, [0,0,1])
        app.xAxisVec = rotatedXAxisVec
        app.yAxisVec = rotatedYAxisVec

        if app.cubeFloorVecs.shape[0]==8:
            app.cubeFloorVecs = rotateCube(app, app.cubeFloorVecs, 10)
            app.cubeFloorCoords = vecs2Graph(app, app.cubeFloorVecs)

        if app.rightCubeWallCoords.shape[0]==8:
    
            app.rightCubeWallVecs = rotateCube(app, app.rightCubeWallVecs, 10)
            app.leftCubeWallVecs = rotateCube(app, app.leftCubeWallVecs, 10)

            #print(app.leftCubeWallVecs)
            app.leftCubeWallCoords = vecs2Graph(app, app.leftCubeWallVecs)
            app.rightCubeWallCoords = vecs2Graph(app, app.rightCubeWallVecs)
    
    elif event.key == 'w':
        for row in app.CUBE: 
            row[2]+=10
        #move the cube up
    elif event.key =='s':
        for row in app.CUBE:
            row[2]-=10
        #move the cube down
    elif event.key == 'a':
        for row in app.CUBE: 
            row[0]+=10
        #move the cube left (x) 
    elif event.key == 'd':
        for row in app.CUBE:
            row[0]-=10
        #move the cube right (x)
    elif event.key == 'z':
        for row in app.CUBE:
            row[1]-=10
        #move the cube left (y)
    elif event.key == 'x':
        for row in app.CUBE:
            row[1]+=10
        #move the cube right (y)
    elif event.key == 'v':   app.view = not app.view      #change view
        
    elif event.key == 'c':
        if app.view: #rotation? 
            app.cameraBasis = rotateCube(app, app.cameraBasis,10)
            app.lwImageCoords = perspectiveRender(app, app.cameraBasis.T, app.lw.vecs)
            app.floorImageCoords = perspectiveRender(app, app.cameraBasis.T, app.fv.vecs)
            app.ccImageCoords = perspectiveRender(app, app.cameraBasis.T, app.classCube2.vecs)
            app.rwImageCoords = perspectiveRender(app, app.cameraBasis.T, app.rw.vecs)

    #update cubepoints 
    app.CUBEPOINTS = vecs2Graph(app, app.CUBE)

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
        #for v in [e1,e2,e3,e4]:
            #print(f'basis v')
            #thickness is height 
            #abs(e1[0]-e2[0]) is length
            #abs(e1[1]-e2[1]) is width
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
        
        #l = abs(e1[0]-e2[0])
        #w = abs(e1[1]-e2[1])
        #h = thickness 
        #app.altCubeFloor = Cube(l,w,h,e3)

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

    #right wall
    #app.cubeFloorVecs[2], 
    #app.cubeFloorVecs[2] + np.array([0,0,app.cubeWallHeight])
    #app.cubeFloorVecs[4],
    #app.cubeFloorVecs[4] + np.array([0,0,app.cubeWallHeight])

    #app.cubeFloorVecs[2] + np.array([-10, 0, 0]), 
    #app.cubeFloorVecs[2] + np.array([-10,0,app.cubeWallHeight])
    #app.cubeFloorVecs[4] + np.array([-10, 0, 0]), 
    #app.cubeFloorVecs[4] + np.array([-10,0,app.cubeWallHeight])

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

    print(app.leftCubeWallVecs)

    #rl = app.altCubeFloor.height
    #rw = app.altCubeFloor.width
    #rh = app.cubeWallHeight
    #x,y,z = app.altCubeFloor.origin 

    #temp = (x-rl, y-rl, z)

    #app.rightCubeWall = Cube(rl, rw, rh, (x-rl,y,0))
    #app.rightCubeWallCoords = vecs2Graph(app, app.rightCubeWall.vecs)

def mousePressed(app, event): 
    if app.drawCubeFloor and app.cubeFloorCoords.shape[0]<8:
        makeCubeFloor(app, event)
    elif app.cubeFloorCoords.shape[0]==8 and app.cubeWallHeight==None:
        makeCubeWalls(app, event)

    #app.classCube.isCollide(app.classCube2)
    if app.makeCubes:
        origin = graph2Vecs(app, [[event.x, event.y]], z=app.fv.height)[0]
        app.newCube = Cube(30, 30, 30, origin)
        app.tempMisc.append(app.newCube)

    c = np.array([[event.x, event.y]])
    v = graph2Vecs(app, c)[0]
    print(v)

def mouseDragged(app, event):
    if app.makeCubes:
        origin = graph2Vecs(app, [[event.x, event.y]], z=app.fv.height)[0]
        app.newCube = Cube(30, 30, 30, origin)
        if app.tempMisc != []:
            app.tempMisc[-1] = app.newCube

def mouseReleased(app, event):
    if app.makeCubes:


        if (app.newCube.origin[0] + app.newCube.length > app.fv.origin[0] + app.fv.length):
            ox = app.fv.origin[0] + app.fv.length - app.newCube.length 
        elif (app.newCube.origin[0]<app.fv.origin[0]):
            ox = app.fv.origin[0]
        else: ox = app.newCube.origin[0]

        if (app.newCube.origin[1] + app.newCube.width > app.fv.origin[1] + app.fv.width
        ): 
            oy = app.fv.origin[1] + app.fv.width - app.newCube.width
        elif (app.newCube.origin[1]<app.fv.origin[1]):
            oy = app.fv.origin[1]
        else: oy = app.newCube.origin[1]

        oz = app.fv.height
        app.newCube = Cube(30,30,30, (ox,oy,oz))

        for cube in app.misc[2:]:
            if (cube.origin[0] + cube.length > app.newCube.origin[0] > cube.origin[0]):
                app.tracker+=1
                print(f'oop {app.tracker}')
                #app.tempMisc.pop()
                #return
            # or cube.origin[0] + cube.length < app.newCube.origin[0] + app.newCube.length):

        imc = perspectiveRender(app, app.cameraBasis, app.newCube.vecs)
        app.miscImageCoords.append(imc)
        app.misc.append(app.newCube)
        print(app.misc[-1].origin)
        app.tempMisc.pop()

def mouseMoved(app, event): 
    if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==2:
        floatCubeFloor(app, event)
    elif app.cubeFloorVecs.shape[0]==8 and app.cubeWallHeight==None:
        print('here!')
        floatCubeWalls(app, event)

def drawCube(app, canvas, cubeCoords, color='black'):
    for i in range(cubeCoords.shape[0]):
        p1 = cubeCoords[i]
        for j in range(cubeCoords.shape[0]):
            p2 = cubeCoords[j]
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)

def drawSamples(app, canvas):
    #get a sample cube floor 
    drawCube(app, canvas, app.sampleCubeFloorCoords, 'green')

    #sample walls 
    drawCube(app, canvas, app.sampleCubeRWCoords, 'green')
    drawCube(app, canvas, app.sampleCubeLWCoords, 'green')

    #and a sample cube on top of the floor
    drawCube(app, canvas, app.sampleCubeCoords, 'blue')

def redrawAll(app, canvas):

    if app.view:
        #here's our view window
        drawCube(app, canvas, app.lwImageCoords, color = 'purple')
        drawCube(app, canvas, app.floorImageCoords, color = 'purple')
        drawCube(app, canvas, app.ccImageCoords, color = 'orange')
        drawCube(app, canvas, app.rwImageCoords, color = 'purple')
        for imc in app.miscImageCoords:
            drawCube(app, canvas, imc, color = 'orange')

        #drawCube(app, canvas, app.unitCubeCoords, color = 'blue')
        #for coord in app.lwImageCoords:
        #    x,y = coord
        #    r=2
        #    canvas.create_oval(x-r, y-r, x+r, y+r, fill = 'purple')
        #pass
    
    else:
        drawCube(app, canvas, app.CUBEPOINTS, color='blue')
        for c in app.test: #walls, floor 
            c = vecs2Graph(app, c.vecs)
            drawCube(app, canvas, c, 'purple')
        for cube in app.misc[2:]:
            c = vecs2Graph(app, cube.vecs)
            drawCube(app, canvas, c, 'orange')
        for cube in app.tempMisc:
            c = vecs2Graph(app, cube.vecs)
            drawCube(app, canvas, c, 'red')
        coords = vecs2Graph(app, app.classCube.vecs)
        drawCube(app, canvas, coords, color = 'orange')

        ox, oy = app.origin
        #z axis
        canvas.create_line(ox,oy, ox, 0)
        #x axis
        xAxisx = g2x(app, app.width*(math.cos(app.xAxisAngle)))
        xAxisy = g2y(app, app.height*(math.sin(app.xAxisAngle)))
        canvas.create_line(ox, oy, xAxisx, xAxisy)
        #y axis
        yAxisx = g2x(app, (app.width)*(math.cos(app.yAxisAngle)))
        yAxisy = g2y(app, (app.height)*(math.sin(app.yAxisAngle)))
        canvas.create_line(ox, oy, yAxisx, yAxisy)

        #drawSamples(app, canvas

         #cube floor (static)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8:
            drawCube(app, canvas, app.cubeFloorCoords, 'red')

        #cube floor (moving)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==2:
            drawCube(app, canvas, app.tempCubeFloorCoords, 'red')

        #walls (static)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8 and app.rightCubeWallCoords.shape[0]==8:
            drawCube(app, canvas, app.rightCubeWallCoords, 'red')
            drawCube(app, canvas, app.leftCubeWallCoords, 'red')
        
        elif app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8 and app.cubeWallHeight==None:
            #print(app.tempRightCubeWallCoords)
            drawCube(app, canvas, app.tempRightCubeWallCoords, 'red')
            drawCube(app, canvas, app.tempLeftCubeWallCoords, 'red')

        #unit cube, for rotation demonstration
        if app.showUnitCube:
            for point in app.CUBEPOINTS:
                canvas.create_oval(point[0]-3, point[1]-3, point[0]+3, point[1]+3, fill='blue')

            CUBE = app.CUBE
            for i in range(app.CUBEPOINTS.shape[0]): #rows
                p1 = app.CUBEPOINTS[i]
                v1 = app.CUBE[i]
                for j in range(app.CUBEPOINTS.shape[0]): #rows
                    p2 = app.CUBEPOINTS[j]
                    v2 = app.CUBE[j]
                    diffVec = v1-v2 
                    if math.sqrt(diffVec[0]**2 + diffVec[1]**2 + diffVec[2]**2) <= 60: 
                        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill = 'blue')

            #rotating axes 
            xAxisCoords = vecs2Graph(app, [app.xAxisVec])
            x,y = xAxisCoords[0][0], xAxisCoords[0][1]
            #print(x,y)
            canvas.create_line(ox,oy,x,y, fill='red')

            yAxisCoords = vecs2Graph(app, [app.yAxisVec])
            x,y = yAxisCoords[0][0], yAxisCoords[0][1]
            #print(x,y)
            canvas.create_line(ox,oy,x,y, fill='orange')
        
runApp(width=600, height=600)


