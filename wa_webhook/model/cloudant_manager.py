from typing import Dict
from cloudant.client import Cloudant
import settings
import logging

class CloudantManager():
    def __init__(self) -> None:
        self.client = None
        self.database = None

    def connect(self, url: str = settings.CLOUDANT_URL, 
                cloudant_user : str = settings.CLOUDANT_USER, 
                 auth_token : str = settings.CLOUDANT_APIKEY):
        
        self.client = Cloudant(cloudant_user=cloudant_user, auth_token=auth_token, url=url)
        self.client.connect()

    def set_database(self, database_name):
        try:
            self.database = self.client.create_database(database_name, throw_on_exists=False)

        except Exception as e:
            logging.error(f"Error while creating database: {str(e)}")
            raise

    def create_document(self, document:Dict):
        if self.database is not None:
            try:
                document_result = self.database.create_document(document)
                if document_result.exists():
                    return True
                else:
                    return False
            except Exception as e:
                logging.error(f"Error while creating document: {str(e)}")
                raise
        else:
            raise ValueError("Database connection was unsuccessful. Please select or create a new database.")

    def disconnect(self):
        try:
            if self.client is not None:
                self.client.disconnect()
                logging.info("Disconnected from Cloudant")
        except Exception as e:
            logging.error(f"Error while disconnecting from Cloudant: {str(e)}")
            raise 
