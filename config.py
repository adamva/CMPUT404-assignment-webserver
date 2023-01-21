import logging
from datetime import datetime
current_time = datetime.now().strftime("%Y-%m-%d")

LOG_LEVEL = logging.INFO
LOG_FILENAME = f'webserver-{current_time}.log'
LOG_DATEFMT = '%Y-%m-%dT%H:%M:%S'
LOG_FORMAT = '%(asctime)s %(name)s %(message)s'