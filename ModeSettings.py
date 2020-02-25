import numpy as np

class Mode():
    def __init__(self):
        self.xStart = 0
        self.yStart = 0
        self.maxTraySize = 0
        self.numberTrayRows = 0
        self.xXRFOffset = 27
        self.yXRFOffset = 30
        self.zXRFOffset = 0
        self.xAdvance = 0
        self.yAdvance = 0
        self.c1 = np.array([0,170,205])
        self.c2 = np.array([70,255,255])
        self.tapeMin = 100
        self.tapeMax = 250
        self.findLabels = True

    def getColorLimits(self):
        return  (self.c1, self.c2, self.tapeMin, self.tapeMax)

    def getAdvanceOffset(self):
        return (self.xAdvance, self.yAdvance)

    def getXRFOffset(self):
        return (self.xXRFOffset, self.yXRFOffset, self.zXRFOffset)

    def getTraySettings(self):
        return (self.xStart, self.yStart, self.maxTraySize)

    def advance(self, x, y):
        return x, y

class TrayMode(Mode):
    def __init__(self):
        super(TrayMode, self).__init__()
        self.xStart = 0
        self.yStart = 300
        self.maxTraySize = 8
        self.numberTrayRows = 1
        self.xXRFOffset = 0 #-3
        self.yXRFOffset = -41 #-48
        self.xAdvance = 25
        self.yAdvance = 65.3
        self.tapeMin = 110
        self.tapeMax = 350

    def advance(self, x, y):
        y = y + self.yAdvance
        return (x, y)
    
class FilterMode(Mode):
    def __init__(self):
        super(FilterMode, self).__init__()
        self.xStart = 0
        self.yStart = 380
        self.maxTraySize = 30
        self.numberTrayRows = 3
        self.xXRFOffset = 0 #-3
        self.yXRFOffset = -41 #-48
        self.xAdvance = 0
        self.yAdvance = 40
        self.c1 = np.array([0,0,0])
        self.c2 = np.array([255,255,55])
        self.tapeMin = 200
        self.tapeMax = 350
        self.findLabels = False

    def advance(self, x, y):
        if x > 60:
            x = self.xStart
            y = y+36.25
        else:
            x = x+31
            y = y
        return (x, y)

def getMode(modeNumber):
    if modeNumber == 0:
        return TrayMode()
    if modeNumber == 1:
        return FilterMode()
    else:
        return None
