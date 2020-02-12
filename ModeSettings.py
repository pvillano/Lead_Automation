class Mode():
    def __init__(self):
        self.xStart = 0
        self.yStart = 0
        self.maxTraySize = 0
        self.numberTrayRows = 0
        self.xXRFOffset = 27
        self.yXRFOffset = 30
        self.zXRFOffset = 0

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
        self.yStart = 330
        self.maxTraySize = 8
        self.numberTrayRows = 1

    def advance(self, x, y):
        y = y + 65.3
        return (x, y)

def getMode(modeNumber):
    if modeNumber == 0:
        return TrayMode()
    else:
        return None
