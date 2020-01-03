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
class button:
    def __init__(self, name, position, device, color):
        defaultColor = (128,128,128)
        defaultPressedColor = (255,255,255)
        if color == None:
            for index, groupName in enumerate(buttonColorDefaults):
                if str(groupName) == str(group):
                    color = effects.wheel(buttonColorDefaults[groupName])
                else:  color = defaultColor
            
        self.name = name
        self.group = group
        self.position = position
        self.posX = self.position[0]
        self.posY = self.position[1]
        self.pressed = False
        self.defaultColor = color
        self.colorLast = color
        self.currentColor = color
        self.colorPressed = defaultPressedColor
        self.lit = True
        self.shown = False
        self.device = device
        UIbuttons.append(self)
        
    def update(self):
        for button in UIbuttons:
            if button.shown:
                if button.lit:
                    if button.pressed:
                        button.device.pixels[button.posX,button.posY] = button.colorPressed
                    else:
                        button.device.pixels[button.posX,button.posY] = button.currentColor
                else:
                    button.device.pixels[button.posX,button.posY] = 0
        trellis.pixels.show()

    def changeColor(self,color):
        self.currentColor = color

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

        
    def setUpColoredButtons(self,buttons):
        for index, button in enumerate(buttons):
            hue = int((index / len(buttons)) * 255)
            button.color = effects.wheel(hue)
            button.name = "color " + str(index)
    
######################################################################
class buttonPanel:
    def __init__(self,name,buttons):
        self.name = name
        self.shown = False
        self.buttons = []
        self.buttonMatrix = buttonMatrix
        UIpanels.append(self)
        
    
    def addToPanel(self,button):
        self.buttons.append(button)
        if self.shown:
            self.showOn()
        else: self.showOff()

    def update(self):
        if self.shown:
            for button in self.buttons:
                button.update()

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


######################################################################
class buttonMatrix:
    def __init__(self, device, name, xmin, ymin, xmax, ymax):
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

        
    def updatePressed(self):
        try:
            self.keysPressed = set(self.device.pressed_keys)
        except:
            print("Error Getting Key Presses")
    
    def checkForInputs(self):
        self.updatePressed()
        #Only Most Recent Press
        for press in self.keysPressed - self.currentPress:
            self.lastPressed = press
            onAnyPress(press)
                
        
        for release in self.currentPress - self.keysPressed:
            if release:
                onAnyRelease(release)
        self.currentPress = self.keysPressed

    
        

    def index2xy(self,pixelIndex):
        x = pixelIndex % self.xrange
        y = math.floor(pixelIndex / self.xrange)
        return [x,y]
    def xy2index(self, coords):
        x = coords[0]
        y = coords[1]
        return (y * self.xrange) + x



matrix = buttonMatrix(trellis,"neotrellis",0,0,7,3,)
brightnessButtons = [
    button(('Brightness Min'),'brightness',(4,0),trellis,(0,0,0)),
    button(('Brightness Minus'),'brightness',(5,0),trellis,(32,32,32)),
    button(('Brightness Plus'),'brightness',(6,0),trellis,(192,192,192)),
    button(('Brightness Max'),'brightness',(7,0),trellis,(255,255,255)),
    ]
colorButtons = [
    button(('Colored Button'),'color',(5,1),trellis,None),
    button(('Colored Button'),'color',(6,1),trellis,None),
    button(('Colored Button'),'color',(7,1),trellis,None),
    button(('Colored Button'),'color',(5,2),trellis,None),
    button(('Colored Button'),'color',(6,2),trellis,None),
    button(('Colored Button'),'color',(7,2),trellis,None),
    button(('Colored Button'),'color',(5,3),trellis,None),
    button(('Colored Button'),'color',(6,3),trellis,None),
    button(('Colored Button'),'color',(7,3),trellis,None),
    ]
menuButtons = [
    button(('menu 1'),'menu',(0,0),trellis,(194,128,0)),
    button(('menu 2'),'menu',(1,0),trellis,(194,194,0)),
    button(('menu 3'),'menu',(2,0),trellis,(194,194,0)),
    button(('menu 4'),'menu',(3,0),trellis,(194,194,0)),
    ]
color1 = effects.wheel(10)
color2 = effects.wheel(40)
color3 = effects.wheel(80)
cursorButtons = [
    button(('Cursor UL'),'cursorArrowAlt',(0,1),trellis,color1),
    button(('Cursor CL'),'cursorArrow',(0,2),trellis,color2),
    button(('Cursor DL'),'cursorArrowAlt',(0,3),trellis,color1),
    button(('Cursor UC'),'cursorArrow',(1,1),trellis,color2),
    button(('Cursor DC'),'cursorArrow',(1,3),trellis,color2),
    button(('Cursor UR'),'cursorArrowAlt',(2,1),trellis,color1),
    button(('Cursor CR'),'cursorArrow',(2,2),trellis,color2),
    button(('Cursor DR'),'cursorArrowAlt',(2,3),trellis,color1),
    button(('Cursor CC'),'cursorCenter',(1,2),trellis,color3),
]
channelButtons = [
    button(('R Channel'),'channel',(3,1),trellis,(255,0,0)),
    button(('G Channel'),'channel',(3,2),trellis,(0,255,0)),
    button(('B Channel'),'channel',(3,3),trellis,(0,0,255)),

]
colorButtons[0].setUpColoredButtons(colorButtons)



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
colorPanel = buttonPanel("colorPanel",colorButtons)
brightnessPanel = buttonPanel("brightnessPanel",brightnessButtons)
channelPanel = buttonPanel("channelPanel",channelButtons)
cursorPanel = buttonPanel("cursorPanel",cursorButtons)
cursorArrowPanel = buttonPanel("cursorArrowPanel",None)
for button in cursorButtons:
    if button.group == "cursorArrow":
        cursorArrowPanel.addToPanel(button)
cursorArrowAltPanel = buttonPanel("cursorArrowAltPanel",None)
for button in cursorButtons:
    if button.group == "cursorArrowAlt":
        cursorArrowAltPanel.addToPanel(button)
cursorButtonPanel = buttonPanel("cursorButton",None)
for button in cursorButtons:
    if button.group == "cursorButton":
        cursorButtonPanel.addToPanel(button)

menuPanel = buttonPanel("menuPanel",buttonMatrix)

colorPanel.showOff()    
brightnessPanel.showOff()
channelPanel.showOff()
for panel in UIpanels:
    print(panel.name,panel.shown)


while True:
    
    
    

    
