import uuid

from common.log_event import log_event
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from pydantic_models.request_model import RequestModel

from settings import CLOUDANT_APIKEY, CLOUDANT_URL, CLOUDANT_DB, LABEL_ERROR

def save_history(request_model: RequestModel):

    try:
        authenticator = IAMAuthenticator(CLOUDANT_APIKEY)
        cloudant_client = CloudantV1(authenticator=authenticator)
        cloudant_client.set_service_url(CLOUDANT_URL)

        event_doc = Document(
            log_event=request_model.model_dump()
        )
        response = cloudant_client.put_document(
            db=CLOUDANT_DB,
            doc_id=str(uuid.uuid4()),
            document=event_doc
        ).get_result()
        
        log_event("Cloudant response: " + str(response))

        return {
            "code": 1,
            "description": response
        }
    
    except Exception as e:

        log_event(str(e), LABEL_ERROR)

        return {
            "code": 1,
            "description": str(e)
        }
    
