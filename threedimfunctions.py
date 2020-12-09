#threedimfunctions 
#   - functions used for transitioning between 3D vectors <-> tkinter
#   - functions for perspective rendering vectors and 3D rotation 

import numpy as np
import math

def deg2Rad(deg): return deg*math.pi/180

#regular graph coordinate (with origin at 0,0) --> tkinter x coordinate
def g2x(x, originX): return x+originX

#regular graph coordinate (with origin at 0,0) --> tkinter y coordinate
def g2y(y, originY): return originY-y

#calculates tkinter (x,y) equivalent of 3D vectors
def vecs2Graph(app, vecs): 
    #takes in 2d ndarray of vecs [x,y,z]
    #returns a 2d ndarray of Tkinter coordinates [x,y]
    graphPoints = np.empty((0,2))

    for vec in vecs:
        #adding the horizontal components of the vectors 
        tx = vec[0]*math.cos(app.xAxisAngle) + vec[1]*(math.cos(app.yAxisAngle))
        #adding the vertical components of the vectors 
        ty = vec[0]*math.sin(app.xAxisAngle) + vec[1]*(math.sin(app.yAxisAngle)) + vec[2]
        
        #offsets, since prev tx,ty consider 0,0 to be center of the screen 
        tx = g2x(tx, app.origin[0])
        ty = g2y(ty, app.origin[1])

        newPoint = np.array([[tx,ty]])
        graphPoints = np.append(graphPoints, newPoint, axis=0)
    return graphPoints

#calculates 3D vector (x,y,z) equivalent of tkinter coordinates 
def graph2Vecs(app, graph, z=0): 
    #takes in 2d ndarray of TKinter coordinates [x,y]
    #returns a 2d ndarray of vecs [x,y,z]
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

#rotate a vector in 3D space around an axis 
def rotateVec(app, vec, angle, axis): 
    #rotation matrix adapted from 
    #https://developer.mozilla.org/en-US/docs/Web/CSS/transform-function/rotate3d()

    if angle%360 == 0:
        return vec 

    a = deg2Rad(angle)
    x,y,z = axis[0], axis[1], axis[2] 

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

#calculate the perspective rendered coordinates of cube vectors 
def perspectiveRender(app, cameraBasis, cubeVectors): 
    #concepts lifted from Prof. Offner's 21-241 perspective rendering lectures

    #takes in: cameraOrigin (vector of camera location), 
    #          cameraBasis (matrix w/ columns as vectors of camera's basis)
    #          cubeVectors (matrix w/ vectors as rows)
    #returns:  matrix of coordinates to render (coordinates as rows)

    numVecs = cubeVectors.shape[0]

    #use 'change of coordinates' to get a new basis of cubeVectors 
    # note: the cubeVector locations have not changed, 
    # but they are expressed now in terms of the camera's basis 
    # instead of the standard basis for R^3.
    #the new basis of cubeVectors is a matrix w/ vectors as columns
    cameraViewCubeVecs = np.linalg.inv(cameraBasis) @ cubeVectors.T

    imgCoords = np.zeros((numVecs,2)) #rows of (x,y) coordinates for Tkinter

    #loop through the vecs (columns)
    for i in range(cameraViewCubeVecs.shape[1]): 
        #the third element in the column of a vector
        divisor = cameraViewCubeVecs[:,i][2] 

        #since the image plane is exactly one v3 (third vector of camera basis)
        # away from the camera, we scale each vector by 1/divisor 
        # to get the vectors that lie on the image plane 
        cameraViewCubeVecs[:,i] *= 1/(divisor) 

        #now the first two components of each vector are the pixel addresses 
        # of the perspective rendered coordinates of the vector 
        imgCoords[i] = -cameraViewCubeVecs[:2, i] 

    return imgCoords