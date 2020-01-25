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

def processColor(img):
  #For finding filters- just leave defaults for orange tape
  orange = findColor(img, color1=np.array([0,0,0]), color2=np.array([255,255,55]))
  orange = cv2.cvtColor(orange, cv2.COLOR_RGB2GRAY)
  center = idTape(orange)
  orange = standardize(img, orange)
  out = img.copy()
  if center is not None:
    cv2.circle(img, (center[0], center[1]), 120, (0,255,0), 2)
  return quadView(img, orange), center

def processFrame(img):
  ret, process, angled, match, text, label = findSticker(img)
  ret = standardize(img, ret)
  process = standardize(img, process)
  angled = standardize(img, angled)
  return quadView(img, ret, process, angled), label

def standardize(img, ret):
  if len(ret.shape) < 3:
    ret = cv2.cvtColor(ret, cv2.COLOR_GRAY2RGB)
  ret = cv2.resize(ret, dsize=(img.shape[1], img.shape[0]))
  return ret

def showImage(img):
  cv2.imshow("Display", img)
  cv2.waitKey()

def matchLabel(text):
    match = re.search('([A-Z]|[0-9]){3}\.([A-Z]|[0-9]){4}\.([A-Z]|[0-9]){2}', text)
    if match:
        return match
    else:
        match = re.search('([A-Z]|[0-9]){4}\.([A-Z]|[0-9]){3}\.([A-Z]|[0-9]){2}', text)
    if match:
      return match
    else:
      match = re.search('([A-Z]){2}\.([A-Z]|[0-9]){3}\.([A-Z]|[0-9]){2}', text)
    return match

def matchLabel2(text):
  match = re.search('2019\.[0-9]{3}\.[P,S,D][0-9]', text)
  if match:
    return match

def ocr(grayIm):
    label = ""
    pytesseract.pytesseract.tesseract_cmd= r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(grayIm,  config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.")
    match = matchLabel(text)
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
  refContours, heirarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  return ref, thresh, refContours, heirarchy

def getBoxChars(rect):
  xSpan = rect[2]
  ySpan = rect[3]
  xCenter = rect[0] + xSpan/2
  yCenter = rect[1] + ySpan/2
  return (int(xSpan)+20, int(ySpan)+20), (int(xCenter), int(yCenter))

def idTape(orange):
  refContours, heirarchy = cv2.findContours(orange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  biggest = 0
  tRect = None
  for c in refContours:
    area = cv2.contourArea(c)
    rect,size = boxContour(c)
    if size > biggest:
      biggest = size
      tRect = rect
  if tRect is not None:
    tSize, tCenter = getBoxChars(tRect)
    print(tSize, tCenter)
    for i in range(2):
      if tSize[i] < 150 or tSize[i] > 250:
        return None
    return tCenter
  return None


def correctAngle(pImg, rawImg, sub=True):
  refContours, heirarchy = cv2.findContours(pImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
  if tRect is not None:
    tSize, tCenter = getBoxChars(tRect)
    process = pImg.copy()
    x, y, w, h, _ = tRect
    cv2.rectangle(process, (x,y), (x+w,y+h), (255,0,0))
    if tAngle < -45:
      tAngle += 90
    tAngle += 180
      #tCenter = (tCenter[1], tCenter[0])
    M = cv2.getRotationMatrix2D(tCenter ,tAngle,1)
    dims = rawImg.shape
    rows = dims[0]
    cols = dims[1]
    rotated = cv2.warpAffine(rawImg, M, (cols, rows), 1)
    if sub:
      rotated = cv2.getRectSubPix(rotated, tSize, tCenter)
      return process, rotated
    else:
      return process, rotated, tCenter
  return None

def findSticker(img):
  squareKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
  blur = cv2.bilateralFilter(img, 3, 25, 255)
  ret = cv2.adaptiveThreshold(blur[:,:,0], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 3)
  ret = cv2.erode(ret, squareKernel, iterations=4)
  ret = cv2.Canny(ret, 100,200)
  gaus = cv2.GaussianBlur(blur, (9,9), 10)
  unsharp = cv2.addWeighted(blur, 4, gaus, -3, 0)
  process, angled = correctAngle(ret, unsharp)
  if angled is not None:
    text, label, match = ocr(angled)
    #print(text, match==None)
    return ret, process, angled, match, text, label
  else:
    return ret, blur, blur, False, "", ""

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
  vals = collectImage("s1.jpg")
  cv2.imshow("t",processFrame(vals[0])[0])
  cv2.waitKey()
  '''for i in range(1,8):
    target = 's'+str(i)+".jpeg"
    vals = collectImage(target)
    findSticker(vals[0])'''

if __name__ == '__main__':
  defaultRun()
  
  
