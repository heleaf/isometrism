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

def graph2Vecs(app, graph): #takes in 2d ndarray of points [x,y]
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
        v = np.append(v, 0) #add on z coord 
        vecs = np.append(vecs, [v], axis=0)

    return vecs

def appStarted(app):
    app.rotationAngle = 0

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

    app.drawWalls = False

def keyPressed(app, event):

    if event.key == '1':
        app.drawFloor = not app.drawFloor 
        app.floorCoords = np.empty((0,2))
        app.tempFloorCoords = np.empty((0,2)) 
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
        app.rotationAngle+=10
        app.xAxisAngle = deg2Rad(app.xAxisInitAngle+app.rotationAngle)
        app.yAxisAngle = deg2Rad(app.yAxisInitAngle+app.rotationAngle)
        #moves the axes/cube 
    
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
    
def mouseMoved(app, event): 
    if app.drawFloor and app.floorCoords.shape[0]==1:
        floatFloor(app, event)
    
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
        for j in range(app.CUBEPOINTS.shape[0]): #rows
            p2 = app.CUBEPOINTS[j]
       
            if ((CUBE[i][0]==CUBE[j][0] and CUBE[i][1]==CUBE[j][1]) or
                (CUBE[i][0]==CUBE[j][0] and CUBE[i][2]==CUBE[j][2]) or 
                (CUBE[i][1]==CUBE[j][1] and CUBE[i][2]==CUBE[j][2])
            ): 
                canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill = 'blue')

runApp(width=600, height=600)


