
import time
import random
import board
import adafruit_ws2801
import neopixel
try:
    import urandom as random  # for v1.0 API support
except ImportError:
    import random
import adafruit_fancyled.adafruit_fancyled as fancy



num_pix = 17  # Number of NeoPixels
pix_pin = board.D1  # Pin where NeoPixels are connected
strip = neopixel.NeoPixel(pix_pin, num_pix)
 
min_alpha = 0.1  # Minimum brightness
max_alpha = 0.4  # Maximum brightness
alpha = (min_alpha + max_alpha) / 2  # Start in middle
alpha_delta = 0.01  # Amount to change brightness each time through loop
alpha_up = True  # If True, brightness increasing, else decreasing
 
strip.fill([0, 0, 255])  # Fill blue, or change to R,G,B of your liking
 





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
            randomPixel = random.randrange(self.pixelMin, self.pixelMax+1)
            while (self.pixels[randomPixel] != 0):
                if (tryCount < maxTries):
                    break
                randomPixel = random.randrange(self.pixelMin, self.pixelMax+1)
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
    colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,255)]
    for device in activeDevices:
        for pixelID in range(device.range):
            cIndex = device.counter.loopCount >> 2
            device.pixels[pixelID] = colors[cIndex % len(colors)]
            fadeBackground(activeDevices,16)
        device.counter.loopCount += 1
        


######################### EFFECTS ##############################
def effect_raindrops(activeDevices, colors, dropsPerFrame, framesBetweenDrops, fadeAmount):
    for device in activeDevices:
        if (device.counter.frameCount % framesBetweenDrops) == 0:
            for frameID in range(dropsPerFrame):
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
            offset = device.counter.loopCount
            spreadMod = 0.1
            spread = ((device.counter.loopCount * spreadMod) * pixelID) 
            change =  (device.counter.loopCount * 1)
            hue =  offset + spread + change + randomSeed
            color = wheel(hue)
            device.pixels[pixelID] = color
        device.counter.tickCount += 1

def effect_slowRainbowSpin(activeDevices,spreadMod):
    for device in activeDevices:
        device.counter.loopTimeTarget = 0
        for pixelID in range(device.range):
            offset = device.counter.loopCount
            spread = (spreadMod * pixelID)
            change =  (device.counter.loopCount * 1)
            hue =  offset + spread + change + randomSeed
            color = wheel(hue)
            device.pixels[pixelID] = color
        device.counter.tickCount += 1

def effect_SpinUp(activeDevices,spinSpeed, colors):
     for device in activeDevices:
        t = (0.1 * spinSpeed) - (0.1 * device.counter.tickCount)
        if t < 0:
             t = 0
        device.counter.loopTimeTarget = t
        for pixelID in range(device.range):
            cindex = int( (pixelID  * 0.5) + device.counter.tickCount + device.clounter.loopCount) % (len(colors)-1)
            device.pixels[pixelID] = colors[cindex]
            device.counter.tickCount += 1
        device.clounter.loopCount += 1


def effect_acrReactor(activeDevices,):

    whiteLevel = random.randrange(0,12)
    min_alpha = 0.0  # Minimum brightness
    max_alpha = 1.0  # Maximum brightness
    #delta = max_alpha - min_alpha
    
    alpha = (min_alpha + max_alpha) / 2  # Start in middle
    alpha_delta = 0.01  # Amount to change brightness each time through loop
    alpha_up = True  # If True, brightness increasing, else decreasing
    color = [whiteLevel, whiteLevel, 255]

    for device in activeDevices:
        device.pixels.fill(color)
        if random.randint(1, 20) == 1:  # 1-in-5 random chance
            alpha_up = not alpha_up  # of reversing direction
        if alpha_up:  # Increasing brightness?
            alpha += alpha_delta  # Add some amount
            if alpha >= max_alpha:  # At or above max?
                alpha = max_alpha  # Limit to max
                alpha_up = False  # and switch direction
        else:  # Else decreasing brightness
            alpha -= alpha_delta  # Subtract some amount
            if alpha <= min_alpha:  # At or below min?
                alpha = min_alpha  # Limit to min
                alpha_up = True  # and switch direction
 
        device.pixels.brightness = alpha  # Set brightness to 0.0 to 1.0
    #time.sleep(0.1)

        

def effect_acrReactor_startup(activeDevices, dropsPerFrame, framesBetweenDrops, fadeAmount):
    whiteLevel = random.randint(0,32)
    colors = [(whiteLevel,whiteLevel,255),(0,0,255)]
    for device in activeDevices:
        if (device.counter.frameCount % framesBetweenDrops) == 0:
            device.pixels[device.randomDarkPixel()] = colors[device.counter.tickCount % len(colors)]
            device.counter.tickCount += 1
        fadeBackground(activeDevices,fadeAmount)
    device.counter.loopCount += 1

######################### STARTUP ##############################
def startup():
    print("Starting...")
    
    
def checkLoop(userInputs):
    print("Checking for user input...")
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


################# DRAW LOOP ############################
def drawLoop(activeDevices):
    
    #test_colors_allPixels(activeDevices)
    #test_colors_eachPixel(activeDevices)
    #test_range(activeDevices)
    
    #palette_arcReactor_heatmap = [        
              #0x000033,           
              #0x0000aa,
              #0x0000ff,
              #0xffffff,
              #0x0000aa,
              #0x000033]           
    
    
    #effect_acrReactor(activeDevices)

    
    effect_acrReactor_startup(activeDevices, 2, 1, 8)
    #effect_SpinUp(activeDevices,0.5, ([0,255,0],[255,255,255]))
    #effect_raindrops(activeDevices, ([0,0,255],[32,32,255]), 2, 1, 8)
    #effect_christmasTree(activeDevices)
    #effect_slowRainbowSqueeze(activeDevices)
    #effect_slowRainbowSpin(activeDevices, 8)
    
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




######################### DRAW INCREMENT ##############################
# Increments once when all devices once they have been drawn
def drawIncrement(activeDevices):
    for device in activeDevices:
        device.counter.frameCount += 1
    
    #counter.frameTimeLast = counter.frameTimeCurrent
    #counter.frameTimeCurrent = time.monotonic()
    #print("Frame {} complete at {} in {} seconds".format(counter.frameCount, counter.frameTimeCurrent, counter.frameTimeCurrent - counter.frameTimeLast))




######################## GLOBAL VARIABLES ##############################
#counter = [counter()]
channelOrderDefault = ["Red","Green","Blue","White"]

devices = [
    ledSegment("WS2812","LED Ring",1,board.A1, None, 0, 9, neopixel.GRB, False),
    ledSegment("WS2812","LED Ring",1,board.NEOPIXEL, None, 0, 9, neopixel.GRB, False)
]
userInputs = [None]
activeDevices =  devices # change to only include some of the devices | [devices[0],devices[1]]

deviceMaster = activeDevices[0]
randomSeed = random.randrange(0,2048)


######################## MAIN CODE ##############################
startup()
while True:
    #checkLoop(userInputs)
    drawLoop(activeDevices)
    showLoop(activeDevices)
    #print("test")
    
