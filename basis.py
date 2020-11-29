import math
import numpy as np
from cmu_112_graphics import *

#origin = (app.width/2, app.height/2)
# (x,y)

#in terms of unit circle...
#z3: subtract height to "increase" , at 90
    # to add a: add (acos90, asin90)
    # aka add (0, a) 
#y3: 120 degrees clockwise: 90-120 = -30 = -30+360 = 330
    # to add a to y: 
    # add acos(120) to x
    # add (acos120, asin120)
#x3: 90+120 = 210 
    # add (acos210, asin210)

#math.cos and numpy.cos take in rad

#need to mess w this later to make rotation look less jank

def deg2Rad(deg):
    return deg*math.pi/180

def g2x(app, x): #regular graph coordinate --> tkinter x coordinate
                 #assumes (app.width/2, app.height/2) is origin
    return x+(app.origin[0])

def g2y(app, y): #regular graph coordinate --> tkinter y coordinate
                 #assumes (app.width/2, app.height/2) is origin 
    return (app.origin[1])-y

def vecs2Graph(app, vecs): #takes in 2d ndarray of vecs [x,y,z]
    graphPoints = np.empty((0,2))

    for vec in vecs:
        tx = vec[0]*math.cos(app.xAxisAngle) + vec[1]*(math.cos(app.yAxisAngle))
        ty = vec[0]*math.sin(app.xAxisAngle) + vec[1]*(math.sin(app.yAxisAngle)) + vec[2]
        tx = g2x(app, tx)
        ty = g2y(app, ty)
        newPoint = np.array([[tx,ty]])
        graphPoints = np.append(graphPoints, newPoint, axis=0)

    return graphPoints

def graph2Vecs(app, graph, z=0): #takes in 2d ndarray of points [x,y]
    ox, oy = app.origin
    vecs = np.empty((0,3))

    ''' 
    matrix A (2x2)
    cos xAxisAngle      cos yAxisAngle
    sin xAxisAngle      sin yAxisAngle 
    
    matrix b (2x1)
    x
    y
    
    matrix v (2x1)
    a <-- xcomponent in vector
    b <-- ycomponent in vector 

    the zcomponent is 0 (floor is level), as a default
    
    we solve Av = b 
    v = Ainv * b 
    '''

    #matrix A 
    A = np.array([[math.cos(app.xAxisAngle), math.cos(app.yAxisAngle)],
                  [math.sin(app.xAxisAngle), math.sin(app.yAxisAngle)]])

    Ainv = np.linalg.inv(A)

    for point in graph: 
        #first adjust points
        x = point[0] - ox #x coord in graph (centered at 0,0)
        y = oy - point[1] #y coord in graph (centered at 0,0)

        #vector b 
        b = np.array([x,y])

        #vector v = [x  y  z]
        v = Ainv @ b
        #print(v)
        v = np.append(v, z) #add on z coord 
        vecs = np.append(vecs, [v], axis=0)

    return vecs

def rotateVec(app, vec, angle, axis): #3D vecs? 
    if angle%360 == 0:
        return vec 

    a = deg2Rad(angle)

    #x,y,z = vec[0], vec[1], vec[2]
    #x,y,z = 0,0,1 rotate around z axis

    x,y,z = axis 

    #rotation matrix formula from 
    #https://developer.mozilla.org/en-US/docs/Web/CSS/transform-function/rotate3d()

    #first row
    r11 = 1 + (1-math.cos(a))*(x**2 - 1)
    r12 = z*math.sin(a) + x*y*(1-math.cos(a))
    r13 = -y*math.sin(a) + x*z*(1-math.cos(a))
    
    #second row 
    r21 = -z*math.sin(a) + x*y*(1-math.cos(a))
    r22 = 1 + (1-math.cos(a))*(y**2 - 1)
    r23 = x*math.sin(a) + y*z*(1-math.cos(a))

    #third row 
    r31 = y*math.sin(a) + x*z*(1-math.cos(a))
    r32 = -x*math.sin(a) + y*z*(1-math.cos(a))
    r33 = 1 + (1-math.cos(a))*(z**2 - 1)

    #rotation matrix 
    R = np.array([[r11, r12, r13], 
                  [r21, r22, r23],
                  [r31, r32, r33]])

    rotatedVec = R @ vec
    return rotatedVec

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

    elif event.key == 'r':
        #rotating cUbE
        newCube = np.empty((0,3))
        for vec in app.CUBE:
            if vec[0]==vec[1]==vec[2]==0:
                rotatedVec = vec
            else:
                rotatedVec = rotateVec(app, vec, 10, [0,0,1])
            #print(rotatedVec)
            #print(vec)
            newCube = np.append(newCube, [rotatedVec], axis=0)
        app.CUBE = newCube

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
    
    #update cubepoints 
    app.CUBEPOINTS = vecs2Graph(app, app.CUBE)

    #update floor
    if app.floorCoords.shape[0]==4:
        app.floorCoords = vecs2Graph(app, app.floorVecs)
        #print('updated floorcoords')
    if app.rightWallCoords.shape[0] == 4:
        app.rightWallCoords = vecs2Graph(app, app.rightWallVecs)
        app.leftWallCoords = vecs2Graph(app, app.leftWallVecs)
    #print(app.CUBE)
    #print(app.CUBEPOINTS)

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

def mousePressed(app, event): 
    if app.drawFloor: 
        makeFloor(app, event)
    if app.floorCoords.shape[0]==4 and app.wallHeight==None:
        app.wallHeight = False
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

        #app.wallHeight = h

def mouseMoved(app, event): 
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

def redrawAll(app, canvas):
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
        #print('wow')
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
        #print('here')
        #we never get here 
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
            if math.sqrt(diffVec[0]**2 + diffVec[1]**2 + diffVec[2]**2) <= 50: 
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


