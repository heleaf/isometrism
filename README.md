![test](https://i.imgur.com/hClwi7B.jpg)

Create an isometric room, add furniture, then ‘step inside’ and look around.

TO RUN: run `main`, which has the following dependencies:
- `threedimfunctions`
- `newbasis`
- `cube`
- `button`
- `cmu_112_graphics`

LIBRARIES: 
- numpy 

SHORTCUT COMMANDS: 
- 1: skip title screen 
- h: toggle help screen 
- r: rotate isometric room clockwise by one step
- t: rotate isometric room counterclockwise by one step
- v: toggle perspective viewing screen
- c: toggle camera visibility 

Note: you cannot modify the camera or the room if you are rotated out of place 
(to reset static rotations from r and t, click the rotation arrow buttons)

Camera movement:
- f: change direction of camera view (clockwise direction)
- g: change direction of camera view (counterclockwise direction)
- w: increase the z axis component of the camera
- s: decrease the z axis component of the camera
- a: increase the y axis component of the camera
- d: decrease the y axis component of the camera
- z: increase the x axis component of the camera
- x: decrease the x axis component of the camera 
