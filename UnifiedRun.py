import ArduinoControl
import XRFControl
from GantryControl import Gantry
import cv2
from time import sleep

XRF_X_OFFSET = 27
XRF_Y_OFFSET = 30
TRAY_SIZE = 8

def mainLoop():
  gant = Gantry()
  ard = ArduinoControl.arduinoControl(gant)
  mXRF = XRFControl.XRF()
  for i in range(TRAY_SIZE):
    label, position = ard.capture()
    targetLabel = correctLabels(label)
    targetPosition = correctPositions(position)
    if (targetPosition is not None) and (not mXRF.error):
      gant.sendTo(targetPosition[0][0], targetPosition[0][1])
      while gant.checkMoving():
        sleep(1)
      success = mXRF.sample(targetLabel[0])
      if success:
        print("Succesfully captured sample "+str(i)+"- "+targetLabel[0])
      else:
        print("Problem reading "+str(i)+"- "+targetLabel[0])
  ard.close()
  gant.sendTo(str(0),str(0))
  gant.close()

def correctLabels(labels):
  '''ELEPHANT- Label song and dance goes here'''
  return labels

def correctPositions(positions):
  ret = []
  for position in positions:
    if position is not None:
      p0 = max(float(position[0]) - XRF_X_OFFSET, 0);
      p1 = float(position[1]) + XRF_Y_OFFSET;
      ret.append([str.format("%4.3f"%(p0)), str.format("%4.3f"%(p1))])
    else:
      ret.append(None)
  return ret

if __name__ == '__main__':
  mainLoop()
