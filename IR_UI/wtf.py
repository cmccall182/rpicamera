import http.server
import socketserver
import os
from zipfile import ZipFile
from http.server import BaseHTTPRequestHandler

PAGE="""\
<html>

<head>
  <title>luhmao</title>
  <link rel="stylesheet" type="text/css" href="css/foopicker.css">
  <link rel="stylesheet" type="text/css" href="css/containerCSS.css">
  <script type="text/javascript" src="js/foopicker.js"></script>
  <script type="text/javascript" src="js/grabDataButton.js"></script>
  <script type="text/javascript" src="js/grabTimeDataButton.js"></script>

  <style type="text/css">
    .container {
      width: 250px;
    }

    label {
      color: #999;
      display: block;
      font-size: 14px;
      font-family: 'Source Sans Pro', sans-serif;
    }

    input[type="text"] {
      padding: 10px;
      width: 100%;
    }
  </style>
</head>

<body>
  <div class="container">
    <label>START DATE</label>
    <input type="text" id="datepicker" value="22-Jul-2019"/>
  </div>
  <br/>
  <div class="container">
    <div>
    <label>END DATE</label>
    <input type="text" id="datepicker2" value="22-Jul-2019"/>
  </div>
  </div>


</body>

</html>
"""


PORT = 8080
curdir = os.getcwd()

def get_all_file_paths(directory): 
        file_paths = [] 

        for root, directories, files in os.walk(directory): 
                for filename in files: 
                        filepath = os.path.join(root, filename) 
                        file_paths.append(filepath) 

        return file_paths  
         
class Request_Handler(BaseHTTPRequestHandler):
        def do_GET(self):
                if self.path == '/index.html':
                        content = PAGE.encode('utf-8')
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/html')
                        self.send_header('Content-Length', len(content))
                        self.end_headers()
                        self.wfile.write(content)
                elif self.path == '/css/foopicker.css':
                        f_name = os.getcwd() + self.path.replace('/', '\\')
                        f = open(f_name, "rb") 
                        self.send_response(200)
                        self.send_header('Content-type', 'text/css')
                        self.end_headers()
                        self.wfile.write(f.read())
                        f.close()
                elif self.path == '/css/containerCSS.css':
                        f_name = os.getcwd() + self.path.replace('/', '\\')
                        f = open(f_name, "rb") 
                        self.send_response(200)
                        self.send_header('Content-type', 'text/css')
                        self.end_headers()
                        self.wfile.write(f.read())
                        f.close()
                elif self.path == '/js/foopicker.js':
                        f_name = os.getcwd() + self.path.replace('/', '\\')
                        f = open(f_name, "rb") 
                        self.send_response(200)
                        self.send_header('Content-type', 'text/css')
                        self.end_headers()
                        self.wfile.write(f.read())
                        f.close()
                elif self.path == '/js/grabDataButton.js':
                        f_name = os.getcwd() + self.path.replace('/', '\\')
                        f = open(f_name, "rb") 
                        self.send_response(200)
                        self.send_header('Content-type', 'text/css')
                        self.end_headers()
                        self.wfile.write(f.read())
                        f.close()
                elif self.path == '/to_zip':
                        zip_path = os.getcwd() + self.path.replace('/', '\\')
                        files = get_all_file_paths(zip_path)
                        with ZipFile("test.zip", "w") as zip:
                                for file in files:
                                        zip.write(file)
                        
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/zip')
                        self.end_headers()
                        with open("test.zip", "rb") as f:
                                self.wfile.write(f.read())
                else:
                        self.send_response(301)
                        self.send_header('Location', '/index.html')
                        self.end_headers()
                return

with socketserver.TCPServer(("", PORT), Request_Handler) as httpd:
        httpd.serve_forever()
