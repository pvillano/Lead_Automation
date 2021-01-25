import numpy as np
import cv2
import pytesseract
import re

# Purely for review/debug. Takes 2 or 4 images, returns a composite for easy viewing
def quadView(v1, v2, v3=None, v4=None):
    v1 = cv2.resize(v1, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    v2 = cv2.resize(v2, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    finalView = np.hstack((v1, v2))
    if v3 is not None:
        v3 = cv2.resize(v3, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        v4 = cv2.resize(v4, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        botView = np.hstack((v3, v4))
        finalView = np.vstack((finalView, botView))
    return finalView


# Mainly for display. Automatically converts gray to rgb, ret resized to match img
def standardize(img, ret):
    if len(ret.shape) < 3:
        ret = cv2.cvtColor(ret, cv2.COLOR_GRAY2RGB)
    ret = cv2.resize(ret, dsize=(img.shape[1], img.shape[0]))
    return ret


# Preliminary code for finding the dirt on a colored background
# do not trust *shrug*
def processDirt(img):
    threshold = 120
    threshold2 = 0
    ret = img.copy()
    # Denoise
    ret = cv2.bilateralFilter(ret, 9, 225, 175)
    color1 = np.array([0, 0, 0])
    # HSV- teal, any saturation, low value
    color2 = np.array([75, 255, 120])
    # Remove the teal background
    hsvImg = cv2.cvtColor(ret, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsvImg, color1, color2)
    ret = cv2.bitwise_and(ret, ret, mask=mask)
    # Make binary
    ret[ret > 0] = 255
    ret2 = ret.copy()
    sCKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    cKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30))
    # Dilate and errode to denoise
    ret = cv2.dilate(ret, sCKernel)
    ret = cv2.erode(ret, cKernel)
    # Remove borders to reduce false positives
    ret[-102:, :, :] = 0
    ret[:, -102:, :] = 0
    ret[0:101, :, :] = 0
    ret[:, 0:101, :] = 0
    # Highlight largest areas of white
    dist = cv2.distanceTransform(ret[:, :, 0], cv2.DIST_L2, 3)
    # Troubleshooting
    _, maxVal, _, maxLoc = cv2.minMaxLoc(dist)
    # Normalize for display
    dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
    # Find target based on distance from black
    _, maxVal, _, maxLoc = cv2.minMaxLoc(dist)
    fin = img.copy()
    if maxVal > 0.9:
        cv2.circle(fin, maxLoc, 90, (0, 255, 0), 2)
    else:
        maxLoc = None
    return quadView(fin, ret), maxLoc


# Wrapper to find arbitrary HSV traits. Defaults to orange tape settings.
# lower and upper bounds in hsv, default is orange tape
# returns part of image which falls in this color range
def findColor(img, color1=np.array([0, 170, 125]), color2=np.array([70, 255, 255])):
    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsvImg, color1, color2)
    return cv2.bitwise_and(img, img, mask=mask)


# Code for finding color regions. Used with default settings to find black filters, used with alternate settings to
# find orange tape in kits.
#trying to find tape or water filter
def processColor(
    img,
    color1=np.array([0, 0, 0]),
    color2=np.array([255, 255, 55]),
    minSize=150, # splotch size
    maxSize=250,
):
    orange = findColor(img, color1, color2)
    orange = cv2.cvtColor(orange, cv2.COLOR_RGB2GRAY)
    center = idTape(orange, minSize, maxSize)
    orange = standardize(img, orange)
    out = img.copy()
    if center is not None:
        cv2.circle(img, (center[0], center[1]), 120, (0, 255, 0), 2)
    return quadView(img, orange), center


# Wrapper to run a full process
#trying to find sticker
def processFrame(img):
    ret, process, angled, match, text, label = findSticker(img)
    ret = standardize(img, ret)
    process = standardize(img, process)
    angled = standardize(img, angled)
    return quadView(img, ret, process, angled), label


def showImage(img):
    cv2.imshow("Display", img)
    cv2.waitKey()


# Regex search. Currently set to find (any three alphabetic).(any 4 alphanumeric).(any 4 alphanumeric)
# This could probably be made more specific for current (2020/03/16) tests
# If you're using multiple formats, include them in an if else loop.
def matchLabel(text):
    match = re.search("([A-Z]){3}\.([A-Z]|[0-9]){4}\.([A-Z]|[0-9]){4}", text)
    """if match:
        return match
    else:
        match = re.search('([A-Z]|[0-9]){4}\.([A-Z]|[0-9]){3}\.([A-Z]|[0-9]){2}', text)
    if match:
      return match
    else:
      match = re.search('([A-Z]){2}\.([A-Z]|[0-9]){3}\.([A-Z]|[0-9]){2}', text)
    if match:
      return match
    else:
      match = re.search('([A-Z]|[0-9]){3}\.([A-Z]|[0-9]){4}\.([A-Z]|[0-9]){2}', text)"""
    return match


# Pytesseract wrapper. Takes a gray image, outputs found text, whether it matched the standard, and what the matching text was
def ocr(grayIm):
    label = ""
    # Pytesseract location
    # TODO RTODO
    # pytesseract.pytesseract.tesseract_cmd = (
    #     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # )
    # Config option only allows alphanumeric characters or periods. If you use extra characters, add them here
    text = pytesseract.image_to_string(
        grayIm,
        config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.",
    )
    match = matchLabel(text)
    if match:
        label = match.group(0)
    return text, label, match


# For testing. Obsolete
def collectImage(target, file=True):
    if file:
        ref = cv2.imread(target)
    else:
        ref = target
    grey = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(grey, 10, 255, cv2.THRESH_BINARY_INV)[1]
    refContours, heirarchy = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    return ref, thresh, refContours, heirarchy


# Helper. Returns slightly expanded size and center of rectangle
def getBoxChars(rect):
    xSpan = rect[2]
    ySpan = rect[3]
    xCenter = rect[0] + xSpan / 2
    yCenter = rect[1] + ySpan / 2
    return (int(xSpan) + 20, int(ySpan) + 20), (int(xCenter), int(yCenter))


# Takes a binarized image and target sizes. The binarized image is searched for
# contours- the largest is assumed to be the tape, if it matches the target sizes.
def idTape(orange, minSize, maxSize):
    refContours, heirarchy = cv2.findContours(
        orange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    biggest = 0
    tRect = None
    for c in refContours:
        area = cv2.contourArea(c)
        rect, size = boxContour(c)
        if size > biggest:
            biggest = size
            tRect = rect
    if tRect is not None:
        tSize, tCenter = getBoxChars(tRect)
        print(tSize, tCenter)
        for i in range(2):
            if tSize[i] < minSize or tSize[i] > maxSize:
                return None
        return tCenter
    # return center if appropriate size
    return None


# Takes a denoised image and a raw image. Locates the label, then returns a
# scaled, cropped, and rotated subregion containing only the label, held
# horizontally.
def correctAngle(pImg, rawImg, sub=True):
    refContours, heirarchy = cv2.findContours(
        pImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )
    biggest = 0
    tAngle = 0
    tContour = 0
    tRect = None
    fContour = None
    temp = rawImg.copy()
    for i in range(len(refContours)):
        c = refContours[i]
        area = cv2.contourArea(c)
        per = cv2.arcLength(c, False)
        # removing children inside of label
        # Only check contours with no children that aren't too large
        if -1 == heirarchy[0][i][2] and per < 1500:
            rect, size = boxContour(c)
            x, y, w, h, _ = rect
            # Pick the largest that has vaguely correct proportions
            if biggest < size and (w / h) > 3: # label shaped
                biggest = size
                tAngle = rect[4]
                tRect = rect
                fContour = c
    if tRect is not None:
        # Take the rectangle. Add it to the process image
        tSize, tCenter = getBoxChars(tRect)
        process = pImg.copy()
        x, y, w, h, _ = tRect
        cv2.rectangle(process, (x, y), (x + w, y + h), (255, 0, 0))
        # Rotate the image so the rectangle is horizontal
        # dont make it upside down
        if tAngle < -45:
            tAngle += 90
        M = cv2.getRotationMatrix2D(tCenter, tAngle, 1)
        dims = rawImg.shape
        rows = dims[0]
        cols = dims[1]
        rotated = cv2.warpAffine(rawImg, M, (cols, rows), 1)
        # Return the rotated region of interest
        if sub:
            rotated = cv2.getRectSubPix(rotated, tSize, tCenter)
            return process, rotated
        else:
            return process, rotated, tCenter
    # Only reached if no lable is found
    return pImg, rawImg


# Should be findLabel, but what can you do. Takes an image, processes it to
# remove noise, and then searches it for the label and the label for text
# TODO: add better explanation, clean out old code.
# filter glare and noise
def findSticker(img):
    smallKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    tinyKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    squareKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 20))
    blur = cv2.bilateralFilter(img, 9, 225, 175)
    ret = cv2.adaptiveThreshold(
        blur[:, :, 1], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 3
    )
    ret = cv2.dilate(ret, smallKernel, iterations=1)
    # cv2.imshow("1D", ret)
    ret = cv2.dilate(ret, tinyKernel, iterations=1)
    # cv2.imshow("2D", ret)
    ret = cv2.erode(ret, squareKernel, iterations=1)
    ret = cv2.erode(ret, tinyKernel, iterations=1)
    # cv2.imshow("Erosion", ret)
    # cv2.waitKey()
    """cv2.imshow("Binary", ret)
  cv2.waitKey()"""
    # ret = cv2.dilate(ret, squareKernel, iterations=2)
    # ret = cv2.erode(ret, squareKernel, iterations=2)
    # ret = cv2.morphologyEx(ret, cv2.MORPH_CLOSE, squareKernel, iterations=1)
    # edge finding
    ret = cv2.Canny(ret, 100, 200)
    gaus = cv2.GaussianBlur(blur, (9, 9), 10)
    unsharp = cv2.addWeighted(blur, 4, gaus, -3, 0)
    #tries to straighten relative to camera
    process, angled = correctAngle(ret, unsharp)
    if angled is not None:
        text, label, match = ocr(angled)
        # print(text, match==None)
        return ret, process, angled, match, text, label
    else:
        return ret, blur, blur, False, "", ""


# Takes a contour, returns the largest square that can fit inside it
# TODO: clarify, possibly remove
def boxContour(c):
    rect = cv2.minAreaRect(c)
    epsilon = 0.01 * cv2.arcLength(c, True)
    pts = cv2.approxPolyDP(c, epsilon, True)
    x, y, w, h = cv2.boundingRect(pts)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    area = cv2.contourArea(box)
    rect = (x, y, w, h, rect[2])
    # cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0))
    return rect, area


# For testing.
def defaultRun():
    vals = collectImage("s1.jpg")
    cv2.imshow("t", processFrame(vals[0])[0])
    cv2.waitKey()
    """for i in range(1,8):
    target = 's'+str(i)+".jpeg"
    vals = collectImage(target)
    findSticker(vals[0])"""


if __name__ == "__main__":
    defaultRun()
