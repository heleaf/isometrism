import numpy as np
from threedimfunctions import *

class Cube(object):

    def __init__(self, length, width, height, origin=(0,0,0)):
        self.length = length
        self.width = width
        self.height = height 

        self.origin = origin

        l = self.length
        w = self.width
        h = self.height

        self.vecs = np.array([[0,0,0],
                            [l,0,0],
                            [0,w,0],
                            [0,0,h],
                            [l,w,0],
                            [l,0,h],
                            [0,w,h],
                            [l,w,h]])

        #self.displayVecs = self.vecs
        
        #if origin!=None: 
        for i in range(self.vecs.shape[0]):
            self.vecs[i] = self.vecs[i]+np.array(self.origin)

    def rotate(self, angle, axis=(0,0,1)):
        if angle%360 != 0:
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

            #rotatedVec = R @ vec
            for i in range(self.vecs.shape[0]):
                self.vecs[i] = R @ self.vecs[i]


    def isCollide(self, other):
        if isinstance(other, Cube):
            print(self.vecs)
            print(other.vecs)
            
            pass
        return None

class Table(Cube):
    tableThickness = 5
    legThickness = 3
    def __init__(self, length, width, height, origin=(0,0,0)):
        self.length = length
        self.width = width
        self.height = height 

        l = self.length
        w = self.width
        h = self.height
        th = Table.tableThickness
        t = Table.legThickness

        self.origin = origin

        self.face = Cube(l,w,th, origin = np.array([0,0,h-th]) + self.origin)

        self.leg1 = Cube(t,t,h-th, origin = self.origin)
        self.leg2 = Cube(t,t,h-th, origin = self.origin + np.array([l-t, 0,0]))
        self.leg3 = Cube(t,t,h-th, origin = self.origin + np.array([0,w-t, 0]))
        self.leg4 = Cube(t,t,h-th, origin = self.origin + np.array([l-t, w-t,0]))

        self.cubes = [self.face, self.leg1, self.leg2, self.leg3, self.leg4]

class Chair(Table):
    def __init__(self, length, width, height, origin=(0,0,0)):
        super().__init__(length, width, height/2, origin)
        o = np.array(self.origin) + np.array([0,0,height/2])
        self.back = Cube(Table.tableThickness, width, height/2, origin = o)
        self.cubes.append(self.back)




