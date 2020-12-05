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
