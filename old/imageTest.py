from PIL import Image
import numpy as np
#from PIL import ImageEnhance
#from cmu_112_graphics import *
#from PIL import PSDraw


im = Image.open('myImage.jpeg')
print(im.size) #2-tuple of width, height in pixels

a = np.asarray(im) 
print(len(a[0]), len(a)) #cols, rows aka width, height

print(a[0][0]) #first pixel 
print(type(a), type(a[0][0][0]))
r,g,b = a[0][0]
#print(type(int(r)))

#Image.effect_noise((100,100), 50)

rows = len(a)
cols = len(a[0])
#b = [['hi']*cols for i in range(rows)]
b = np.zeros((rows, cols))
print(len(b))
print(len(b[0]))
print('test', b[0][0])
#print(type(b))
#print(type(a))
#gray = 100
print('b', type(b))
for row in range(rows):
    #arr = np.zeros((len(row)))
    for col in range(cols):
        #print(type(b[row][col]))
        #break
        #break
        # fix
        r,g,b = a[row][col]
        r,g,b = int(r), int(g), int(b)
        gray = (r+g+b)//3
        #print(type(gray))
        #print(type(b))
        #arr.append(arr, np.array([gray, gray, gray]))
        #print(b[row][col])
    #b[row] = arr

#testIm = Image.fromarray(b)
#b.show()
#convert back to Pillow image after modifying a
#im = Image.fromarray(a)

#with Image.open('myImage.jpeg') as im:
    #print(im.getbands())
    #title = "hi"
    #box = (1*72, 2*72, 7*72, 10*72) # in points

    #ps = PSDraw.PSDraw() # default is sys.stdout
    #ps.begin_document(title)

    # draw the image (75 dpi)
    #ps.image(box, im, 75)
    #ps.rectangle(box)

    # draw title
    #ps.setfont("HelveticaNarrow-Bold", 36)
    #ps.text((3*72, 4*72), "WHAT")

    #ps.end_document()

#import pil

def main():
    myImg = Image.open('myImage.jpeg')
    print(myImg.format) #source of an image
    print(myImg.size) #2-tuple of width, height in pixels
    print(myImg.mode) #RGB, greyscale, etc. 

    enh = ImageEnhance.Contrast(myImg)
    enh.enhance(1.3).show("30% more contrast")

    '''
    # split the image into individual bands
    source = myImg.split()

    R, G, B = 0, 1, 2

    # select regions where red is less than 100
    mask = source[R].point(lambda i: i < 100 and 255)
    #mask = source[R].point(lambda i: i<100 or 255)
    #white represents selected? 
    #selects i<100 as 255 

    # process the green band
    out = source[G].point(lambda i: i * 0.7)

    # paste the processed band back, but only where red was < 100
    source[G].paste(out, None, mask)

    # build a new multiband image
    myImg = Image.merge(myImg.mode, source)
    #myImg.show()

    #mask.show()

    '''

    #r, g, b = myImg.split()
    #r.show() #black and white
    #g.show()
    #b.show()
    #im = Image.merge("RGB", (g,g,r))
    #im.show()
    #im = Image.merge("RGB", (b, g, r))

    #pixel manipulation - >1 --> brighter, <1 --> darker
    #out = myImg.point(lambda i: i*0.5)
    #out.show()

    #myImg.show() #for debugging, saves image to disk

#main()

#color to grayscale

#edge detection

#filling in edges 

#sketchy style

#changing light source

#transition to live video feed

#tkinter GUI

#only filter a part of the screen

#lasso a part of the screen

#audio to play take on me

#pass in video to autorotoscope


#crop
#https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#copying-a-subrectangle-from-an-image