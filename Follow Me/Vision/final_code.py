import cv2
import sys
import os
import time
from deepsort.object_detection import HumanDetector
from deep_sort_realtime.deepsort_tracker import DeepSort

def main():
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
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print("Video capture not opened")
        sys.exit(-1)

    human = HumanDetector()
    tracker = DeepSort(
        max_iou_distance=0.7,
        max_age=20,
        n_init=10,
        nms_max_overlap=1.0,
        max_cosine_distance=0.2,
        nn_budget=None,
        gating_only_position=False,
        override_track_class=None,
        embedder="mobilenet",
        half=True,
        bgr=True,
        embedder_gpu=True,
        embedder_wts=None,
        polygon=False,
        today=None
    )

    start_time = time.time()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame,(640,480))
        if not ret:
            print("Empty frame")
            break

        detections, width_ratio, height_ratio = human.detect(frame)
        img = human.draw(frame)
        
        raw_detect = human.yolo2deep()
        tracks = tracker.update_tracks(raw_detect, frame=frame)
        img = human.drawbbs(img, tracks)

        # Calculate FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time

        cv2.putText(
            img,
            f"FPS: {fps:.2f}",
            (10, 30),  # Coordinates of the text
            cv2.FONT_HERSHEY_SIMPLEX,
            1,  # Font scale
            (0, 255, 0),  # Text color in BGR
            2,  # Thickness
            cv2.LINE_AA,  # Line type
        )
        cv2.imshow('Combined Stream', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    os.environ['GST_DEBUG'] = '3'
    main()
