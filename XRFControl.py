import mk1Auto as m1

class XRF:
  """Controls for the XRF"""
  working = False
  started = False

  def __init__(self):
    self.working = m1.clickAnalyze()
    if self.working:
      self.working = m1.clickDataEntry()
    self.started = self.working

  def sample(sampleName='Unknown'):
    if self.started and self.working:
      self.working = m1.XRFCycle(sampleName)
    return self.working