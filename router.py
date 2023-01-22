import logging
import re
import os

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

def filter(string):
    found_match = re.search('[\[\]<>\{\}|\\^ ]', string)
    return True if found_match else False

def route(path):
    http_code = '400'
    # Deny bad paths
    if filter(path):
        logging.error('Malformed request path received')
        return ('400', path)
    
    # Append path ending & redirect
    valid_file_extensions = ('.html', '.css')
    if not path.endswith('/'):
        if not path.endswith(valid_file_extensions):
            return ('301', path+'/')
            
    # Route known paths else return 404 Not Found
    if re.search(r'/[a-z0-9.-/]*$', path, re.I):
        http_code = '200'
    else:
        logging.error('Unknown path %s', path)
        http_code = '404'
    return (http_code, path)

def get_content(path):
    return ('200', 'WOO')

def serve(web_addr, req_data):
    rsp_data = {'headers':{}}
    rsp_data['status_code'], rsp_data['path'] = route(req_data['path'])
    rsp_data['version'] = req_data.get('version', 'HTTP/1.0')
    rsp_data['message_body'] = ''

    match rsp_data.get('status_code', '500'):
        case '200':
            rsp_data['status_code'], rsp_data['message_body'] = get_content(req_data['path'])
        case '301':
            rsp_data['headers']['Location'] = web_addr + rsp_data['path']
    return rsp_data

