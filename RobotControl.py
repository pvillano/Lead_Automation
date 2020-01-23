import cv2
import mk2Camera
from time import sleep
from GantryControl import Gantry

xCenter = 240
yCenter = 320
pixelsToMM = (100.0/9)
TRAYS = 0
FILTERS = 1

class robotControl():
  def __init__(self, mode = TRAYS):
    self.gant = Gantry()
    self.cap = cv2.VideoCapture(1)
    self.setMode(mode)

  def setMode(self, mode = TRAYS):
    self.mode = mode
    if TRAYS == mode:
      self.maxTraySize = 8
      self.xStart = 75
      self.yStart = 145
    elif FILTERS == mode:
      self.maxTraySize = 30
      self.xStart = 20
      self.yStart = 320
    else:
      self.maxTraySize = 8
      self.xStart = 75
      self.yStart = 145
      print("ERROR: Unknown mode")

  def home(self):
    self.gant.home()
    
  def capture(self):
    self.samples += 1
    print(self.x, self.y)
    l, p = readLabels(1, self.x, self.y, self.gant, self.cap)
    self.advance()
    if self.samples >= self.maxTraySize:
      self.setToStart()
    return l, p

  def advance(self):
    if self.mode == TRAYS:
      self.y += 65.3
    elif self.mode == FILTERS:
      self.advanceFilters()

  def advanceFilters(self):
    columnPosition = self.samples % 3
    if columnPosition < 1:
      #Move to next column
      self.x = self.xStart
      self.y += 36.25
    else:
      self.x += 31

  def sendTo(self, x, y):
    self.gant.sendTo(str(x), str(y))

  def checkMoving(self):
    return self.gant.checkMoving()

  def setToStart(self):
    self.x = self.xStart
    self.y = self.yStart
    self.samples = 0

  def close(self):
    self.cap.release()

def tryToFindLabel(cap, t):
  i = 0
  label = ""
  while i < t:
    ret, frame = cap.read()
    processed, label = mk2Camera.processFrame(frame)
    if "" != label:
      print("Found label")
      i = t
    cv2.imshow('processView',processed)
    cv2.waitKey(1)
    i+=1
  return label

def tryToFindTape(number, x, y, cap):
  i = 0
  while i < number:
    ret, frame = cap.read()
    ret, frame = cap.read()
    processed, center = mk2Camera.processColor(frame)
    #cv2.imshow('processView',processed)
    #cv2.waitKey()
    if center is not None:
      break
    i+=1
  if center is not None:
    xTarget = (center[1] - xCenter)/pixelsToMM
    yTarget = (center[0] - yCenter)/pixelsToMM
    return (str.format("%4.3f"%(x+xTarget)), str.format("%4.3f"%(y+yTarget)))
  else:
    print("Could not find tape")
    return None

def readLabels(number, x, y, gant, cap):
  #Tray Settings
  #yOffset = 65.3
  #xOffset = 25
  #Filter Settings
  yOffset = 40
  xOffset = 0
  labels = []
  positions = []
  repeat = True
  for n in range(number):
    yTarget = y+(n*yOffset)
    gant.sendTo(str.format("%4.3f"%(x)), str.format("%4.3f"%(yTarget)))
    labels.append(tryToFindLabel(cap, 0))
    cX = x-(1*xOffset)
    gant.sendTo(str.format("%4.3f"%(cX)), str.format("%4.3f"%(yTarget)))
    center = tryToFindTape(20, cX, yTarget, cap)
    if center is None and repeat:
      cX = x-(1*xOffset)
      gant.sendTo(str.format("%4.3f"%(cX)), str.format("%4.3f"%(yTarget)))
      center = tryToFindTape(20, cX, yTarget, cap)
      if center is None:
        cX = x-(1*xOffset)
        gant.sendTo(str.format("%4.3f"%(cX)), str.format("%4.3f"%(yTarget)))
        center = tryToFindTape(20, cX, yTarget, cap)
    positions.append(center)
  return labels, positions

def singlePass(number, gant):
  cap = cv2.VideoCapture(1)
  labels, positions = readLabels(number, 62.5, 205, gant, cap)
  cap.release()
  return(labels, positions)


if __name__ == '__main__':
  r = robotControl(mode=FILTERS)
  r.setToStart()
  for i in range(3):
    l, p = r.capture()
    print(p)
  r.close()
  '''
  gant = Gantry()
  labels, positions = singlePass(1, gant)
  print(labels)
  print(positions)
  gant.sendTo(str(0),str(0))
  gant.close()

  #***
  while(True):
    ret, frame = cap.read()
    processed = mk2Camera.processFrame(frame)
    cv2.imshow('frame',processed)
    if cv2.waitKey() & 0xFF == ord('q'):
        break
  
  cv2.destroyAllWindows()'''
