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
        self.c1 = np.array([0,170,125])
        self.c2 = np.array([70,255,255])
        self.tapeMin = 150
        self.tapeMax = 250

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
        self.yStart = 310
        self.maxTraySize = 8
        self.numberTrayRows = 1
        self.xXRFOffset = -3
        self.yXRFOffset = -48
        self.xAdvance = 25
        self.yAdvance = 65.3
        self.tapeMin = 90
        self.tapeMax = 200

    def advance(self, x, y):
        y = y + self.yAdvance
        return (x, y)

def getMode(modeNumber):
    if modeNumber == 0:
        return TrayMode()
    else:
        return None
