import numpy as np
from threedimfunctions import *
from newbasis import *

class Cube(object):
    currentId = 0
    def __init__(self, length, width, height, origin=(0,0,0)):
        self.length = length
        self.width = width
        self.height = height 

        self.origin = origin
        
        self.name = 'Cube'

        l = self.length
        w = self.width
        h = self.height

        self.center = self.origin + np.array([l/2, w/2, h/2])
        self.isClicked = False

        self.id = Cube.currentId
        Cube.currentId+=1

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
            self.vecs[i] = self.vecs[i]+np.array(self.origin)

        #indexes of vectors for each face 
        self.topFaceVecs = []
        self.leftFrontFaceVecs = []
        self.rightFrontFaceVecs = []
        self.leftBackFaceVecs = []
        self.rightBackFaceVecs = []
        self.botFaceVecs = []
        for i in range(self.vecs.shape[0]):
            if self.vecs[i][0] == self.origin[0]+self.length:
                self.leftFrontFaceVecs.append(i)
            if self.vecs[i][1] == self.origin[1]+self.width:
                self.rightFrontFaceVecs.append(i)
            if self.vecs[i][2] == self.origin[2]+self.height:
                self.topFaceVecs.append(i)
            if self.vecs[i][1] == self.origin[1]:
                self.leftBackFaceVecs.append(i)
            if self.vecs[i][0] == self.origin[0]:
                self.rightBackFaceVecs.append(i)
            if self.vecs[i][2] == self.origin[2]:
                self.botFaceVecs.append(i)
    
    def rotate(self, app, angle, rotAxis=(0,0,1)):

        #def rotateCube(app, cube, angle, rotAxis=(0,0,1)): 
        #rotates all the vectors in a cube around an axis
        newCubeVecs = np.empty((0,3))

        for i in range(self.vecs.shape[0]):
            vec = self.vecs[i]
            if vec[0]==vec[1]==vec[2]==0:
                rotatedVec = vec
            else:
                rotatedVec = rotateVec(app, vec, 10, rotAxis)
            #self.vecs[i] = rotatedVec
            newCubeVecs = np.append(newCubeVecs, [rotatedVec], axis=0)
        self.vecs = newCubeVecs
        self.origin = newCubeVecs[0]
        self.hitBoxVecs = self.findHitBoxVecs()

    def rotateSelf(self, app, angle, center, rotAxis=(0,0,1)):

        #make a centered copy of the cube vectors (pretend the cube is centered at the origin)
        centeredVecs = np.empty((0,3))
        for vec in self.vecs:
            centeredVecs = np.append(centeredVecs, [vec-center], axis=0)

        #rotate the centered copy of the cube vectors 
        rotatedCenteredVecs = np.empty((0,3))
        for vec in centeredVecs:
            if vec[0]==vec[1]==vec[2]==0:
                rotatedVec = vec
            else:
                rotatedVec = rotateVec(app, vec, angle, rotAxis)
            rotatedCenteredVecs = np.append(rotatedCenteredVecs, [rotatedVec], axis=0)
        
        #push the rotated vectors back to the cube's original centered position 
        rotatedVecs = np.empty((0,3))
        for vec in rotatedCenteredVecs:
            rotatedVecs = np.append(rotatedVecs, [vec+center], axis=0)

        self.vecs = rotatedVecs
        self.hitBoxVecs = self.findHitBoxVecs()
        '''
        faceVecs = self.getFaceVecs()
        for i in range(len(faceVecs)):
            face = faceVecs[i]
            coords = perspectiveRender(app, app.cameraBasis, face)
            self.imageCoords[i] = coords
        '''

    def findHitBoxVecs(self):
        xMax, yMax, zMax = self.vecs[0]
        xMin, yMin, zMin = self.vecs[0]
        for vec in self.vecs:
            if vec[0]>xMax:
                xMax = vec[0]
            if vec[0]<xMin:
                xMin = vec[0]
            if vec[1]>yMax:
                yMax = vec[1]
            if vec[1]<yMin:
                yMin = vec[1]
            if vec[2]>zMax:
                zMax = vec[2]
            if vec[2]<zMin:
                zMin = vec[2]
        return np.array([[xMax,yMax,zMax], [xMin,yMin,zMin]])

    def mouseInHitbox(self, app, event):
        #making hitBox
        l,w,h = self.length, self.width, self.height
        
        #get leftX from this 
        leftVec = self.origin + np.array([l,0,0])
        leftCoord = vecs2Graph(app, [leftVec])[0]
        leftX = leftCoord[0]

        #get rightX from this 
        rightVec = self.origin + np.array([0,w,0])
        rightCoord = vecs2Graph(app, [rightVec])[0]
        rightX = rightCoord[0]

        #topY from this 
        topVec = self.origin + np.array([0,0,h])
        topCoord = vecs2Graph(app, [topVec])[0]
        topY = topCoord[1]
    
        #botY from this 
        botVec = self.origin + np.array([l,w,0])
        botCoord = vecs2Graph(app, [botVec])[0]
        botY = botCoord[1]

        return leftX <= event.x <= rightX and topY <= event.y <= botY

    def isCollide(self, other):
        if not isinstance(other, Cube):
            return None
        selfMaxVec, selfMinVec = self.findHitBoxVecs()
        sxMax, syMax, szMax = selfMaxVec
        sxMin, syMin, szMin = selfMinVec
        otherMaxVec, otherMinVec = other.findHitBoxVecs()
        oxMax, oyMax, ozMax = otherMaxVec
        oxMin, oyMin, ozMin = otherMinVec

        if ((sxMin < oxMin < sxMax or oxMin < sxMin < oxMax) and 
            (syMin < oyMin < syMax or oyMin < syMin < oyMax)): 
            return True 
        else:
            return False
        
    def getFaceVecs(self):
        topFaceVecs = []
        for i in self.topFaceVecs:
            topFaceVecs.append(self.vecs[i])
        
        leftFrontFaceVecs = []
        for i in self.leftFrontFaceVecs:
            leftFrontFaceVecs.append(self.vecs[i])
        
        rightFrontFaceVecs = []
        for i in self.rightFrontFaceVecs:
            rightFrontFaceVecs.append(self.vecs[i])

        leftBackFaceVecs = []
        for i in self.leftBackFaceVecs:
            leftBackFaceVecs.append(self.vecs[i])
        
        rightBackFaceVecs = []
        for i in self.rightBackFaceVecs:
            rightBackFaceVecs.append(self.vecs[i])

        botFaceVecs = []
        for i in self.botFaceVecs:
            botFaceVecs.append(self.vecs[i])

        return [topFaceVecs, leftFrontFaceVecs, 
                rightFrontFaceVecs, leftBackFaceVecs, 
                rightBackFaceVecs, botFaceVecs]

    def draw(self, app, canvas, color='black', fill=None):
        topFaceVecs, leftFrontFaceVecs, \
        rightFrontFaceVecs, leftBackFaceVecs, \
        rightBackFaceVecs, botFaceVecs = self.getFaceVecs()

        t = topFaceCoords = vecs2Graph(app, topFaceVecs)
        lf = leftFrontFaceCoords = vecs2Graph(app, leftFrontFaceVecs)
        rf = rightFrontFaceCoords = vecs2Graph(app, rightFrontFaceVecs)
        lb = leftBackFaceCoords = vecs2Graph(app, leftBackFaceVecs)
        rb = rightBackFaceCoords = vecs2Graph(app, rightBackFaceVecs)
        b = botFaceCoords = vecs2Graph(app, botFaceVecs)

        for r in [t,lf,rf,lb,rb,b]:
            canvas.create_line(r[0][0], r[0][1], r[1][0], r[1][1], fill=color)
            canvas.create_line(r[1][0],r[1][1], r[3][0], r[3][1], fill=color)
            canvas.create_line(r[3][0], r[3][1], r[2][0], r[2][1], fill=color)
            canvas.create_line(r[2][0],r[2][1], r[0][0], r[0][1], fill=color)

    def getImageCoords(self, app, cameraBasis):
        imageCoords = []
        faceVecs = self.getFaceVecs()
        for face in faceVecs:
            coords = perspectiveRender(app, cameraBasis, np.array(face))
            imageCoords.append(coords)
        return imageCoords

    def drawImageCoords(self, app, canvas, color='black'):
        imageCoords = self.getImageCoords(app, app.cameraBasis)
        for faceCoord in imageCoords:
            x0,y0 = faceCoord[0]
            x1,y1 = faceCoord[1]
            x2,y2 = faceCoord[2]
            x3,y3 = faceCoord[3]
            canvas.create_line(x0,y0,x1,y1,fill=color)
            canvas.create_line(x1,y1,x3,y3,fill=color)
            canvas.create_line(x3,y3,x2,y2,fill=color)
            canvas.create_line(x2,y2,x0,y0,fill=color)

    def __hash__(self):
        return hash(self.name, self.id)
        
    def __repr__(self):
        return f'{self.name}: {self.id}'

class Table(Cube):
    tableThickness = 5
    legThickness = 3
    currentId = 0
    def __init__(self, length, width, height, origin=(0,0,0),
                tableThickness=5, 
                legThickness=3):
        l = self.length = length
        w = self.width = width
        h = self.height = height 
        th = self.tth = tableThickness
        t = self.lth = legThickness

        self.origin = origin
        self.center = self.origin + np.array([l/2, w/2, h/2])

        self.face = Cube(l,w,th, origin = np.array([0,0,h-th]) + self.origin)

        self.leg1 = Cube(t,t,h-th, origin = self.origin)
        self.leg2 = Cube(t,t,h-th, origin = self.origin + np.array([l-t, 0,0]))
        self.leg3 = Cube(t,t,h-th, origin = self.origin + np.array([0,w-t, 0]))
        self.leg4 = Cube(t,t,h-th, origin = self.origin + np.array([l-t, w-t,0]))

        self.cubes = [self.face, self.leg1, self.leg2, self.leg3, self.leg4]

        self.hitBox = Cube(l,w,h, origin=self.origin)
        self.hitBoxVecs = self.hitBox.findHitBoxVecs()

        self.id = Table.currentId
        Table.currentId+=1
        self.name = 'Table'
        
        self.isClicked = False

    def getImageCoords(self, app, cameraBasis):
        imageCoords = []
        for cube in self.cubes:
            faceVecs = cube.getFaceVecs()
            for face in faceVecs:
                coords = perspectiveRender(app, cameraBasis, np.array(face))
                imageCoords.append(coords)
        return imageCoords

    def drawImageCoords(self, app, canvas, color='black'):
        for cube in self.cubes:
            cube.drawImageCoords(app,canvas,color)

    def updateVecs(self):
        self = Table(self.length, self.width, self.height, 
                     origin=self.origin, tableThickness=self.tth, 
                     legThickness=self.lth)
        self.id -= 1 
        Table.currentId -=1

    def draw(self, app, canvas, color='black',fill=None):
        for cube in self.cubes:
            cube.draw(app, canvas, color)

    def rotate(self, app, angle, rotAxis=(0,0,1)):
        for i in range(len(self.cubes)):
            self.cubes[i].rotate(app, angle, rotAxis)

    def rotateSelf(self, app, angle, center, rotAxis=(0,0,1)):
        for cube in self.cubes:
            cube.rotateSelf(app, angle, center, rotAxis)
        self.hitBoxVecs = self.hitBox.findHitBoxVecs()
    
    def isCollide(self, other):
        if not isinstance(other, Cube):
            return None
        elif isinstance(other, Table):
            for cube in self.cubes:
                for cube2 in other.cubes:
                    if cube.isCollide(cube2):
                        return True
            return False
        elif isinstance(other, Cube):
            for cube in self.cubes:
                if cube.isCollide(other):
                    return True
            return False

class Chair(Table):
    currentId = 0
    def __init__(self, length, width, height, origin=(0,0,0), tableThickness=5, 
                legThickness=3):
        super().__init__(length, width, height/2, origin, tableThickness, legThickness)
        o = np.array(self.origin) + np.array([0,0,height/2])
        self.height = height
        self.back = Cube(self.tth, width, height/2, origin = o)
        self.cubes.append(self.back)
        self.id = Chair.currentId
        Chair.currentId+=1
        self.name = 'Chair'

        self.hitBox = Cube(length, width, height, origin)

    def updateVecs(self):
        self = Chair(self.length, self.width, self.height, 
                     origin=self.origin, tableThickness=self.tth, 
                     legThickness=self.lth)
        self.id -= 1 
        Chair.currentId -=1

class Bed(Table):
    currentId = 0
    def __init__(self, length, width, height, origin=(0,0,0), tth=None, lth=None):
        l = self.length = length
        w = self.width = width
        h = self.height = height 
        self.tth = tth
        self.lth = lth
        self.origin = np.array(origin)
        self.center = self.origin + np.array([l/2, w/2, h/2])
        self.headBoard = Cube(l,w*0.2, h, self.origin)
        bodyO = self.origin + np.array([0,w*0.2,0])
        self.body = Cube(l,w*0.8,h*0.8,bodyO)
        pillowHeight = h*0.2
        pillowO = bodyO + np.array([l*.25, 0, h*0.8])
        self.pillow = Cube(l*0.5, l/2, pillowHeight, origin=pillowO)
        self.cubes = [self.headBoard, self.body, self.pillow]

        self.hitBox = Cube(l,w,h, origin=self.origin)
        self.hitBoxVecs = self.hitBox.findHitBoxVecs()
        self.id = Bed.currentId
        Bed.currentId+=1
        self.name = 'Bed'
        self.isClicked = False

    def updateVecs(self):
        self = Bed(self.length, self.width, self.height, 
                     origin=self.origin)
        self.id -= 1 
        Table.currentId -=1

class Lamp(Table):
    currentId = 0
    def __init__(self, length, width, height, origin=(0,0,0), 
                            tableThickness=5, legThickness=2):
        l = self.length = length
        w = self.width = width
        h = self.height = height 
        tth = self.tth = tableThickness
        lth = self.lth = legThickness
        self.origin = np.array(origin)
        self.center = self.origin + np.array([l/2, w/2, h/2])

        botBaseO = self.origin + np.array([l*0.2, w*0.2, 0])
        self.botBase = Cube(l*0.6,w*0.6,tth, botBaseO)
        stemO = self.origin + np.array([(l-lth)/2,(w-lth)/2,tth])
        self.stem = Cube(lth,lth, h-2*tth-0.3*h, origin=stemO)
        topBaseO = self.origin + np.array([0,0,h-2*tth-0.3*h+tth])
        self.topBase = Cube(l,w,tth, origin=topBaseO)
        topBoxO = topBaseO + np.array([l*0.1, w*0.1, tth])
        self.topBox = Cube(l*0.8, w*0.8, h*0.3, origin=topBoxO)
        
        self.cubes = [self.botBase, self.stem, self.topBase, self.topBox]

        self.hitBox = Cube(l,w,h, origin=self.origin)
        self.hitBoxVecs = self.hitBox.findHitBoxVecs()
        self.id = Lamp.currentId
        Lamp.currentId+=1
        self.name = 'Lamp'
        self.isClicked = False

    def updateVecs(self):
        self = Lamp(self.length, self.width, self.height, 
            origin=self.origin, tableThickness=self.tth, legThickness=self.lth)
        self.id -= 1 
        Lamp.currentId -=1
