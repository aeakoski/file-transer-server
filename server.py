#!/usr/bin/env python
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import sys

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self):
        content = ""
        with open("www/index.html", "r") as target:
            content = target.read()
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html())

    def do_POST(self):
        print("GOT POST")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        #print(post_data)
        pd = post_data.split(b"\r\n")

        with open("inbox/data"+str(time.time()), "wb") as fd:
            fd.write(b"\r\n".join(pd[4:-6]))
        self._set_headers()
        self.wfile.write(self._html("POST!"))

def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8080):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print("Starting http server on", addr, port)
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        run(port = int(sys.argv[1]))
    except Exception:
        print("Psst. Supply a serverport as an argument if 8000 does not float yor goat")
        run()
