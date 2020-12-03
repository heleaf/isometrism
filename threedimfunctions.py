import numpy as np
import math

#https://www.math.tamu.edu/~mpilant/math311/ComputerGraphics.pdf 

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
        #adding the horizontal components of the vectors 
        tx = vec[0]*math.cos(app.xAxisAngle) + vec[1]*(math.cos(app.yAxisAngle))
        #adding the vertical components of the vectors 
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

    x,y,z = axis[0], axis[1], axis[2] 

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