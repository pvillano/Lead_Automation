import cv2
import mk2Camera
from time import sleep
from GantryControl import Gantry
import ModeSettings

xCenter = 240
yCenter = 320
pixelsToMM = (100.0/9)
TRAYS = 0
FILTERS = 1

class robotControl():
  def __init__(self, mode = ModeSettings.TrayMode()):
    self.gant = Gantry()
    self.cap = cv2.VideoCapture(1)
    self.setMode(mode)
    self.xMin = 0
    self.xMax = 85
    self.yMin = 0
    self.yMax = 780

  def setMode(self, mode = ModeSettings.TrayMode()):
    self.mode = mode
    (self.xStart, self.yStart, self.maxTraySize) = self.mode.getTraySettings()
    (self.xAdvance, self.yAdvance) = self.mode.getAdvanceOffset()
    (self.c1, self.c2, self.s1, self.s2) = self.mode.getColorLimits()

  def home(self):
    self.gant.home()
    
  def capture(self):
    self.samples += 1
    #print(self.x, self.y)
    l, p = readLabels(1, self.x, self.y, self.gant, self.cap, self.xAdvance, self.yAdvance, self.c1, self.c2, self.s1, self.s2)
    self.advance()
    if self.samples >= self.maxTraySize:
      self.setToStart()
    return l, p

  def advance(self):
    (self.x, self.y) = self.mode.advance(self.x, self.y)
    
  def advanceFilters(self):
    columnPosition = self.samples % 3
    if columnPosition < 1:
      #Move to next column
      self.x = self.xStart
      self.y += 36.25
    else:
      self.x += 31

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

def tryToFindLabel(gant, cap, t, x, y):
  i = 0
  gant.sendTo(str.format("%4.3f"%(x)), str.format("%4.3f"%(y)))
  while i < t:
    label = singleLabelTry(cap, 3)
    if "" != label:
      i = t
    else:
      x += 5
      gant.sendTo(str.format("%4.3f"%(x)), str.format("%4.3f"%(y)))
    i+=1
  if "" == label:
    print("Missed label")
  return label

def singleLabelTry(cap, t):
  i = 0
  label = ""
  while i < t:
    ret, frame = cap.read()
    processed, label = mk2Camera.processFrame(frame)
    if "" != label:
      print("Found label")
      i = t
    #cv2.imshow('processView',processed)
    #cv2.waitKey()
    i+=1
  return label

def tryToFindTape(number, x, y, cap, color1, color2, s1, s2):
  i = 0
  while i < number:
    for j in range(1):
      ret, frame = cap.read()
    processed, center = mk2Camera.processColor(frame, color1, color2, s1, s2)
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

def readLabels(number, x, y, gant, cap, xOffset, yOffset, color1, color2, s1, s2):
  #Tray Settings
  #yOffset = 65.3
  #xOffset = 25
  #Filter Settings
  #yOffset = 40
  #xOffset = 0
  labels = []
  positions = []
  repeat = True
  for n in range(number):
    yTarget = y+(n*yOffset)
    gant.sendTo(str.format("%4.3f"%(x)), str.format("%4.3f"%(yTarget)), "35.0")
    l = tryToFindLabel(gant, cap, 3, x, yTarget)
    if "" == l:
      gant.setZ(40)
      l = tryToFindLabel(gant, cap, 3, x, yTarget)
    gant.setZ(35)
    labels.append(l)
    cX = x+(1*xOffset)
    gant.sendTo(str.format("%4.3f"%(cX)), str.format("%4.3f"%(yTarget)))
    center = tryToFindTape(20, cX, yTarget, cap, color1, color2, s1, s2)
    if center is None and repeat:
      cX = x+(2*xOffset)
      gant.sendTo(str.format("%4.3f"%(cX)), str.format("%4.3f"%(yTarget)))
      center = tryToFindTape(20, cX, yTarget, cap, color1, color2, s1, s2)
      if center is None:
        cX = x+(3*xOffset)
        gant.sendTo(str.format("%4.3f"%(cX)), str.format("%4.3f"%(yTarget)))
        center = tryToFindTape(20, cX, yTarget, cap, color1, color2, s1, s2)
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
  for i in range(4):
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
