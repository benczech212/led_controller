##  LED Controller Project
##  HID button controller


import time
import adafruit_trellism4
import neopixel
import random
import math

trellis = adafruit_trellism4.TrellisM4Express()

class buttonMatrix:
    def __init__(self, name, xmin, ymin, xmax, ymax):
        self.name = name
        self.xmin = xmin
        self.xmax = xmax
        self.xrange = self.xmax - self.xmin + 1
        self.ymin = ymin
        self.ymax = ymax
        self.yrange = self.ymax - self.ymin + 1
        self.range = self.xrange * self.yrange
        self.keysPressed = set()
        self.lastPressed = set()
        self.lastReleased = set()
        self.currentPress = set()

    def index2xy(self,pixelIndex):
        x = pixelIndex % self.xrange
        y = math.floor(pixelIndex / self.xrange)
        return [x,y]
    def xy2index(self, coords):
        x = coords[0]
        y = coords[1]
        return (y * self.xrange) + x



matrix = buttonMatrix("neotrellis",0,0,7,3)





def wheel(pos):
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return int(255 - pos * 3), int(pos * 3), 0
    if pos < 170:
        pos -= 85
        return 0, int(255 - pos * 3), int(pos * 3)
    pos -= 170
    return int(pos * 3), 0, int(255 - (pos * 3))

def sendI2Cmessage(message):
    pass

def onPress(press, buttonMatrix):
    print("Pressed:", press)
    x = press[0]
    y = press[1]
    trellis.pixels[x,y] = wheel(tickCount)
    trellis.pixels.show()   


def onRelease(release, buttonMatrix):
    print("Released:", release)
    
    



def fillTrellisRainbow_AtPoint(press):
    pixel = (press[1] * 8) + press[0]
    pixel_index = (pixel * 256 // 32)
    trellis.pixels.fill(wheel(pixel_index & 255))


def fillTrellisRainbow():
    for x in range(trellis.pixels.width):
        for y in range(trellis.pixels.height):
            pixel_index = (((y * 8) + x) * 256 // 32)
            trellis.pixels[x, y] = wheel(pixel_index & 255)


def updatePressed(device,buttonMatrix):
    buttonMatrix.keysPressed = set(device.pressed_keys)

def checkForInputs(buttonMatrix):
    global tickCount
    updatePressed(trellis, buttonMatrix)
    # Check for Pressed buttons
    for press in buttonMatrix.keysPressed - buttonMatrix.currentPress:
        if press:
            onPress(press, buttonMatrix)
            
    # Check for released buttons
    for release in buttonMatrix.currentPress - buttonMatrix.keysPressed:
        if release:
            onRelease(release, buttonMatrix)
    buttonMatrix.currentPress = buttonMatrix.keysPressed
    tickCount +=1
    
    

tickCount = 0
while True:
    checkForInputs(matrix)
    
    #for i in range(buttonMatrix.xrange):
        #trellis.pixels[]
    
    trellis.pixels.show()
    time.sleep(0.01)
