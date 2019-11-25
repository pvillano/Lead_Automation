import serial

PORT = 'COM8'

class Gantry():
    def __init__(self):
        self.ser = serial.Serial(PORT)
        self.ser.baudrate = 115200
        #getLine(self.ser) #Clear 1st line on serial
        self.verbose = True
        self.moving = False

    def sendTo(self, x, y):
        self.moving = True
        command = "g0 x"+str(x)+" y"+str(y)+"\n"
        sendLine(self.ser, command.encode('utf-8'))
        getLine(self.ser)
        while (self.checkMoving()):
            pass
        return

    def home(self):
        self.moving = True
        command = "g28.2 x0 y0\n"
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
            getState = "$stat\n"
            sendLine(self.ser, getState.encode('utf-8'))
            ret = getLine(self.ser)
            getLine(self.ser)
            self.moving = (ret[-4:-1]=='Run')
        return self.moving

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
    gant.sendTo(str(50),str(100))
    gant.sendTo(str(0),str(0))
    
