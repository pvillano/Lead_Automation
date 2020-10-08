import mk2Camera
import cv2
import numpy as np

if __name__ == "__main__":
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        processed, center = mk2Camera.processFrame(frame)
        print(center)
        cv2.imshow("frame", processed)
        if cv2.waitKey() & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    cap.release()
