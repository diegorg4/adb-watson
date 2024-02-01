from typing import Dict
from common.log_event import log_event
import json

from model.cloudant_manager import CloudantManager
from services.twilio_manager import TwilioManager

from settings import LABEL_ERROR, CLOUDANT_TICKET_DOCUMENTS_DB, TWILIO_CONTENT_SENDPDF_MSID, TWILIO_CONTENT_NOPENDING_MSID

def whatsapp_webhook_service(request_data: Dict):

    if request_data["Body"] == 'RECIBIR':
        send_whatsapp_tickets(request_data)


def send_whatsapp_tickets(request_data: Dict):
    try:
        
        # WaId parameter has this format: 5215554573893 and customer_dn saved is +525554573893

        selector = {
                    "data.customer_dn": f"+{request_data['WaId'][0:2]}{request_data['WaId'][-10:]}",
                    "data.status": "PENDING"
                    }

        fields = ["_id", "_rev", "data"]

        cloudant_client = CloudantManager(CLOUDANT_TICKET_DOCUMENTS_DB)

        response = cloudant_client.query_documents(selector, fields)

        twilio_client = TwilioManager()

        customer_dn = f'+{request_data["WaId"]}' 

        for document in response['docs']:

            content_variables = json.dumps({"file_uuid": document["data"]["file_uuid"]})
    
            twilio_client.create_message_with_content(
                    to=customer_dn,
                    content_sid=TWILIO_CONTENT_SENDPDF_MSID,
                    content_variables=content_variables
                  )
            
            cloudant_client.update_document_fields(document["_id"], {"status":"DELIVERED"})

        if len(response['docs']) < 1:

            twilio_client.create_message_no_content(
                    to=customer_dn,
                    content_sid=TWILIO_CONTENT_NOPENDING_MSID
                  )

    except Exception as e:
        
        log_event("Exception on send_tickets_to_whatsapp: " + str(e), LABEL_ERROR)
        
        return {
            "code": 0,
            "description": str(e)
        }



    