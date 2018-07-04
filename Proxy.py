import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import urllib3

with open('config.json', 'r') as f:
    config = json.load(f)

# Proxy server setting
HOST_NAME = 'localhost'
PORT_NUMBER = config['PORT_NUMBER']

# Maximo setting
BASE_MAXIMO_URL = config['BASE_MAXIMO_URL']
HEADER = {'MAXAUTH': config['MAXAUTH']}

def log(message):
    print(time.asctime(), message)

def log_failure(e):
    with open('logs\\response_ERR_%s.txt' % time.strftime('%Y-%m-%d-%H-%M-%S'), 'w') as f:
        f.write(str(e))
        
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = BASE_MAXIMO_URL + self.path
        log('Sending request to: %s' % url )
        try:
            response = requests.post(url, headers=HEADER)
            with open('response_%s.txt' %time.asctime(), 'w') as f:
                f.write('Reponse: %s : %s' % (response.status_code, response.reason))
        except requests.exceptions.Timeout as e:
            log("A timeout occured")
            #log_failure(e)
        except requests.exceptions.RequestException as e: 
            log("Other Request failures")
            log_failure(e)
        except:
            log("Other failures")


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
