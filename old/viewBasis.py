import math
import numpy as np
from cmu_112_graphics import *
from threedimfunctions import *
from cube import *

def appStarted(app):
    app.origin = app.width/2, app.height*0.3
    app.xAxisInitAngle = 180
    app.yAxisInitAngle = 270

    app.xAxisAngle = deg2Rad(app.xAxisInitAngle)
    app.yAxisAngle = deg2Rad(app.yAxisInitAngle)

    app.c = Cube(100,100,100, (0,0,0))

    app.xAxisVec = np.array([1,0,0])

    app.s = 100
    app.leftCorner = (250, 300)

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
    if event.key =='r':
        app.c.vecs = rotateCube(app, app.c.vecs, 10)

def mousePressed(app, event):
    ox, oy = app.origin
    lx, ly = app.leftCorner
    a = abs(ox - lx)
    b = abs(oy - ly)
    c = math.sqrt(a**2 + b**2)
    theta = math.acos(a/c)
    print(theta*180/math.pi)

    th = (theta*180/math.pi) + 180

def drawCube(app, canvas, cubeCoords, color='black'):
    for i in range(cubeCoords.shape[0]):
        p1 = cubeCoords[i]
        for j in range(cubeCoords.shape[0]):
            p2 = cubeCoords[j]
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)

def redrawAll(app, canvas):
    #coords = vecs2Graph(app, app.c.vecs)
    #drawCube(app, canvas, coords)

    #canvas.create_line

    #x axis to start. 
    #x,y = vecs2Graph(app, [app.width*app.xAxisVec])[0]
    #print(x,y)
    #canvas.create_line(x,y, -x,y)
    canvas.create_line(0, app.height*0.6, app.width, app.height*0.6, fill = 'green')
    ox,oy = app.origin
    s = app.s
    lx, ly = app.leftCorner
    canvas.create_rectangle(lx,ly, lx+s,ly+s)

    #canvas.create_rectangle(lx+0.4*s, ly-0.4*s, lx+s-0.4*s, ly+s-0.4*s)
    canvas.create_line(lx,ly, ox, oy, fill = 'blue')
    canvas.create_line(lx+s, ly, ox,oy, fill= 'blue')
    canvas.create_line(lx, ly+s, ox,oy, fill= 'blue')
    canvas.create_line(lx+s, ly+s, ox,oy, fill='blue')

    #print(oy - (ly), ox- (lx))


    pass

runApp(width=600, height=600)


