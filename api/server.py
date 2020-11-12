#--------------------------------------------------------------------
# imports
#---------------------------------------------------------------------
import http.server
import socketserver
from socketserver import ThreadingMixIn
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import threading
import time
import math
import cv2
import os
import numpy as np
import logging
from tempfile import NamedTemporaryFile
import datetime
import imutils

# Operating system portability- if not on a linux machine, you aren't using
# a raspberry pi, and thus the camera module won't work
if sys.platform == 'linux' or sys.platform == 'linux2':
    sys.path.append(os.getcwd() + '/python')
    make_done_dir = "sudo mkdir done"
    rm_done_dir = "sudo rmdir done"
    check_done_dir = "/home/pi/IR_UI/done"
    rm_mnt = "sudo rmdir /mnt"
    mkdir_mnt = "sudo mkdir /mnt"
    delete_zips_from_mnt = "rm /mnt/*.zip"
    
else:
    sys.path.append(os.getcwd() + '\\python')
    make_done_dir = ""
    rm_done_dir = ""
    check_done_dir = ""
    rm_mnt = ""
    mkdir_mnt = ""

#--------------------------------------------------------------------------
# Personal file imports, path of files is determined in operating system
# guards above
#--------------------------------------------------------------------------
import cfg
import zipHandler
import heartbeat
import cameraThread
import calculationThreads
#------------------------------------------------------------------------------
# Class: Request_Handler
#
# Description: the server logic
#
# Inputs: BaseHTTPRequestHandler
#
# Outputs: Server Threads for handling requests
#------------------------------------------------------------------------------
class Request_Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
#           Portability
            if sys.platform == 'linux' or sys.platform == 'linux2':
                file_name = os.getcwd() + self.path
                                        
            else:
                file_name = os.getcwd() + self.path.replace('/', '\\')
                
#---------------calculate path and type of file----------------------
            if file_name.endswith("favicon.ico"):
                mime_type = 'image/x-icon'
                file_size = os.path.getsize(file_name)
                self.sendHeaders(mime_type, file_size)
                self.fileTransfer(file_name)
                
            if file_name.endswith("index.html" or "/"):
                mime_type = 'text/html'
                file_size = os.path.getsize(cfg.PATH_TO_INDEX)
                self.sendHeaders(mime_type, file_size)
                self.fileTransfer(cfg.PATH_TO_INDEX)

            elif file_name.endswith("stream.html"):
                mime_type = 'text/html'
                file_size = os.path.getsize(file_name)
                self.sendHeaders(mime_type, file_size)
                self.fileTransfer(file_name)

            elif file_name.endswith(".html"):
                mime_type = 'text/html'
                file_size = os.path.getsize(file_name)
                self.sendHeaders(mime_type, file_size)
                self.fileTransfer(file_name)

            elif file_name.endswith(".css"):
                mime_type = 'text/css'
                file_size = os.path.getsize(file_name)
                self.sendHeaders(mime_type, file_size)
                self.fileTransfer(file_name)

            elif file_name.endswith(".js"):
                mime_type = 'application/javascript'
                file_size = os.path.getsize(file_name)
                self.sendHeaders(mime_type, file_size)
                self.fileTransfer(file_name)

            #stop everything, delete old zips, zip/send file, restart processes
            elif '.zip' in file_name:
                temp_state = cfg.process_state
                cfg.process_state = "off"
                time.sleep(2)
                os.system(delete_zips_from_mnt)
                
                mime_type = 'application/zip'
                new_file_name = zipHandler.zipfileHandler(file_name)
                print('new_file_name: ' + new_file_name)

                file_size = os.path.getsize(new_file_name)
                self.sendHeaders(mime_type, file_size)
                self.fileTransfer(new_file_name)
                
                os.system(delete_zips_from_mnt)
                cfg.process_state = temp_state
                calculationThread.camera_measuring()

#           status bar displayed on webpage
            elif "getStatus" in file_name:
                mime_type = 'text/plain'
                file_size = len(cfg.process_state)
                self.sendHeaders(mime_type, file_size)
                self.wfile.write(cfg.process_state.encode("utf-8"))

#---------------Non-file handlers-----------------------------------------
            elif "stream.mjpg" in file_name:
                mime_type = 'multipart/x-mixed-replace; boundary=FRAME'
                self.sendHeaders(mime_type, 0)
                if os.path.isdir(check_done_dir):
                    os.system(rm_done_dir)
                cfg.process_state = "setup"
                self.camera_streaming()
                
                    
            elif "done.dat" in file_name:
                self.send_response(200)
                self.end_headers()
                urldict = cfg.parseMyURLDaddy(file_name)
                cfg.process_state = "measuring"
                
                if sys.platform == 'linux' or sys.platform == 'linux2':
                    #update date time so that new folders are accurate
                    ts = urldict["ts"]
                    ts = ts.replace(",", " ")
                    os.system("date -s '" + ts + "'")
                    os.system(make_done_dir)
                    
                else:
                    pass
                
                #start measuring thread
                calculationThreads.camera_measuring()
                
#           process handlers for IR data collection
#           restart IR
            elif "startIR" in file_name:
                cfg.process_state = "off"
                print("IR restarting")
                time.sleep(2)
                print("IR running")
                cfg.process_state = "measuring"
                mime_type = 'text/html'
                file_size = os.path.getsize(cfg.PATH_TO_INDEX)
                self.sendHeaders(mime_type, file_size)
                self.fileTransfer(cfg.PATH_TO_INDEX)
                print("started measuring thread")
                calculationThreads.camera_measuring()

            #halt collection
            elif "stopIR" in file_name:
                print("IR stopped")
                cfg.process_state = "off"
                mime_type = 'text/html'
                file_size = os.path.getsize(cfg.PATH_TO_INDEX)
                self.sendHeaders(mime_type, file_size)
                self.fileTransfer(cfg.PATH_TO_INDEX)
                
#           #delete data and turn collection off
            elif "resetPI" in file_name:
                print("Resetting Pi")
                os.system(rm_mnt)
                os.system(mkdir_mnt)
                cfg.process_state = "off"
                mime_type = 'text/html'
                file_size = os.path.getsize(cfg.PATH_TO_INDEX)
                self.sendHeaders(mime_type, file_size)
                self.fileTransfer(cfg.PATH_TO_INDEX)

            elif "squigglyshit" in file_name:
                print("lol")
                
#-----------invaLid path---------------------------------------------------
        except IOError as e:
            print(str(e))
            self.send_error(404)
            
        finally:
            pass

#------------------------------------------------------------------------------
# Function: Request_Handler.sendHeaders
#
# Description: sends file headers to client
#
# Inputs: self, mime_type, file_size
#
# Outputs: None
#------------------------------------------------------------------------------
    def sendHeaders(self, mime_type, file_size):

        if((mime_type == 'multipart/x-mixed-replace; boundary=FRAME')):
    #-----------this is the stream-------------------
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', mime_type)
            self.end_headers()
            
    #--------if zip file------------------------------------------------------
        elif(mime_type == "application/zip"):
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.end_headers()
            
        else:
    #-------if sending a file of CSS, JS, HTML
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', file_size)
            self.end_headers()
#------------------------------------------------------------------------------
# Function: Request_Handler.fileTransfer
#
# Description: sends file to client
#
# Inputs: self, file_name
#
# Outputs: None
#------------------------------------------------------------------------------
    def fileTransfer(self, file_name):
        f = open(file_name, 'rb')
        for line in f:
                self.wfile.write(line)
        f.close()
        
#------------------------------------------------------------------------------
# Function: Request_Handler.fileTransfer
#
# Description: sends file to client
#
# Inputs: self, file_name
#
# Outputs: None
#------------------------------------------------------------------------------        
    def camera_streaming(self):
        nmin = 0
        nmax = 255
        alpha1 = 0.5
        alpha2 = 0.5
        time.sleep(4)
        while( cfg.process_state == "setup"):                
            frame = cfg.camera_buffer
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
            frame = cv2.addWeighted(frame, alpha1, heatmap, alpha2,0)
            #cv2.putText(frame, 'Ambient: ' +  str(np.mean(data)), (10,10),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,255,255),1,cv2.CV_AA)
            cv2.imencode('.jpeg', frame)
            
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
                
#------------------------------------------------------------------------------
# Class: ThreadingTCPServer
#
# Description: Server class that handles requests through threads
#
# Inputs: ThreadingMixIn, HTTPServer
#
# Outputs: None
#------------------------------------------------------------------------------
class ThreadingTCPServer(ThreadingMixIn, HTTPServer):
    pass

#-----------------------------------------------------------------------------
# Run Request_Handler as a threading TCP server, this is basically main
#-----------------------------------------------------------------------------
with ThreadingTCPServer(("", cfg.PORT), Request_Handler) as httpd:
    try:
        if os.path.isdir(check_done_dir):
            cfg.process_state = "measuring"
            print("started measuring thread")
            calculationThreads.camera_measuring()
            
        heartbeat.heartbeat()
        print("started heartbeat")
        
        cameraThread.cameraThread()
        
        print("started camera thread, serving forever")
        httpd.serve_forever()
        
    except Exception as e:
        print(str(e))
        
    finally:
        print("CAMERA IS CLOSING")
        heartbeat.heartbeat.join(self)
        cameraThread.cameraThread.join(self)
        selfcalculationThreads.camera_measuring(self)
        print("CAMERA IS CLOSED")
        httpd.server_close()
        httpd.shutdown()
