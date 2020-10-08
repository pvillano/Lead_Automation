import cv2
import mk2Camera
from GantryControl import Gantry

# Tray settings
# xStart = 75
# yStart = 145
# Filter settings
xStart = 85
yStart = 333
xCenter = 240
yCenter = 320
pixelsToMM = 100.0 / 9
TRAYS = 0
FILTERS = 1
SOIL = 2


def tryToFindLabel(cap, t):
    i = 0
    label = ""
    while i < t:
        ret, frame = cap.read()
        processed, label = mk2Camera.processFrame(frame)
        if "" != label:
            print("Found label")
            i = t
        cv2.imshow("processView", processed)
        cv2.waitKey(1)
        i += 1
    return label


def tryToFindTape(number, x, y, cap):
    i = 0
    while i < number:
        ret, frame = cap.read()
        processed, center = mk2Camera.processColor(frame)
        # cv2.imshow('processView',processed)
        # cv2.waitKey(1)
        if center is not None:
            break
        i += 1
    if center is not None:
        xTarget = (center[1] - xCenter) / pixelsToMM
        yTarget = (center[0] - yCenter) / pixelsToMM
        return (
            str.format("%4.3f" % (x + xTarget)),
            str.format("%4.3f" % (y + yTarget)),
        )
    else:
        print("Could not find tape")
        return None


def readLabels(number, x, y, gant, cap):
    # Tray Settings
    # yOffset = 65.3
    # xOffset = 25
    # Filter Settings
    yOffset = 40
    xOffset = 0
    labels = []
    positions = []
    repeat = True
    for n in range(number):
        yTarget = y + (n * yOffset)
        gant.sendTo(str.format("%4.3f" % (x)), str.format("%4.3f" % (yTarget)))
        labels.append(tryToFindLabel(cap, 0))
        cX = x - (1 * xOffset)
        gant.sendTo(str.format("%4.3f" % (cX)), str.format("%4.3f" % (yTarget)))
        center = tryToFindTape(20, cX, yTarget, cap)
        if center is None and repeat:
            cX = x - (1 * xOffset)
            gant.sendTo(str.format("%4.3f" % (cX)), str.format("%4.3f" % (yTarget)))
            center = tryToFindTape(20, cX, yTarget, cap)
            if center is None:
                cX = x - (1 * xOffset)
                gant.sendTo(str.format("%4.3f" % (cX)), str.format("%4.3f" % (yTarget)))
                center = tryToFindTape(20, cX, yTarget, cap)
        positions.append(center)
    return labels, positions


def singlePass(number, gant):
    cap = cv2.VideoCapture(1)
    labels, positions = readLabels(number, 62.5, 205, gant, cap)
    cap.release()
    return (labels, positions)


if __name__ == "__main__":
    gant = Gantry()
    labels, positions = singlePass(1, gant)
    print(labels)
    print(positions)
    gant.sendTo(str(0), str(0))
    gant.close()
