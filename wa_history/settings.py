import os
from dotenv import load_dotenv
load_dotenv()

CLOUDANT_URL = os.getenv('CLOUDANT_URL','')
CLOUDANT_USER = os.getenv('CLOUDANT_USER','')
CLOUDANT_APIKEY = os.getenv('CLOUDANT_APIKEY','')
CLOUDANT_DB = os.getenv('CLOUDANT_DB','test')

LOGGING_URL = os.getenv('LOGGING_URL','http://logging:8000/logging/')

LABEL_CRITICAL = 'CRITICAL'
LABEL_ERROR = 'ERROR'
LABEL_WARNING = 'WARNING'
LABEL_INFO = 'INFO'
LABEL_DEBUG = 'DEBUG'
