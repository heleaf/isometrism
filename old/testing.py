#cube practice 

def getStdBasis(n): #for R^n 
    pass
#cube points: 
#[0,0,0] origin
#[1,0,0] e1
#[0,1,0] e2
#[0,0,1] e3
#[1,1,0] e1+e2
#[1,0,1] e1+e3
#[0,1,1] e2+e3
#[1,1,1] e1+e2+e3 
#powerset 

'''
            for i in range(app.tempCubeFloorCoords.shape[0]): #rows
                p1 = app.tempCubeFloorCoords[i]
                #v1 = app.cubeFloorVecs[i]
                for j in range(app.tempCubeFloorCoords.shape[0]): #rows
                    p2 = app.tempCubeFloorCoords[j]
                    #v2 = app.CUBE[j]
                    #diffVec = v1-v2 
                    #if math.sqrt(diffVec[0]**2 + diffVec[1]**2 + diffVec[2]**2) <= 60: 
                    canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill = 'blue')
            '''

'''
STD3 = np.array([[1,0,0],
                [0,1,0],
                [0,0,1]]) #x,y,z 
'''
'''
CUBE = np.array([[0,0,0],
                 [1,0,0],
                 [0,1,0],
                 [0,0,1],
                 [1,1,0],
                 [1,0,1],
                 [0,1,1],
                 [1,1,1]])
'''

'''
print(math.cos(deg2Rad(210)), math.sin(deg2Rad(210)))
print(math.cos(deg2Rad(90)), math.sin(deg2Rad(90)))
print(math.cos(deg2Rad(330)), math.sin(deg2Rad(330)))
'''

 #print(tx,ty)

    #need to find length, and angle 
    #length: math.sqrt(e1[0]**2 + e1[1]**2 + e1[2]**2)

    #angle: 
        #find angle between x and y (vectors)
        # x dot y = |x| |y| cos theta
        #for z, just move the thing up or down LOL 

    '''
    '''

    #for vec in STD3: 
    #   print(vec)
        #vec[0] is x coord -- add vec[0]*math.sin(deg2Rad(210)) to totalY
        #                  -- add vec[0]*math.cos(deg2Rad(210)) to totalX
        #totalY += vec[0]*math.sin(deg2Rad(210+r))
        #totalX += vec[0]*math.cos(deg2Rad(210+r))

        #totalY = g2y(app, totalY)
        #totalX = g2x(app, totalX)

        #vec[1] is y coord -- add vec[1]*math.sin(deg2Rad(330)) to totalY
        #                  -- add vec[1]*math.cos(deg2Rad(330)) to totalX 
        #totalY += vec[1]*math.sin(deg2Rad(330+r))
        #print(vec[1]*math.sin(deg2Rad(330+r)))

        #totalY = g2y(app, totalY)
        #totalX += vec[1]*math.cos(deg2Rad(330+r))
        #print(vec[1]*math.cos(deg2Rad(330+r)))

        #vec[2] is z coord -- add vec[2]to totalY
        #totalY += vec[2]

        #print(totalX, totalY)

        #adjust
        #totalX = g2x(app, totalX)
        #totalY = g2y(app, totalY)
        #print(vec[0], vec[1], vec[2])

        #canvas.create_line(ox,oy, totalX, totalY, fill='red', width=5

'''
        
        testVec = np.array([[100,0, 100]])
        testCoords = vecs2Graph(app, testVec) 
        x = testCoords[0][0]
        y = testCoords[0][1]
        canvas.create_line(ox, oy, x,y, fill = 'red')

        rotatedVec = rotateVec(app, testVec[0], 180, [0,0,1])
        rotatedCoords = vecs2Graph(app, [rotatedVec])
        x = rotatedCoords[0][0]
        y = rotatedCoords[0][1]
        canvas.create_line(ox,oy,x,y, fill='pink')
        
    


        #print(app.rotationAngleX, app.rotationAngleY)
        #app.xAxisInitAngle -= (xAxisTheta*180/math.pi)
        #app.yAxisInitAngle -= (yAxisTheta*180/math.pi)

        #app.xAxisAngle = deg2Rad((xAxisTheta*180/math.pi))
        #app.yAxisAngle = deg2Rad((yAxisTheta*180/math.pi))

        #app.xAxisAngle = deg2Rad(app.xAxisInitAngle - (xAxisTheta*180/math.pi))
        #app.yAxisAngle = deg2Rad(app.yAxisInitAngle - (yAxisTheta*180/math.pi))
        #app.yAxisAngle = deg2Rad(app.yAxisInitAngle+app.rotationAngleX)
        #app.xAxisAngle = deg2Rad(app.xAxisInitAngle+app.rotationAngleY)


        #find angle to norm ? 


        
        #yAxisCoords = vecs2Graph(app, [app.yAxisVec])[0]

        #print(xAxisCoords)
        #print(yAxisCoords)
        #app.rotationAngle-=30
        #app.xAxisAngle = deg2Rad(app.xAxisInitAngle+app.rotationAngle)
        #app.yAxisAngle = deg2Rad(app.yAxisInitAngle+app.rotationAngle)

        #ok, this seems to work (except for the lengths of the vectors)
        #now we just need to get the angles from these vecs. 

                #print(xAxisTheta, yAxisTheta)

        
        print('x')
        print(f'rotated by {xAxisTheta*180/math.pi}')
        print(f'current x axis angle {app.xAxisInitAngle}')
        print(f'real axis angle? {app.xAxisInitAngle - xAxisTheta*180/math.pi}')

        print('y')
        print(f'rotated by {yAxisTheta*180/math.pi}')
        print(f'current y axis angle {app.yAxisInitAngle}')
        print(f'real axis angle? {app.yAxisInitAngle - yAxisTheta*180/math.pi}')
        #print(app.xAxisInitAngle)
        
        #app.rotationAngleX = (xAxisTheta*180/math.pi)
        #app.rotationAngleY = (yAxisTheta*180/math.pi) 

        '''
        #x axis
        #xAxisx = g2x(app, app.width*(math.cos(app.xAxisAngle)))
        #xAxisy = g2y(app, app.height*(math.sin(app.xAxisAngle)))
        #canvas.create_line(ox, oy, xAxisx, xAxisy)

        '''
                xAxisCoords = vecs2Graph(app, [app.xAxisVec])[0]
        #print(app.xAxisVec)
        #print(rotatedXAxisVec)
        #print(xAxisCoords)
        #a,b,c of the vec
        #print(app.xAxisVec)
        #print(app.yAxisVec)
        ax, bx = app.xAxisVec[0], app.xAxisVec[1]
        xAxisTheta = math.acos(ax/(math.sqrt(ax**2 + bx**2)))
        #print(xAxisCoords)
        

        ay, by = app.yAxisVec[0], app.yAxisVec[1]
        yAxisTheta = math.acos(ay/(math.sqrt(ay**2 + by**2)))

                #app.rotationAngle = 0

        #print(app.xAxisVec)

    elif event.key == 'r':
    
        '''

'''
#### perspective rendering 
    app.cameraOrigin = np.array([130,130,100])
    app.imageTopLeft = np.array([200,  45, 200])

    #these things change based on your rotation // image view (camera origin may change too / stay the same?)
    a3 = app.imageTopLeft - app.cameraOrigin
    a1 = np.array([-1,0,0])
    a2 = np.array([0,0,-1])

    '''
    '''app.cameraMatrix = np.zeros((3,3))
    cameraBasis = [a1,a2,a3]
    for i in range(len(cameraBasis)):
        app.cameraMatrix[:, i] = cameraBasis[i] #adding in columns '''
    '''
    cameraBasis = np.array([a1,a2,a3])
    
    app.cameraMatrix = cameraBasis.T

    #vecs2Modify = np.zeros((3,8))
    #print(vecs2Modify)
    #for i in range (app.lw.vecs.shape[0]):
    #    vecs2Modify[:, i] = app.lw.vecs[i]
    #print(vecs2Modify)

    projectionLW = np.linalg.inv(app.cameraMatrix) @ app.lw.vecs.T 

    app.imageCoords = np.zeros((2,8))
    for i in range(projectionLW.shape[1]): # in terms of columns
        col = projectionLW[:,i]
        divisor = col[2]
        projectionLW[:,i] /= divisor
        app.imageCoords[:, i] = projectionLW[:2, i] #add in first two components only 

    print('imageCoords')
    print(app.imageCoords.T)

    app.lwImageCoords = perspectiveRender(app, cameraBasis, app.lw.vecs)
    print(app.lwImageCoords)
'''

def drawVector(app, canvas):
    #origin
    ox, oy = app.width/2, app.height/2

    #rotation angle
    r = app.rotationAngle

    e1 = [100, 100, 200]

    #z axis
    canvas.create_line(ox,oy, ox, g2y(app, e1[2]), fill='red')

    #x axis
    xAngle = deg2Rad(210+r)
    xAxisx = g2x(app, e1[0]*(math.cos(xAngle))) #+ app.width/2
    xAxisy = g2y(app, e1[0]*(math.sin(xAngle))) #+ app.height/2
    canvas.create_line(ox, oy, xAxisx, xAxisy, fill='red')

    #y axis
    yAngle = deg2Rad(330+r)
    yAxisx = g2x(app, e1[1]*(math.cos(yAngle))) #+ app.width/2
    yAxisy = g2y(app, e1[1]*(math.sin(yAngle))) #+ app.height/2
    canvas.create_line(ox, oy, yAxisx, yAxisy, fill='red')

    tx = e1[0]*math.cos(xAngle) + e1[1]*(math.cos(yAngle))
    ty = e1[0]*math.sin(xAngle) + e1[1]*(math.sin(yAngle)) + e1[2]
    canvas.create_line(ox,oy, g2x(app, tx), g2y(app, ty), fill='blue')
    canvas.create_oval(g2x(app, tx)-5, g2y(app, ty)-5,g2x(app, tx)+5, g2y(app, ty)+5)

def drawBasis(app, canvas):
    #origin
    ox, oy = app.width/2, app.height/2

    #rotation angle
    r = app.rotationAngle 

    for vec in CUBE:
        #z axis
        #canvas.create_line(ox,oy, ox, g2y(app, e1[2]), fill='red')

        #x axis
        xAngle = deg2Rad(210+r)
        xAxisx = g2x(app, vec[0]*(math.cos(xAngle))) #+ app.width/2
        xAxisy = g2y(app, vec[0]*(math.sin(xAngle))) #+ app.height/2
        #canvas.create_line(ox, oy, xAxisx, xAxisy, fill='red')

        #y axis
        yAngle = deg2Rad(330+r)
        yAxisx = g2x(app, vec[1]*(math.cos(yAngle))) #+ app.width/2
        yAxisy = g2y(app, vec[1]*(math.sin(yAngle))) #+ app.height/2
        #canvas.create_line(ox, oy, yAxisx, yAxisy, fill='red')

        tx = vec[0]*math.cos(xAngle) + vec[1]*(math.cos(yAngle))
        ty = vec[0]*math.sin(xAngle) + vec[1]*(math.sin(yAngle)) + vec[2]
        canvas.create_line(ox,oy, g2x(app, tx), g2y(app, ty), fill='blue')
        #canvas.create_oval(g2x(app, tx)-5, g2y(app, ty)-5,g2x(app, tx)+5, g2y(app, ty)+5)


def drawPaper(self, canvas):

    #unmoving rect
    x0,y0 = self.rect[0]
    x1,y1 = self.rect[1]
    canvas.create_line(x0,y0,x0,y1)
    canvas.create_line(x0,y0,x1,y0)
    canvas.create_line(x1,y1,x1,y0)
    canvas.create_line(x1,y1,x0,y1)

    #moving rect
    #left side 
    a0,b0 = self.rect2[0] #top left
    a1,b1 = self.rect2[1] #bottom left
    #right side 
    a2,b2 = self.rect2[2] #top right
    a3,b3 = self.rect2[3] #bottom left

    canvas.create_line(a0, b0, a1, b1) #left
    canvas.create_line(a0, b0, a2, b2) #top 
    canvas.create_line(a2, b2, a3, b3) #right
    canvas.create_line(a1, b1, a3, b3) #bottom

    if (self.rect2[0][1]>self.rect2[2][1]):
        canvas.create_polygon(a0,b0,a1,b1,a3,b3,a2,b2,fill='red')
    else:
        canvas.create_polygon(a0,b0,a1,b1,a3,b3,a2,b2,fill='blue') 

def drawCircles(self, canvas):
    #circles
    r = self.r
    for x,y in self.circs:
        canvas.create_oval(x-r, y-r, x+r, y+r)


def movePaper(self):
    narrowToWide = np.array([[-5,0],[-5,0],[5,0],[5,0]])
    wideToNarrow = np.array([[5,0],[5,0],[-5,0],[-5,0]])

    r0 = self.rect2[0]
    r1 = self.rect2[1]
    r2 = self.rect2[2]
    r3 = self.rect2[3]

    #if self.rect2[0][1]<self.rect2[2][1] and self.incr:
    if self.incr:
        self.rect2 = self.rect2 + narrowToWide
        if abs(self.rect2[0][0]-self.rect2[2][0])>=self.xWidth:
            self.incr = False
    #elif self.rect2[0][1]<self.rect2[2][1] and not self.incr:
    elif not self.incr:
        self.rect2 = self.rect2 + wideToNarrow
        if self.rect2[2][0]-self.rect2[0][0]<=0:
            self.rect2 = np.array([r2, r3, r0, r1])
            self.incr = True

## keypressed scrapped
'''
    if event.key == 't':
        #transpose 
        self.rect = np.transpose(self.rect)
    elif event.key == 'r':
        #rotate 
        rot = rotMat(180)
        #self.rect = self.rect @ rot
        temp = self.rect + np.array([[-self.width/2, -self.height/2],
                                    [-self.width/2, -self.height/2]])
        #self.rect = temp
        newTemp = np.matmul(rot, np.transpose(temp))
        self.rect = newTemp + np.array([[self.width/2, self.height/2],
                                    [self.width/2, self.height/2]])
    elif event.key == 'q':
        temp = self.rect - np.array([[-self.width/2, -self.height/2],
                                    [-self.width/2, -self.height/2]])
        self.rect = temp
'''

def rotMat(theta):
        return np.array([[math.cos(theta), -math.sin(theta)],
                         [math.sin(theta), math.cos(theta)]])
        #return rot