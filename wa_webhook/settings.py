import os
from dotenv import load_dotenv

SERVICE_NAME = 'WA-MAIN-WEBHOOK'

environment = os.getenv('ENVIRONMENT','')

load_dotenv(dotenv_path=f"{environment}.env")

REDIS_QUEUE = 'send_pdfs_queue'
REDIS_PORT = 6379
REDIS_DB_ID = 0
REDIS_IP = os.getenv('REDIS_IP','redis')
SERVER_SLEEP = 0.05

DN_PATTERN = r'^(\+52)?(\d{10})$'
EMAIL_PATTERN = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
TRIP_TYPE_PATTERN = r'^(sencillo|redondo)$'

LOGGING_URL = os.getenv('LOGGING_URL','')
QUADIENT_URL = os.getenv('QUADIENT_URL','')

print("Logging URL:" + LOGGING_URL)
print("Quadient URL:" + QUADIENT_URL)

LABEL_CRITICAL = 'CRITICAL'
LABEL_ERROR = 'ERROR'
LABEL_WARNING = 'WARNING'
LABEL_INFO = 'INFO'
LABEL_DEBUG = 'DEBUG'

