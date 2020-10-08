import numpy as np
import cv2
import time
from mk2Camera import findSticker


def nothing(x):
    pass


cap = cv2.VideoCapture(0)
cv2.namedWindow("BoroscopeView")


def buildAppContours(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (2, 2))
    edges = cv2.Canny(blur, 40, 150)
    _, contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    return img


def boxContour(img, c):
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img, [box], 0, (255, 255, 0), 2)


def buildThreshContours(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    squareKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    blur = cv2.bilateralFilter(gray, 21, 25, 255)
    ret = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, squareKernel)
    ret = cv2.adaptiveThreshold(
        ret, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2
    )
    ret = cv2.cvtColor(ret, cv2.COLOR_GRAY2RGB)
    return ret


while True:
    cLabel = ""
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame, match, text, label = findSticker(frame)
    if match:
        print("Found label " + label)
        cLabel = label
    else:
        print(text)
    cv2.imshow("BoroscopeView", frame)
    if cv2.waitKey(1) != -1:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
