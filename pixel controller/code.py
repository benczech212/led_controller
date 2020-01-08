
import time
import random
import board
import adafruit_ws2801
import neopixel





class effects:
    def __init__(self, name, loopTimeTarget):
        self.name = name # Effect Name
        self.loopTimeTarget = loopTimeTarget



class ledSegment:
    def __init__(self, ledType, name, initialBrightness, dataPin, clockPin, pixelMin, pixelMax, order, autoWrite):
        self.name = name            # Name of the segment
        self.ledType = ledType      # 
        self.initialBrightness = initialBrightness  # Master initialBrightness (int or float from 0 to 1)
        self.dynamicBrightness = 1
        self.dataPin = dataPin      # pin segment is connected to
        self.clockPin = clockPin    # 
        self.pixelMin = pixelMin    # fist pixel in semgent
        self.pixelMax = pixelMax    # last pixel in segment
        self.order = order          # Order of pixels | neopixel.RGB, neopixel.GRB, neopixel.GRBW
        self.autoWrite = autoWrite
        self.range = (self.pixelMax - self.pixelMin) + 1
        self.pixels = self.initializePixels()
        self.channelCount = len(self.order)
        self.channelNames = self.nameChannels()
        self.counter = counter()        
        self.enabled = True
        
    def nameChannels(self):
        channelNames = []
        for channel in self.order:
            channelNames.append(channelOrderDefault[channel])
        return channelNames
    
    def initializePixels(self):
        try:
            if self.ledType == "WS2812":
                # 3 Wire NeoPixels
                return neopixel.NeoPixel(self.dataPin, self.range, brightness=self.initialBrightness, auto_write=self.autoWrite, pixel_order=self.order)
            elif self.ledType == "WS2801":
                # 4 Wire SPI LEDs
                return adafruit_ws2801.WS2801(self.clockPin, self.dataPin, self.range, brightness=self.initialBrightness, auto_write=self.autoWrite)
            else: 
                # Invalid LED Type
                print("Invalid LED Type {}".format(self.ledType))
                raise NameError("Invalid LED Type")
        except:
            pass
    def randomPixel(self):
        try:
            randomPixel = random.randrange(self.pixelMin, self.pixelMax)
        except:
            randomPixel = self.pixelMin
        return randomPixel

    def randomDarkPixel(self):
        tryCount = 0
        maxTries = 64
        try:
            randomPixel = random.randrange(self.pixelMin, self.pixelMax)
            while (self.pixels[randomPixel] != 0):
                if (tryCount < maxTries):
                    break
                randomPixel = random.randrange(self.pixelMin, self.pixelMax)
                tryCount += 1
        except:
            randomPixel = self.pixelMin
        return randomPixel
    
       
class counter:
    def __init__(self):
        now = time.monotonic()
        self.tickCount = 0
        self.tickTimeLast = now
        self.tickTimeCurrent = now
        self.tickTimeTarget = 0

        self.frameCount = 0
        self.frameTimeLast = now
        self.frameTimeCurrent = now
        self.frameTimeTarget = 0

        self.loopCount = 0
        self.loopTimeLast = now
        self.loopTimeCurrent = now
        self.loopTimeTarget = 0
        
######################### PRINT FUNCTIONS ##############################
print_lineWidth = 60

def print_devider(char):
    printBuffer = char * print_lineWidth
    print(printBuffer)

######################### HELPERS ##############################

def random_color():
    return wheel(random.randrange( 0, 255))

def random_colorRandomBrightness():
    return wheel(random.randrange( 0, int(255 * random.randrange(1,255))))

def random_colorWbrightness(brightnessFloat):
    return wheel(random.randrange( 0, int(255 * brightnessFloat)))

def wheel(hue):
    # Input a hue value (int or float from 0 - 255) > Outputs a 32-bit color value on the color wheel.
    hue = int(hue % 256)
    if hue < 85:
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
    return (r, g, b)



    
def ArrayToTuple(array):
    tupple = ()
    for i in array:
        tupple.append(i)
    return tupple
    
def TuppleToArray(tupple):
    array = []
    for i in range(len(tupple)):
        array.append(i)
    return array

######################### TESTING ##############################

def test_colors_allPixels(activeDevices):
    delayBetweenColors = 1
    colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,255),]
    for device in activeDevices:
        color = colors[device.counter.tickCount % len(colors)]
        device.pixels.fill(color)
        device.pixels.show()
        device.counter.tickCount+=1
    time.sleep(delayBetweenColors)
        

def test_range(activeDevices):
    #IN PROGRESS
    for device in activeDevices:
        print_devider("-")
        print('Testing Pixel Range for Device "{}"'.format(device.name))
        print('Min Pixel: {} | Max Pixel: {} | Total Range: {}'.format(device.pixelMin, device.pixelMax, device.range))
        print_devider(".")
        device.pixels[device.pixelMin] = (255,255,255)
        device.pixels[device.pixelMax] = (255,255,255)
        #device.pixels.show()
        time.sleep(0.1)
        
        
def test_colors_eachPixel(activeDevices):
    for device in activeDevices:
        pass



######################### EFFECTS ##############################
def effect_raindrops(activeDevices, colors, dropsPerFrame, framesBetweenDrops, fadeAmount):
    for device in activeDevices:
        if (device.counter.frameCount % framesBetweenDrops) == 0:
            for dropID in range(dropsPerFrame):
                device.pixels[device.randomDarkPixel()] = colors[device.counter.tickCount % len(colors)]
                device.counter.tickCount += 1
        fadeBackground(activeDevices,fadeAmount)
        
    device.counter.loopCount += 1

    

def fadeBackground(activeDevices,fadeAmount):
    for device in activeDevices:
        for pixelID in range(device.range):
            currentColor = device.pixels[pixelID]
            newColor = [0,0,0]
            for channelID in range(len(currentColor)):
                if currentColor[channelID] <= fadeAmount:
                    newColor[channelID] = 0
                else:
                    newColor[channelID] = currentColor[channelID] - fadeAmount
            device.pixels[pixelID] = (newColor[device.order[0]],newColor[device.order[1]],newColor[device.order[2]])
        device.pixels.show()


        #for pixelID in range(device.range):
        
        #    newColor = [0,0,0]
        #    for channelID in range(len(currentColor)):
        #        if currentColor[channelID] <= fadeAmount:
        #            newColor[channelID] = 0
        #        else:
        #            newColor[channelID] = currentColor[channelID] - fadeAmount
        #    device.pixels[pixelID] = newColor
        #device.pixels.show()
        
            


def effect_christmasTree(activeDevices):
    for device in activeDevices:
        loopCount = device.counter.loopCount
        tickCount = device.counter.tickCount
        for pixelID in range(device.range):
            slowChange = loopCount >> 4
            fastChange = (loopCount + (pixelID * loopCount)) + (loopCount * 2)
            offset = ( loopCount + (tickCount & 2) ) * 8
            hue = (slowChange + fastChange + offset + pixelID ) * ( 0.05)
            hue %= 256
            device.pixels[pixelID] = wheel(int(hue))
            tickCount+=1
        loopCount+=1



def effect_slowRainbowSqueeze(activeDevices):
    for device in activeDevices:
        device.counter.loopTimeTarget = 0
        for pixelID in range(device.range):
            offset = device.counter.loopCount * -1
            spreadMod = 0.1
            spread = ((device.counter.loopCount * spreadMod) * pixelID) 
            change =  (device.counter.loopCount * 1)
            hue =  offset + spread + change + randomSeed
            color = wheel(hue)
            device.pixels[pixelID] = color
        device.counter.tickCount += 1


######################### STARTUP ##############################
def startup():
    print("Starting...")
    
    
def checkLoop():
    print("Checking for user input...")


################# DRAW LOOP ############################
def drawLoop(activeDevices):
    
    #test_colors_allPixels(activeDevices)
    #test_colors_eachPixel(activeDevices)
    #test_range(activeDevices)
    randomColors = [(255,255,255),(0,0,255)]
    effect_raindrops(activeDevices, randomColors, 2, 8, 4)
    #effect_christmasTree(activeDevices)
    #effect_slowRainbowSqueeze(activeDevices)
    
    drawIncrement(activeDevices)



######################### SHOW LOOP ##############################
def showLoop(activeDevices):
    for device in activeDevices:
        if device.enabled:
            device.pixels.show()
            device.counter.loopTimeLast = device.counter.loopTimeCurrent
            device.counter.loopTimeCurrent = time.monotonic()    
            device.counter.loopCount += 1
        else:
            device.pixels.fill(0)
            device.pixels.show()
    #print("Loop {} complete at {} in {} seconds".format(counter.loopCount, counter.loopTimeCurrent, counter.loopTimeCurrent - counter.loopTimeLast))


######################### IDLE LOOP ##############################
# When the draw loop and show loop are completed, loop the idle loop until the time target is met
def idleLoop(activeDevices):
    
    idle = True
    while idle:
        deviceMaster.counter.loopTimeCurrent = time.monotonic()
        runningFor = deviceMaster.counter.loopTimeCurrent - deviceMaster.counter.loopTimeLast
        timeRemaining = deviceMaster.counter.loopTimeTarget - runningFor
        if timeRemaining <= 0:
            print("Loop Completed")
            idle = False    
        else:
            print("Idle...")
            time.sleep(0.01) # wait for 0.01 sec and try again
            #time.sleep(timeRemaining)


######################### DRAW INCREMENT ##############################
# Increments once when all devices once they have been drawn
def drawIncrement(activeDevices):
    for device in activeDevices:
        device.counter.frameCount += 1
    
    #counter.frameTimeLast = counter.frameTimeCurrent
    #counter.frameTimeCurrent = time.monotonic()
    #print("Frame {} complete at {} in {} seconds".format(counter.frameCount, counter.frameTimeCurrent, counter.frameTimeCurrent - counter.frameTimeLast))



######################### MAIN LOOP ##############################
def mainLoop():
    
    
    checkLoop()
    drawLoop(activeDevices)
    showLoop(activeDevices)
    idleLoop(activeDevices)


######################## GLOBAL VARIABLES ##############################
#counter = [counter()]
channelOrderDefault = ["Red","Green","Blue","White"]

devices = [
    ledSegment("WS2801","Christmas Lights", 1, board.SCL, board.SDA, 0, 23, neopixel.RGB, False),
    ledSegment("WS2812","Status Light",1,board.NEOPIXEL, None, 0, 0, neopixel.GRB, False)
]

activeDevices =  devices # change to only include some of the devices | [devices[0],devices[1]]

deviceMaster = activeDevices[0]
randomSeed = random.randrange(0,2048)


######################## MAIN CODE ##############################
startup()
while True:
    mainLoop()
    
