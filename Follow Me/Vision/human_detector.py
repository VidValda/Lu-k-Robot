import cv2

from deepsort.object_detection import HumanDetector



if __name__ == "__main__":
   
  capture = cv2.VideoCapture(0)
  human = HumanDetector()
  while (capture.isOpened()):
      ret, frame = capture.read()
      human.detect(frame)
      img = human.draw(frame)
      cv2.imshow('webCam',img)
      if (cv2.waitKey(1) == ord('s')):
          break
  
  capture.release()
  cv2.destroyAllWindows()