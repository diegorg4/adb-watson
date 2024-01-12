import os
from dotenv import load_dotenv

SERVICE_NAME = 'WA-HISTORY'

environment = os.getenv('ENVIRONMENT','')

load_dotenv(dotenv_path=f"{environment}.env")

CLOUDANT_URL = os.getenv('CLOUDANT_URL','')
CLOUDANT_USER = os.getenv('CLOUDANT_USER','')
CLOUDANT_APIKEY = os.getenv('CLOUDANT_APIKEY','')
CLOUDANT_DB = os.getenv('CLOUDANT_DB','test')

LOGGING_URL = os.getenv('LOGGING_URL', '')

print("Logging URL:" + LOGGING_URL)
print("Cloudant URL:" + CLOUDANT_URL)

LABEL_CRITICAL = 'CRITICAL'
LABEL_ERROR = 'ERROR'
LABEL_WARNING = 'WARNING'
LABEL_INFO = 'INFO'
LABEL_DEBUG = 'DEBUG'