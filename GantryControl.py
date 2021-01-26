import serial, json
from PyQt5.QtCore import QObject, pyqtSignal

PORT = "COM8"
# tinyG controller, takes g code, does jerk limited motion
# TODO link tinyG wiki
# Wrapper for hardware communications.
class Gantry(QObject):
    # Hook to let GUI view current position- not in current use.
    positionChanged = pyqtSignal(str, str)

    def __init__(self):
        super(Gantry, self).__init__()
        self.ser = serial.Serial(PORT)
        self.ser.baudrate = 115200
        self.verbose = True
        self.moving = False

    def lowerTo(self, z):
        """
        motion with limit switch, if it is still attached...
        """
        self.moving = True
        command = "g38.2 z" + str(z) + " f800\n"
        self.sendLine(command.encode("utf-8"))
        self.getLine()
        while self.checkMoving():
            pass
        return

    def setZ(self, z):
        #
        self.moving = True
        command = "g0 z" + str(z) + "\n"
        self.sendLine(command.encode("utf-8"))
        self.getLine()
        while self.checkMoving():
            pass
        return

    def sendTo(self, x, y, z=None):
        self.moving = True
        if z is not None:
            command = "g0 x" + str(x) + " y" + str(y) + " z" + str(z) + "\n"
        else:
            command = "g0 x" + str(x) + " y" + str(y) + "\n"
        # print(command)
        self.sendLine(command.encode("utf-8"))
        self.getLine()
        while self.checkMoving():
            pass
        self.positionChanged.emit(x, y)
        # print("Finished move")
        return

    def home(self):
        self.moving = True
        command = "g28.2 x0 y0 z0\n"
        self.sendLine(command.encode("utf-8"))
        self.getLine()
        while self.checkMoving():
            pass
        return

    def checkMoving(self):
        """
        try to get stopped signal
        """
        if self.moving:
            getState = '{"stat":n}\n'
            self.sendLine(getState.encode("utf-8"))
            ret = self.getLine()
            # print(ret)
            ret = json.loads(ret)
            if "r" not in ret.keys():
                self.moving = True
                return True
            if "stat" not in ret["r"].keys():
                self.moving = True
                return True
            state = ret["r"]["stat"]
            if state == 5 or state == 7 or state == 9:
                self.moving = True
            else:
                self.moving = False
        return self.moving

    def close(self):
        self.ser.close()

    def getLine(self):
        ser_bytes = self.ser.readline()
        decoded_bytes = ser_bytes.decode("utf-8")
        self.ser.flush()
        return decoded_bytes

    def sendLine(self, data):
        self.ser.write(data)
        self.ser.flush()


if __name__ == "__main__":
    gant = Gantry()
    gant.sendTo(str(50), str(100))
    gant.sendTo(str(0), str(0))
