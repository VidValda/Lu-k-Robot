import cv2

from deepsort.object_detection import HumanDetector
from deep_sort_realtime.deepsort_tracker import DeepSort

if __name__ == "__main__":
   
    capture = cv2.VideoCapture(0)
    human = HumanDetector()
    tracker = DeepSort(
        max_iou_distance=0.7,
        max_age=200,
        n_init=3,
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

    while (capture.isOpened()):
        
        ret, frame = capture.read()
        detections, width_ratio, height_ratio = human.detect(frame)
        img = human.draw(frame)
        raw_detect = human.yolo2deep()
        tracks = tracker.update_tracks(raw_detect, frame=frame) # bbs expected to be a list of detections, each in tuples of ( [left,top,w,h], confidence, detection_class )
        img = human.drawbbs(img,tracks)

        

        cv2.imshow('webCam',img)

        if (cv2.waitKey(1) == ord('s')):
            break

    capture.release()
    cv2.destroyAllWindows()