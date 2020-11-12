#------------------------------------------------------------------------------
# imports
#------------------------------------------------------------------------------
from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
import time
import math
import cv2
import os
import numpy as np
import logging
from tempfile import NamedTemporaryFile
#------------------------------------------------------------------------------
# Function: RunCamera
#
# Description: turns on the pi camera, overlays a heat map, and streams the
# data
#
# Inputs: None
#
# Outputs: None
#------------------------------------------------------------------------------
def RunCamera(self):
    with picamera.PiCamera(resolution='288x368', framerate=20) as camera:
        nmin = 0
        nmax = 255
        alpha1 = 0.5
        alpha2 = 0.5
        camera_output = PiRGBArray(camera, size=(288,368))
        time.sleep(2) #lets camera warm up
        try:
            for frame in camera.capture_continuous(camera_output, format="rgb"):
                frame = frame.array
                frame = cv2.flip(frame, 0)
                frame = frame[20:340, 10:250] #this does the adjustment so the heatmap is correctly overlayed on the camera image
                heatmap = np.zeros((32,24,3), np.uint8)
                data = np.fromfile('/tmp/imagedata.csv', dtype=float, count=-1, sep=',')
                index = 0
                if len(data) == 768:
                    for y in range(0,32):
                        for x in range(0,24):
                            val = (data[index]*10)-100
                            if math.isnan(val):
                                val = 0
                            if val > 255:
                                val = 255
                            heatmap[y,x] = (val,val,val)
                            index+=1
                    heatmap = cv2.flip(heatmap, -1)
                    prev_heatmap = heatmap
                heatmap = cv2.normalize(heatmap, None, nmin,nmax, cv2.NORM_MINMAX)
                heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
                heatmap = cv2.resize(heatmap,(240,320),interpolation=cv2.INTER_CUBIC)
                sharp = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
                frame = cv2.filter2D(frame, -1, sharp)
                frame = cv2.addWeighted(frame,alpha1,heatmap,alpha2,0)
                #cv2.putText(frame, 'Ambient: ' +  str(np.mean(data)), (10,10),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,255,255),1,cv2.CV_AA)
                cv2.imencode('.jpeg', frame)
                #cv2.imshow('Thermal', frame)
                camera_output.truncate(0)
                #output = frame.tosring()
                with NamedTemporaryFile() as temp:
                    name = "".join([str(temp.name),".jpeg"])
                    cv2.imwrite(name, frame)
                    f = open(name, 'rb')
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(f.read())
                    self.wfile.write(b'\r\n')
        except Exception as e:
            logging.warning(
                'Removed streaming client %s: %s',
                self.client_address, str(e))

def wTf(what_is_this):
    switcher = {
        0: "Measuring",
        1: "Streaming",
        2: "Dead",
    }
    return switcher.get(what_is_this)

