import serial

PORT = 'COM4'

class Gantry():
    def __init__(self):
        self.ser = serial.Serial(PORT)
        getLine(self.ser) #Clear 1st line on serial
        self.verbose = True
        self.moving = False

    def sendTo(self, x, y):
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
        return self.moving

    def close(self):
        self.ser.close()

def getLine(ser):
  ser_bytes = ser.readline()
  decoded_bytes = (ser_bytes[0:len(ser_bytes)-2].decode('utf-8'))
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
    ser = serial.Serial('COM3')
    ser.baudrate = 115200
    print(ser)
    t=input('Press q to exit\n')
    while(t != 'q'):
        ser_bytes = ser.read(10)
        print(ser_bytes)
        decoded_bytes = ser_bytes.decode('utf-8')
        print(decoded_bytes)
        #t=input('Press q to exit\n')
