import logging

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

def parse(raw_data):
    """ Parse a raw HTTP request data string and return its headers and payload
    
    Parameters:
        raw_data (string): A HTTP request string

    Returns:
        http_request (dict): A dict containing the request line, headers, and message body
    """
    http_request = {
        'method': '',
        'path': '',
        'version': '',
        'headers': {},
        'message_body': ''
    }
    split_data = raw_data.splitlines()
    logging.debug("Got split_data: %s", split_data)
    # Parse the request line
    try:
        request_line = split_data[0].split()
        logging.debug("Got request_line: %s", request_line)
    except Exception as e:
        logging.error("Could not parse raw request http status line %s", e)
        return http_request
    
    http_request['method'] = request_line[0]
    http_request['path'] = request_line[1]
    http_request['version'] = request_line[2]

    # Parse the headers
    message_body_idx = -1
    for i in range(1, len(split_data)):
        # Stop reading headers when message body reached
        if split_data[i] == '':
            message_body_idx = i + 1
            break
        header = split_data[i].split(': ')
        http_request['headers'][header[0]] = header[1]

    # Join message body back together if it exists
    if message_body_idx != -1:
        http_request['message_body'] = '\n'.join(split_data[message_body_idx:])
        logging.debug("Got a message_body: %s", http_request['message_body'])
    
    logging.debug("Returning http_request data: %s", http_request)
    return http_request
    