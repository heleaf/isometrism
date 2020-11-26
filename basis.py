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
    return x+(app.width/2)

def g2y(app, y): #regular graph coordinate --> tkinter y coordinate
                 #assumes (app.width/2, app.height/2) is origin 
    return (app.height/2)-y

def appStarted(app):
    app.rotationAngle = 0

    app.xAngle = deg2Rad(210+app.rotationAngle)
    app.yAngle = deg2Rad(330+app.rotationAngle)

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

def redrawAll(app, canvas):
    r = app.rotationAngle

    #origin
    ox, oy = app.width/2, app.height/2

    #z axis
    canvas.create_line(ox,oy, ox, 0)

    #x axis
    xAngle = deg2Rad(210+r)
    xAxisx = g2x(app, app.width*(math.cos(xAngle)))
    xAxisy = g2y(app, app.height*(math.sin(xAngle)))
    canvas.create_line(ox, oy, xAxisx, xAxisy)

    #y axis
    yAngle = deg2Rad(330+r)
    yAxisx = g2x(app, (app.width)*(math.cos(yAngle)))
    yAxisy = g2y(app, (app.height)*(math.sin(yAngle)))
    canvas.create_line(ox, oy, yAxisx, yAxisy)

    '''
    for point in app.CUBEPOINTS:
        canvas.create_oval(point[0]-3, point[1]-3, point[0]+3, point[1]+3, fill='blue')
    '''
    #print(app.CUBEPOINTS.shape[0])

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
                                    
    #drawBasis(app, canvas)
    #drawVector(app, canvas)

def vecs2Graph(app, vecs):
    #origin
    ox, oy = app.width/2, app.height/2

    #rotation angle
    r = app.rotationAngle

    xAngle = deg2Rad(210+r)
    yAngle = deg2Rad(330+r) 

    graphPoints = np.empty((0,2))
    for vec in vecs:
        tx = vec[0]*math.cos(xAngle) + vec[1]*(math.cos(yAngle))
        ty = vec[0]*math.sin(xAngle) + vec[1]*(math.sin(yAngle)) + vec[2]
        tx = g2x(app, tx)
        ty = g2y(app, ty)
        newPoint = np.array([[tx,ty]])
        graphPoints = np.append(graphPoints, newPoint, axis=0)

    return graphPoints

    #print(tx,ty)

    #need to find length, and angle 
    #length: math.sqrt(e1[0]**2 + e1[1]**2 + e1[2]**2)

    #angle: 
        #find angle between x and y (vectors)
        # x dot y = |x| |y| cos theta
        #for z, just move the thing up or down LOL 

    '''
    '''

    #for vec in STD3: 
    #   print(vec)
        #vec[0] is x coord -- add vec[0]*math.sin(deg2Rad(210)) to totalY
        #                  -- add vec[0]*math.cos(deg2Rad(210)) to totalX
        #totalY += vec[0]*math.sin(deg2Rad(210+r))
        #totalX += vec[0]*math.cos(deg2Rad(210+r))

        #totalY = g2y(app, totalY)
        #totalX = g2x(app, totalX)

        #vec[1] is y coord -- add vec[1]*math.sin(deg2Rad(330)) to totalY
        #                  -- add vec[1]*math.cos(deg2Rad(330)) to totalX 
        #totalY += vec[1]*math.sin(deg2Rad(330+r))
        #print(vec[1]*math.sin(deg2Rad(330+r)))

        #totalY = g2y(app, totalY)
        #totalX += vec[1]*math.cos(deg2Rad(330+r))
        #print(vec[1]*math.cos(deg2Rad(330+r)))

        #vec[2] is z coord -- add vec[2]to totalY
        #totalY += vec[2]

        #print(totalX, totalY)

        #adjust
        #totalX = g2x(app, totalX)
        #totalY = g2y(app, totalY)
        #print(vec[0], vec[1], vec[2])

        #canvas.create_line(ox,oy, totalX, totalY, fill='red', width=5

runApp(width=600, height=600)


