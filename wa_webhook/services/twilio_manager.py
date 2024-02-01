from twilio.rest import Client
from common.log_event import log_event
from typing import Dict

from settings import LABEL_ERROR, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_CONTENT_START_MSID, TWILIO_WHATSAPP_SENDER,TWLIO_MSG_SERVICE_SID

class TwilioManager():

    def __init__(self):

        self.__client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def create_message_no_content(self, to:str, content_sid:str):
    
        try:

            message = self.__client.messages.create(
                                content_sid=content_sid,
                                from_=TWILIO_WHATSAPP_SENDER,
                                messaging_service_sid=TWLIO_MSG_SERVICE_SID,
                                to=f'whatsapp:{to}'
                            )
            log_event("Response from twilio: " + message.sid)
        
        except Exception as e:

            log_event("Exception on twilio_manager: " + str(e), LABEL_ERROR)

    '''
        Create message requieres Mexico numbers to have +521
    '''
    
    def create_message_with_content(self, to:str, content_sid:str, content_variables:str):
    
        '''
            To parameter requires from +XXXXX
        '''
        try:

            message = self.__client.messages.create(
                                content_sid=content_sid,
                                from_=TWILIO_WHATSAPP_SENDER,
                                messaging_service_sid=TWLIO_MSG_SERVICE_SID,
                                to=f'whatsapp:{to}',
                                content_variables=content_variables
                            )
            log_event("Response from twilio: " + message.sid)
        
        except Exception as e:

            log_event("Exception on twilio_manager: " + str(e), LABEL_ERROR)