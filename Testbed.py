import cv2
import mk2Camera

if __name__ == '__main__':
  cap = cv2.VideoCapture(0)
  while(True):
    ret, frame = cap.read()

    processed = mk2Camera.processFrame(frame)
    cv2.imshow('frame',processed)
    if cv2.waitKey() & 0xFF == ord('q'):
        break
  cap.release()
  cv2.destroyAllWindows()