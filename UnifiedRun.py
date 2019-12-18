import ArduinoControl
import XRFControl
from GantryControl import Gantry
import cv2
from time import sleep, time

#Tray Settings
#XRF_X_OFFSET = 27
#XRF_Y_OFFSET = 30
#TRAY_SIZE = 8
#Filter Settings
XRF_X_OFFSET = -24.23
XRF_Y_OFFSET = -35.19
TRAY_SIZE = 14
SAMPLES_TO_READ = 14*1
DEBUG = False

def mainLoop():
  start_time = time()
  gant = Gantry()
  ard = ArduinoControl.arduinoControl(gant)
  if askToHome():
    gant.home()
  mXRF = XRFControl.XRF()
  i = 0
  while i < SAMPLES_TO_READ:
    if (i != 0) and (((i) % TRAY_SIZE) == 0):
      gant.sendTo(str(0),str(0))
      cTime = time()
      elapsed = cTime - start_time
      start_time = cTime
      print("Time: %s seconds, %s minutes" % ((elapsed), (elapsed/60.0)))
      #input("Tray done! Reload tray and press enter ")
    label, position = ard.capture()
    targetLabel = correctLabels(label, i)
    targetPosition = correctPositions(position)
    if (targetPosition is not None):# and (not mXRF.error):
      if DEBUG:
        print(position)
        print(targetPosition)
        print(targetLabel)
      gant.sendTo(targetPosition[0][0], targetPosition[0][1])
      while gant.checkMoving():
        sleep(1)
      success = mXRF.sample(targetLabel)
      if success:
        print("Succesfully captured sample "+str(i)+"- "+targetLabel)
      else:
        print("Problem reading "+str(i)+"- "+targetLabel)
        input("Please manually run XRF and hit enter")
        mXRF.reset()
    i += 1
  ard.close()
  if not DEBUG:
    gant.sendTo(str(0),str(0))
    cTime = time()
    elapsed = cTime - start_time
    start_time = cTime
    print("Time: %s seconds, %s minutes" % ((elapsed), (elapsed/60.0)))
  gant.close()

def askToHome():
  yes = input("Home AXLE before start? (y/n): ")
  while (yes != 'y') and (yes != 'n'):
    print(yes)
    yes = input("Enter exactly y or n: ")
  return yes == 'y'

def correctLabels(labels, i):
  '''ELEPHANT- Label song and dance goes here'''
  ret = "Tray "
  ret += str(int((int(i)/int(TRAY_SIZE))+int(1)))
  ret += " Filter "
  ret += str((i % TRAY_SIZE)+1)
  return ret

def correctPositions(positions):
  ret = []
  for position in positions:
    if position is not None:
      p0 = max(float(position[0]) + XRF_X_OFFSET, 0);
      p1 = float(position[1]) + XRF_Y_OFFSET;
      ret.append([str.format("%4.3f"%(p0)), str.format("%4.3f"%(p1))])
    else:
      ret.append(None)
  return ret

if __name__ == '__main__':
  mainLoop()
