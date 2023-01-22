import logging
import re
import os.path

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
        req_file_content = open(root_folder+'/notfound.html').read()

    return (http_code, req_file, req_file_content)

def serve(web_addr, content_root_folder, req_data):
    rsp_data = {'headers':{}}
    rsp_data['status_code'], rsp_data['path'] = route(req_data['path'])
    rsp_data['version'] = req_data.get('version', 'HTTP/1.0')
    rsp_data['message_body'] = ''

    match rsp_data.get('status_code', '500'):
        case '200':
            rsp_data['status_code'], rsp_data['path'], rsp_data['message_body'] = get_content(content_root_folder, req_data['path'])
        case '301':
            rsp_data['headers']['Location'] = web_addr + rsp_data['path']
    logging.debug(f'Response: {rsp_data}')
    return rsp_data

