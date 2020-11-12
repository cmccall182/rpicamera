from threading import Thread
import os
import time
import re
import sys
import cv2
import imutils
import datetime
import numpy as np
import cfg
   
class camera_measuring(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.last_capture = None
        self.average = None
        self.daemon = True
        
        self.start()
    
    def run(self):
        time.sleep(10)
        motion_count = 0
        output = None
        while (cfg.process_state == "measuring"):
            if(not os.path.isdir("/mnt/database/images/" + datetime.datetime.now().strftime('%Y-%m-%d'))):
                os.makedirs("/mnt/database/images/" + datetime.datetime.now().strftime('%Y-%m-%d'))
            path = '/mnt/database/images/' + datetime.datetime.now().strftime('%Y-%m-%d') + '/' + datetime.datetime.now().strftime('%H:%M:%S') +'.jpg';
            
            
            if np.array_equal(output,cfg.camera_buffer):
                print("images are the same")
                continue
            
            output = cfg.camera_buffer

                
            output = imutils.resize(output, width=500)
            gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21,21), 0)
            
            if self.last_capture is None:
                #background calculation
                self.last_capture = gray.copy().astype("float")
                continue
            
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
                
                if motion_count >= 8:
                    print("image captured")
                    self.last_capture = gray.copy().astype("float")
                    cv2.imencode('.jpeg', output)
                    cv2.imwrite(path, output)
                    motion_count = 0
                    
            time.sleep(.01)
