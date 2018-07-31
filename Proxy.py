""" 
   Copyright 2018 OSIsoft, LLC.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json

with open('config.json', 'r') as f:
    config = json.load(f)

# Proxy server setting
HOST_NAME = '10.54.51.132'
PORT_NUMBER = config['PORT_NUMBER']

# Maximo setting
BASE_MAXIMO_URL = config['BASE_MAXIMO_URL']
HEADER = {'MAXAUTH': config['MAXAUTH']}

def log(message):
    print(time.asctime(), message)

def log_failure(e):
    with open('logs\\response_ERR_%s.txt' % time.strftime('%Y-%m-%d-%H-%M-%S'), 'w') as f:
        f.write(str(e))
        
session = requests.Session()
class MyHandler(BaseHTTPRequestHandler):
    def createRequest(self):
        # We update the format, from a request from Notifications to a request appropriate to Maximo
        url = BASE_MAXIMO_URL + self.path
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        params = json.loads((post_body).decode('utf-8'))
        request = requests.Request('POST', url, params=params, headers=HEADER).prepare()
        request.url = request.url.replace('%3A', ':').replace('%2B','%2b')
        return request
        
    def do_POST(self):
        request = self.createRequest()
        log('Sending request to: %s' % request.url)
        # We send the response and log success and failures
        try:
            response = session.send(request)
            with open('logs\\response_%s.txt' % time.strftime('%Y-%m-%d-%H-%M-%S'), 'w') as f:
                f.write('Reponse: %s : %s\r\n' % (response.status_code, response.reason))
                f.write(response.text)
        except requests.exceptions.Timeout as e:
            # If Maximo is on a different network, timeouts can occur.
            # You can force a retry to connect after x minutes, etc. in this block
            log("A timeout occured")
        except requests.exceptions.RequestException as e: 
            log("Other Request failures")
            log_failure(e)
        except:
            log("Other failures")
            log_failure(e)
        
        self.send_response(200)
        self.end_headers()
        
if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    log('Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    print('Hit control-c to stop server')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    log('Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
