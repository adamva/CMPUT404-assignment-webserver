#  coding: utf-8
# Native libraries
import logging
import socketserver
# Local files
import config as cfg
import httpRequestParser

# Global variables
logging.basicConfig(filename=cfg.LOG_FILENAME, format=cfg.LOG_FORMAT, datefmt=cfg.LOG_DATEFMT, level=cfg.LOG_LEVEL)

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2023 Adam Ahmed
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        # Get client request IP & port
        self.req_ip, self.req_port = self.request.getpeername()
        logging.info("Incoming request host: %s", self.req_ip)

        # Read HTTP request
        # TODO Ask about reading all data, the while True if not data break results in a hang
        raw_data = self.request.recv(cfg.BUFFER_SIZE).strip()

        # Bounce large requests HTTP 400
        if len(raw_data) > cfg.REQUEST_MAX_SIZE:
            logging.info("400 Bad Request for host: %s request too large\n")
            self.request.sendall(bytearray("HTTP/1.1 400 Bad Request\n\n",'utf-8'))
        else:
            logging.info(f"Parsing request size {len(raw_data)}")
            self.req_data = httpRequestParser.parse(raw_data.decode())
            # logging.info(self.req_data)
            self.request.sendall(bytearray("HTTP/1.1 200 OK\n\n",'utf-8'))

if __name__ == "__main__":

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((cfg.BIND_HOST, cfg.BIND_PORT), MyWebServer)
    logging.info(f'Started webserver at host: {cfg.BIND_HOST} port: {cfg.BIND_PORT}')

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
