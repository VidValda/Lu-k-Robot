from serial_studio import SerialStudio
from face import Expressions
from time import sleep

import communication 
import camera

class LukRobotV1:


    def __init__(self, baudrate):
        self.serstdio = SerialStudio(baudrate)
        self.face = Expressions(0,0,255)
        self.face.happy()
        self.image = 0
        sleep(3)

    def run(self):
        camera.send_video_stream()