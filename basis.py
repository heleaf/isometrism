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

def deg2Rad(deg):
    return deg*math.pi/180

def g2x(app, x): #regular graph coordinate --> tkinter x coordinate
                 #assumes (app.width/2, app.height/2) is origin
    return x+(app.origin[0])

def g2y(app, y): #regular graph coordinate --> tkinter y coordinate
                 #assumes (app.width/2, app.height/2) is origin 
    return (app.origin[1])-y

def appStarted(app):
    app.rotationAngle = 0

    app.origin = (app.width/2, app.height/2)

    app.xAxisDeg = 200
    app.yAxisDeg = 340

    app.xAngle = deg2Rad(app.xAxisDeg+app.rotationAngle)
    app.yAngle = deg2Rad(app.yAxisDeg+app.rotationAngle)

    app.CUBE = np.array([[0,0,0],
                        [50,0,0],
                        [0,50,0],
                        [0,0,50],
                        [50,50,0],
                        [50,0,50],
                        [0,50,50],
                        [50,50,50]])

    app.CUBEPOINTS = vecs2Graph(app, app.CUBE)

def keyPressed(app, event):
    if event.key == 'r':
        app.rotationAngle+=10
        app.xAngle = deg2Rad(app.xAxisDeg+app.rotationAngle)
        app.yAngle = deg2Rad(app.yAxisDeg+app.rotationAngle)
        #moves the axes/cube 
    
    elif event.key == '2':
        #try shifting origin? 
        #app.origin = (app.origin[0]+20, app.origin[1]+20)
        #works 

        #try changing initial angles? 
        app.xAxisDeg-=10
        app.yAxisDeg+=10
        app.xAngle = deg2Rad(app.xAxisDeg+app.rotationAngle)
        app.yAngle = deg2Rad(app.yAxisDeg+app.rotationAngle)
        #works 
    
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

def redrawAll(app, canvas):
    ox, oy = app.origin

    #z axis
    canvas.create_line(ox,oy, ox, 0)

    #x axis
    xAxisx = g2x(app, app.width*(math.cos(app.xAngle)))
    xAxisy = g2y(app, app.height*(math.sin(app.xAngle)))
    canvas.create_line(ox, oy, xAxisx, xAxisy)

    #y axis
    yAxisx = g2x(app, (app.width)*(math.cos(app.yAngle)))
    yAxisy = g2y(app, (app.height)*(math.sin(app.yAngle)))
    canvas.create_line(ox, oy, yAxisx, yAxisy)

    '''
    for point in app.CUBEPOINTS:
        canvas.create_oval(point[0]-3, point[1]-3, point[0]+3, point[1]+3, fill='blue')
    '''

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

def vecs2Graph(app, vecs):
    ox, oy = app.origin

    graphPoints = np.empty((0,2))

    for vec in vecs:
        tx = vec[0]*math.cos(app.xAngle) + vec[1]*(math.cos(app.yAngle))
        ty = vec[0]*math.sin(app.xAngle) + vec[1]*(math.sin(app.yAngle)) + vec[2]
        tx = g2x(app, tx)
        ty = g2y(app, ty)
        newPoint = np.array([[tx,ty]])
        graphPoints = np.append(graphPoints, newPoint, axis=0)

    return graphPoints

runApp(width=600, height=600)


