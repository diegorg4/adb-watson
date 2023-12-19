import os
from dotenv import load_dotenv
load_dotenv()

REDIS_QUEUE = 'send_pdfs_queue'
REDIS_PORT = 6379
REDIS_DB_ID = 0
REDIS_IP = os.getenv('REDIS_IP','redis')
SERVER_SLEEP = 0.05
QUADIENT_URL = 'https://adb-quadient-server/generate-pdf'