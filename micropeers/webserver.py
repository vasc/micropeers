#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class MicropeersServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write( 'hello\n' )
        self.wfile.write(self.path)

    @staticmethod
    def serve_forever(port):
        HTTPServer(('', port), MicropeersServer).serve_forever()


if __name__ == "__main__":
    MicropeersServer.serve_forever(8484)
