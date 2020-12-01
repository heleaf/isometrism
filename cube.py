import numpy as np
from threedimfunctions import *

class Cube(object):

    def __init__(self, length, width, height, origin=(0,0,0)):
        self.l = length
        self.w = width
        self.h = height 

        l = self.l
        w = self.w
        h = self.h

        self.vecs = np.array([[0,0,0],
                            [l,0,0],
                            [0,w,0],
                            [0,0,h],
                            [l,w,0],
                            [l,0,h],
                            [0,w,h],
                            [l,w,h]])
        
        #if origin!=None: 
        for i in range(self.vecs.shape[0]):
            self.vecs[i] = self.vecs[i]+np.array(origin)

    def rotate(self, angle, axis=(0,0,1)):
        
        pass


    def isCollide(self, other):
        if isinstance(other, Cube):
            pass
        return None