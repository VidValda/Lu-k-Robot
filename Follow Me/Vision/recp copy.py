import cv2
import requests
import numpy as np
from threading import Thread
import sys

from deepsort.object_detection import HumanDetector
from deep_sort_realtime.deepsort_tracker import DeepSort


class VideoStream:
    def __init__(self, url):
        self.url = url
        self.frame = None
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        try:
            stream = requests.get(self.url, stream=True)
            bytes = b''
            for chunk in stream.iter_content(chunk_size=1024):
                    bytes += chunk
                    a = bytes.find(b'\xff\xd8')
                    b = bytes.find(b'\xff\xd9')
                    if a != -1 and b != -1:
                        jpg = bytes[a:b+2]
                        bytes = bytes[b+2:]
                        self.frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    if self.stopped:
                        stream.close()
                        break
        except requests.exceptions.ConnectionError as e:
            print("Error de conexión: ", e)
    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

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

# URL del stream de video
stream_url = 'http://192.168.43.217:5000/video'

# Inicia el stream
video_stream = VideoStream(stream_url).start()

while True:
    frame = video_stream.read()
    
    if frame is not None:
        detections, width_ratio, height_ratio = human.detect(frame)
        img = human.draw(frame)
        raw_detect = human.yolo2deep()
        tracks = tracker.update_tracks(raw_detect, frame=frame) # bbs expected to be a list of detections, each in tuples of ( [left,top,w,h], confidence, detection_class )
        img = human.drawbbs(img,tracks)  
        cv2.imshow('Frame', img)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_stream.stop()
cv2.destroyAllWindows()
