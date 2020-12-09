import numpy as np
import math

def deg2Rad(deg): return deg*math.pi/180

#regular graph coordinate --> tkinter x coordinate
def g2x(x, originX): return x+originX

#regular graph coordinate --> tkinter y coordinate
def g2y(y, originY): return originY-y

def vecs2Graph(app, vecs): 
    #takes in 2d ndarray of vecs [x,y,z]
    #returns a 2d ndarray of Tkinter coordinates [x,y]
    graphPoints = np.empty((0,2))

    for vec in vecs:
        #adding the horizontal components of the vectors 
        tx = vec[0]*math.cos(app.xAxisAngle) + vec[1]*(math.cos(app.yAxisAngle))
        #adding the vertical components of the vectors 
        ty = vec[0]*math.sin(app.xAxisAngle) + vec[1]*(math.sin(app.yAxisAngle)) + vec[2]
        #offset to the origin
        tx = g2x(tx, app.origin[0])
        ty = g2y(ty, app.origin[1])
        newPoint = np.array([[tx,ty]])
        graphPoints = np.append(graphPoints, newPoint, axis=0)

    return graphPoints

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

def perspectiveRender(app, cameraBasis, cubeVectors): 
    #concepts lifted from Professor Offner's 21-241 perspective rendering lectures

    #takes in: cameraOrigin(vector), 
    #          cameraBasis (matrix w/ columns as vectors of camera's basis)
    #          cubeVectors (matrix w/ vectors as rows)
    #returns:  matrix of coordinates to render (coordinates as rows)

    #get new basis of cubeVectors (matrix w/ vectors as columns)
    numVecs = cubeVectors.shape[0]
    cameraViewCubeVecs = np.linalg.inv(cameraBasis) @ cubeVectors.T

    imgCoords = np.zeros((numVecs,2)) #rows of (x,y) coordinates for Tkinter
    for i in range(cameraViewCubeVecs.shape[1]): #loop through the vecs (columns)
        divisor = cameraViewCubeVecs[:,i][2] #the third element in the column of a vector
        cameraViewCubeVecs[:,i] *= 1/(divisor) #scale down to get points in the image plane 
        imgCoords[i] = -cameraViewCubeVecs[:2, i] #get the first two components (pixel addresses)

    return imgCoords