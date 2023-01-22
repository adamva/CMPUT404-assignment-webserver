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
        httpRequest (dict): A dict containing the request line, headers, and message body
    """
    httpRequest = {}
    split_data = raw_data.splitlines()

    # Parse the request line
    request_line = split_data[0].split()
    httpRequest["method"] = request_line[0]
    httpRequest["path"] = request_line[1]
    httpRequest["version"] = request_line[2]

    # Parse the headers
    message_body_idx = 0
    for i in range(1, len(split_data)):
        # Stop reading headers when message body reached
        if split_data[i] == '':
            message_body_idx = i + 1
            break
        else: 
            header = split_data[i].split(': ')
            httpRequest[header[0]] = header[1]
    # Join message body back together
    httpRequest['message_body'] = "\n".join(split_data[message_body_idx:len(split_data)])
    return httpRequest
    