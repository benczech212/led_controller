##  LED Controller Project
##  HID button controller


import time
import adafruit_trellism4
import neopixel
import random
import math
import effects
import printHelper 




trellis = adafruit_trellism4.TrellisM4Express()
UIbuttons = []
UIpanels = []
buttonColorDefaults = {"menu":96,"brightness":0,"color":0,"channel":0,"cursorArrow":64,"cursorArrowAlt":90,"cursorButton":32}
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


######################################################################
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



######################################################################
class buttonColor:
    def __init__(self, shownColor,notShownColor,selectedColor,highlightedColor,velocity):
        
        self.shownColor = shownColor
        self.notShownColor = notShownColor
        self.selectedColor = selectedColor
        self.highlightedColor = highlightedColor
        self.last = [0,0,0]
        self.current = [0,0,0]
        self.target = [0,0,0]
        self.delta = [0,0,0]
        self.nextStep = [0,0,0]
        self.velocity = velocity
        self.setColorTarget(shownColor)
    
    def setColorTarget(self,colorTarget):
        self.target = colorTarget
        self.update()

    def update(self):
        for i in range(len(self.current)):
            self.delta[i] = (self.target[i]-self.current[i])
            
        for i in range(len(self.current)):
            if abs(self.target[i] - self.current[i]) < self.velocity:
                # Less than 1 step away 
                self.nextStep[i] = self.target[i]
            elif (self.target[i] > self.current[i]):
                # Fade Up 1 Velocity
                self.nextStep[i] = self.current[i] + self.velocity
            else:
                # Fade Down 1 Velocity
                self.nextStep[i] = self.current[i] - self.velocity




class button:
    def __init__(self, device, name, position):
        self.device = device
        self.name = name
        self.pos = position
        self.posX = position[0]
        self.posY = position[1]
        self.pressed = False
        self.lit = True
        self.shown = True
        self.color = buttonColor((255,255,0),(0,0,0),(32,32,32),(128,0,128),8)
        UIbuttons.append(self)
        
    def update(self,buttonMatrix):
        for button in UIbuttons:
            if button.shown:
                button.color.update()
                if button.pressed:
                    button.color.target = button.color.selectedColor
                else:
                    button.color.target = button.color.shownColor
            else:
                button.color.target = button.color.notShownColor
        trellis.pixels.show()

    def changeColor(self,color):
        self.color.current = color

    def changeColorBack(self):
        temp = self.currentColor
        self.currentColor = self.colorLast
        self.colorLast = temp

    def findMaxLengthName(self):
        result = {"name":"","length":0 }
        for index, button in enumerate(UIbuttons):
            if len(str(button.name)) > result["name"]:
                result["name"] = str(button.name)
                result["length"] = len(str(button.name))
        return result
        
    def pixel(self):
        return self.device.pixels[self.posX,self.posY]

    def showToggle(self):
        self.shown = not(self.shown)

    def showOn(self):
        self.shown = True

    def showOff(self):
        self.shown = False
        
    def onPress(self):
        if self.shown:
            print("Button {} Down".format(self.name))    
            self.color.target = self.color.selectedColor
            self.pressed = True

        
    def setUpColoredButtons(self,buttons):
        for index, button in enumerate(buttons):
            hue = int((index / len(buttons)) * 255)
            button.color = effects.wheel(hue)
            button.name = "color " + str(index)
    
######################################################################
class buttonPanel:
    def __init__(self,name,buttons):
        self.name = name
        self.shown = True
        self.buttons = []
        self.buttonMatrix = buttonMatrix
        UIpanels.append(self)
        
    
    def addToPanel(self,button):
        self.buttons.append(button)
        if self.shown:
            self.showOn()
        else: self.showOff()

    def update(self):
        pass

    def showOff(self):
        self.shown = False
        for button in self.buttons:
            button.shown = False
            button.currentColor = 0
    def showOn(self):
        self.shown = True
        for button in self.buttons:
            button.shown = True
            button.currentColor = button.color
    def showToggle(self):
        self.shown != self.shown
        if self.shown:
            self.showOn()
        else: self.showOff()
    def onPress(self):
        pass


######################################################################
class buttonMatrix:
    def __init__(self, device, name, xmin, ymin, xmax, ymax, buttonPannels):
        self.device = device
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
        self.buttonPanels = buttonPannels
        

    def update(self):
        self.checkForInputs()
        self.updatePanels()
        self.updateButtons()
                
    def updatePanels(self):
        for panel in self.buttonPanels:
            panel.update()

    def updateButtons(self):
        for button in UIbuttons:
            button.update(self)

    def checkForInputs(self):
        try:
            self.keysPressed = set(self.device.pressed_keys)
        except:
            print("Error Getting Key Presses")
            raise
        #Only Most Recent Press
        for press in self.keysPressed - self.currentPress:
            self.lastPressed = press
            self.onPress(press)
        for release in self.currentPress - self.keysPressed:
            if release:
                onAnyRelease(release)

    def onPress(self,press):
        for panel in UIpanels:
            if panel.shown:
                panel.onPress()
                for button in panel.buttons:
                    if button.shown:
                        button.onPress()

        

    def index2xy(self,pixelIndex):
        x = pixelIndex % self.xrange
        y = math.floor(pixelIndex / self.xrange)
        return [x,y]
    def xy2index(self, coords):
        x = coords[0]
        y = coords[1]
        return (y * self.xrange) + x


brightnessButtons = [
    button(trellis,'Brightness Min',(4,0)),
    button(trellis,'Brightness Min',(5,0)),
    #button(trellis,'Brightness Min',(6,0)),
    #button(trellis,'Brightness Min',(7,0)),
]
brightnessPanel = buttonPanel("brightness",brightnessButtons)
matrix = buttonMatrix(trellis,"neotrellis",0,0,7,3,[brightnessPanel])

    #button(trellis,('Brightness Minus'),(5,0),buttonColor(,
    #button(trellis,('Brightness Plus'),(6,0),buttonColor((255,255,0),(0,0,0),(196,196,196),(128,0,128),8)),
    #button(trellis,('Brightness Max'),(7,0),buttonColor((255,255,0),(0,0,0),(255,255,255),(128,0,128),8)),
    




def onTestButtonPress():
    colorPanel.showToggle()


def onAnyPress(press):
    try:
        print("Down:", press)
        for uiButton in UIbuttons:
            if uiButton.position == press:
                if uiButton.shown:
                    print("UI Button Down:{} {} {}".format(uiButton.name, press, uiButton.color))
    except:
        print("Error running onAnyPress",__name__)




def onAnyRelease(release):
    print("Released:", release)
    for uiButton in UIbuttons:
        if uiButton.position == release:
            if uiButton.shown:
                print("UI Button Up:{} {}".format(uiButton.name, release))

    
def updateButtonUI():
    for button in UIbuttons:
        if button.shown:
            button.update()

def enableAllButtons(delayBetweenButtons):
    printh.printDevider("=")
    print("- | {:4} | {:20} | {:9}| {:12} |".format("ID","Name","(X, Y)","Color"))
    printh.printDevider("-")
    for index, button in enumerate(UIbuttons):
        print("- | #{:3} | {:20} | {:8} {}".format(index,str(button.name),str(button.position),printHelper.formatRGBval(button.color,1,True)))
        button.device.pixels[button.posX,button.posY] = button.color    
        if delayBetweenButtons != 0:
            button.device.pixels.show()
            time.sleep(delayBetweenButtons)
    printh.printDevider("=")
    button.device.pixels.show()


def findMaxLengthButtonName():
    maxLength = 0
    for button in UIbuttons:
        if len(button.name) > maxLength:
            maxLength = len(button.name)
    return maxLength    



def mainLoop():
    matrix.checkForInputs()
    updateButtonUI()
    trellis.pixels.show()

#for all buttons
for button in UIbuttons:
    button.showOn()
    print(button.shown)


#for colorButtons
#colorPanel = buttonPanel("colorPanel",colorButtons)
#brightnessPanel = buttonPanel("brightnessPanel",brightnessButtons)
#channelPanel = buttonPanel("channelPanel",channelButtons)
#cursorPanel = buttonPanel("cursorPanel",cursorButtons)
#cursorArrowPanel = buttonPanel("cursorArrowPanel",None)
#menuPanel = buttonPanel("menuPanel",menuButtons)

#colorPanel.showOff()    
#brightnessPanel.showOff()
#channelPanel.showOff()
#for panel in UIpanels:
    #print(panel.name,panel.shown)


while True:
    matrix.update()        
    
        
    
    

    
