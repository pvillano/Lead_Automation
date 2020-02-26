import mk2Camera
import cv2
import numpy as np

if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    while(True):
        ret, frame = cap.read()
        processed,center = mk2Camera.processColor(frame, color1=np.array([0,0,0]), color2=np.array([255,255,40]), minSize=170, maxSize=230)
        print(center)
        cv2.imshow('frame',processed)
        if cv2.waitKey() & 0xFF == ord('q'):
            break
  
    cv2.destroyAllWindows()
    cap.release()
