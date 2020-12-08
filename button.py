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
            self.iconName = iconName

        elif iconName == 'Table':
            ovec[1] -= self.h*0.2
            ovec[2] -= self.h*0.1
            length = (self.w - (self.padding*2))/4
            width = self.w - (self.padding*2)*1.5 
            height = self.h - (self.padding*2)*1.5
            th = min(self.w, self.h)*0.02
            self.icon = [Table(length, width, height, ovec, tableThickness=th, legThickness=th)]
            self.iconName = iconName

        elif iconName == 'Cube':
            length = width = (self.w - (self.padding*2))/4
            height = self.h - (self.padding*2)
            self.icon = [Cube(length, width, height, ovec)] 
            self.iconName = iconName

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
            self.iconName = iconName

        elif iconName == 'Left Turn' or iconName == 'Help' or iconName == 'Camera' or iconName == 'Eye':
            r = (min(self.w, self.h) - self.padding*2 )/2
            self.icon = [MiscIcon(r, self.origin, name=iconName)]
            self.iconName = iconName

        else:
            self.icon = None
            self.iconName = None

    def draw(self, app, canvas, fillColor, lineColor):
        x, y = self.origin
        w, h = self.w, self.h
        canvas.create_rectangle(x-w/2, y-h/2, x+w/2, y+h/2, fill=self.fillColor, outline=self.lineColor)
        if self.icon!=None:
            for obj in self.icon:
                obj.draw(app, canvas, self.lineColor, self.fillColor)

class MiscIcon(object):
    def __init__(self, radius, origin, name=None, lineColor='black', lineWidth=2):
        self.radius = radius
        self.origin = origin
        self.name = name 
        self.lineColor = lineColor
        self.lineWidth = lineWidth

    def draw(self, app, canvas, lineColor, fillColor):
        ox,oy = self.origin 
        r = self.radius
        if self.name == 'Left Turn':
            canvas.create_oval(ox-r, oy-(r*0.7), ox+r, oy+(r*0.8), fill=None, outline=lineColor, width=self.lineWidth)
            canvas.create_arc(ox-r, oy-(r*0.7), ox+r, oy+(r*0.8), start=60, extent=-60, fill=None, outline=fillColor, width=self.lineWidth*1.5)
            canvas.create_line(ox-r*0.2, oy-r, ox+r*0.5, oy-(r*0.7), fill=lineColor, width=self.lineWidth)
            canvas.create_line(ox-r*0.2, oy-(r*0.3), ox+r*0.5,oy-(r*0.7), fill=lineColor, width=self.lineWidth)

        elif self.name == 'Help':
            canvas.create_polygon(ox-r*0.2, oy-r, ox+r*0.2, oy-r, ox+r*0.1, oy+r*0.2, ox-r*0.1, oy+r*0.2, fill=lineColor, width=0)
            cy = oy + r*0.6
            cx = ox
            cr = r*0.2
            canvas.create_oval(cx-cr, cy-cr, cx+cr, cy+cr, fill=lineColor, width=0)

        elif self.name == 'Camera':
            sr = r*0.4
            canvas.create_oval(ox-sr, oy-sr, ox+sr, oy+sr, fill=lineColor, outline=lineColor, width=self.lineWidth)

        elif self.name == 'Eye':
            canvas.create_polygon(ox-r*1.2,oy, ox,oy-r, ox+r*1.2,oy, ox,oy+r, fill=lineColor, outline=lineColor, width=self.lineWidth)
            sr = r*0.5
            canvas.create_oval(ox-sr, oy-sr, ox+sr, oy+sr, fill=fillColor, outline=lineColor, width=self.lineWidth)
