import numpy as np
import cv2
import time
import imutils
from imutils import contours
import pytesseract
import re

def quadView(v1, v2, v3=None, v4=None):
  v1=cv2.resize(v1, None, fx=.5, fy=.5, interpolation = cv2.INTER_CUBIC)
  v2=cv2.resize(v2, None, fx=.5, fy=.5, interpolation = cv2.INTER_CUBIC)
  finalView = np.hstack((v1, v2))
  if v3 is not None:
    v3=cv2.resize(v3, None, fx=.5, fy=.5, interpolation = cv2.INTER_CUBIC)
    v4=cv2.resize(v4, None, fx=.5, fy=.5, interpolation = cv2.INTER_CUBIC)
    botView = np.hstack((v3, v4))
    finalView = np.vstack((finalView, botView))
  return finalView

def findColor(img, color1=np.array([0,170,125]), color2=np.array([70,255,255])):
  hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsvImg, color1, color2)
  return cv2.bitwise_and(img, img, mask=mask)

def processFrame(img):
  orange = findColor(img)
  return quadView(img, orange)

def showImage(img):
  cv2.imshow("Display", img)
  cv2.waitKey()

def matchLabel(text):
    match = re.search('([A-Z]|[0-9]){3}\.([A-Z]|[0-9]){4}\.([A-Z]|[0-9]){2}', text)
    if match:
        return match
    else:
        match = re.search('([A-Z]|[0-9]){4}\.([A-Z]|[0-9]){3}\.([A-Z]|[0-9]){2}', text)
    return match

def matchLabel2(text):
  match = re.search('2019\.[0-9]{3}\.[P,S,D][0-9]', text)
  if match:
    return match

def ocr(grayIm):
    label = ""
    text = pytesseract.image_to_string(grayIm)
    match = matchLabel2(text)
    if match:
        label = match.group(0)
    return text, label, match

def collectImage(target, file=True):
  if file:
    ref = cv2.imread(target)
  else:
    ref = target
  grey = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
  thresh = cv2.threshold(grey, 10, 255, cv2.THRESH_BINARY_INV)[1]
  _, refContours, heirarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  return ref, thresh, refContours, heirarchy

def getBoxChars(rect):
  xSpan = rect[2]
  ySpan = rect[3]
  xCenter = rect[0] + xSpan/2
  yCenter = rect[1] + ySpan/2
  return (int(xSpan)+20, int(ySpan)+20), (int(xCenter), int(yCenter))

def correctAngle(pImg, rawImg):
  _, refContours, heirarchy = cv2.findContours(pImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  #display = cv2.cvtColor(rawImg, cv2.COLOR_GRAY2RGB)
  biggest = 0
  tAngle = 0
  tContour = 0
  tRect = None
  fContour = None
  for c in refContours:
    area = cv2.contourArea(c)
    per = cv2.arcLength(c, False)
    if per > 100:
      rect, size = boxContour(c)
      if size > 2000 and biggest < size:
        biggest = size
        tAngle = rect[4]
        tRect = rect
        fContour = c
        '''
        (x,y),(MA,ma),angle = cv2.fitEllipse(c)
        if biggest < size:
          biggest = area
          tAngle = angle
          centerX = x
          centerY = y
          cv2.ellipse(display, center = (int(x),int(y)), axes = (int(MA/2),int(ma/2)), angle=angle, startAngle=0, endAngle=360, color=(0,0,255))
          cv2.circle(display, (int(x),int(y)), radius=2, color=(0,255,0))'''
  if tRect is not None:
    tSize, tCenter = getBoxChars(tRect)
    print(tSize)
    if tAngle < -45:
      tAngle += 90
      #tCenter = (tCenter[1], tCenter[0])
    M = cv2.getRotationMatrix2D(tCenter ,tAngle,1)
    dims = rawImg.shape
    rows = dims[0]
    cols = dims[1]
    rotated = cv2.warpAffine(rawImg, M, (cols, rows), 1)
    rotated = cv2.getRectSubPix(rotated, tSize, tCenter)
    return rotated
  return None

def findSticker(img):
  squareKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
  blur = cv2.bilateralFilter(img, 25, 25, 255)
  ret = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)[1]
  #showImage(ret)
  #ret = cv2.erode(ret, squareKernel, iterations=10)
  #ret = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 1)
  ret = cv2.Canny(ret, 100,200)
  angled = correctAngle(ret, blur)
  if angled is not None:
    text, label, match = ocr(angled)
    print(text, match==None)
    return angled, match, text, label
  else:
    return blur, False, "", ""

def boxContour(c):
  rect = cv2.minAreaRect(c)
  epsilon = .01*cv2.arcLength(c, True)
  pts = cv2.approxPolyDP(c, epsilon, True)
  x,y,w,h = cv2.boundingRect(pts)
  box = cv2.boxPoints(rect)
  box = np.int0(box)
  area = cv2.contourArea(box)
  rect = (x, y, w, h, rect[2])
  #cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0))
  return rect, area

def defaultRun():
  vals = collectImage("s5.jpeg")
  findSticker(vals[0])
  '''for i in range(1,8):
    target = 's'+str(i)+".jpeg"
    vals = collectImage(target)
    findSticker(vals[0])'''

if __name__ == '__main__':
  defaultRun()
  
  