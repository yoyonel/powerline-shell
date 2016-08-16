# url: https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
import simplejson
import logging
import os


# url: http://stackoverflow.com/questions/13180720/maintaining-logging-and-or-stdout-stderr-in-python-daemon
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# url: http://stackoverflow.com/questions/4906977/access-environment-variables-from-python
fh = logging.FileHandler(os.environ["PLS_PATH"]+"/logs/"+"pls_httpserver.log")
# fh = logging.NullHandler()
logger.addHandler(fh)


class LocalData(object):
    """

    """
    records = {}
    lock = threading.Lock()


class HTTPRequestHandler(BaseHTTPRequestHandler):
    @staticmethod
    def get_suffix(prefix, path):
        """

        :param prefix:
        :param path:
        :return:
        """
        # urls:
        # - https://docs.python.org/2/library/re.html
        # - http://stackoverflow.com/questions/12572362/get-a-string-after-a-specific-substring
        m = re.search('(?:'+prefix+')(.*)', path)
        return m.group(1)

    def do_POST(self):
        """

        :return:
        """
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
                # recordID = self.path.split('/')[-1]
                recordID = self.get_suffix('api/v1/addrecord/', self.path)
                # LocalData.records[recordID] = data
                LocalData.lock.acquire()
                LocalData.records[recordID] = data_json
                LocalData.lock.release()
                logger.debug("record %s is added successfully" % recordID)
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return

    def do_GET(self):
        """

        :return:
        """
        if re.search('/api/v1/getrecord/*', self.path) is not None:
            # recordID = self.path.split('/')[-1]
            # m = re.search('(?:api/v1/getrecord/)(.*)', self.path)
            # recordID = m.group(1)
            recordID = self.get_suffix('api/v1/getrecord/', self.path)
            # print("recordID: ", recordID)
            # print("LocalData.records.keys():", LocalData.records.keys())
            LocalData.lock.acquire()
            if recordID in LocalData.records.keys():
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(LocalData.records[recordID])
            else:
                self.send_response(400, 'Bad Request: record does not exist')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
            LocalData.lock.release()
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
        self.server_thread = None

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
