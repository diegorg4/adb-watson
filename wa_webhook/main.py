# API dependencies
from typing import Annotated

from pydantic_models.request_model import RequestModel

from fastapi import FastAPI, Request, status, Form
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from services.travels_service import travels_service
from services.send_tickets_service import send_tickets_service
from services.send_quadient_tickets import send_quadient_tickets
from services.send_whatsapp_ticket_test import send_whatsapp_ticket_test
from services.whatsapp_webhook_service import whatsapp_webhook_service
from services.fetch_tickets import fetch_tickets

from common.log_event import log_event

from settings import LABEL_ERROR
import json

# FastAPI server init
app = FastAPI()

# Create a POST endpoint at /list-trips/
@app.post("/ticket-sales-agent/")
async def ticket_sales_agent(request_data: RequestModel):
    
    log_event("Webhook Request Payload:" + request_data.model_dump_json())

    if request_data.service == "TRAVELS":
        return travels_service(request_data)
    
    elif request_data.service == "SENDTICKETS":
        return send_tickets_service(request_data)
    
    elif request_data.service == "QUADIENT":
        return send_quadient_tickets(request_data)

    elif request_data.service == "WHATSAPP":
        return send_whatsapp_ticket_test(request_data)    

    else:
        return {
                "code":0, 
                "description":"Service not found"
            }
    
@app.get("/fetch-tickets/{file_uuid}")
async def fetch_tickets_func(file_uuid: str):
     
    return fetch_tickets(file_uuid)

'''
    After configuring the webhook on Twilio, it calls this webhook. Twilio calls a POST request with x-www-form-urlencoded body request.
    Example request: 
    SmsMessageSid=SM95e176e0c93d71984d5ecc10152ce51c&NumMedia=0&ProfileName=Diego+Rom%C3%A1n&SmsSid=SM95e176e0c93d71984d5ecc10152ce51c&WaId=5215554573893&SmsStatus=received&Body=RECIBIR&To=whatsapp%3A%2B5215539242554&NumSegments=1&ReferralNumMedia=0&MessageSid=SM95e176e0c93d71984d5ecc10152ce51c&AccountSid=AC2b7d593f0bd08e9e7d6e9253dc0e0306&From=whatsapp%3A%2B5215554573893&ApiVersion=2010-04-01
'''
@app.post("/whatsapp-webhook/")
async def whatsapp_webhook(
        SmsMessageSid: str = Form(...),
        NumMedia: int = Form(...),
        ProfileName: str = Form(...),
        SmsSid: str = Form(...),
        WaId: str = Form(...),
        SmsStatus: str = Form(...),
        Body: str = Form(...),
        To: str = Form(...),
        NumSegments: int = Form(...),
        ReferralNumMedia: int = Form(...),
        MessageSid: str = Form(...),
        AccountSid: str = Form(...),
        From: str = Form(...),
        ApiVersion: str = Form(...),
    ):

    request_data = {
        "SmsMessageSid": SmsMessageSid,
        "NumMedia": NumMedia,
        "ProfileName": ProfileName,
        "SmsSid": SmsSid,
        "WaId": WaId,
        "SmsStatus": SmsStatus,
        "Body": Body,
        "To": To,
        "NumSegments": NumSegments,
        "ReferralNumMedia": ReferralNumMedia,
        "MessageSid": MessageSid,
        "AccountSid": AccountSid,
        "From": From,
        "ApiVersion": ApiVersion,
    }

    log_event("Whatsapp webhook call:" + json.dumps(request_data))

    return whatsapp_webhook_service(request_data)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
     
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
     
	log_event(f"{request}: {exc_str}", LABEL_ERROR)
     
	content = {'code': 0, 'message': exc_str}
     
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

