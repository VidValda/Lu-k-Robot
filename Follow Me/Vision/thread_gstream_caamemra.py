import cv2
import sys
import os
import multiprocessing

from deepsort.object_detection import HumanDetector


human = HumanDetector()


def read_frames(gst_pipeline, frame_queue):
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print("Video capture not opened")
        sys.exit(-1)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Empty frame")
            break

        frame_queue.put(frame)

    cap.release()

def display_frames(frame_queue):
    while True:
        frame = frame_queue.get()

        detections, width_ratio, height_ratio = human.detect(frame)
        img = human.draw(frame)
        
        #raw_detect = human.yolo2deep()
        #tracks = tracker.update_tracks(raw_detect, frame=frame)
        #img = human.drawbbs(img, tracks)


        #frame = cv2.resize(frame,(640,480))
        cv2.imshow('UDP Stream', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def main():
    gst_pipeline = (
        "udpsrc port=5555 "
        "caps=\"application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264\" "
        " ! rtph264depay "
        " ! queue"
        " ! h264parse"
        " ! avdec_h264"
        " ! videoconvert "
        " ! appsink"
    )

    frame_queue = multiprocessing.Queue()

    # Create separate processes for reading and displaying frames
    read_process = multiprocessing.Process(target=read_frames, args=(gst_pipeline, frame_queue))
    display_process = multiprocessing.Process(target=display_frames, args=(frame_queue,))

    read_process.start()
    display_process.start()

    read_process.join()
    display_process.join()

if __name__ == '__main__':
    os.environ['GST_DEBUG'] = '3'
    main()
