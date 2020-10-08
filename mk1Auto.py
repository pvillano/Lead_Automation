import pyautogui
from time import sleep

PICPATH = "C:\\Users\\SciAps\\Documents\\Lead_Automation\\automationScreenshots\\"
ANALYZE = "Capture1.PNG"
DATAENTRY = "Capture3.PNG"
KEYBOARD = "Capture4.PNG"
KEYBOARD_ALT = "Capture4a.PNG"
FRAME_TOP = "Capture6.PNG"
START = "Capture7.PNG"
CLEAR = "Capture8.PNG"
ENTER = "Capture9.PNG"
DONESIGN = "Capture10.PNG"
MAX_WAIT = 120
SCREEN_HEIGHT = 440


def checkCondition(img, screen):
    pic = PICPATH + img
    ret = False
    standards = 1.0
    while not ret:
        try:
            x, y = pyautogui.locateCenterOnScreen(pic, confidence=standards)
            ret = True
        except Exception as e:
            sleep(0.2)
            standards = standards * 0.9
            if standards < 0.5:
                return False
    return ret


def findScreenBounds(topFile=FRAME_TOP):
    pic = PICPATH + topFile
    ret = False
    standards = 1.0
    while not ret:
        try:
            x, y, w, h = pyautogui.locateOnScreen(pic, confidence=standards)
            ret = True
        except Exception as e:
            sleep(0.2)
            standards = standards * 0.9
            if standards < 0.5:
                return (-1, -1, -1, -1)
    return (x, y, w, h + SCREEN_HEIGHT)


def findAltOnScreen(buttonFile, altFile, screen):
    pic1 = PICPATH + buttonFile
    pic2 = PICPATH + altFile
    standards = 1.0
    ret = False
    while not ret:
        try:
            x, y = pyautogui.locateCenterOnScreen(
                pic1, confidence=standards, region=screen
            )
            ret = True
        except Exception as e:
            try:
                x, y = pyautogui.locateCenterOnScreen(
                    pic2, confidence=standards, region=screen
                )
                print("found alt image!")
                ret = True
            except Exception as e:
                sleep(0.2)
                standards = standards * 0.9
                if standards < 0.5:
                    print("Trouble finding %s or its alt" % buttonFile)
                    return -1, -1
    return x, y


def findOnScreen(buttonFile, screen):
    pic = PICPATH + buttonFile
    ret = False
    standards = 1.0
    while not ret:
        try:
            x, y = pyautogui.locateCenterOnScreen(
                pic, confidence=standards, region=screen
            )
            ret = True
        except Exception as e:
            sleep(0.2)
            standards = standards * 0.9
            if standards < 0.5:
                # print("Trouble finding %s"%buttonFile)
                return -1, -1
    return x, y


def waitFor(buttonFile, screen):
    x, y = findOnScreen(buttonFile, screen)
    i = 0
    while -1 == x and i < MAX_WAIT:
        sleep(1)
        x, y = findOnScreen(buttonFile, screen)
        i = i + 1
    if i == MAX_WAIT:
        return False
    else:
        return True


def clickButton(buttonFile, screen):
    success = False
    try:
        sleep(0.2)
        x, y = findOnScreen(buttonFile, screen)
        pyautogui.click(x, y)
        success = True
    except Exception as e:
        print(e)
    return success


def fancyPrint(char):
    pyautogui.keyUp("shift")
    # print(char)
    if char.isnumeric() or char.islower():
        pyautogui.hotkey(char)
        # print("Not upper")
    elif char.isupper():
        # print("Upper")
        pyautogui.keyDown("shift")
        pyautogui.hotkey(char.lower())
        pyautogui.keyUp("shift")
        pyautogui.press("shift")
    else:
        pyautogui.hotkey(char)
        # print("Other")


def clickAnalyze(screen):
    analyze = clickButton(ANALYZE, screen)
    return analyze


def clickDataEntry(screen):
    return clickButton(DATAENTRY, screen)


def enterData(sampleName, screen):
    x, y = findAltOnScreen(KEYBOARD, KEYBOARD_ALT, screen)
    pyautogui.click(x + 115, y)
    success = clickButton(CLEAR, screen)
    if success:
        for c in sampleName:
            fancyPrint(c)
        return True
    else:
        return False


def clickStart(screen):
    return clickButton(START, screen)


def XRFStart(sampleList, screen):
    working = clickAnalyze(screen)
    if working:
        working = clickDataEntry(screen)
    if working:
        for sample in sampleList:
            working = XRFCycle(sample, screen)
            if not working:
                print("An error occured")
                break


def XRFCycle(sampleName, screen):
    working = enterData(sampleName, screen)
    if working:
        working = clickStart(screen)
        sleep(0.5)
        pyautogui.hotkey("enter")
    if not working:
        print("There was an error")
        return False
    else:
        sleep(3)
        if waitFor(DONESIGN, screen):
            sleep(4)
            # print("Hitting enter now")
            pyautogui.hotkey("enter")
            print("Everything fine w/ %s" % sampleName)
            return True
        else:
            print("Timed out on %s" % sampleName)
            return False


if __name__ == "__main__":
    testList = []
    for i in range(10):
        testStr = "SS.00" + str(i)
        for j in range(10):
            test2Str = testStr + ".S" + str(j)
            testList.append(test2Str)
    testScreen = findScreenBounds()
    print(testScreen)
    # XRFCycle('Teting')
    XRFStart(testList, testScreen)
    # XRFCycle("Test1")
