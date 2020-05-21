from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import os
import datetime
import imutils
import math
import time

last_capture = None
average = None
camera = PiCamera()
camera.resolution = (640, 480)
camera_output = PiRGBArray(camera, size=(640,480))
motion_count = 0

for frame in camera.capture_continuous(camera_output, format='bgr', use_video_port=True):
#while 1:
    if(not os.path.isdir("/mnt/database/images/" + datetime.datetime.now().strftime('%Y-%m-%d'))):
        os.makedirs("/mnt/database/images/" + datetime.datetime.now().strftime('%Y-%m-%d'))
    path = '/mnt/database/images/' + datetime.datetime.now().strftime('%Y-%m-%d') + '/' + datetime.datetime.now().strftime('%H-%M-%S') +'.jpg';
    
    """
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
    heatmap = cv2.normalize(heatmap, None, 0,255, cv2.NORM_MINMAX)
    heatmap = cv2.resize(heatmap,(240,320),interpolation=cv2.INTER_CUBIC)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2GRAY)
    heatmap = cv2.GaussianBlur(heatmap, (21,21), 0)
    if last_capture is None:
        #background calculation
        last_capture = heatmap.copy().astype("float")
        camera_output.truncate(0)
        continue
    
    cv2.accumulateWeighted(heatmap, last_capture, 0.5)
    
    delta = cv2.absdiff(heatmap, cv2.convertScaleAbs(last_capture))
    
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
            setup_led.blink()
            measure_led.blink()
            last_capture = heatmap.copy().astype("float")
            heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
            cv2.imencode('.jpeg', heatmap)
            cv2.imwrite(path, heatmap)
            motion_count = 0
    time.sleep(1)
    """
    
    output = frame.array
    output = imutils.resize(output, width=500)
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)
    
    if last_capture is None:
        #background calculation
        last_capture = gray.copy().astype("float")
        camera_output.truncate(0)
        continue
    
    cv2.accumulateWeighted(gray, last_capture, 0.5)
    delta = cv2.absdiff(gray, cv2.convertScaleAbs(last_capture))
    
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
            last_capture = gray.copy().astype("float")
            cv2.imencode('.jpeg', output)
            cv2.imwrite(path, output)
            motion_count = 0
    camera_output.truncate(0)
