from cube import *

class Button(object):
    def __init__(self, origin, w, h, color='white', padding=10):
        self.w = w
        self.h = h 
        self.color = color
        self.padding = padding
        self.origin = origin
        self.iconName = None
        self.icon = None
        self.isPressed = False

    def setIcon(self, ovec, iconName):
        if iconName == 'Chair':
            length = width = (self.w - (self.padding*2))/4
            height = self.h - (self.padding*2)
            th = min(self.w, self.h)*0.02
            ovec[2] -= self.h*0.2
            self.icon = Chair(length, width, height, ovec, tableThickness = th, legThickness=th)
            self.iconName = 'Chair'
        elif iconName == 'Table':
            ovec[1] -= self.h*0.2
            ovec[2] -= self.h*0.1
            length = (self.w - (self.padding*2))/4
            width = self.w - (self.padding*2)*1.5 
            height = self.h - (self.padding*2)*1.5
            th = min(self.w, self.h)*0.02
            self.icon = Table(length, width, height, ovec, tableThickness=th, legThickness=th) 
            self.iconName = 'Table'
        elif iconName == 'Cube':
            length = width = (self.w - (self.padding*2))/4
            height = self.h - (self.padding*2)
            self.icon = Cube(length, width, height, ovec) 
            self.iconName = 'Cube'
        else:
            self.icon = None
            self.iconName = None