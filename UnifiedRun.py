import ArduinoControl
import XRFControl

XRF_X_OFFSET = -30
XRF_Y_OFFSET = -233
TRAY_SIZE = 8

def mainLoop():
  labels, positions = ArduinoControl.singlePass(TRAY_SIZE)
  targetLabels = correctLabels(labels)
  targetPositions = correctPositions(positions)
  mXRF = XRFControl.XRF()
  for i in range(TRAY_SIZE):
    if (targetPositions[i] is not None) and (mXRF.working):
      ArduinoControl.sendTo(None, targetPositions[i][0], targetPositions[i][1])
      mXRF.sample(targetLabels[i])
  ArduinoControl.sendTo(None, 0, 0)

def correctLabels(labels):
  '''ELEPHANT- Label song and dance goes here'''
  return labels

def correctPositions(positions):
  ret = []
  for position in positions:
    if position is not None:
      p0 = float(position[0]) + XRF_X_OFFSET;
      p1 = float(position[1]) + XRF_Y_OFFSET;
      ret.append([str.format("%4.3f"%(p0)), str.format("%4.3f"%(p1))])
    else:
      ret.append(None)
  return ret

if __name__ == '__main__':
  mainLoop()