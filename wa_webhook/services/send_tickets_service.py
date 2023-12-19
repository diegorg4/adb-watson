from pydantic_models.request_model import RequestModel
from twilio.rest import Client
import redis

import uuid
import settings
import logging
import json

# Connect to Redis server
redis_db = redis.Redis(host=settings.REDIS_IP, port=settings.REDIS_PORT)

def send_tickets_service(request_data: RequestModel):
    try:
        if request_data.trip_type == 'sencillo':
            customer_playload = {"Clients":[{
                            "ClientID":str(uuid.uuid4()),
                            "name":request_data.customer_name,
                            "email":request_data.customer_email,
                            "phone":request_data.customer_dn,
                            "trip_type":request_data.trip_type,
                            "trip":[
                                {
                                    "type":"ida",
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
                            "ClientID":str(uuid.uuid4()),
                            "name":request_data.customer_name,
                            "email":request_data.customer_email,
                            "phone":request_data.customer_dn,
                            "trip_type":request_data.trip_type,
                            "trip":[
                                {
                                    "type":"ida",
                                    "origin":request_data.origin,
                                    "destination":request_data.destination,
                                    "date":request_data.leaving_date,
                                    "price":request_data.leaving_price,
                                    "flight":"X0096",
                                    "gate":"15"
                                },
                                {
                                    "type":"vuelta",
                                    "origin":request_data.destination,
                                    "destination":request_data.origin,
                                    "date":request_data.returning_date,
                                    "price":request_data.returning_price,
                                    "flight":"A0056",
                                    "gate":"34"
                                }
                            ]
                        }]}
            
        job_data = {'id':str(uuid.uuid4()), 
                    'data':customer_playload,
                    'customer_dn':request_data.customer_dn,
                    'wa_message':request_data.wa_message
                    }

        redis_db.lpush(settings.REDIS_QUEUE, json.dumps(job_data))

        logging.INFO(f"Job queued. Data: {json.dumps(job_data)}")
        
        return {"code":1, "description": f"Job pending. Id: {job_data['id']}"}
    
    except Exception as e:
        
        logging.ERROR(f"Exception ocurred: {str(e)}")

        return {"code":0, "description":str(e)}