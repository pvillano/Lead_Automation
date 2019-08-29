import cv2
import mk2Camera
import serial
from time import sleep

PORT = '/dev/cu.usbmodem14201'
xCenter = 360
yCenter = 640
pixelsToMM = 23.4

def sendTo(ser, x, y):
  if ser is None:
    ser = serial.Serial(PORT)
  xPos = 0
  yPos = 0
  line1 = getLine(ser)
  if ("Enter target x:" != line1):
    print(line1)
    return
  sendLine(ser, x)
  line2 = getLine(ser)
  if ("Enter target y:" != line2):
    print(line2)
    return
  sendLine(ser, y)
  pos1 = getLine(ser)
  xPos, yPos = sortData(pos1, xPos, yPos)
  pos2 = getLine(ser)
  xPos, yPos = sortData(pos2, xPos, yPos)
  print("Arrived at ("+str(xPos)+", "+str(yPos)+")")

def sortData(pos, x, y):
  if 'x' == pos[0]:
    x = pos[16:]
    y = y
  if 'y' == pos[0]:
    y = pos[16:]
    x = x
  return x, y

def getLine(ser):
  ser_bytes = ser.readline()
  decoded_bytes = (ser_bytes[0:len(ser_bytes)-2].decode('utf-8'))
  ser.flush()
  return decoded_bytes

def sendLine(ser, data):
  ser.write(str(data))
  ser.flush()

def tryToFindLabel(cap, t):
  i = 0
  while i < t:
    ret, frame = cap.read()
    processed, label = mk2Camera.processFrame(frame)
    if "" != label:
      print("Found label")
      i = t
    cv2.imshow('processView',processed)
    cv2.waitKey(1)
    i+=1
  return label

def tryToFindTape(number, x, y, ser, cap):
  i = 0
  while i < number:
    ret, frame = cap.read()
    processed, center = mk2Camera.processColor(frame)
    cv2.imshow('processView',processed)
    cv2.waitKey(1)
    if center is not None:
      break
    i+=1
  if center is not None:
    xTarget = (center[1] - xCenter)/pixelsToMM
    yTarget = (yCenter - center[0])/pixelsToMM
    sendTo(ser, str.format("%4.3f"%(x+xTarget)), str.format("%4.3f"%(y+yTarget)))
    sleep(1)
    print("Taking pictures")
    ret, frame = cap.read()
    ret, frame = cap.read()
    cv2.imshow('processView',frame)
    name = str(y)+".jpg"
    cv2.imwrite(name, frame)
    cv2.waitKey(500)
    return (str.format("%4.3f"%(x+xTarget)), str.format("%4.3f"%(y+yTarget)))
  else:
    print("Could not find tape")
    return None

def readLabels(number, x, y, ser, cap):
  labels = []
  positions = []
  for n in range(number):
    yTarget = y-(n*65.3)
    sendTo(ser, x, yTarget)
    labels.append(tryToFindLabel(cap, 20))
    cX = x+25
    sendTo(ser, cX, yTarget)
    center = tryToFindTape(20, cX, yTarget, ser, cap)
    if center is None:
      cX = x+50
      sendTo(ser, cX, yTarget)
      center = tryToFindTape(20, cX, yTarget, ser, cap)
      if center is None:
        cX = x+75
        sendTo(ser, cX, yTarget)
        center = tryToFindTape(20, cX, yTarget, ser, cap)
    positions.append(center)
  return labels, positions

def singlePass(number):
  cap = cv2.VideoCapture(0)
  ser = serial.Serial(PORT)
  print(getLine(ser))
  labels, positions = readLabels(number, -50, 0, ser, cap)
  sendTo(ser, 0, 0)
  cap.release()
  ser.close()
  return(labels, positions)


if __name__ == '__main__':
  singlePass(8);
'''
  while(True):
    ret, frame = cap.read()
    processed = mk2Camera.processFrame(frame)
    cv2.imshow('frame',processed)
    if cv2.waitKey() & 0xFF == ord('q'):
        break
  
  cv2.destroyAllWindows()'''