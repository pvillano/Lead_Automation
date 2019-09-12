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
FINE = 0
INIT_ERROR = 1
CLICK_ERROR = 2
RESPONSE_ERROR = 3
TRIES_MAX = 3

class buttonTask:
    def __init__(self, picpath, iPic, pic, fPic, screen):
        self.picpath = picpath
        self.iPic = iPic
        self.pic = pic
        self.fPic = fPic
        self.screen = screen
        self.ok = True
        self.tries = TRIES_MAX

    def regulatedCycle(self):
        if not self.bSearchRoutine(self.iPic):
            return INIT_ERROR
        self.clickButton(self.picpath+self.pic)
        if not self.ok:
            return CLICK_ERROR
        self.ok = self.bSearchRoutine(self.fPic)
        while ((not self.ok) and (self.tries > 0)):
            self.clickButton(self.picpath+self.pic)
            self.ok = self.bSearchRoutine(self.fPic)
            self.tries -= 1
        if self.ok:
            return FINE
        return RESPONSE_ERROR

    def clickButton(self, pic):
        success = False
        try:
            sleep(.2)
            x, y = self.searchRoutine(pic)
            if(x!=-1 and y!=-1):
                pyautogui.click(x, y)
                success = True
        except Exception as e:
            print(e)
        self.ok = success

    def bSearchRoutine(self, img):
        if img is None:
            return True
        a, b = self.searchRoutine(self.picpath+img)
        return (a != -1 and b != -1) 

    def searchRoutine(self, img):
          ret = False
          standards = 1.0
          while not ret:
            try:
              x, y = pyautogui.locateCenterOnScreen(img, confidence=standards, region=self.screen)
              ret = True
            except Exception as e:
              sleep(.2)
              standards = standards*.9
              if standards < .5:
                return -1, -1
          return x, y

class startTask(buttonTask):
    def __init__(self, screen):
        super().__init__(PICPATH, SMALL_KEYBOARD, START, TIME, screen)

    def regulatedCycle(self):
        if not self.bSearchRoutine(self.iPic):
            print("Wrong start conditions, trying enter")
            pyautogui.hotkey('enter')
            sleep(1)
            if not self.bSearchRoutine(self.iPic):
                print("Trying manual click")
                self.clickButton(self.picpath+ENTER)
                if not self.bSearchRoutine(self.iPic):
                    print("Couldn't resolve")
                    return INIT_ERROR
        self.clickButton(self.picpath+self.pic)
        if not self.ok:
            return CLICK_ERROR
        self.ok = self.bSearchRoutine(self.fPic)
        while ((not self.ok) and (self.tries > 0)):
            self.clickButton(self.picpath+self.pic)
            self.ok = self.bSearchRoutine(self.fPic)
            self.tries -= 1
        if self.ok:
            return FINE
        return RESPONSE_ERROR

class dataEntryTask(buttonTask):
    def __init__(self, screen):
        super().__init__(PICPATH, DATA_READY, KEYBOARD_ALT, CLEAR, screen)
        self.aPic = KEYBOARD
        self.clearPic = CLEAR

    def regulatedCycle(self, sampleName):
        if not self.bSearchRoutine(self.iPic):
            print("Trying enter")
            pyautogui.hotkey('enter')
            sleep(.2)
        if not self.bSearchRoutine(self.iPic):
            return INIT_ERROR
        self.clickButton()
        if not self.ok:
            return CLICK_ERROR
        self.ok = self.bSearchRoutine(self.fPic)
        while ((not self.ok) and (self.tries > 0)):
            self.clickButton()
            self.ok = self.bSearchRoutine(self.fPic)
        if self.ok:
            for c in sampleName:
                self.fancyPrint(c)
            sleep(.1)
            pyautogui.hotkey('enter')
            return FINE
        return RESPONSE_ERROR

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

    def clickButton(self):
        self.clickAlt()
        if self.ok:
            self.clickSimpleButton()

    def clickSimpleButton(self):
        super().clickButton(self.picpath+self.clearPic)

    def clickAlt(self):
        standards = 1.0
        success = False
        while not success:
            try:
                sleep(.2)
                x, y = pyautogui.locateCenterOnScreen(self.picpath+self.pic, confidence=standards, region=self.screen)
                success=True
            except Exception as e:
                try:
                    x, y = pyautogui.locateCenterOnScreen(self.picpath+self.aPic, confidence=standards, region=self.screen)
                    success=True
                except Exception as e:
                    standards = standards*.9
                    if standards < .5:
                        self.ok=False
                        print("Couldn't find target")
                        return
        pyautogui.click(x+115, y)
        success = True
        self.ok = success
        
if __name__ == '__main__':
    test = dataEntryTask(None)
    test.regulatedCycle(None)
