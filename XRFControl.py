import mk1Auto as m1
import pyautogui

class XRF:
  """Controls for the XRF"""
  working = False
  started = False
  screen = (-1,-1,-1,-1)

  def __init__(self):
    self.screen = m1.findScreenBounds()
    if self.screen == (-1,-1,-1,-1):
      return
    self.working = m1.clickAnalyze(self.screen)
    if self.working:
      self.working = m1.clickDataEntry(self.screen)
    self.started = self.working

  def sample(self, sampleName='Unknown'):
    if self.started and self.working:
      self.working = m1.XRFCycle(sampleName, self.screen)
    return self.working


#if __name__ == '__main__':
  #r = (r[0],r[1],r[2],r[3]+440)
  #print(r)
  #pyautogui.screenshot('temp.png', region = r)
