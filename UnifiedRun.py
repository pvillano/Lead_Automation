import RobotControl
import XRFControl
from time import sleep, time
import argparse
from PyQt5.QtCore import QObject, pyqtSignal
import ModeSettings

DEBUG = False
TRAYS = 0
FILTERS = 1

# Controls a single run of samples.
class unifiedRun(QObject):
    sampleStatusOK = pyqtSignal(int, bool)
    trayDoneTime = pyqtSignal(int)
    batchDone = pyqtSignal()

    def __init__(self):
        super(unifiedRun, self).__init__()
        self.paused = False
        self.done = False
        self.robot = RobotControl.robotControl()
        if not DEBUG:
            self.xrf = XRFControl.XRF()
            print("XRF mode on")

    def cont(self, nextSample):
        if not nextSample:
            self.done = True
        self.paused = False

    def close(self):
        self.robot.sendTo(0, 0)
        self.robot.close()

    def home(self):
        self.robot.home()

    def runDummy(self, opt=None):
        sleep(5)
        self.batchDone.emit()

    def runBatch(self, mode, samples, name):
        """
        called to run a batch
        """
        print("Starting batch")
        start_time = time()
        i = 0
        # set by gui
        self.mode = ModeSettings.getMode(mode)
        traySize = self.mode.maxTraySize
        xrfXOffset, xrfYOffset, xrfZOffset = self.mode.getXRFOffset()
        self.robot.setMode(self.mode)
        # Wait for robot to reach its start position.
        self.robot.setToStart()
        while self.robot.checkMoving():
            print("sleeping")
            sleep(1)
        # Check that you have samples left or are running in continuous mode.
        while i < samples or -1 == samples:
            # End of tray routine. If you've processed a multiple of the traysize,
            # return to the home position and wait for user input.
            if (i != 0) and (((i) % traySize) == 0):
                self.robot.sendTo(0, 0)
                cTime = time()
                elapsed = cTime - start_time
                start_time = cTime
                self.trayDoneTime.emit(elapsed)
                self.paused = True
                while self.paused or self.robot.checkMoving():
                    # print("sleeping")
                    sleep(1)
                    if self.done:
                        self.robot.sendTo(0, 0, 0)
                        self.batchDone.emit()
                        return

            # need to mess stuff up here
            # move to correct position and capture
            label, position = self.robot.capture()
            targetLabel = label[0]
            targetPosition = self.mode.correctPositions(position)
            # If the target and label were found, move to the target, lower onto it,
            # and run the XRF if not in DEBUG.
            if (targetPosition is not None) and (DEBUG or not self.xrf.error):
                if DEBUG:
                    print(position)
                    print(targetPosition)
                    print(targetLabel)
                self.robot.sendTo(targetPosition[0][0], targetPosition[0][1])
                self.robot.lowerTo(self.mode.zEnd)
                while self.robot.checkMoving():
                    print("sleeping")
                    sleep(1)
                if not DEBUG:
                    success = self.xrf.sample(targetLabel)
                else:
                    sleep(1)
                    success = True
                # send signal
                self.sampleStatusOK.emit(i + 1, success)
            else:
                if not DEBUG:
                    self.xrf.reset()
                self.sampleStatusOK.emit(i + 1, False)
            i += 1
            self.robot.setHeight(self.mode.zStart)
        self.robot.sendTo(0, 0, 0)
        self.batchDone.emit()


def correctPositions(positions, xrfXOffset, xrfYOffset):
    ret = []
    for position in positions:
        if position is not None:
            p0 = max(float(position[0]) + xrfXOffset, 0)
            # p0 = min(p0, 45)
            p1 = float(position[1]) + xrfYOffset
            ret.append([f"{p0:4.3f}", f"{p1:4.3f}"])
        else:
            return None
    return ret
