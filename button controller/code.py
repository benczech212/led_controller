##  LED Controller Project
##  HID button controller



import board
import adafruit_trellism4
import neopixel
import adafruit_ws2801
import random
import time
import math
import busio
import effects
import printHelper 


trellis = adafruit_trellism4.TrellisM4Express()
UIbuttons = []
UIpanels = []
buttonColorDefaults = {"menu":96,"brightness":0,"color":0,"channel":0,"cursorArrow":64,"cursorArrowAlt":90,"cursorButton":32}
channelOrderDefault = ["G","R","B"]
debugLevel = 1
debugLevelNames = ["None", "Basic", "Most", "All"]
debugLevelName = debugLevelNames[debugLevel]
print("Starting with Debug level {} {}".format(debugLevel,debugLevelName))

def rgbINT2FLOAT(colorInt):
    #colorInt = [colorInt[0],colorInt[1],colorInt[2]]
    colorFloat = [0,0,0]
    for channel in range(3):
        colorFloat[channel] = float(colorInt[channel] / 255)
    return colorFloat

def rgbFLOAT2INT(colorFloat):
    #colorFloat = [colorFloat[0],colorFloat[1],colorFloat[2]]
    colorInt = [0,0,0]
    for channel in range(3):
        colorInt[channel] = int(colorFloat[channel]*255)
    return colorInt

def list2uint(inputList):
    try:    
        a0 = inputList[2]
        a1 = inputList[1]
        a2 = inputList[0]
    except: print("Error with list2uint")
    output = (a0,a1,a2)
    #print(output)
    return output

def find_nearest1(array,value):
    idx,val = min(enumerate(array), key=lambda x: abs(x[1]-value))
    return idx

######################################################################
class colorHelper:
    def __init__(self):
        pass
    def random_color(self):
        return effects.wheel(random.randrange( 0, 255))

    def random_colorRandomBrightness():
        return effects.wheel(random.randrange( 0, int(255 * random.randrange(1,255))))

    def random_colorWbrightness(brightnessFloat):
        return effects.wheel(random.randrange( 0, int(255 * brightnessFloat)))

colorh = colorHelper()

class printHelper:
    def __init__(self):
        self.lineWidth = 120
        fullUnicode = True
        self.walls = ["|","/"]
        self.devider = [".","-","=","_",]
        if fullUnicode:
            self.walls = ["|","ǁ","װ","⋘","⋙","⸨","⸩"]
            self.box1 = ["˥","˩","¯","¬",]
            self.pipes = ["˦","˧","˨","˪","˫","Ͱ"]
            self.dots = ["ˬ","˯","˰","̂̂",]
            self.glifs = ["͇","̄","̅","͢"]
            self.coolChars = ["ǁ","ǂ","Ħ","©","¦","§","¤","ł","ˬ","҉","֍","֎","օ", "☢"]
            self.arrows = ["ᗑ","ᗒ","ᗓ","ᗔ","ᗕ","ᗖ","ᗗ","ᗘ","ᗙ","ᗚ","ᗛ"]
            self.symbols = ["⃑	⃒	⃓	⃔	⃕	⃖	⃗	⃘	⃙	⃚	⃛	⃜	⃝	⃞	⃟	⃠"]
            self.arrows2 = ["↑","→","↓","↔","↕","↖","↗","↘","↙","↚","↛","↜","↝","↞","↟","↠ ↱","↲","↳","↴","↵","↶","↷","↸","↹","↺","↻","↼","↽","↾","↿","⇀ ⇑","⇒","⇓","⇔","⇕","⇖","⇗","⇘","⇙","⇚","⇛","⇜","⇝","⇞","⇟","⇠ ⇱","⇲","⇳","⇴","⇵","⇶","⇷","⇸","⇹","⇺","⇻","⇼","⇽","⇾","⇿","∀"]
            self.crosses = ["⊕","⊖","⊗","⊘","⊙","⊚","⊛","⊜","⊝","⊞","⊟","⊠"]
            self.drawing = ["━","│","┃","┄","┅","┆","┇","┈","┉","┊","┋","┌","┍","┎","┏","┐ ┡","┢","┣","┤","┥","┦","┧","┨","┩","┪","┫","┬","┭","┮","┯","┰ ╁","╂","╃","╄","╅","╆","╇","╈","╉","╊","╋","╌","╍","╎","╏","═╡","╢","╣","╤","╥","╦","╧","╨","╩","╪","╫","╬","╭","╮","╯","╰ ▁","▂","▃","▄","▅","▆","▇","█","▉","▊","▋","▌","▍","▎","▏","▐ □","▢","▣","▤","▥","▦","▧","▨","▩","▪","▫","▬","▭","▮","▯","▰ ◁","◂","◃","◄","◅","◆","◇","◈","◉","◊","○","◌","◍","◎","●","◐ ◡","◢","◣","◤","◥","◦","◧","◨","◩","◪","◫","◬","◭","◮","◯","◰"]
    def printDevider(self,deviderChar):
        print(deviderChar*self.lineWidth)

    def formatRGBval(color,formatPreset,labelToggle):
        textBuffer = ""
        #displayAs = "FLOAT"
        displayAs = "INT"
        if labelToggle:
            labels = ["R:","G:","B:"]
        else:
            labels = ["","",""]
        if displayAs == "FLOAT":
            #display as FLOAT
            #color = rgbINT2FLOAT(color)
            if formatPreset == 1:
                
                textBuffer = "|{}:{:5.0%}|{}{:5.0%}|{}{:5.0%}|".format(labels[0],color[0],labels[1],color[1],labels[2],color[2])
                #textBuffer = "|{}{:5.0%}|{}{:5.0%}|{}{:5.0%}|".format(labels[0],color[0],labels[1],color[1],labels[2],color[2])
            else:
                textBuffer = "{:3.0},{:3.0},{:3.0}".format(color[0],color[1],color[2])
            return textBuffer
        else:
            #display as INT    
            if formatPreset == 1:
                textBuffer = "|{}{:4}|{}{:4}|{}{:4}|".format(labels[0],color[0],labels[1],color[1],labels[2],color[2])
            else:
                textBuffer = "{}{:3},{}{:3},{}{:3}".format(labels[0],color[0],labels[1],color[1],labels[2],color[2])
            return textBuffer
printh = printHelper()

class errorHandler:
    def __init__(self):
        pass
    def printError(message):
        print("!"*60)
        print(message)
        print("!"*60)
errorH = errorHandler()

   
class button:
    buttons = []
    buttonCount = 0
    
    def __init__(self,matrix,panel,name,position,palette,velocity):
        self.device = matrix.device
        self.matrix = matrix
        self.panel = panel
        self.name = name
        self.setPosition(position)
        self.pressed = False
        self.pressCount = 0
        self.lastPressed = []
        self.currentPress = set()
        self.visible = True
        self.pixelMap = pixelMap(self.matrix.rangeX,self.matrix.rangeY)
        #self.pixelColor = pixelColor(trellis,self,position,palette,velocity)
        self.buttonID = button.buttonCount
        self.ledPixel = ledPixel(trellis,self.buttonID)
        self.buttons.append(self)
        
        self.longPressThreshold = 5
        button.buttonCount += 1
        matrix.buttons.append(self)
        panel.buttons.append(self)
    
    def updateAllButtons(self):
        for button in self.buttons:
            button.update()

    def update(self):
        if self.visible:
            self.ledPixel.ledColor.visible = True
            self.checkIfPressed()
        else: self.ledPixel.ledColor.visible = False
        self.ledPixel.ledColor.update()

    def checkIfPressed(self):
        try:
            allPressed = set(self.device.pressed_keys)
        except:
            if debugLevel >= 1:
                message = "Error getting keys pressed"
                errorH.printError(message)
            raise
        for press in allPressed:# - self.currentPress:
            if press:
                if self.posX == press[0] and self.posY == press[1]:
                    self.onPress()
        for release in self.currentPress - allPressed:
            if release:
                if self.posX == release[0] and self.posY == release[1]:
                    self.onRelease()
        self.currentPress = allPressed
        

    def onPress(self):
        if debugLevel > 0: print("{} Down | Press Count {}".format(self.name,self.pressCount))

        self.ledPixel.ledColor.color_target = (255,255,255)
        self.ledPixel.ledColor.changeVelocity(0.1)
        self.pressCount += 1
        if self.pressCount >= self.longPressThreshold:
            self.onLongPress()
        

    def onLongPress(self):
        print("Long Press {} | {}".format(self.name, self.pos))
        
        ####################################
        # Move to ledSegment Class
        device = self.matrix.device
        baseHue = random.randrange(0,255)
        spread = 0.5
        pixelRange = len(testCanvas.array)-1

        for i,pos in enumerate(testCanvas.array):
            hue = int( (spread * 255) / pixelRange) * i
            color = effects.wheel(hue)
            print("Pos {} | i {} | hue {} | color {}".format(pos, i, hue, color))
            self.device.pixels[pos[0],pos[1]] = color
        
        pixelRange = len(externalLEDs.pixels)-1

        ####################################
        

    def onRelease(self):
        if debugLevel > 0:
            print("{} Up".format(self.name))
        self.ledPixel.ledColor.color_target = self.ledPixel.ledColor.palette[0]
        self.ledPixel.ledColor.changeVelocity(0.05)
        self.pressCount = 0
        
    def addOnPress(self,function):
        self.onPress = function

    def setPosition(self,position):
        self.pos = position
        self.posX = position[0]
        self.posY = position[1]  
        
class buttonPanel:
    buttonPanels = []
    def __init__(self,matrix,name):
        self.matrix = matrix
        self.name = name
        self.device = matrix.device
        self.visible = True
        self.buttons = []
        buttonPanel.buttonPanels.append(self)

    def update(self):
        if self.visible:
            for button in self.buttons:
                button.update()

class buttonMatrix:
    buttonMatrixes = []
    def __init__(self,device):
        self.device = device
        self.rangeX = 8
        self.rangeY = 4
        self.range = self.rangeX * self.rangeY  
        self.buttons = []
        buttonMatrix.buttonMatrixes.append(self)
    
    def update(self):
        for panel in buttonPanel.buttonPanels:
            if panel.visible:
                panel.update()

    def moveButtonPosition(self,button,newPosition):
        button.setPosition(newPosition)

class timer:
    def __init__(self):
        self.name = None
        self.reset()
        
        
    def reset(self):
        self.timeNow = 0
        self.maxTimestamps = 128
        self.timestamps = []
        self.timeTarget = 0
        self.timeStarted = 0
        self.timeRunning = 0
        self.timeLeft = 0
        self.avgCycleTime = 0
        self.cycleCount = 0
        self.cycleDeviation = 0.0
    
    def setTarget(self,target):
        self.timeTarget = target
    def setName(self,name):
        self.name = name
    def start(self, target):
        self.timeTarget = target
        self.timeStarted = time.monotonic()
        print("Started Timer at {} Duration Target {}".format(self.timeStarted, self.timeTarget))
    
    def calc(self):
        self.timeNow = time.monotonic()
        self.timeRunning = self.timeNow - self.timeStarted
        self.timeLeft = self.timeTarget - self.timeRunning

    def getRemaining(self):
        self.calc()
        return self.timeLeft
    def getRunningFor(self):
        self.calc()
        return self.timeRunning

    def cycleTick(self):
        self.timeNow = time.monotonic()
        self.timestamps.append(self.timeNow)
        if len(self.timestamps) > self.maxTimestamps:
            self.timestamps.pop(0)
        self.calc()
        self.cycleCount += 1
        self.calcAvgCycle()    
        
    def printStatus(self):
        print("Now {:6f} | Target {:6f} | Avg Cycle {:3f} | Cycle Count {:6} | Target Deviation {:2.3}".format(self.timeNow,self.timeTarget,self.avgCycleTime,self.cycleCount,self.cycleDeviation))

    def calcAvgCycle(self):
        self.durations = [0] * len(self.timestamps)
        for i in range(len(self.timestamps)-1):
            self.durations[i] = (self.timestamps[i+1] - self.timestamps[i])
        self.avgCycleTime = sum(self.durations) / len(self.durations)
        self.cycleDeviation = self.timeTarget - self.avgCycleTime
        
class counter:
    def __init__(self, maxCount):
        self.name = None
        self.reset()
        self.maxCount = maxCount
        self.timer = timer()

    def reset(self):
        self.count = 0
        self.maxCount = 0
        self.loopCount = 0

    def setMaxCount(self, value):
        self.maxCount = value
    
    def setName(self,value):
        self.name = value
    
    def tick(self):
        self.count += 1
        self.timer.cycleTick()
        if self.count > self.maxCount:
            # One Loop Completed
            self.count = 0
            self.onLoop()
    def printStatus(self):
        print("Tick Count {:4} of {:4}   | Loop Count {:4} ".format(self.count,self.maxCount,self.loopCount))
    def onLoop(self):
        self.loopCount += 1

class canvas:
    def __init__(self,posStart,posEnd):
        self.posStart = posStart
        self.posEnd = posEnd
        self.sizeX = posEnd[0] - posStart[0] + 1
        self.sizeY = posEnd[1] - posStart[1] + 1
        self.array = []

        self.resolution = self.sizeX * self.sizeY
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                self.array.append([self.posStart[0] + x,self.posStart[1] + y])

    def testArea(self):
        index = 0
        for i in self.array:
            trellis.pixels[i[0],i[1]] = effects.wheel(index * 8)
            index += 1

    def fill(self,color):
        for i in self.array:
            trellis.pixels[i[0],i[1]] = color
    def fillFromPixels(self,pixels):
        pixelsRangePercents = []
        canvasRangePercents = []
        
        for index in range(len(pixels)):
            pixelsRangePercents.append(index / len(pixels))
        for index, canvasStep in enumerate(self.array):
            canvasRangePercents.append(index / len(self.array))
        for index,i in enumerate(canvasRangePercents):
            self.array[index] = pixels[find_nearest1(pixelsRangePercents,i)]
            print()


class pixelMap:
    def __init__(self,rangeX,rangeY):
        #offset needed?
        self.rangeX = rangeX
        self.rangeY = rangeY
        self.range = rangeX * rangeY
        self.pixelMin = 0
        self.pixelMax = self.pixelMin + self.range

    def getPixelMap(self):
        pixelMap = []
        for i in range(self.range):
            pixelMap.append(self.index2pos(i))
        return pixelMap
    def index2pos(self,index):
        x = index % self.rangeX
        y = math.floor(index / self.rangeX)     
        return [x,y]
    def pos2index(self,pos):
        x = pos[0]
        y = pos[1]
        return (x + (y * x) )

trellis.pixelMap = pixelMap(8,4)
trellis.name = "onboard LEDs"

class ledColor:
    def __init__(self,ledPixel, palette, brightness, velocity):
        self.palette = palette
        self.channelCount = len(palette[0])
        self._validatePalette()
        self.changeBrightness(brightness)
        self.changeVelocity(velocity)
        self.visible = True
        self.color_current = [0,0,0]
        self.color_current_last = [0,0,0]
        self.color_target = [0,0,0]
        self.color_target_last = [0,0,0]
        self.color_next = [0,0,0]
        #self.idle = True
        self.ledPixel = ledPixel
    def update(self):
        self.calc_colorNext()
        self.color_current = self.color_next
        
    def calc_colorNext(self):
        changeType = "linear step"
        if self.visible:
            if changeType == "linear step":
                for i in range(self.channelCount):
                    step = 0
                    difference = self.color_target[i] - self.color_current[i]
                    if difference != 0:
                        if difference > self.velocityInt: # if positive Delta is max clamp to max
                            step = self.velocityInt
                        elif (difference * -1) > (self.velocityInt): # if negative Delta is max clamp to max
                            step = self.velocityInt * -1
                        else: # if less than max velocity, use difference
                            step = difference
                        self.color_next[i] = self.color_current[i] + step
                    else: # No Change
                        self.color_next[i] = self.color_target[i]
            
            self.color_current_last = self.color_current
            self.color_current = self.color_next



    def changeVisibility(self,state):
        self.visible = state
    def toggleVisibility(self):
        self.visible != self.visible
    def changeBrightness(self,newBrightness):
        self.brightness = newBrightness
        self.brightnessInt = int(newBrightness * 255)
    def changeVelocity(self,newVelocity):
        self.velocity = newVelocity
        self.velocityInt = int(newVelocity * 255)
    def changeColorTarget(self,newColor):
        self.color_target_last = self.color_target
        self.color_target = newColor
    

    def _validatePalette(self):
        validPalette = []
        for color in self.palette:
            if len(color) == self.channelCount:
                validPalette.append(color)
        self.palette = validPalette



class ledPixel:
    ledPixels = []
    def __init__(self,driver,index):
        self.driver = driver
        self.index = index
        self.pos = self.driver.pixelMap.index2pos(index)
        self.posX = self.pos[0]
        self.posY = self.pos[1]
        self.visible = True
        print("Adding Pixel to {} | i{} | pos {} |".format(driver.name,self.index,self.pos))
        self.ledColor = ledColor(self,[[0,0,0]],1.0,1.0)
        ledPixel.ledPixels.append(self)

class ledSegment:
    def __init__(self):
        pass 


class ledDriver:
    channelOrderDefault = ["Red","Green","Blue","White"]
    channelLabelsDefault = []
    for name in channelOrderDefault:
        channelLabelsDefault.append(name[0])
     
    def __init__(self,device,name,ledType,brightnessGain,dataPin, clockPin, pixelMin, pixelMax, rangeX, order, autoWrite):
        if debugLevel > 0:
            print("="*60)
            print(" ---- Adding LED Driver '{}' ----- ".format(name))
           
        try:
            self.name = name
            self.device = device
            self.ledType = ledType
            self.brightness = 1.0
            self.brightnessGain = brightnessGain
            self.dataPin = dataPin
            self.clockPin = clockPin
            self.pixelMin = pixelMin
            self.pixelMax = pixelMax
            self.pixelRange = pixelMax - pixelMin + 1
            self.rangeX = rangeX
            self.rangeY = self.pixelRange // rangeX
            self.order = order
            self.autoWrite = autoWrite
            self.visible = True
            self.counter = counter(1024)
            self.channelCount = len(order)
            self.channelNames = []
            self.channelLabels = []
            if debugLevel > 0:
                 print("Type {}".format(self.ledType))
                 print("Brightness {}".format(self.brightnessGain))
                 print("Data Pin {}".format(self.dataPin))
                 print("Clock Pin {}".format(self.clockPin))
                 print("pixelMin {}".format(self.pixelMin))
                 print("pixelMax {}".format(self.pixelMax))
                 print("pixelRange {}".format(self.pixelRange))
                 print("rangeX {}".format(self.rangeX))
                 print("rangeY {}".format(self.rangeY))
                 print("."*60)
            for channel in order:
                self.channelNames.append(ledDriver.channelOrderDefault[channel])
                self.channelNames.append(ledDriver.channelLabelsDefault[channel])
            self.pixels = self.initializePixels()
            print(self.pixels)
            self.pixelMap = pixelMap(self.rangeX,self.rangeY)
            for index in range(len(self.pixels)):
                pos = self.pixelMap.index2pos(index)
                self.ledPixel = ledPixel(self,index)
            #for index in range(self.pixelRange):
            self.clearPixels()
            self.testPixels()
            self.clearPixels()


        except OSError:
            print("Error Setting up {}".format(self.name))
            print(OSError)
            print("!"*60)
    def update(self):
        self.pixels.show()

    def initializePixels(self):
        try:
            if self.ledType == "WS2812":
                # 3 Wire NeoPixels
                try:
                    return neopixel.NeoPixel(self.dataPin, self.pixelRange, brightness=self.brightnessGain, auto_write=self.autoWrite, pixel_order=self.order)
                except:
                    pass
            elif self.ledType == "WS2801":
                # 4 Wire SPI LEDs
                try:
                    return adafruit_ws2801.WS2801(self.clockPin, self.dataPin, self.pixelRange, brightness=self.brightnessGain, auto_write=self.autoWrite)
                except:
                    pass
            elif self.ledType == "INUSE":
                try:
                    pass
                except:
                    pass
        except:
            pass
            

    def randomPixel(self):
            try: randomPixel = random.randrange(self.pixelMin, self.pixelMax)
            except: randomPixel = self.pixelMin
            return randomPixel
    def clearPixels(self):
        self.pixels.fill(0)
        self.pixels.show()
    def testPixels(self):
        if debugLevel > 0:
            print("Testing Pixels")
        colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,255)]
        colorNames = ["Red","Green","Blue","White"]
        for index, color in enumerate(colors):
            if debugLevel > 0:
                print(" --> {}".format(colorNames[index]))
            self.pixels.fill(color)
            self.update()
            time.sleep(0.25)
            self.clearPixels()
            self.update()
            time.sleep(0.25)
        loopCount = 127
        if debugLevel > 0:
            print("Testing color spectrum")
        for loop in range (loopCount):
            scale = 1.0
            stepFloat = (1 / self.pixelRange) * scale
            stepInt = int(stepFloat * 255)
            for pixelID in range(self.pixelRange):    
                hue = (stepInt * pixelID) + loop
                color = effects.wheel(hue)
                if debugLevel > 1:
                    print("loopNum {} | pixel ID {:3} | Hue {:3} | color {} ".format(loop, pixelID,hue,color))

                self.pixels[pixelID] = color
            self.pixels.show()
            if debugLevel > 1:
                print("."*60)
        if debugLevel > 1:
            print("-"*60)
    @classmethod
    def inUse(cls, pixelObject):
        pass

            
            
               

    



###################################################################

    

    
def printDebug():
        #Debug Print
        printh.printDevider("=")
        counter1.printStatus()
        counter1.timer.printStatus()
        printh.printDevider(".")


def buttonMove_NegX(button):
    button.setPosition([button.posX-1,button.posY])
def buttonMove_PosX(button):
    button.setPosition([button.posX+1,button.posY])

matrix = buttonMatrix(trellis)
buttonPanels = {
    "menu":buttonPanel(matrix,"Menu Panel"),
    "cursorX":buttonPanel(matrix,"Cursor Panel X"),
    "cursorY":buttonPanel(matrix,"Cursor Panel Y"),
    "cursor":buttonPanel(matrix,"Cursor Point Panel"),
    "colorSelect":buttonPanel(matrix,"Cursor Panel"),
    "brightness":buttonPanel(matrix,"Cursor Panel"),    }

buttons_menu = {
    "menu1":button(matrix,buttonPanels["menu"],"Menu Button 1",[5,1],[[0,255,0]],0.02),
    "menu2":button(matrix,buttonPanels["menu"],"Menu Button 2",[6,1],[[0,255,0]],0.02),
    "menu3":button(matrix,buttonPanels["menu"],"Menu Button 3",[7,1],[[0,255,0]],0.02),
   # "menu4":button(matrix,buttonPanels["menu"],"Menu Button 4",[3,0],[[0,255,0]],0.02),
   }
buttons_cursorX = {
    "X-":button(matrix,buttonPanels["cursorX"],"Cursor X-",[0,2],[[0,255,64]],0.02),
    "X+":button(matrix,buttonPanels["cursorX"],"Cursor X+",[2,2],[[0,255,64]],0.02),}
buttons_cursorY = {
    "Y+":button(matrix,buttonPanels["cursorY"],"Cursor Y+",[1,1],[[0,255,64]],0.02),
    "Y-":button(matrix,buttonPanels["cursorY"],"Cursor Y-",[1,3],[[0,255,64]],0.02),}

button_cursor = button(matrix,buttonPanels["cursor"],"Cursor",[1,2],[[255,0,64]],0.02)
counter1 = counter(255)


testCanvas = canvas([0,0],[7,0])
#testCanvas.testArea()
externalLEDs = ledDriver(None,"1M Strip","WS2812",1.0,board.SCL,None,0,29,1,neopixel.GRB,False)
    #externalLEDs = ledDriver(None,"Christmas Lights","WS2801",1.0,board.SDA,board.SCL,0,23,1,neopixel.GRB,False)
    
#onboardLEDs = ledDriver(trellis,"LED Buttons","INUSE",1.0,board.NEOPIXEL,None,0,31,8,neopixel.GRB,False)



#buttonMove_NegX(button_cursor)

#buttons_cursorX["X-"].onPress(buttons_cursorX["X-"].setPosition([buttons_cursorX["X-"].posX-1,buttons_cursorX["X-"].posY]))




#allButtons = []#None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,]
#i = 0
#for x in range(8):
    #for y in range(4):
        #allButtons.append(button(trellis,"button " + str(i),[x,y],[effects.wheel(i*8)],0.04))
        #thisButton = allButtons[len(allButtons)-1]
        #thisButton.addOnPress(testOnPress(thisButton))
        #i += 1



def mainLoop():
    global counter1, timer1
    
    matrix.update()
    #TODO: Move .show() to ledDriver Update
    trellis.pixels.show()
    externalLEDs.update()
    ##################################
    counter1.timer.setTarget(0.1)
    counter1.tick()
    if debugLevel >= 2:
        printDebug()

        





while True:    
    for loopCycle in range(128):
        mainLoop()
        externalLEDs.pixels.fill((255,255,255))
        pixelBuffer = externalLEDs.pixels
        testCanvas.fillFromPixels(pixelBuffer)
        #print(clock.timestamps)
        
        