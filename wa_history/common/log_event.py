from common.http_requests import post_request

from settings import SERVICE_NAME, LOGGING_URL, LABEL_INFO

def log_event(message:str, level:str=LABEL_INFO, log_internal=True):

    if log_internal:
        print(level + ": " + message)

    post_request(LOGGING_URL, {"service":SERVICE_NAME, "message":message, "level":level}, verbose=False)