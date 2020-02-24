import serial, json
from PyQt5.QtCore import QObject, pyqtSignal

PORT = 'COM8'

class Gantry(QObject):
    positionChanged = pyqtSignal(str, str)
    
    def __init__(self):
        super(Gantry, self).__init__()
        self.ser = serial.Serial(PORT)
        self.ser.baudrate = 115200
        self.verbose = True
        self.moving = False

    def lowerTo(self, z):
        self.moving = True
        command = "g38.2 z"+str(z)+" f800\n"
        sendLine(self.ser, command.encode('utf-8'))
        getLine(self.ser)
        while (self.checkMoving()):
            pass
        return

    def setZ(self, z):
        self.moving = True
        command = "g0 z"+str(z)+"\n"
        sendLine(self.ser, command.encode('utf-8'))
        getLine(self.ser)
        while (self.checkMoving()):
            pass
        return

    def sendTo(self, x, y, z=None):
        self.moving = True
        if z is not None:
            command = "g0 x"+str(x)+" y"+str(y)+" z"+str(z)+"\n"
        else:
            command = "g0 x"+str(x)+" y"+str(y)+"\n"
        #print(command)
        sendLine(self.ser, command.encode('utf-8'))
        getLine(self.ser)
        while (self.checkMoving()):
            pass
        self.positionChanged.emit(x,y)
        #print("Finished move")
        return

    def home(self):
        self.moving = True
        command = "g28.2 x0 y0 z0\n"
        sendLine(self.ser, command.encode('utf-8'))
        getLine(self.ser)
        while (self.checkMoving()):
            pass
        return

    def sendToOld(self, x, y):
        self.moving = True
        xPos = 0
        yPos = 0
        line1 = getLine(self.ser)
        if ("Enter target x:" != line1):
            print(line1)
            return
        sendLine(self.ser, x.encode('utf-8'))
        line2 = getLine(self.ser)
        if ("Enter target y:" != line2):
            print(line2)
            return
        sendLine(self.ser, y.encode('utf-8'))
        pos1 = getLine(self.ser)
        xPos, yPos = sortData(pos1, xPos, yPos)
        pos2 = getLine(self.ser)
        xPos, yPos = sortData(pos2, xPos, yPos)
        if(self.verbose):
              print("Arrived at ("+str(xPos)+", "+str(yPos)+")")
        self.moving = False

    def checkMoving(self):
        if self.moving:
            getState = "{\"stat\":n}\n"
            sendLine(self.ser, getState.encode('utf-8'))
            ret = getLine(self.ser)
            #print(ret)
            ret = json.loads(ret)
            if "r" not in ret.keys():
                self.moving = True
                return True
            if ("stat" not in ret["r"].keys()):
                self.moving = True
                return True
            state = ret["r"]["stat"]
            if state == 5 or state == 7 or state == 9:
                self.moving = True
            else:
                self.moving = False
        return self.moving

    def getPos(self):
        getX = "{\"posx\":n}\n"
        sendLine(self.ser, getX.encode('utf-8'))
        xPos = getLine(self.ser)
        xPos = json.loads(xPos)
        xPos = xPos["r"]["posx"]
        getY = "{\"posy\":n}\n"
        sendLine(self.ser, getY.encode('utf-8'))
        yPos = getLine(self.ser)
        yPos = json.loads(yPos)
        yPos = yPos["r"]["posy"]
        return(xPos, yPos)

    def close(self):
        self.ser.close()

def getLine(ser):
  ser_bytes = ser.readline()
  decoded_bytes = (ser_bytes.decode('utf-8'))
  ser.flush()
  return decoded_bytes

def sendLine(ser, data):
  ser.write(data)
  ser.flush()

def sortData(pos, x, y):
  if 'x' == pos[0]:
    x = pos[16:]
    y = y
  if 'y' == pos[0]:
    y = pos[16:]
    x = x
  return x, y

if __name__ == '__main__':
    gant = Gantry()
    #gant.getPos()
    gant.sendTo(str(50),str(100))
    gant.sendTo(str(0),str(0))
    
