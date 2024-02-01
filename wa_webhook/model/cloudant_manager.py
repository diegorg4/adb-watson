from typing import Dict, List
import uuid
from common.log_event import log_event

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1, Document

from settings import CLOUDANT_APIKEY, CLOUDANT_URL, LABEL_ERROR

class CloudantManager():
    def __init__(self, db_name: str) -> None:

        self._authenticator = IAMAuthenticator(CLOUDANT_APIKEY)

        self._cloudant_client = CloudantV1(authenticator=self._authenticator)

        self._cloudant_client.set_service_url(CLOUDANT_URL)

        self.db_name = db_name

    def put_document(self, document:Dict) -> Dict:

        try:
            event_doc = Document(data=document)

            response = self._cloudant_client.put_document(
                db          =   self.db_name,
                doc_id      =   str(uuid.uuid4()),
                document    =   event_doc
            ).get_result()
            
            log_event("Post document response: " + str(response))

            return {
                "code": 1,
                "description": response
            }

        except Exception as e:

            log_event(str(e), LABEL_ERROR)

            return {
                "code": 0,
                "description": str(e)
            }
        
    def query_documents(self, selector: Dict, fields: List, sort: List = []) -> Dict:

        try:

            response = self._cloudant_client.post_find(
                db=self.db_name,
                selector=selector,
                fields=fields,
                sort=sort

            ).get_result()

            log_event("Query documents response: " + str(response))

            return response


        except Exception as e:
            
            log_event(str(e), LABEL_ERROR)

            return {
                "code": 0,
                "description": str(e)
            }
    
    def update_document_fields(self, doc_id: str, updated_fields: Dict) -> Dict:
        try:
            # Retrieve the existing document
            existing_doc = self._cloudant_client.get_document(
                db=self.db_name,
                doc_id=doc_id
            ).get_result()

            # Update the specified fields
            for field, value in updated_fields.items():
                existing_doc['data'][field] = value

            # Save the updated document
            response = self._cloudant_client.put_document(
                db=self.db_name,
                doc_id=doc_id,
                document=existing_doc
            ).get_result()

            log_event("Update document fields response: " + str(response))

            return response

        except Exception as e:

            log_event("Exception on cloud_manager updating document: " + str(e), LABEL_ERROR)

            return {
                "code": 0,
                "description": str(e)
            }

