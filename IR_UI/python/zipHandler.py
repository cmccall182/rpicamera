#--------------------------------------------------------------------
#Global imports
#---------------------------------------------------------------------
import sys
import urllib.parse
import os
import time
from zipfile import ZipFile


#--------------------------------------------------------------------------
# Personal file imports
#--------------------------------------------------------------------------
import cfg
#------------------------------------------------------------------------------
# Function: zipfileHandler
#
# Description: zips certain data into a file of variable name based on the
# data/contents
#
# Inputs: Path of url/query
#
# Outputs: name of zipped file
#------------------------------------------------------------------------------
def zipfileHandler(file_name):
    filename_searched = '' #the path to the file
    filename_specific = '' #the actual file name without the path
    data = []
    dataLocation = '' #csv files directory
    imagesLocation = '' # image directory

    urldict = cfg.parseMyURLDaddy(file_name)
#---Operating system guards for portability, directory structures---------------
    if sys.platform == 'linux' or sys.platform == 'linux2':
        dataLocation = '/mnt/database/data'
        imagesLocation = '/mnt/database/images'
    else:
        dataLocation = os.getcwd() + '\\files\\mnt\\data'
        imagesLocation = os.getcwd() + '\\files\\mnt\\images'


#---request for all data or all data of a specific type------------------------
    if urldict['id'] == 'all_data':
            data = get_all_file_paths(dataLocation)
            data.extend(get_all_file_paths(imagesLocation))
            filename_specific = '/all_data'
    elif urldict['id'] == 'images':
            data = get_all_file_paths(imagesLocation)
            filename_specific = '/images'
    elif urldict['id'] == 'data':
            data = get_all_file_paths(dataLocation)
            filename_specific = '/data'
#---its a date-based download request, pathname will be in format /MM-dd-yyyy.zip
    else:
            timestamp = urldict['ts']
            int_month = timestamp[0:2]
            int_day = timestamp[3:5]
            int_year = timestamp[6:10]

            filename_specific = '/' + int_year + '-' + int_month + '-' + int_day
            filename_searched = dataLocation + filename_specific + '.csv'

            data = [dataLocation + filename_specific + '.csv', ] #specific file
            data.extend(get_all_file_paths(imagesLocation + filename_specific)) #directory yyyy-mm-dd

    os.chdir("/mnt")
    with ZipFile(filename_specific[1:] + '.zip', "a") as zip:
            for files in data:
                    zip.write(files)
                    
    print('zipfile return value: ' + filename_specific + '.zip')
    time.sleep(2)
    return "/mnt" + filename_specific + '.zip'

#------------------------------------------------------------------------------
# Function: get_all_file_paths
#
# Description: parses a URL for timestamp and sets the time, run from IR HTML
# page
#
# Inputs: Path of url
#
# Outputs:
#------------------------------------------------------------------------------
def get_all_file_paths(directory):
    #tabulates the file paths of every file in a given directory
    file_paths = []

    for root, directories, files in os.walk(directory):
            for filename in files:
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)
    return file_paths