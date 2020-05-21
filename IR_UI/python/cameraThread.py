from threading import Thread
import os
import time
import re
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera

import cfg

class cameraThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        
        try:
            self.camera = PiCamera() 
        except Exception as e:
            print(str(e))
        self.daemon = True
        self.start()
    
    def run(self):
        try:
            self.camera.resolution = (288, 368)
            self.camera_output = PiRGBArray(self.camera, size=(288, 368))
            self.camera_framerate=20
            while (1):
                while (cfg.process_state == "measuring" or cfg.process_state == "setup"):
                    for frame in self.camera.capture_continuous(self.camera_output, format='bgr', use_video_port=True):
                        cfg.camera_buffer = frame.array
                        
                        #move pointer back to index 0 to overwrite array, rather than append to infinite
                        self.camera_output.truncate(0)
                time.sleep(1)
                
        except Exception as e:
            print(str(e))
            
        finally:
            self.camera.close()
            print("hello DOPEY")
            
