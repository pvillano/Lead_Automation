import numpy as np


class Mode:
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
        self.zStart = -30
        self.zEnd = -58
        self.c1 = np.array([0, 170, 205])
        self.c2 = np.array([70, 255, 255])
        self.tapeMin = 100
        self.tapeMax = 250
        self.findLabels = True

    def getColorLimits(self):
        return (self.c1, self.c2, self.tapeMin, self.tapeMax)

    def getAdvanceOffset(self):
        return (self.xAdvance, self.yAdvance)

    def getXRFOffset(self):
        return (self.xXRFOffset, self.yXRFOffset, self.zXRFOffset)

    def getTraySettings(self):
        return (self.xStart, self.yStart, self.maxTraySize)

    def advance(self, x, y):
        return x, y

    def correctPositions(self, positions):
        ret = []
        for position in positions:
            if position is not None:
                p0 = max(float(position[0]) + self.xXRFOffset, 0)
                # p0 = min(p0, 58)
                p1 = float(position[1]) + self.yXRFOffset
                ret.append([str.format("%4.3f" % (p0)), str.format("%4.3f" % (p1))])
            else:
                return None
        return ret


class TrayMode(Mode):
    def __init__(self):
        super(TrayMode, self).__init__()
        self.xStart = 5
        self.yStart = 310
        self.maxTraySize = 8
        self.numberTrayRows = 1
        self.xXRFOffset = 0  # -3
        self.yXRFOffset = -41  # -48
        self.xAdvance = 25
        self.yAdvance = 450.0 / 7.0
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
        self.xXRFOffset = 0  # -3
        self.yXRFOffset = -36  # -48
        self.xAdvance = 0
        self.yAdvance = 40
        self.zStart = -50
        self.zEnd = -72
        self.c1 = np.array([0, 0, 0])
        self.c2 = np.array([255, 255, 40])
        self.tapeMin = 170
        self.tapeMax = 230
        # self.findLabels = False

    def advance(self, x, y):
        if x > 60:
            x = self.xStart
            y = y + 36.25
        else:
            x = x + 31
            y = y
        return (x, y)

    def correctPositions(self, positions):
        ret = []
        for position in positions:
            if position is not None:
                p0 = max(float(position[0]) + self.xXRFOffset, 0)
                p1 = float(position[1]) + self.yXRFOffset
                ret.append([str.format("%4.3f" % (p0)), str.format("%4.3f" % (p1))])
            else:
                return None
        return ret


def getMode(modeNumber):
    if modeNumber == 0:
        return TrayMode()
    if modeNumber == 1:
        return FilterMode()
    else:
        return None
