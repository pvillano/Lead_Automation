import cv2
import mk2Camera
from GantryControl import Gantry
import ModeSettings

# Settings for how to interpret camera data.
xCenter = 240
yCenter = 320
pixelsToMM = 100.0 / 9
TRAYS = 0
FILTERS = 1

# Interface between programs and low level robot controls. Other programs tell
# the robot what to do, this controls the broad strokes of what's done, while
# the Gantry controls how it's actually done on hardware.
class robotControl:
    def __init__(self, mode=ModeSettings.TrayMode()):
        self.gant = Gantry()
        self.cap = cv2.VideoCapture(1)
        self.setMode(mode)
        # Hardware specific, width and length of the track.
        self.xMin = 0
        self.xMax = 85
        self.yMin = 0
        self.yMax = 780  # length of the gantry

    # Cludge for loading the settings for the current mode.
    def setMode(self, mode=ModeSettings.TrayMode()):
        self.mode = mode
        (self.xStart, self.yStart, self.maxTraySize) = self.mode.getTraySettings()
        (self.xAdvance, self.yAdvance) = self.mode.getAdvanceOffset()
        (self.c1, self.c2, self.s1, self.s2) = self.mode.getColorLimits()

    def home(self):
        self.gant.home()

    # Single basic reading. Finds label and target, moves to the next sample.
    def capture(self, scan_for_label=True):
        self.samples += 1
        # print(self.x, self.y)
        l, p = self.readLabels(
            self.x,
            self.y,
            self.gant,
            self.cap,
            self.xAdvance,
            self.yAdvance,
            self.c1,
            self.c2,
            self.s1,
            self.s2,
            self.mode.findLabels and scan_for_label,
        )
        self.advance()
        if self.samples >= self.maxTraySize:
            self.setToStart()
        return l, p

    # Collects the data.
    # TODO: clean up.
    def readLabels(
        self,
        x,
        y,
        gant,
        cap,
        xOffset,
        yOffset,
        color1,
        color2,
        s1,
        s2,
        findLabels=True,
    ):
        labels = []
        positions = []
        repeat = True
        print("Finding labels? ", findLabels)
        # Try to find label. If nothing is found, search the nearby area.
        yTarget = y + yOffset
        gant.sendTo(
            f"{x:4.3f}",
            f"{yTarget:4.3f}",
            f"{self.mode.zStart:4.3f}",
        )
        label = ""
        if findLabels:
            label = tryToFindLabel(gant, cap, 3, x, yTarget)
            if "" == label:
                # wiggle around to try to find label
                label = tryToFindLabel(gant, cap, 3, x, yTarget - 5)
            if "" == label:
                label = tryToFindLabel(gant, cap, 3, x, yTarget + 5)
            if "" == label:
                gant.setZ(self.mode.zStart - 10)
                label = tryToFindLabel(gant, cap, 3, x, yTarget)
            if "" == label:
                label = tryToFindLabel(gant, cap, 3, x, yTarget - 5)
            if "" == label:
                label = tryToFindLabel(gant, cap, 3, x, yTarget + 5)
        gant.setZ(self.mode.zStart)
        labels.append(label)
        if findLabels and "" == label:
            return labels, [None]
        center_x = x + xOffset
        # Try to find the target. If nothing is found, search along the x-axis.
        gant.sendTo(f"{center_x:4.3f}", f"{yTarget:4.3f}")
        # black sample or colored sample marker
        center = tryToFindTape(20, center_x, yTarget, cap, color1, color2, s1, s2)
        if center is None and repeat:
            center_x = x + (2 * xOffset)
            gant.sendTo(f"{center_x:4.3f}", f"{yTarget:4.3f}")
            center = tryToFindTape(20, center_x, yTarget, cap, color1, color2, s1, s2)
            if center is None:
                center_x = x + (3 * xOffset)
                gant.sendTo(f"{center_x:4.3f}", f"{yTarget:4.3f}")
                center = tryToFindTape(
                    20, center_x, yTarget, cap, color1, color2, s1, s2
                )
        positions.append(center)
        if center is None:
            print("Missed tape")
        return labels, positions

    # Move to the next sample.
    def advance(self):
        (self.x, self.y) = self.mode.advance(self.x, self.y)

    def lowerTo(self, z):
        self.gant.lowerTo(str(z))

    def setHeight(self, z):
        self.gant.setZ(str(z))

    def sendTo(self, x, y, z=None):
        x = float(x)
        y = float(y)
        if x < self.xMin:
            x = self.xMin
        elif x > self.xMax:
            x = self.xMax
        if y < self.yMin:
            y = self.yMin
        elif y > self.yMax:
            y = self.yMax
        self.gant.sendTo(str(x), str(y), z)

    def checkMoving(self):
        return self.gant.checkMoving()

    def setToStart(self):
        self.x = self.xStart
        self.y = self.yStart
        self.samples = 0

    def close(self):
        self.cap.release()


# Depreciated.
def tryToFindLabel(gant, cap, t, x, y):
    i = 0
    gant.sendTo(f"{x:4.3f}", f"{y:4.3f}")
    label = ""
    while i < t:
        label = singleLabelTry(cap, 3)
        if "" != label:
            i = t
        else:
            x += 5
            gant.sendTo(f"{x:4.3f}", f"{y:4.3f}")
        i += 1
    if "" == label:
        print("Missed label")
    return label


# Depreciated.
def singleLabelTry(cap, t):
    i = 0
    label = ""
    while i < t:
        ret, frame = cap.read()
        processed, label = mk2Camera.processFrame(frame)
        if "" != label:
            print("Found label " + label)
            i = t
        cv2.imshow("processView", processed)
        cv2.waitKey(1)
        i += 1
    return label


# Depreciated.
def tryToFindTape(number, x, y, cap, color1, color2, s1, s2):
    i = 0
    while i < number:
        for j in range(1):
            ret, frame = cap.read()
        processed, center = mk2Camera.processDirt(frame)
        # processed, center = mk2Camera.processColor(frame, color1, color2, s1, s2)
        if center is not None:
            break
        i += 1
    cv2.imshow("processView", processed)
    cv2.waitKey(1)
    # cv2.destroyAllWindows()
    if center is not None:
        xTarget = (center[1] - xCenter) / pixelsToMM
        yTarget = (center[0] - yCenter) / pixelsToMM
        return (
            f"{x + xTarget:4.3f}",
            f"{y + yTarget:4.3f}",
        )
    else:
        # print("Could not find tape")
        return None


if __name__ == "__main__":
    r = robotControl(mode=FILTERS)
    r.setToStart()
    for i in range(4):
        l, p = r.capture()
        print(p)
    r.close()
