import cv2
import sys
import os
def main():
    # Define the GStreamer pipeline for receiving UDP stream
    # Adjust the caps (capabilities) as per your stream's format
    gst_pipeline = (
        "udpsrc port=5555 "
        "caps=\"application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264\" "
        " ! rtph264depay "
        " ! queue max-size-buffers=1000 max-size-bytes=0 max-size-time=0 "
        " ! h264parse "
        " ! avdec_h264 "
        " ! videoconvert "
        " ! videoscale "
        " ! appsink drop=1"
    )

    # Create a video capture object with the GStreamer pipeline
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print("Video capture not opened")
        sys.exit(-1)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Empty frame")
            break

        # Display the frame
        frame = cv2.resize(frame,(640,480))
        cv2.imshow('UDP Stream', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    os.environ['GST_DEBUG'] = '3'
    main()