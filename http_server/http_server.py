# url: https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
import simplejson
import logging


# url: http://stackoverflow.com/questions/13180720/maintaining-logging-and-or-stdout-stderr-in-python-daemon
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# fh = logging.FileHandler("./daemon-docker.log")
fh = logging.NullHandler()
logger.addHandler(fh)


class LocalData(object):
    records = {}


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if re.search('/api/v1/addrecord/*', self.path) is not None:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # print("ctype:", ctype)
            if ctype == 'application/json':
                length = int(self.headers.getheader('content-length'))
                data = self.rfile.read(length)
                # url: http://stackoverflow.com/questions/31371166/reading-json-from-simplehttpserver-post-data
                data_json = simplejson.loads(data)
                # print("data:", data)
                # print("=> {}".format(simplejson.loads(data)))
                # data = cgi.parse_qs(data, keep_blank_values=1)
                recordID = self.path.split('/')[-1]
                # LocalData.records[recordID] = data
                LocalData.records[recordID] = data_json
                logger.debug("record %s is added successfully" % recordID)
            else:
                data = {}
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return

    def do_GET(self):
        if re.search('/api/v1/getrecord/*', self.path) is not None:
            recordID = self.path.split('/')[-1]
            # print("recordID: ", recordID)
            # print("LocalData.records.keys():", LocalData.records.keys())
            if recordID in LocalData.records.keys():
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(LocalData.records[recordID])
            else:
                self.send_response(400, 'Bad Request: record does not exist')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)


class SimpleHttpServer():
    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    def addRecord(self, recordID, jsonEncodedRecord):
        LocalData.records[recordID] = jsonEncodedRecord

    def stop(self):
        self.server.shutdown()
        self.waitForThread()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('port', type=int, help='Listening port for HTTP Server')
    parser.add_argument('ip', help='HTTP Server IP')
    args = parser.parse_args()

    server = SimpleHttpServer(args.ip, args.port)
    logger.debug('HTTP Server Running...........')
    server.start()
    server.waitForThread()
