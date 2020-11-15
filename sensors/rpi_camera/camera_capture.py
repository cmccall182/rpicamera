from picamera.array import PiRGBArray
from picamera import PiCamera
from motion_calculation import motionDetect
import time
import traceback

class rpiCamera():
    def __init__(self):
        self.camera = PiCamera() 

    def capture(self):
        motion_detection = motionDetect()
        try:
            self.camera.resolution = (288, 368)
            self.camera_output = PiRGBArray(self.camera, size=(288, 368))
            self.camera_framerate=20
            while (1):
                for frame in self.camera.capture_continuous(self.camera_output, format='bgr', use_video_port=True)
                    if (motion_detection.detect_motion(frame)):
                        #save image to mongodb
                    self.camera_output.truncate(0)
                time.sleep(1)
                
        except Exception as e:
             traceback.print_exc()
            
        finally:
            self.camera.close()
            
