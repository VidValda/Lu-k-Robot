import cv2
import requests
import numpy as np
from threading import Thread
import sys
import time

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

# URL del stream de video
stream_url = 'http://192.168.43.111:5005/video'

# Inicia el stream
video_stream = VideoStream(stream_url).start()

start_time = time.time()
frame_count = 0

while True:
    frame = video_stream.read()

    if frame is not None:

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
        cv2.imshow('Frame', frame)

        # Presiona 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video_stream.stop()
cv2.destroyAllWindows()
