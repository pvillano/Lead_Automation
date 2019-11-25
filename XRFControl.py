import mk2Auto as m1
import pyautogui

class XRF:
  """Controls for the XRF"""
  error = False
  started = False
  screen = (-1,-1,-1,-1)

  def __init__(self):
    self.screen = m1.findScreenBounds()
    if self.screen == (-1,-1,-1,-1):
      return
    self.error, self.a, self.b = m1.XRFStart(None, self.screen)
    if self.error:
      print("Error")
    self.started = not self.error

  def sample(self, sampleName='Unknown'):
    if self.started and not self.error:
      self.error = not m1.XRFCycle(sampleName, self.screen, self.a, self.b)
    return not self.error

  def reset(self):
    self.error = False


if __name__ == '__main__':
  mXRF = XRF()
  success = True
  i = 0
  while (i < 20 and success):
    targetLabel = "Sample " + str(i)
    success = mXRF.sample(targetLabel)
    i += 1
  #r = (r[0],r[1],r[2],r[3]+440)
  #print(r)
  #pyautogui.screenshot('temp.png', region = r)
