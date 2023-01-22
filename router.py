import logging
import re

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
        logging.error("Malformed request path received")
        return '400'
    
    # # Only serve known web file types
    # valid_file_extension = ('/', '.html', '.css')
    # if not path.endswith(valid_file_extension):
    #     logging.error("Unknown file type")
    #     return 404
    
    # Route known paths else return 404 Not Found
    if path == '/':
        http_code = '200'
    elif path == '/deep/':
        http_code = '200'
    else:
        logging.error("Unknown path %s", path)
        http_code = '404'
    return http_code