
import time
import board
import neopixel
import random
import math
import adafruit_fancyled.adafruit_fancyled as fancy

channelOrderDefault = ["Red","Green","Blue","White"]        

class Segment:

    def __init__(self, ledType, name, intensity, pin, pixelMin, pixelMax, order, autoWrite):
        self.ledType = ledType      # Type of LED IC: WS2812, WS2801
        self.name = name            # Name of the segment
        self.intensity = intensity  # Master Intensity (int or float)
        self.pin = pin              # pin segment is connected to
        self.pixelMin = pixelMin    # fist pixel in semgent
        self.pixelMax = pixelMax    # last pixel in segment
        self.order = order          # Order of pixels | neopixel.RGB, neopixel.GRB, neopixel.GRBW
        self.autoWrite = autoWrite
        self.range = (self.pixelMax - self.pixelMin) + 1
        self.pixels = neopixel.NeoPixel(self.pin, self.range, brightness=self.intensity, auto_write=self.autoWrite,pixel_order=self.order)
        self.channelCount = len(self.order)
        self.channelNames = self.nameChannels()
            
        
    def nameChannels(self):
        channelNames = []
        for channel in self.order:
            channelNames.append(channelOrderDefault[channel])
        return channelNames
    
    def initializePixels(self):

        if self.ledType == "WS2812":
            # 3 Wire NeoPixels
            pass
        elif self.ledType == "WS2801":
            # 4 Wire SPI LEDs
            self.pixels = adafruit_ws2801.WS2801(self.clock, self.pin, numleds, brightness=bright, auto_write=False)

#=====================================================================
#Fade from 1 color to another 
class fade:
    def __init__(self,startColor,endColor,frames):
        self.startColor = startColor
        self.endColor = endColor
        self.frames = frames
        self.colorVector = self.calcColorVector()
        self.perFrame = self.calcPerFrame()
        self.direction = self.calcDirection()
        #self.saveColorAtFrames = self.saveColorAtFrames()

    def calcColorVector(self):
        colorVector = []
        for channel in range(len(self.endColor)):
            colorVector.append(self.endColor[channel] - self.startColor[channel])
        return colorVector

    def calcPerFrame(self):
        perFrame = []
        for channel in range(len(self.endColor)):
            perFrame.append(self.colorVector[channel] / self.frames )
        return perFrame
        
    def calcDirection(self):
        direction = []
        for channel in range(len(self.perFrame)):
            if self.perFrame[channel] == 0:
                direction.append("SAME")
            elif self.perFrame[channel] > 0:
                direction.append("UP")
            else:
                direction.append("DOWN")
        return direction

    def colorAtFrame(self, frameNumber):
        frameNumber %= (self.frames - 1) #if frame number is greater than max frames, loop back
        color = []
        for channel in range(len(self.perFrame)):
            color.append(int(self.perFrame[channel] * frameNumber) + self.startColor[channel])
        return color





        

def effect_startup(segment):
    pass
    
            
      

def effect_spectrumSquish():
    
    for pixelID in range(len(leds)):
        spreadPerPixel = 4
        perPixelChange = ( (pixelID * spreadPerPixel) * frameCount)
        slowChange = frameCount >> 4
        fastChange = (tickCount + perPixelChange ) + (frameCount * 2)
        offset = ( frameCount + (tickCount & 2) ) * 8
        hue = (slowChange + fastChange + offset + pixelID ) * ( 0.05)
        hue %= 256
        leds[pixelID] = wheel(int(hue))
        tickCount+=1
    frameCount += 1


def update():
    pass



def wheel(hue):
    ORDER = neopixel.GRB
    if hue < 0 or hue > 255:
        r = g = b = 0
    elif hue < 85:
        r = int(hue * 3)
        g = int(255 - hue*3)
        b = 0
    elif hue < 170:
        hue -= 85
        r = int(255 - hue*3)
        g = 0
        b = int(hue*3)
    else:
        hue -= 170
        r = 0
        g = int(hue*3)
        b = int(255 - hue*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


#def rainbow_cycle(wait):
    #for j in range(255):
        #for i in range(num_pixels):
            #pixel_index = (i * 256 // num_pixels) + j
            #pixels[i] = wheel(pixel_index & 255)
        #pixels.show()
        #time.sleep(wait)


strip = Segment("strip1",1,board.D9,0,29,neopixel.GRB,False)


loopCount = 0
loopCountMax = 256


frames = 200
grad = [(0.00, 0x0000ff),
        (0.10, 0xffffff),
        (0.20, 0x000000),
        (0.30, 0x4444cc),
        (0.40, 0xffffff),
        (0.45, 0x222222),
        (0.50, 0x000000),
        (0.60, 0xff0000),
        (0.70, 0x000000),
        (0.80, 0x00ff00),
        (0.90, 0x000000)]
palette = fancy.expand_gradient(grad, frames)

while True:
    for i in range(strip.range):
        loopCount %= loopCountMax
        color = fancy.palette_lookup(palette, float((loopCount/loopCountMax)))
        strip.pixels[i % (strip.range) ] = (color.pack())
        strip.pixels.show()
    loopCount += 1