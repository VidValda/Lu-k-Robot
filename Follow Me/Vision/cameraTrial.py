import cv2
import time


if __name__ == "__main__":
   
    capture = cv2.VideoCapture(2)

    start_time = time.time()
    frame_count = 0
    while (capture.isOpened()):
        
        ret, frame = capture.read()
        
        # Calculate FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time

        cv2.putText(
            frame,
            f"FPS: {fps:.2f}",
            (10, 30),  # Coordinates of the text
            cv2.FONT_HERSHEY_SIMPLEX,
            1,  # Font scale
            (0, 255, 0),  # Text color in BGR
            2,  # Thickness
            cv2.LINE_AA,  # Line type
        )

        cv2.imshow('webCam',frame)

        if (cv2.waitKey(1) == ord('s')):
            break

    capture.release()
    cv2.destroyAllWindows()