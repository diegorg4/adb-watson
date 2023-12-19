import settings
import logging
import json

from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1, Document

def pre_webhook_service():
    
    # Create an IAM authenticator.
    authenticator = IAMAuthenticator(settings.CLOUDANT_APIKEY)

    # Construct the service client.
    cloudant_service = CloudantV1(authenticator=authenticator)

    # Set our custom service URL
    cloudant_service.set_service_url(settings.CLOUDANT_URL)

    db_name = "test"