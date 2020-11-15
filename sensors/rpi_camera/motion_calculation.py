import cv2
import imutils
import numpy as np
   
class motionDetect():
    def __init__(self):
        self.last_capture = None

    def detect_motion(frame):
        motion_count = 0
        
        if np.array_equal(frame,self.last_capture):
            #same frame
            return False
        
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21,21), 0)
        
        if self.last_capture is None:
            #background calculation
            self.last_capture = gray.copy().astype("float")
            return False
        
        cv2.accumulateWeighted(gray, self.last_capture, 0.5)
        delta = cv2.absdiff(gray, cv2.convertScaleAbs(self.last_capture))
        
        thresh = cv2.threshold(delta, 5, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        counts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        counts = imutils.grab_contours(counts)
        
        for c in counts:
            if cv2.contourArea(c) < 5000:
                continue
            #change detected
            motion_count += 1
            
            if motion_count >= 20:
                self.last_capture = gray.copy().astype("float")
                cv2.imencode('.jpeg', output)
                cv2.imwrite(path, output)
                motion_count = 0
                return True
        return False