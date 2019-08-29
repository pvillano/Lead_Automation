import ArduinoControl
import XRFControl
from GantryControl import Gantry

XRF_X_OFFSET = 0
XRF_Y_OFFSET = -165
TRAY_SIZE = 8

def mainLoop():
  gant = Gantry()
  #labels, positions = ArduinoControl.singlePass(TRAY_SIZE, gant)
  labels = ['SS.003.P2', 'SS.004.P2', 'SS.006.D1', '', 'SS.006.S2', '', 'SS.006.D2', 'SS.004.D3']
  positions = [('-49.274', '8.761'), ('-50.726', '-55.471'), ('-49.915', '-121.241'), ('-49.615', '-184.575'), ('-52.222', '-250.559'), ('-51.880', '-317.226'), ('-48.932', '-383.381'), ('-51.068', '-448.852')]
  print(labels)
  print(positions)
  targetLabels = correctLabels(labels)
  targetPositions = correctPositions(positions)
  print("***********************")
  print(targetLabels)
  print(targetPositions)
  #mXRF = XRFControl.XRF()
  for i in range(TRAY_SIZE):
    if (targetPositions[i] is not None):# and (mXRF.working):
      gant.sendTo(targetPositions[i][0], targetPositions[i][1])
      #mXRF.sample(targetLabels[i])
  gant.sendTo(str(0),str(0))
  gant.close()

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
