import RobotControl
import XRFControl
import cv2
from time import sleep, time
import argparse
from PyQt5.QtCore import QObject, pyqtSignal

DEBUG = True
TRAYS = 0
FILTERS = 1

class unifiedRun(QObject):
  sampleStatusOK = pyqtSignal(int, bool)
  trayDoneTime = pyqtSignal(int)
  batchDone = pyqtSignal()
  
  def __init__(self):
    super(unifiedRun, self).__init__()
    self.robot = RobotControl.robotControl()
    self.xrf = XRFControl.XRF()

  def close(self):
    self.robot.sendTo(0, 0)
    self.robot.close()

  def home(self):
    self.robot.home()

  def runDummy(self, opt=None):
    sleep(5)
    self.batchDone.emit()

  def runBatch(self, mode, samples, name):
    start_time = time()
    i = 0
    (xrfXOffset, xrfYOffset, traySize) = getSettings(mode = mode)
    self.robot.setMode(mode)
    self.robot.sendTo(0, 250)
    self.robot.sendTo(0, 280)
    self.robot.setToStart()
    while self.robot.checkMoving():
        print("sleeping")
        sleep(1)
    while i < samples:
      if (i != 0) and (((i) % traySize) == 0):
        robot.sendTo(0, 0)
        cTime = time()
        elapsed = cTime - start_time
        start_time = cTime
        self.trayDoneTime.emit(elapsed)
        #ELEPHANT- add user input
        while self.robot.checkMoving():
          print("sleeping")
          sleep(1)
      label, position = self.robot.capture()
      targetLabel = correctLabels(label, i, traySize, name)
      targetPosition = correctPositions(position, xrfXOffset, xrfYOffset)
      if (targetPosition is not None) and (not self.xrf.error):
        if DEBUG:
          print(position)
          print(targetPosition)
          print(targetLabel)
        self.robot.sendTo(targetPosition[0][0], targetPosition[0][1])
        while self.robot.checkMoving():
          print("sleeping")
          sleep(1)
        success = self.xrf.sample(targetLabel)
        self.sampleStatusOK.emit(i+1, success)
      else:
        self.xrf.reset()
        self.sampleStatusOK.emit(i+1, False)
      i += 1
    self.robot.sendTo(0, 280)
    self.robot.sendTo(0, 250)
    self.robot.sendTo(0, 0)
    self.batchDone.emit()
  
def mainLoop(mode, samples, home = False, name="Tray"):
  start_time = time()
  (xrfXOffset, xrfYOffset, traySize) = getSettings(mode = mode)
  robot = RobotControl.robotControl(mode = mode)
  if home:
    robot.home()
  mXRF = XRFControl.XRF()
  i = 0
  while i < samples:
    if (i != 0) and (((i) % traySize) == 0):
      robot.sendTo(0, 0)
      cTime = time()
      elapsed = cTime - start_time
      start_time = cTime
      print("Time: %s seconds, %s minutes" % ((elapsed), (elapsed/60.0)))
      #input("Tray done! Reload tray and press enter ")
    label, position = robot.capture()
    targetLabel = correctLabels(label, i, traySize, name)
    targetPosition = correctPositions(position, xrfXOffset, xrfYOffset)
    if (targetPosition is not None) and (not mXRF.error):
      if DEBUG:
        print(position)
        print(targetPosition)
        print(targetLabel)
      robot.sendTo(targetPosition[0][0], targetPosition[0][1])
      while robot.checkMoving():
        sleep(1)
      success = mXRF.sample(targetLabel)
      if success:
        print("Succesfully captured sample "+str(i)+"- "+targetLabel)
      else:
        print("Problem reading "+str(i)+"- "+targetLabel)
        input("Please manually run XRF and hit enter")
        mXRF.reset()
    i += 1
  if not DEBUG:
    robot.sendTo(str(0),str(0))
    cTime = time()
    elapsed = cTime - start_time
    start_time = cTime
    print("Time: %s seconds, %s minutes" % ((elapsed), (elapsed/60.0)))
  robot.close()

#Redundant
def askToHome():
  yes = input("Home AXLE before start? (y/n): ")
  while (yes != 'y') and (yes != 'n'):
    print(yes)
    yes = input("Enter exactly y or n: ")
  return yes == 'y'

def correctLabels(labels, i, traySize, name = "Tray"):
  '''ELEPHANT- Label song and dance goes here'''
  ret = name
  ret += ".Item."
  ret += str((i % traySize)+1)
  return ret

def correctPositions(positions, xrfXOffset, xrfYOffset):
  ret = []
  for position in positions:
    if position is not None:
      p0 = max(float(position[0]) + xrfXOffset, 0);
      p1 = float(position[1]) + xrfYOffset;
      ret.append([str.format("%4.3f"%(p0)), str.format("%4.3f"%(p1))])
    else:
      return None
  return ret

def getSettings(mode):
  if TRAYS == mode:
    return (27, 30, 8)
  elif FILTERS == mode:
    return (-8.9, -43.62, 30)
  else:
    print("ERROR: Unknown mode")
    return (0, 0, 0)

if __name__ == '__main__':
  #Default settings:
  mode = TRAYS
  samples = 8*1
  home = True
  text = 'Consolidated XRF automation software, used to control the AXLE gantry and interface with the XRF GUI'
  parser = argparse.ArgumentParser(description = text)
  parser.add_argument("-f", "--filters", help="Filter mode- for use with filter trays", action="store_true")
  parser.add_argument("-s", "--samples", help="Number of samples to test", type=int)
  parser.add_argument("-c", "--continuous", help="Continuous mode- disables homing", action="store_true")
  args = parser.parse_args()
  if args.filters:
    mode = FILTERS
  if args.samples is not None:
    samples = args.samples
  if args.continuous:
    home = False
  mainLoop(mode, samples, home)
