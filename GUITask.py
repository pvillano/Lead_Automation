import pyautogui
from time import sleep

PICPATH = 'C:\\Users\\SciAps\\Documents\\Lead_Automation\\automationScreenshots\\'
ANALYZE_CHECK_I = 'Capture.PNG'
ANALYZE = 'Capture1.PNG'
ANALYZE_CHECK_F = 'Capture2.PNG'
DATAENTRY = 'Capture3.PNG'
DATA_READY = 'Capture5.PNG'
KEYBOARD = 'Capture4.PNG'
KEYBOARD_ALT = 'Capture4a.PNG'
SMALL_KEYBOARD = 'Capture5.PNG'
FRAME_TOP = 'Capture6.PNG'
START = 'Capture7.PNG'
CLEAR = 'Capture8.PNG'
ENTER = 'Capture9.PNG'
DONESIGN = 'Capture10.PNG'
TIME = 'Capture11.PNG'
NONE = 0
BAD_INITIAL_CONDITIONS = 1
BAD_FINAL_CONDITIONS = 2
NO_TARGET = 3

class GenericTask:
    
    def __init__(self):
        self.error = 0
        self.ok = True
        self.steps = 0
        self.triesLeft = 3
        self.maxTries = 3

    def errorCorrect(self):
        return

    def checkIConds(self):
        return

    def checkFConds(self):
        return

    def performStep(self, step):
        return

    def handleErrors(self):
        while (self.ok) and (self.error != 0):
            self.errorCorrect()
            self.triesLeft -= 1
            if (self.triesLeft <= 0):
                self.ok = False
            if not self.ok:
                return
        self.triesLeft = self.maxTries
        
    def regulatedCycle(self, step=None):
        self.checkIConds()
        self.handleErrors()
        if not self.ok:
            return self.error
        for step in range(self.steps):
            self.performStep(step)
            self.handleErrors()
            if not self.ok:
                return self.error
        self.checkFConds()
        self.handleErrors()
        if not self.ok:
            return self.error
        return 0

class GUITask(GenericTask):
    
    def __init__(self, screen):
        super().__init__()
        self.steps = 1
        self.screen = screen
        self.picpath = PICPATH
        self.iPic = None
        self.fPic = None
        self.errorDict = self.setupErrorDict()
        self.stepDict = self.setupStepDict()
        self.name = "GenericTask"

    def setupStepDict(self):
        ret = {}
        return ret

    def performStep(self, step):
        f = self.stepDict.get(step, self.unknownStep)
        self.error = f(step)

    def unknownStep(self, step):
        print("Unknown step %d" %step)

    def handleErrors(self):
        GenericTask.handleErrors(self)

    def setupErrorDict(self):
        ret = {
            BAD_INITIAL_CONDITIONS:self.startError,
            BAD_FINAL_CONDITIONS:self.endError,
            NO_TARGET:self.targetError}
        return ret

    def startError(self):
        print(self.name+" doesn't have valid start conditions")
        self.ok = False

    def endError(self):
        print(self.name+" couldn't produce valid end conditions")
        self.ok = False

    def targetError(self):
        print(self.name+" couldn't find the button it needed")
        self.ok = False

    def unknownError(self):
        print("Unknown error %d" %self.error)
        self.ok = False

    def errorCorrect(self):
        print("Correcting errors")
        f = self.errorDict.get(self.error, self.unknownError)
        f()

    def checkIConds(self):
        necesary, target = self.validatePic(self.iPic)
        if necesary:
            found, x, y = self.findAny([target])
            if not found:
                self.error = BAD_INITIAL_CONDITIONS

    def checkFConds(self):
        necesary, target = self.validatePic(self.fPic)
        if necesary:
            found, x, y = self.findAny([target])
            if not found:
                self.error = BAD_FINAL_CONDITIONS

    def validatePic(self, pic):
        if pic is None:
            return False, None
        else:
            return True, self.picpath+pic

    def findAny(self, pics):
        standards = 1.0
        success = False
        while not success:
            for pic in pics:
                try:
                    x,y = pyautogui.locateCenterOnScreen(pic, confidence=standards, region=self.screen)
                    success = True
                except Exception as e:
                    pass
            standards = standards*.9
            if standards <.5:
                print("Couldn't find targets")
                return False, -1, -1
            sleep(.2)
        return True, x, y

    def clickButton(self, pics, xOff=0, yOff=0):
        targets = []
        for pic in pics:
            valid, target = self.validatePic(pic)
            if valid:
                targets.append(target)
        fine, x, y = self.findAny(targets)
        if not fine:
            self.error = NO_TARGET
            return
        pyautogui.click(x+xOff, y+yOff)

class clickAnalyze(GUITask):
    def __init__(self, screen):
        super().__init__(screen)
        self.iPic = ANALYZE_CHECK_I
        self.fPic = ANALYZE_CHECK_F
        self.name = "clickAnalyze"

    def setupStepDict(self):
        ret = {0:self.cAnalyze}
        return ret

    def cAnalyze(self, step):
        super().clickButton([ANALYZE])
        return(self.error)

class clickDataEntry(GUITask):
    def __init__(self, screen):
        super().__init__(screen)
        self.iPic = ANALYZE_CHECK_F
        self.fPic = SMALL_KEYBOARD
        self.name = "clickDataEntry"

    def setupStepDict(self):
        ret = {0:self.cDataEntry}
        return ret

    def cDataEntry(self, step):
        super().clickButton([DATAENTRY])
        return(self.error)

class clickSample(GUITask):
    def __init__(self, screen):
        super().__init__(screen)
        self.iPic = SMALL_KEYBOARD
        self.fPic = CLEAR
        self.name = "clickSample"

    def setupStepDict(self):
        ret = {0:self.cSample}
        return ret

    def cSample(self, step):
        super().clickButton([KEYBOARD, KEYBOARD_ALT], xOff=115, yOff=0)
        return(self.error)

class clickClear(GUITask):
    def __init__(self, screen):
        super().__init__(screen)
        self.iPic = CLEAR
        self.fPic = None
        self.name = "clickClear"

    def setupStepDict(self):
        ret = {0:self.cClear}
        return ret

    def cClear(self, step):
        super().clickButton([CLEAR])
        return(self.error)

class clickStart(GUITask):
    def __init__(self, screen):
        super().__init__(screen)
        self.iPic = SMALL_KEYBOARD
        self.fPic = TIME
        self.name = "clickStart"

    def setupStepDict(self):
        ret = {0:self.cStart}
        return ret

    def cStart(self, step):
        super().clickButton([START])
        return(self.error)

class enterData(GUITask):
    def __init__(self, screen):
        super().__init__(screen)
        self.iPic = CLEAR
        self.fPic = SMALL_KEYBOARD
        self.name = "enterData"

    def setName(self, sample):
        self.sampleName = sample

    def setupStepDict(self):
        ret = {0:self.dataEntry}
        return ret

    def dataEntry(self, step):
        for char in self.sampleName:
            self.fancyPrint(char)
        pyautogui.hotkey('enter')
        return(self.error)
    
    def fancyPrint(self, char):
        pyautogui.keyUp('shift')
        if char.isnumeric() or char.islower():
            pyautogui.hotkey(char)
        elif char.isupper():
            pyautogui.keyDown('shift')
            pyautogui.hotkey(char.lower())
            pyautogui.keyUp('shift')
            pyautogui.press('shift')
        else:
            pyautogui.hotkey(char)

class fullRun(GUITask):
    def __init__(self, screen, sampleList):
        self.sampleList = sampleList
        self.Fs = [clickAnalyze(screen),
                   clickDataEntry(screen),
                   clickSample(screen),
                   clickClear(screen),
                   enterData(screen),
                   clickStart(screen)]
        self.Fs.append(runSample(screen, self.Fs))
        super().__init__(screen)
        self.iPic = ANALYZE_CHECK_I
        self.fPic = SMALL_KEYBOARD
        self.name = "fullRun"
        self.steps = 3

    def setupStepDict(self):
        ret = {0:self.Fs[0].regulatedCycle,
               1:self.Fs[1].regulatedCycle,
               2:self.runAllSamples}
        return ret

    def runAllSamples(self, step):
        for sample in self.sampleList:
            run = self.Fs[-1]
            run.setName(sample)
            self.error = run.regulatedCycle(step)
        return self.error

class runSample(GUITask):
    def __init__(self, screen, Fs):
        self.Fs= Fs
        super().__init__(screen)
        self.iPic = SMALL_KEYBOARD
        self.fPic = SMALL_KEYBOARD
        self.name = "inputSingleSample"
        self.steps = 4

    def setName(self, sample):
        self.sampleName = sample
        self.Fs[4].setName(sample)

    def setupStepDict(self):
        ret = {0:self.Fs[2].regulatedCycle,
               1:self.Fs[3].regulatedCycle,
               2:self.Fs[4].regulatedCycle,
               3:self.Fs[5].regulatedCycle}
        return ret

if __name__ == '__main__':
    test = fullRun(None, ['s1','s2'])
    #test = clickClear(None)
    test.regulatedCycle()
