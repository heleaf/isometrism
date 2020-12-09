#button
#   - Button and MiscIcon classes for button creation w/ customized icons 
#   - key methods: checking is mouse hovers over a button 
#                  setting custom icons
#                  draw

import numpy as np
import math
from cmu_112_graphics import *
from cube import *
from newbasis import *

class Button(object):
    font = 'Courier'
    def __init__(self, origin, w, h, padding=10,
                iconName=None, ovec=None, app=None,
                fillColor='white', lineColor='black'):
        self.w = w
        self.h = h 
        self.fillColor = fillColor
        self.lineColor = lineColor
        self.padding = padding
        self.origin = origin
        self.isPressed = False
        self.setIcon(iconName, ovec=ovec, app=app)

    #checks if mouse intersects the button
    def mouseOver(self, app, event):
        ox,oy = self.origin 
        w,h = self.w, self.h
        return ox-w/2 <= event.x <= ox+w/2 and oy-h/2 <= event.y <= oy+h/2

    def setIcon(self, iconName, ovec=None, app=None):
        if ovec == True: #if the icon uses vectors 
            ovec = graph2Vecs(app, [self.origin])[0]

        if iconName == 'Chair':
            length = width = (self.w - (self.padding*2))/4
            height = self.h - (self.padding*2)
            th = min(self.w, self.h)*0.02
            ovec[2] -= self.h*0.2
            self.icon = [Chair(length, width, height, ovec, 
                        tableThickness = th, legThickness=th)]
            self.iconName = iconName

        elif iconName == 'Table':
            ovec[1] -= self.h*0.2
            ovec[2] -= self.h*0.1
            length = (self.w - (self.padding*2))/4
            width = self.w - (self.padding*2)*1.5 
            height = self.h - (self.padding*2)*1.5
            th = min(self.w, self.h)*0.02
            self.icon = [Table(length, width, height, ovec, 
                        tableThickness=th, legThickness=th)]
            self.iconName = iconName

        elif iconName == 'Bed':
            ovec[1] -= self.h*0.2
            ovec[2] -= self.h*0.05
            length = (self.w - (self.padding*2))/3
            width = self.w - (self.padding*2)*1.5 
            height = self.h - (self.padding*2)*1.8
            self.icon = [Bed(length, width, height, ovec)] 
            self.iconName = iconName

        elif iconName == 'Lamp':
            length = width = (self.w - (self.padding*2))/4
            height = self.h - (self.padding*2)
            th = min(self.w, self.h)*0.02
            ovec[2] -= self.h*0.2
            self.icon = [Lamp(length, width, height, ovec, 
                        tableThickness = th, legThickness=th)]
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

        elif iconName == 'Camera':
            r = (min(self.w, self.h) - self.padding*2 )/2
            self.icon = [MiscIcon(r, self.origin, name=iconName, ovec=ovec)]
            self.iconName = iconName
        
        elif (iconName == 'Left Turn' or iconName == 'Right Turn' or
            #iconName == 'Left Arrow' or iconName == 'Right Arrow' or
            iconName == 'Help' or iconName == 'Eye' or iconName == 'Clear'):
            r = (min(self.w, self.h) - self.padding*2 )/2
            self.icon = [MiscIcon(r, self.origin, name=iconName)]
            self.iconName = iconName

        elif iconName == 'Left Arrow' or iconName == 'Right Arrow':
            r = min(self.w, self.h) - self.padding*2.5
            self.icon = [MiscIcon(r, self.origin, name=iconName)]
            self.iconName = iconName

        else:
            self.icon = None
            self.iconName = None

    def draw(self, app, canvas, fillColor, lineColor):
        x, y = self.origin
        w, h = self.w, self.h
        canvas.create_rectangle(x-w/2, y-h/2, x+w/2, y+h/2, 
                                fill=self.fillColor, width=0)
        if self.icon!=None:
            for obj in self.icon:
                obj.draw(app, canvas, self.lineColor, self.fillColor)

class MiscIcon(object): #each button may have a specified icon
    def __init__(self, radius, origin, name=None, 
                lineColor='black', lineWidth=2, ovec=None):
        self.radius = radius
        self.origin = origin
        self.name = name 
        self.lineColor = lineColor
        self.lineWidth = lineWidth
        self.ovec=ovec
    
    def draw(self, app, canvas, lineColor, fillColor):
        ox,oy = self.origin 
        r = self.radius
        if self.name == 'Left Turn':
            canvas.create_oval(ox-r, oy-(r*0.7), ox+r, oy+(r*0.8), fill=None, 
                                        outline=lineColor, width=self.lineWidth)
            canvas.create_arc(ox-r, oy-(r*0.7), ox+r, oy+(r*0.8), start=60, 
            extent=-60, fill=None, outline=fillColor, width=self.lineWidth*1.8)
            canvas.create_line(ox-r*0.2, oy-r, ox+r*0.5, oy-(r*0.7), 
                                        fill=lineColor, width=self.lineWidth)
            canvas.create_line(ox-r*0.2, oy-(r*0.3), ox+r*0.5,oy-(r*0.7), 
                                        fill=lineColor, width=self.lineWidth)

        elif self.name == 'Right Turn':
            canvas.create_oval(ox-r, oy-(r*0.7), ox+r, oy+(r*0.8), fill=None, 
                                        outline=lineColor, width=self.lineWidth)
            canvas.create_arc(ox-r, oy-(r*0.7), ox+r, oy+(r*0.8), start=120, 
            extent=60, fill=None, outline=fillColor, width=self.lineWidth*1.8)
            canvas.create_line(ox-r*0.5, oy-(r*0.7), ox+r*0.2, oy-r, 
                                        fill=lineColor, width=self.lineWidth)
            canvas.create_line(ox-r*0.5, oy-(r*0.7), ox+r*0.2, oy-(r*0.3), 
                                        fill=lineColor, width=self.lineWidth)

        elif self.name == 'Right Arrow':
            canvas.create_text(ox,oy-r, text='>', fill=lineColor, 
                                        font=Button.font)
            canvas.create_text(ox,oy+r, text='g', fill=lineColor, 
                                        font=Button.font)

        elif self.name == 'Left Arrow': 
            canvas.create_text(ox,oy-r, text='<', fill=lineColor, 
                                        font=Button.font)
            canvas.create_text(ox,oy+r, text='f', fill=lineColor, 
                                        font=Button.font)

        elif self.name == 'Help':
            canvas.create_polygon(ox-r*0.2, oy-r, ox+r*0.2, oy-r, 
            ox+r*0.1, oy+r*0.2, ox-r*0.1, oy+r*0.2, fill=lineColor, width=0)
            cy = oy + r*0.6
            cx = ox
            cr = r*0.2
            canvas.create_oval(cx-cr,cy-cr,cx+cr,cy+cr,fill=lineColor,width=0)

        elif self.name == 'Clear':
            canvas.create_oval(ox-r, oy-r, ox+r, oy+r, fill=lineColor, width=0)
            r2 = r*0.4
            canvas.create_line(ox-r2, oy-r2, ox+r2, oy+r2, fill=fillColor, 
                                                        width=self.lineWidth)
            canvas.create_line(ox-r2, oy+r2, ox+r2, oy-r2, fill=fillColor, 
                                                        width=self.lineWidth)
        elif self.name == 'Camera':
            sr = r*0.2
            canvas.create_oval(ox-sr, oy-sr, ox+sr, oy+sr, fill=lineColor, 
                                    outline=lineColor, width=self.lineWidth)
            
            z = np.array([[0,0,r*0.6],[0,0,-r*0.6]])
            y = np.array([[0,r*0.75,0],[0,-r*0.75,0]])
            x = np.array([[r*0.75,0,0],[-r*0.75,0,0]])

            ax = [x,y,z]

            for a in ax:
                for v in a:
                    v+=np.array(self.ovec)

            coords = []
            for a in ax:
                coords.append(vecs2Graph(app, a))

            for i in range(len(coords)):
                x0,y0 = coords[i][0]
                x1,y1 = coords[i][1]
                canvas.create_line(x0,y0,x1,y1,fill=lineColor)
                if i==0: 
                    canvas.create_text(x0,y0, text='z', fill=lineColor, 
                                            anchor=NE, font=Button.font) #NE
                    canvas.create_text(x1,y1, text='x', fill=lineColor, 
                                            anchor=SW, font=Button.font) #SW
                elif i==1: 
                    canvas.create_text(x0,y0, text='d', fill=lineColor, 
                                            anchor=NW, font=Button.font) #NW
                    canvas.create_text(x1,y1, text='a', fill=lineColor, 
                                            anchor=SE, font=Button.font) #SE
                elif i==2: 
                    canvas.create_text(x0,y0, text='w', fill=lineColor, 
                                            anchor=S, font=Button.font)
                    canvas.create_text(x1,y1, text='s', fill=lineColor, 
                                            anchor=N, font=Button.font)
            
        elif self.name == 'Eye':
            canvas.create_polygon(ox-r*1.2,oy, ox,oy-r, ox+r*1.2,oy, ox,oy+r, 
                        fill=lineColor, outline=lineColor, width=self.lineWidth)
            sr = r*0.5
            canvas.create_oval(ox-sr, oy-sr, ox+sr, oy+sr, fill=fillColor, 
                                        outline=lineColor, width=self.lineWidth)
