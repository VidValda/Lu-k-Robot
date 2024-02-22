import cv2
import subprocess
import numpy as np

from deepsort.object_detection import HumanDetector
from deep_sort_realtime.deepsort_tracker import DeepSort

if __name__ == "__main__":
   
    capture = cv2.VideoCapture(0)
    human = HumanDetector()
    tracker = DeepSort(
        max_iou_distance=0.7,
        max_age=150,
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

    # Define el comando de GStreamer
    command = [
        'gst-launch-1.0 -v udpsrc port=5000 ! application/x-rtp, encoding-name=H264, payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink'
    ]
    

    # Iniciar el proceso de GStreamer
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10**8)

    while (True):
        
        # Leer los datos del proceso
        raw_frame = process.stdout.read(1280 * 720 * 3)  # Tamaño del frame (ajustar según la resolución)
        if not raw_frame:
            break

        # Convertir los datos en un array de numpy
        frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((720, 1280, 3))  # Ajustar el tamaño según la resolución

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
    # Cerrar el proceso y las ventanas
    process.terminate()
    cv2.destroyAllWindows()








