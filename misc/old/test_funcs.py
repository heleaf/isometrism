def drawAxes(app, canvas):
    ox, oy = app.origin
    #z axis
    canvas.create_line(ox,oy, ox, 0)
    #x axis
    xAxisx = g2x(app, app.width*(math.cos(app.xAxisAngle)))
    xAxisy = g2y(app, app.height*(math.sin(app.xAxisAngle)))
    canvas.create_line(ox, oy, xAxisx, xAxisy)
    #y axis
    yAxisx = g2x(app, (app.width)*(math.cos(app.yAxisAngle)))
    yAxisy = g2y(app, (app.height)*(math.sin(app.yAxisAngle)))
    canvas.create_line(ox, oy, yAxisx, yAxisy)

def drawUnitCube(app, canvas):
    #unit cube, for rotation demonstration
    for point in app.CUBEPOINTS:
        canvas.create_oval(point[0]-3, point[1]-3, point[0]+3, point[1]+3, fill='blue')

    CUBE = app.CUBE
    for i in range(app.CUBEPOINTS.shape[0]): #rows
        p1 = app.CUBEPOINTS[i]
        v1 = app.CUBE[i]
        for j in range(app.CUBEPOINTS.shape[0]): #rows
            p2 = app.CUBEPOINTS[j]
            v2 = app.CUBE[j]
            diffVec = v1-v2 
            if math.sqrt(diffVec[0]**2 + diffVec[1]**2 + diffVec[2]**2) <= 60: 
                canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill = 'blue')

    #rotating axes 
    xAxisCoords = vecs2Graph(app, [app.xAxisVec])
    x,y = xAxisCoords[0][0], xAxisCoords[0][1]
    #print(x,y)
    canvas.create_line(ox,oy,x,y, fill='red')

    yAxisCoords = vecs2Graph(app, [app.yAxisVec])
    x,y = yAxisCoords[0][0], yAxisCoords[0][1]
    #print(x,y)
    canvas.create_line(ox,oy,x,y, fill='orange')

def drawSamples(app, canvas):
    #get a sample cube floor 
    drawCube(app, canvas, app.sampleCubeFloorCoords, 'green')

    #sample walls 
    drawCube(app, canvas, app.sampleCubeRWCoords, 'green')
    drawCube(app, canvas, app.sampleCubeLWCoords, 'green')

    #and a sample cube on top of the floor
    drawCube(app, canvas, app.sampleCubeCoords, 'blue')

def rotateSamples(app):
    #sample cube floor
    app.sampleCubeFloorVecs = rotateCube(app, app.sampleCubeFloorVecs, 10)
    app.sampleCubeFloorCoords = vecs2Graph(app, app.sampleCubeFloorVecs) 

    app.sampleCubeRWVecs = rotateCube(app, app.sampleCubeRWVecs, 10)
    app.sampleCubeRWCoords = vecs2Graph(app, app.sampleCubeRWVecs)

    app.sampleCubeLWVecs = rotateCube(app, app.sampleCubeLWVecs, 10)
    app.sampleCubeLWCoords = vecs2Graph(app, app.sampleCubeLWVecs)
    
    #sample cube
    app.sampleCubeVecs = rotateCube(app, app.sampleCubeVecs, 10)
    app.sampleCubeCoords = vecs2Graph(app, app.sampleCubeVecs) 

    app.CUBE = rotateCube(app, app.CUBE, 10)
    app.CUBEPOINTS = vecs2Graph(app, app.CUBE)

def keyPressed(app, event):
        elif event.key == 'w':
        for row in app.CUBE: 
            row[2]+=10
        #move the cube up
    elif event.key =='s':
        for row in app.CUBE:
            row[2]-=10
        #move the cube down
    elif event.key == 'a':
        for row in app.CUBE: 
            row[0]+=10
        #move the cube left (x) 
    elif event.key == 'd':
        for row in app.CUBE:
            row[0]-=10
        #move the cube right (x)
    elif event.key == 'z':
        for row in app.CUBE:
            row[1]-=10
        #move the cube left (y)
    elif event.key == 'x':
        for row in app.CUBE:
            row[1]+=10
        #move the cube right (y)
def rotateRandomStuff(app):
    app.classCube.vecs = rotateCube(app, app.classCube.vecs, 10)
    app.classCube.origin = app.classCube.vecs[0]
    #for reference, rotating the "axes" of the cube objs
    rotatedXAxisVec = rotateVec(app, app.xAxisVec, 10, [0,0,1])
    rotatedYAxisVec = rotateVec(app, app.yAxisVec, 10, [0,0,1])
    app.xAxisVec = rotatedXAxisVec
    app.yAxisVec = rotatedYAxisVec

def initialize(app):
    app.CUBE = np.array([[10,10,0],
                        [60,10,0],
                        [10,60,0],
                        [10,10,50],
                        [60,60,0],
                        [60,10,50],
                        [10,60,50],
                        [60,60,50]])
    app.CUBEPOINTS = vecs2Graph(app, app.CUBE)
    app.showUnitCube = False
     app.xAxisVec = np.array([100,0,0])
    app.yAxisVec = np.array([0,100,0])

    app.sampleCubeFloorVecs = np.array([[287.7097569,   39.75633592,  0.        ],
                                    [287.7097569,   39.75633592,  10.        ],
                                    [ 43.73894914, 301.26997008,   0.        ],
                                    [ 43.73894914, 301.26997008,  10.        ],
                                    [ 43.73894914,  39.75633592,   0.        ],
                                    [ 43.73894914, 39.75633592,  10.        ],
                                    [287.7097569,  301.26997008,   0.        ],
                                    [287.7097569,  301.26997008, 10.        ]])
    
    app.sampleCubeFloorCoords = vecs2Graph(app, app.sampleCubeFloorVecs)

    app.sampleCubeRWVecs = np.array([[ 43.73894914, 301.26997008,   0.        ],
                                [ 43.73894914, 301.26997008, 138.        ],
                                [ 33.73894914, 301.26997008,   0.        ],
                                [ 33.73894914, 301.26997008, 138.        ],
                                [ 43.73894914,  39.75633592,   0.        ],
                                [ 43.73894914,  39.75633592, 138.        ],
                                [ 33.73894914, 39.75633592,   0.        ],
                                [ 33.73894914, 39.75633592, 138.        ]])
    app.sampleCubeRWCoords = vecs2Graph(app, app.sampleCubeRWVecs)

    app.sampleCubeLWVecs = np.array([[287.7097569,   39.75633592,   0.        ],
                                    [287.7097569,   39.75633592, 138.        ],
                                    [287.7097569,   29.75633592,   0.        ],
                                    [287.7097569,   29.75633592, 138.        ],
                                    [ 43.73894914,  39.75633592,   0.        ],
                                    [ 43.73894914,  39.75633592, 138.        ],
                                    [ 43.73894914,  29.75633592,   0.        ],
                                    [ 43.73894914,  29.75633592, 138.        ]])
    app.sampleCubeLWCoords = vecs2Graph(app, app.sampleCubeLWVecs)

    app.sampleCubeVecs = np.array([[100, 70,  10],
                                [150, 70,  10],
                                [100, 120,  10],
                                [100,  70,  60],
                                [150, 120,  10],
                                [150,  70,  60],
                                [100, 120,  60],
                                [150, 120,  60]])
    app.sampleCubeCoords = vecs2Graph(app, app.sampleCubeVecs)


        #old collision detection
        '''
        for i in range(len(app.occupiedX)):
            startX = min(app.occupiedX[i])
            endX = max(app.occupiedX[i])
            startY = min(app.occupiedY[i])
            endY = max(app.occupiedY[i])
            if ((startX < ox2 < endX or startX < ox2+l2 < endX) and
                (startY < oy2 < endY or startY < oy2+w2 < endY)):
                print('nope')
                app.furniture['standard'].pop()
                app.newFurniture = None
                app.chairButton.isPressed = False
                app.tableButton.isPressed = False
                return 

        #passing collision detection
        app.occupiedX.append([ox2, ox2+app.newFurniture.length])
        app.occupiedY.append([oy2, oy2+app.newFurniture.width])
        '''


        '''
    #change this to be something based on where the room is
    #app.cameraOrigin = np.array([100,0,30])
    imageDistance = 35
    imageLength = 80
    imageHeight = 80

    #be able to move the camera (then recalculate all imageCoordsFront)
    #generate the camera based on where the player's room is built
    #imageLength = imageHeight = 100

    #front facing (push forward on x)
    imageTopLeft = app.cameraOrigin + np.array([imageDistance, imageLength/2, imageHeight/2])
    imageTopRight = imageTopLeft + np.array([0,-imageLength, 0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([0,-imageLength,-imageHeight])
    app.cameraImageCoords = app.imageCoordsFront = vecs2Graph(app, [imageTopLeft, imageTopRight, imageBotRight, imageBotLeft])

    a1 = np.array([0,imageLength/app.width,0])
    a2 = np.array([0,0,imageHeight/app.height])
    a3 = imageTopLeft 
    app.cameraBasis = np.array([a1,a2,a3]).T #basis of camera vectors as columns 

    #left facing (flipped)
    #b1 = np.array([imageLength/app.width,0,0])
    #b2 = np.array([0,0,imageHeight/app.height])
    #b3 = app.cameraOrigin + np.array([imageLength/2, imageDistance, imageHeight/2])

    #app.cameraBasis = np.array([b1,b2,b3]).T 
    #gibbirish
    '''
    '''
    c1 = np.array([imageLength/app.width,0,0])
    c2 = np.array([0,0,imageHeight/app.height])
    c3 = app.cameraOrigin + np.array([-imageLength/2, imageDistance, imageHeight/2])

    app.cameraBasis = np.array([c1,c2,c3]).T
    '''
    '''

    #this left facing is better, i think
    d1 = np.array([-imageLength/app.width,0,0])
    d2 = np.array([0,0,imageHeight/app.height])
    d3 = app.cameraOrigin + np.array([-imageLength/2, imageDistance, imageHeight/2])
    
    imageTopLeft = d3
    imageTopRight = imageTopLeft + np.array([imageLength,0,0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([imageLength, 0, -imageHeight])
    app.imageCoordsLeft = vecs2Graph(app, [imageTopLeft, imageTopRight, imageBotRight, imageBotLeft]) 

    #???? its flipped tho ok now its good right####
    e1 = np.array([imageLength/app.width,0,0])
    e2 = np.array([0,0,imageHeight/app.height])
    e3 = app.cameraOrigin + np.array([imageLength/2, -imageDistance, imageHeight/2]) 

    imageTopLeft = e3
    imageTopRight = imageTopLeft + np.array([-imageLength, 0,0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([-imageLength, 0, -imageHeight])
    app.imageCoordsRight = vecs2Graph(app, [imageTopLeft, imageTopRight, imageBotRight, imageBotLeft])
    #if still bad do -imageLength/app.width for e1 and e3
    

    #look back
    f1 = np.array([0,-imageLength/app.width, 0])
    f2 = np.array([0,0,imageHeight/app.height])
    f3 = app.cameraOrigin + np.array([-imageLength/2, -imageDistance, imageHeight/2])

    imageTopLeft = f3
    imageTopRight = imageTopLeft + np.array([0,imageLength,0])
    imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    imageBotRight = imageTopLeft + np.array([0, imageLength, -imageHeight])
    app.imageCoordsBack = vecs2Graph(app, [imageTopLeft, imageTopRight, imageBotRight, imageBotLeft])
    #f3 
    #app.cameraBasis = np.array([f1,f2,f3]).T

    #a - front
    #e - right 
    #f - back
    #d - left


    #app.cameraBasisAlts = [np.array([a1,a2,a3]).T, np.array([d1,d2,d3]).T, np.array([f1,f2,f3]).T]
    #app.cameraImageAlts = [app.imageCoordsFront, app.imageCoordsLeft, app.imageCoordsBack]

    app.cameraBasisAlts = [np.array([a1,a2,a3]).T, np.array([e1,e2,e3]).T, np.array([f1,f2,f3]).T, np.array([d1,d2,d3]).T]
    app.cameraImageAlts = [app.imageCoordsFront, app.imageCoordsRight, app.imageCoordsBack, app.imageCoordsLeft]
    '''

    #app.cameraBasis = np.array([b1,b2,b3]).T

    #left facing (push forward on y)
    '''
    imageTopLeft = app.cameraOrigin + np.array([imageLength/2, -imageDistance, imageHeight/2])
    a1 = np.array([imageLength/app.width, 0,0])
    a2 = np.array([0,0,imageHeight/app.height])
    a3 = imageTopLeft
    '''
    #app.cameraBasis = np.array([a1,a2,a3]).T 
    #app.cameraBasisAlts.append(np.array([a1,a2,a3]))
    #imageTopRight = imageTopLeft + np.array([-imageLength, 0,0])
    #imageBotLeft = imageTopLeft + np.array([0,0,-imageHeight])
    #imageBotRight = imageTopLeft + np.array([-imageLength, 0, -imageHeight])


    def renderCube(app, canvas, cube):
    topFaceVecs = []
    for i in cube.topFaceVecs:
        topFaceVecs.append(cube.vecs[i])
    
    leftFrontFaceVecs = []
    for i in cube.leftFrontFaceVecs:
        leftFrontFaceVecs.append(cube.vecs[i])
    
    rightFrontFaceVecs = []
    for i in cube.rightFrontFaceVecs:
        rightFrontFaceVecs.append(cube.vecs[i])

    leftBackFaceVecs = []
    for i in cube.leftBackFaceVecs:
        leftBackFaceVecs.append(cube.vecs[i])
    
    rightBackFaceVecs = []
    for i in cube.rightBackFaceVecs:
        rightBackFaceVecs.append(cube.vecs[i])

    botFaceVecs = []
    for i in cube.botFaceVecs:
        botFaceVecs.append(cube.vecs[i])

    t = topFaceCoords = vecs2Graph(app, topFaceVecs)
    lf = leftFrontFaceCoords = vecs2Graph(app, leftFrontFaceVecs)
    rf = rightFrontFaceCoords = vecs2Graph(app, rightFrontFaceVecs)
    lb = leftBackFaceCoords = vecs2Graph(app, leftBackFaceVecs)
    rb = rightBackFaceCoords = vecs2Graph(app, rightBackFaceVecs)
    b = botFaceCoords = vecs2Graph(app, botFaceVecs)

    #print(rightBackFaceVecs)
    
    #if rb[1][1]>rb[0][1] and rb[2][0]>rb[0][0]:
    #    canvas.create_polygon(t[0][0], t[0][1], t[1][0], t[1][1], t[3][0], t[3][1], t[2][0], t[2][1],fill='yellow')
    #    canvas.create_polygon(rf[0][0], rf[0][1], rf[1][0], rf[1][1], rf[3][0], rf[3][1], rf[2][0], rf[2][1],fill='red') 
    #    canvas.create_polygon(rb[0][0], rb[0][1], rb[1][0], rb[1][1], rb[3][0], rb[3][1], rb[2][0], rb[2][1],fill='orange')
    #else:
    canvas.create_polygon(t[0][0], t[0][1], t[1][0], t[1][1], t[3][0], t[3][1], t[2][0], t[2][1],fill='yellow')
    canvas.create_polygon(lf[0][0], lf[0][1], lf[1][0], lf[1][1], lf[3][0], lf[3][1], lf[2][0], lf[2][1],fill='orange')
    canvas.create_polygon(rf[0][0], rf[0][1], rf[1][0], rf[1][1], rf[3][0], rf[3][1], rf[2][0], rf[2][1],fill='red') 

def drawCube(app, canvas, cubeCoords, color='black'):
    for i in range(cubeCoords.shape[0]):
        p1 = cubeCoords[i]
        for j in range(cubeCoords.shape[0]):
            p2 = cubeCoords[j]
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)

def drawCubeOutline(app, canvas, cube, color='black'):
    topFaceVecs = []
    for i in cube.topFaceVecs:
        topFaceVecs.append(cube.vecs[i])
    
    leftFrontFaceVecs = []
    for i in cube.leftFrontFaceVecs:
        leftFrontFaceVecs.append(cube.vecs[i])
    
    rightFrontFaceVecs = []
    for i in cube.rightFrontFaceVecs:
        rightFrontFaceVecs.append(cube.vecs[i])

    leftBackFaceVecs = []
    for i in cube.leftBackFaceVecs:
        leftBackFaceVecs.append(cube.vecs[i])
    
    rightBackFaceVecs = []
    for i in cube.rightBackFaceVecs:
        rightBackFaceVecs.append(cube.vecs[i])

    botFaceVecs = []
    for i in cube.botFaceVecs:
        botFaceVecs.append(cube.vecs[i])

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
        #canvas.create_polygon(r[0][0], r[0][1], r[1][0], r[1][1], r[3][0], r[3][1], r[2][0], r[2][1], fill=None, outline=color)

    #canvas.create_polygon(t[0][0], t[0][1], t[1][0], t[1][1], t[3][0], t[3][1], t[2][0], t[2][1],fill=None)


def rotateRenderedWalls(app):
    app.CORW.vecs = rotateCube(app, app.CORW.vecs, 10)

    #print('after')
    #print(app.CORW.rightBackFaceVecs) #[0, 2, 3, 6]
    #print(app.CORW.vecs)
    print(app.rightCubeWallCoords)
    
    maxVal = max(app.rightCubeWallCoords[:,0])
    minVal = min(app.rightCubeWallCoords[:,0])
    #print(val)
    
    if maxVal == app.rightCubeWallCoords[-1][0]: #good for detecting initial turn 
        print('we need right back')
    elif minVal!=app.rightCubeWallCoords[-1][0]: #good for detecting end of turn
        print('we still need right back')
    else:
        print('nope')

    app.COLW.vecs = rotateCube(app, app.COLW.vecs, 10)