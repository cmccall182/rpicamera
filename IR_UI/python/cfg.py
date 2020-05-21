#--------------------------------------------------------------------
# imports
#---------------------------------------------------------------------
import sys
import urllib.parse
import os
from picamera import PiCamera
#--------------------------------------------------------------------------
# Personal file imports
#--------------------------------------------------------------------------


#--------------------------------------------------------------------
#Global variables
#---------------------------------------------------------------------
if sys.platform == 'linux' or sys.platform == 'linux2':
    PATH_TO_INDEX = "/home/pi/IR_UI/index.html"
else:
    PATH_TO_INDEX = "\\index.html"
    
PORT = 8081
check_disk = 0
process_state = "off"
stream_tempfile_name = ""
camera_running = False
ir_running = False
camera_buffer = None
#------------------------------------------------------------------------------
# Function: parseMyURLDaddy
#
# Description: parses a URL for timestamp and potentially other info and returns
# the a dictionary of queries
#
# Inputs: Path of url
#
# Outputs: dictionary of queries
#------------------------------------------------------------------------------
def parseMyURLDaddy(file_name):
    query = urllib.parse.urlparse(file_name).query
    components = dict(qc.split("=") for qc in query.split("&"))
    return components;

#------------------------------------------------------------------------------
# Function: timeSet
#
# Description: parses a URL for timestamp and sets the time, run from IR HTML
# page
#
# Inputs: Path of url
#
# Outputs:
#------------------------------------------------------------------------------
def timeSet(file_name):
    query = urlparse(file_name).query
    components = dict(qc.split("=") for qc in query.split("&"))
    ts = ts.replace(",", " ")
    os.system("date -s '" + ts + "'")
    os.system("sudo /home/pi/stop.sh")

