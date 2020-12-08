import numpy as np
import math
from cmu_112_graphics import *
from cube import *
from newbasis import *

class Button(object):
    def __init__(self, origin, w, h, padding=10, fillColor='white', lineColor='black'):
        self.w = w
        self.h = h 
        self.fillColor = fillColor
        self.lineColor = lineColor
        self.padding = padding
        self.origin = origin
        self.iconName = None
        self.icon = None
        self.isPressed = False

    def mouseOver(self, app, event):
        ox,oy = self.origin 
        w,h = self.w, self.h
        return ox-w/2 <= event.x <= ox+w/2 and oy-h/2 <= event.y <= oy+h/2

    def setIcon(self, ovec, iconName):
        if iconName == 'Chair':
            length = width = (self.w - (self.padding*2))/4
            height = self.h - (self.padding*2)
            th = min(self.w, self.h)*0.02
            ovec[2] -= self.h*0.2
            self.icon = [Chair(length, width, height, ovec, tableThickness = th, legThickness=th)]
            self.iconName = 'Chair'
        elif iconName == 'Table':
            ovec[1] -= self.h*0.2
            ovec[2] -= self.h*0.1
            length = (self.w - (self.padding*2))/4
            width = self.w - (self.padding*2)*1.5 
            height = self.h - (self.padding*2)*1.5
            th = min(self.w, self.h)*0.02
            self.icon = [Table(length, width, height, ovec, tableThickness=th, legThickness=th)]
            self.iconName = 'Table'
        elif iconName == 'Cube':
            length = width = (self.w - (self.padding*2))/4
            height = self.h - (self.padding*2)
            self.icon = [Cube(length, width, height, ovec)] 
            self.iconName = 'Cube'
        elif iconName == 'Room':
            fl = fw = (self.w - self.padding*2)/2
            fh = min(self.w, self.h)*0.02 
            floor = Cube(fl, fw, fh, ovec)

            rh = (self.h - (self.padding*2) - fh)*0.5
            rovec = np.array(ovec)+np.array([-fh,0,0])
            right = Cube(fh, fw, rh, rovec)

            lovec = np.array(ovec)+np.array([0,-fh,0])
            left = Cube(fl, fh, rh, lovec)

            self.icon = [floor, right, left]
            self.iconName = 'Room'
            #length = width = (self.w - self.padding*2).4
            #self.iconName = 'Room'
        else:
            self.icon = None
            self.iconName = None

    def draw(self, app, canvas, fillColor, lineColor):
        x, y = self.origin
        w, h = self.w, self.h
        canvas.create_rectangle(x-w/2, y-h/2, x+w/2, y+h/2, fill=self.fillColor, outline=self.lineColor)
        if self.icon!=None:
            for cube in self.icon:
                cube.draw(app, canvas, self.lineColor)