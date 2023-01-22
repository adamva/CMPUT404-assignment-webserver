import logging
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

# Logging
current_time = datetime.now().strftime("%Y-%m-%d")
LOG_LEVEL = logging.INFO
LOG_FILENAME = f'webserver-{current_time}.log'
LOG_DATEFMT = '%Y-%m-%dT%H:%M:%S'
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'

# Webserver
BIND_HOST = 'localhost'
BIND_PORT = 8080

BUFFER_SIZE = 1024
REQUEST_MAX_SIZE = 2000000 # 2MB
