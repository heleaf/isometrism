import math
import numpy as np
from cmu_112_graphics import *
from threedimfunctions import *
from oldfloor import *
from cube import *

def appStarted(app):
    app.rotationAngle = 0

    app.xRotationAngle = 0
    app.yRotationAngle = 0

    app.origin = (app.width/2, app.height/2)

    app.xAxisInitAngle = 200
    app.yAxisInitAngle = 340

    app.xAxisAngle = deg2Rad(app.xAxisInitAngle+app.rotationAngle)
    app.yAxisAngle = deg2Rad(app.yAxisInitAngle+app.rotationAngle)

    app.CUBE = np.array([[0,0,0],
                        [50,0,0],
                        [0,50,0],
                        [0,0,50],
                        [50,50,0],
                        [50,0,50],
                        [0,50,50],
                        [50,50,50]])

    app.CUBEPOINTS = vecs2Graph(app, app.CUBE)
    app.showUnitCube = False

    app.drawFloor = False
    app.floorCoords = np.empty((0,2))
    app.tempFloorCoords = np.empty((0,2))

    app.wallHeight = None
    app.leftWallCoords = np.empty((0,2))
    app.rightWallCoords = np.empty((0,2))
    app.tempLeftWallCoords = np.empty((0,2))
    app.tempRightWallCoords = np.empty((0,2))

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

    app.sampleCubeFloor = np.array([[300.47989017,  26.98620265,   0.        ],
                            [300.47989017,  26.98620265,  10.        ],
                            [ 46.39939357, 298.60952565,   0.        ],
                            [ 46.39939357, 298.60952565,  10.        ],
                            [ 46.39939357,  26.98620265,   0.        ],
                            [ 46.39939357,  26.98620265,  10.        ],
                            [300.47989017, 298.60952565,   0.        ],
                            [300.47989017, 298.60952565,  10.        ]])
    #print(app.sampleCubeFloor.shape)
    app.sampleCubeFloorCoords = vecs2Graph(app, app.sampleCubeFloor)

    app.sampleCube = np.array([[100, 70,  10],
                                [150, 70,  10],
                                [100, 120,  10],
                                [100,  70,  60],
                                [150, 120,  10],
                                [150,  70,  60],
                                [100, 120,  60],
                                [150, 120,  60]])
    app.sampleCubeCoords = vecs2Graph(app, app.sampleCube)
    app.view = False

    app.classCube = Cube(50,100,150, (100,100,100))

def rotateCube(app, cube, angle, rotAxis=(0,0,1)):
    newCube = np.empty((0,3))
    for vec in cube:
        if vec[0]==vec[1]==vec[2]==0:
            rotatedVec = vec
        else:
            rotatedVec = rotateVec(app, vec, 10, rotAxis)
        newCube = np.append(newCube, [rotatedVec], axis=0)
    return newCube

def keyPressed(app, event):

    if event.key == '1':
        app.drawFloor = not app.drawFloor 
        app.floorCoords = np.empty((0,2))
        app.tempFloorCoords = np.empty((0,2))
        app.leftWallCoords = np.empty((0,2))
        app.rightWallCoords = np.empty((0,2))
        app.tempLeftWallCoords = np.empty((0,2))
        app.tempRightWallCoords = np.empty((0,2))
        app.wallHeight = None
        #app.drawWalls = app.drawFloor
        #print(f'app.drawfloor: {app.drawFloor}')

    elif event.key == '2':
        #try shifting origin? 
        #app.origin = (app.origin[0]+20, app.origin[1]+20)
        #works 

        #try changing initial angles? 
        app.xAxisInitAngle-=10
        app.yAxisInitAngle+=10
        app.xAxisAngle = deg2Rad(app.xAxisInitAngle+app.rotationAngle)
        app.yAxisAngle = deg2Rad(app.yAxisInitAngle+app.rotationAngle)
        #works 

    elif event.key == '3':
        #try rotating the room 
        if app.drawFloor: 
            app.floorVecs = rotateCube(app, app.floorVecs, 10)

        if app.wallHeight!=None and app.wallHeight!=False:
            app.rightWallVecs = rotateCube(app, app.rightWallVecs, 10)
            app.leftWallVecs = rotateCube(app, app.leftWallVecs, 10)

        #this doesn't work that well. we may need to make the floor out of 'cubes' 
    
    elif event.key == '4':
        app.drawCubeFloor = not app.drawCubeFloor
        app.cubeFloorVecs = np.empty((0,3))
        app.tempCubeFloorVecs = np.empty((0,3))

        app.cubeWallHeight = None
        app.leftCubeWallCoords = np.empty((0,2))
        app.rightCubeWallCoords = np.empty((0,2))
        app.tempLeftCubeWallCoords = np.empty((0,2))
        app.tempRightCubeWallCoords = np.empty((0,2))

    elif event.key == 'h':
        #toggle unit cube
        app.showUnitCube = not app.showUnitCube

    elif event.key == 'r':
        #rotating cUbE
        app.CUBE = rotateCube(app, app.CUBE, 10)

        #custom cube floor
        if app.cubeFloorVecs.shape[0]==8:
            app.cubeFloorVecs = rotateCube(app, app.cubeFloorVecs, 10)
            app.cubeFloorCoords = vecs2Graph(app, app.cubeFloorVecs)

        #sample cube floor
        app.sampleCubeFloor = rotateCube(app, app.sampleCubeFloor, 10)
        app.sampleCubeFloorCoords = vecs2Graph(app, app.sampleCubeFloor) 
        
        #sample cube
        app.sampleCube = rotateCube(app, app.sampleCube, 10)
        app.sampleCubeCoords = vecs2Graph(app, app.sampleCube) 

        #for reference, rotating the "axes" of the cube objs
        rotatedXAxisVec = rotateVec(app, app.xAxisVec, 10, [0,0,1])
        rotatedYAxisVec = rotateVec(app, app.yAxisVec, 10, [0,0,1])
        app.xAxisVec = rotatedXAxisVec
        app.yAxisVec = rotatedYAxisVec
    
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

    elif event.key == 'v':
        #change view
        app.view = not app.view

    #update cubepoints 
    app.CUBEPOINTS = vecs2Graph(app, app.CUBE)

    #update floor
    if app.floorCoords.shape[0]==4:
        app.floorCoords = vecs2Graph(app, app.floorVecs)
        #print('updated floorcoords')
    if app.rightWallCoords.shape[0] == 4:
        app.rightWallCoords = vecs2Graph(app, app.rightWallVecs)
        app.leftWallCoords = vecs2Graph(app, app.leftWallVecs)

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
        
        l = abs(e1[0]-e2[0])
        w = abs(e1[1]-e2[1])
        h = thickness 
        app.altCubeFloor = Cube(l,w,h,e3)

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

def makeCubeWalls(app, event):
    #app.cubeWallHeight = None
    #app.leftCubeWallCoords = np.empty((0,2))
    #app.rightCubeWallCoords = np.empty((0,2))
    #app.tempLeftCubeWallCoords = np.empty((0,2))
    #app.tempRightCubeWallCoords = np.empty((0,2))

    #floorcoords = vecs2Graph(app, app.cubeFloorCoords)

    app.cubeWallHeight = app.cubeFloorCoords[0][-1]-event.y
    print(app.cubeWallHeight)

    rl = app.altCubeFloor.height
    rw = app.altCubeFloor.width
    rh = app.cubeWallHeight
    x,y,z = app.altCubeFloor.origin 

    #temp = (x-rl, y-rl, z)

    app.rightCubeWall = Cube(rl, rw, rh, (x-rl,y,0))
    app.rightCubeWallCoords = vecs2Graph(app, app.rightCubeWall.vecs)
    #app.cubeWallHeight = app.cubeFloorCoords

def mousePressed(app, event): 
    if app.drawCubeFloor:
        makeCubeFloor(app, event)
    if app.cubeFloorCoords.shape[0]==8 and app.cubeWallHeight==None:
        app.cubeWallHeight = False
        return
        #print(app.cubeFloorCoords)
    if app.cubeWallHeight == False:
        makeCubeWalls(app, event)
    if app.drawFloor and app.floorCoords.shape[0]!=4: 
        makeFloor(app, event)
    if app.floorCoords.shape[0]==4 and app.wallHeight==None:
        app.wallHeight = False
        return
    if app.wallHeight==False:
        print(app.wallHeight)
        #make walls
        app.wallHeight = app.floorCoords[3][1]-event.y

        c0,d0 = app.floorCoords[0]
        c1,d1 = app.floorCoords[1]
        c2,d2 = app.floorCoords[2]
        c3,d3 = app.floorCoords[3]

        #right wall
        rw0 = np.array([c2,d2-app.wallHeight])
        rw1 = np.array([c2,d2])
        rw2 = np.array([c3,d3-app.wallHeight])
        rw3 = np.array([c3,d3])

        app.rightWallCoords = np.array([rw0, rw1, rw2, rw3])
        #print(app.rightWallCoords.shape)

        #left wall
        lw0 = np.array([c0,d0-app.wallHeight])
        lw1 = np.array([c0,d0])
        lw2 = np.array([c2,d2-app.wallHeight])
        lw3 = np.array([c2,d2])

        app.leftWallCoords = np.array([lw0, lw1, lw2, lw3])

        #app.drawWalls = False
        app.rightWallVecs = graph2Vecs(app, app.rightWallCoords)
        app.leftWallVecs = graph2Vecs(app, app.leftWallCoords)
        #store for later use 
        #app.wallHeight = h

def mouseMoved(app, event): 
    if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==2:
        floatCubeFloor(app, event)
    if app.drawFloor and app.floorCoords.shape[0]==1:
        floatFloor(app, event)
    if app.floorCoords.shape[0]==4 and app.wallHeight == False:
        #app.wallHeight = None
        print(event.y)
        h = app.floorCoords[3][1] - event.y

        c0,d0 = app.floorCoords[0]
        c1,d1 = app.floorCoords[1]
        c2,d2 = app.floorCoords[2]
        c3,d3 = app.floorCoords[3]

        #right wall
        rw0 = np.array([c2,d2-h])
        rw1 = np.array([c2,d2])
        rw2 = np.array([c3,d3-h])
        rw3 = np.array([c3,d3])

        app.tempRightWallCoords = np.array([rw0, rw1, rw2, rw3])
        #print(app.rightWallCoords.shape)

        #left wall
        lw0 = np.array([c0,d0-h])
        lw1 = np.array([c0,d0])
        lw2 = np.array([c2,d2-h])
        lw3 = np.array([c2,d2])

        app.tempLeftWallCoords = np.array([lw0, lw1, lw2, lw3])

def drawCube(app, canvas, cubeCoords, color='black'):
    for i in range(cubeCoords.shape[0]):
        p1 = cubeCoords[i]
        for j in range(cubeCoords.shape[0]):
            p2 = cubeCoords[j]
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)

def redrawAll(app, canvas):
    c = vecs2Graph(app, app.classCube.vecs)
    drawCube(app, canvas, c, 'orange')

    if app.rightCubeWallCoords.shape[0]==8:
        drawCube(app, canvas, app.rightCubeWallCoords, 'red')

    if not app.view:
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

        #get a sample cube floor 
        drawCube(app, canvas, app.sampleCubeFloorCoords, 'green')

        #and a sample cube on top of the floor
        drawCube(app, canvas, app.sampleCubeCoords, 'blue')

        #cube floor (moving)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==2:
            drawCube(app, canvas, app.tempCubeFloorCoords, 'red')
            
        #cube floor (static)
        if app.drawCubeFloor and app.cubeFloorVecs.shape[0]==8:
            drawCube(app, canvas, app.cubeFloorCoords, 'red')
         
        #floor 
        if app.drawFloor and app.floorCoords.shape[0]==1:
            c0,d0 = app.tempFloorCoords[0]
            c1,d1 = app.tempFloorCoords[1]
            c2,d2 = app.tempFloorCoords[2]
            c3,d3 = app.tempFloorCoords[3]
            canvas.create_polygon(c0,d0,c1,d1,c3,d3,c2,d2, fill = 'yellow')
        elif app.drawFloor and app.floorCoords.shape[0]==4: 
            c0,d0 = app.floorCoords[0]
            c1,d1 = app.floorCoords[1]
            c2,d2 = app.floorCoords[2]
            c3,d3 = app.floorCoords[3]
            canvas.create_polygon(c0,d0,c1,d1,c3,d3,c2,d2, fill = 'yellow')
            
        #we drawin a wall now 
        if (app.wallHeight!=None or app.wallHeight!=False) and app.rightWallCoords.shape[0]==4:
            #right
            c0,d0 = app.rightWallCoords[0]
            c1,d1 = app.rightWallCoords[1]
            c2,d2 = app.rightWallCoords[2]
            c3,d3 = app.rightWallCoords[3]
            canvas.create_polygon(c0,d0,c1,d1,c3,d3,c2,d2, fill = 'green')

            #left 
            c0,d0 = app.leftWallCoords[0]
            c1,d1 = app.leftWallCoords[1]
            c2,d2 = app.leftWallCoords[2]
            c3,d3 = app.leftWallCoords[3]
            canvas.create_polygon(c0,d0,c1,d1,c3,d3,c2,d2, fill = 'blue')

        if app.floorCoords.shape[0]==4 and app.tempRightWallCoords.shape[0]==4 and app.wallHeight == False:
            #right
            c0,d0 = app.tempRightWallCoords[0]
            c1,d1 = app.tempRightWallCoords[1]
            c2,d2 = app.tempRightWallCoords[2]
            c3,d3 = app.tempRightWallCoords[3]
            canvas.create_polygon(c0,d0,c1,d1,c3,d3,c2,d2, fill = 'green')

            #left 
            c0,d0 = app.tempLeftWallCoords[0]
            c1,d1 = app.tempLeftWallCoords[1]
            c2,d2 = app.tempLeftWallCoords[2]
            c3,d3 = app.tempLeftWallCoords[3]
            canvas.create_polygon(c0,d0,c1,d1,c3,d3,c2,d2, fill = 'blue')

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
    else:
        #here's our view window
        #start by facing the X Axis 
        pass

runApp(width=600, height=600)


