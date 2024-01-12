import json
import requests
import settings

service_name = settings.SERVICE_NAME

def send_post_request(url: str, payload: dict):
    try:
        json_payload = json.dumps(payload)

        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(settings.LOGGING_URL, data=json_payload, headers=headers)

        response.raise_for_status()
        
        if response.status_code == 200:
            return response.json()
        else:
            print ({"error": f"Unexpected status code: {response.status_code}"})

    except requests.exceptions.RequestException as e:    
        print ({"error": f"Request Exception: {e}"})

    except json.JSONDecodeError as e:
        print ({"error": f"JSON Decode Error: {e}"})

    except Exception as e:
        print ({"error": f"Unexpected Error: {e}"})

def log_event(message:str, level:str=settings.LABEL_INFO):
    send_post_request(settings.LOGGING_URL, {"service":service_name,"message":message, "level":level})