import logging
import re
import os.path
from datetime import datetime

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

MIME_TYPES = {
    'html': 'text/html; charset=utf-8',
    'css': 'text/css; charset=utf-8'
}

def filter(string):
    found_match = re.search('[\[\]<>\{\}|\\^ ]', string)
    return True if found_match else False

def is_valid_file_type(filename):
    valid_file_extensions = ('.html', '.css')
    return True if filename.endswith(valid_file_extensions) else False

def route(path):
    http_code = '400'
    # Deny bad paths
    if filter(path):
        logging.error('Malformed request path received')
        return ('400', path)
    
    # Append path ending & redirect
    # TODO Redirect works in curl/browser but unit test fails...
    #   Found out that request.urlopen('https://www.google.com/foobar', None, 3) returns a code 200 regardless
    #   even google says 200 but its definetly a 301
    if not path.endswith('/'):
        if not is_valid_file_type(path):
            return ('301', path+'/')
            
    # Route known paths else return 404 Not Found
    if re.search(r'/[a-z0-9.-/]*$', path, re.I):
        http_code = '200'
    else:
        logging.error('Unknown path %s', path)
        http_code = '404'
    return (http_code, path)

def get_content(root_folder, path):
    http_code = '404'
    req_file_content = ''
    
    req_file = path+'index.html' if path.endswith('/') else path
    req_file_path = root_folder+req_file
    if os.path.isfile(req_file_path):
        logging.debug(f'Getting content for {req_file_path}')
        req_file_content = open(req_file_path).read()
        http_code = '200'
    else:
        req_file = root_folder+'/notfound.html'
        req_file_content = open(req_file).read()

    return (http_code, req_file, req_file_content)

def serve(web_addr, content_root_folder, req_data):
    rsp_data = {
        'headers': {
                'Content-Type': 'application/octet-stream',
                'Content-Length': '0'
            }
        }
    rsp_data['status_code'], rsp_data['path'] = route(req_data['path'])
    rsp_data['version'] = req_data.get('version', 'HTTP/1.0')
    rsp_data['message_body'] = ''

    rsp_data_code = rsp_data.get('status_code', '500')
    req_data_method = req_data.get('method', 'GET')
    if rsp_data_code == '500':
        logging.debug('Issuing 500 Internal Server Error')
    elif rsp_data_code == '400':
        logging.debug('Issuing 400 Bad Request')
    elif rsp_data_code == '301':
        logging.debug('Issuing 301 Redirect to %s', rsp_data['path'])
        rsp_data['headers']['location'] = web_addr + rsp_data['path']
    elif rsp_data_code == '200' and req_data_method == 'GET':
        rsp_data['status_code'], rsp_data['path'], rsp_data['message_body'] = get_content(content_root_folder, req_data['path'])
        rsp_content_type = MIME_TYPES.get(rsp_data['path'].split('.')[-1], 'application/octet-stream')
        rsp_content_length = str(len(rsp_data['message_body'].encode()))
        rsp_data['headers']['Content-Type'] = rsp_content_type
        rsp_data['headers']['Content-Length'] = rsp_content_length
    else: # Deny methods other than GET
        logging.debug('Issuing 405 Method Not Allowed for method %s', req_data_method)
        rsp_data['status_code'] = '405'

    rsp_data['headers']['date'] = datetime.utcnow().strftime('%a, %d %b %Y %T GMT')
    logging.debug(f'Response: {rsp_data}')
    return rsp_data

