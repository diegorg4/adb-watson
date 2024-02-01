from pydantic_models.request_model import RequestModel
from common.http_requests import post_request
from typing import Dict
from model.cloudant_manager import CloudantManager
from services.twilio_manager import TwilioManager

from settings import environment, QUADIENT_URL, LABEL_ERROR, DN_PATTERN, TWILIO_CONTENT_START_MSID, CLOUDANT_TICKET_DOCUMENTS_DB       
import json
import re
import base64
import os
import locale

from common.log_event import log_event
from twilio.rest import Client


def send_quadient_tickets(request_data: RequestModel):

    matches_positions = [(match.start(), match.end()) for match in re.finditer(DN_PATTERN, request_data.customer_dn)]

    # DN can come as (+52)(\d{10}) or \d{10}. The regex pattern groups (+52) so the last pattern found needs to be taken as the DN
    # (+52)(\d{10}) matches two subgroups and we need the second (latest) and (\d{10}) matches the first, also the latest [-1]
    
    if matches_positions:
        
        latest_match_start, latest_match_end = matches_positions[-1]
        
        latest_match = request_data.customer_dn[latest_match_start:latest_match_end]
        
        # Quadient service requieres this format
        if "+52" not in request_data.customer_dn:

            request_data.customer_dn = "+52" + latest_match

    else:
        log_event("customer DN pattern didn't match a result", LABEL_ERROR)

        return {"code":"0", "description":"customer DN pattern didn't match a result"}
        
    try:
        if request_data.trip_type == 'sencillo':
            
            customer_playload = {"Clients":[{
                            "ClientID":"0044",
                            "MailFrom": "l.ramirez@quadient.com",
                            "name":request_data.customer_name,
                            "email":request_data.customer_email,
                            "phone":request_data.customer_dn,
                            "trip_type":request_data.trip_type,
                            "trip":[
                                {
                                    "type":"IDA",
                                    "origin":request_data.origin,
                                    "destination":request_data.destination,
                                    "date":request_data.leaving_date,
                                    "price":request_data.leaving_price,
                                    "flight":"X0096",
                                    "gate":"15"
                                }
                            ]
                        }]}


        elif request_data.trip_type == 'redondo':
            
            customer_playload = {"Clients":[{
                            "ClientID":"0044",
                            "name":request_data.customer_name,
                            "MailFrom": "l.ramirez@quadient.com",
                            "email":request_data.customer_email,
                            "phone":request_data.customer_dn,
                            "trip_type":request_data.trip_type,
                            "trip":[
                                {
                                    "type":"IDA",
                                    "origin":request_data.origin,
                                    "destination":request_data.destination,
                                    "date":request_data.leaving_date,
                                    "price":request_data.leaving_price,
                                    "flight":"X0096",
                                    "gate":"15"
                                },
                                {
                                    "type":"VUELTA",
                                    "origin":request_data.destination,
                                    "destination":request_data.origin,
                                    "date":request_data.returning_date,
                                    "price":request_data.returning_price,
                                    "flight":"A0056",
                                    "gate":"34"
                                }
                            ]
                        }]}

        log_event(f"Body request to quadient service: {json.dumps(customer_playload)}")

        response = post_request(QUADIENT_URL, customer_playload, headers={"Authorization": "Bearer I+mPpGm/ykdzE5w2+YAggBCBsPunYs0hf1c5LGB7U7jl"}, verbose=False)

        log_event(f"Response from quadient service: {response}", log_internal=False)

        response_data = json.loads(response)

        save_pdf(response_data)

        save_transaction_metadata(response_data['job-id'], request_data.customer_dn)
        
        start_whatsapp_conversation(request_data.customer_dn)

        return {"code":1, "description": "Sent", "file-uuid": response_data['job-id']}
    
    except Exception as e:
        
        log_event(str(e), LABEL_ERROR)

        return {"code":0, "description": str(e)}

def save_pdf(response_data: Dict):

    try:

        binary_file = base64.b64decode(response_data['data'][0]['file'])

        file_path = os.path.join(   os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                    "files",
                                    f"{response_data['job-id']}."
                                    f"{response_data['data'][0]['contentType'].split('/')[1]}"
                                )

        with open(file_path, 'wb') as output_file:

            output_file.write(binary_file)

    except Exception as e:

        log_event(str(e), LABEL_ERROR)
    

def start_whatsapp_conversation(customer_dn:str):

    twilio_client = TwilioManager()
    
    twilio_client.create_message_no_content(
                    to=customer_dn,
                    content_sid=TWILIO_CONTENT_START_MSID
                  )

def save_transaction_metadata(file_uuid:str, customer_dn:str):

    from datetime import datetime
    import pytz

    now_utc = datetime.now(pytz.utc)

    timezone = pytz.timezone("America/Mexico_City")

    current_datetime = now_utc.astimezone(timezone)

    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    custom_cloudant = CloudantManager(CLOUDANT_TICKET_DOCUMENTS_DB)

    custom_cloudant.put_document({  
                                    "env": environment,
                                    "file_uuid":file_uuid,
                                    "customer_dn":customer_dn,
                                    "status":"PENDING",
                                    "date": formatted_datetime
                                  })