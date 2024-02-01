from pydantic_models.request_model import RequestModel
from twilio.rest import Client
from common.log_event import log_event

from settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, LABEL_ERROR

def send_whatsapp_ticket_test(request_data: RequestModel):

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
                              content_sid='HX63dca9cb7213c9f28888f23534f9e0ff',
                              from_='whatsapp:+5215539242554',
                              messaging_service_sid='MGfa5b6732b046616de08b0ffc40345268',
                                to='whatsapp:+5215554573893'
                          )

        return {"code":1, "message":message.sid}
    
    except Exception as e:
        
        log_event(str(e), LABEL_ERROR)

        raise
    
        