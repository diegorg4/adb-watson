import redis
import settings
import json
import requests
import logging
import uuid
import time

redis_db = redis.Redis(host=settings.REDIS_IP, port=settings.REDIS_PORT)

def process_pending_jobs():

    while True:
        _, job_data = redis_db.brpop(settings.REDIS_QUEUE)

        customer_data_str = job_data.decode('utf-8')

        customer_data = json.loads(customer_data_str)

        base_64_ticket = http_post_request(url=settings.QUADIENT_URL, playload=customer_data['data'])

        pdf_uuid = upload_pdf_to_meta(base_64_file=base_64_ticket)

        send_whatsapp_message(customer_dn=customer_data['customer_dn'], wa_message=customer_data['wa_message'], file_uuid=pdf_uuid)

        time.sleep(settings.SERVER_SLEEP)

def http_post_request(url:str, playload:dict):
    try:
        response = requests.post(url, json=playload)
        response.raise_for_status()

        return response.json()

    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")

    except Exception as err:
        logging.error(f"An error occurred: {err}")

    return None

def upload_pdf_to_meta(base_64_file:str):

    return str(uuid.uuid4())

def send_whatsapp_message(customer_dn:str, wa_message:str, file_uuid:str):
    return True

if __name__ == '__main__':
    
    logging.info("Processing pending jobs...")
    process_pending_jobs()
