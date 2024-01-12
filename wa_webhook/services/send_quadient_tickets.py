from pydantic_models.request_model import RequestModel
from common.http_requests import post_request

from settings import QUADIENT_URL, LABEL_ERROR, DN_PATTERN
import json
import re

from common.log_event import log_event
from settings import LABEL_ERROR

def send_quadient_tickets(request_data: RequestModel):

    matches_positions = [(match.start(), match.end()) for match in re.finditer(DN_PATTERN, request_data.customer_dn)]

    if matches_positions:
        latest_match_start, latest_match_end = matches_positions[-1]
        latest_match = request_data.customer_dn[latest_match_start:latest_match_end]
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

        return {"code":1, "description": "Sent"}
    
    except Exception as e:
        
        log_event(str(e), LABEL_ERROR)

        return {"code":0, "description": str(e)}