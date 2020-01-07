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
        