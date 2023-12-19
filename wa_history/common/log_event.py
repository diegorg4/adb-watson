import json
import requests
import settings

def send_post_request(url: str, payload: dict):
    try:
        print("POST REQUEST READY TO BE SENT")
        # Convert the payload to JSON format
        json_payload = json.dumps(payload)

        # Set the headers
        headers = {'Content-Type': 'application/json'}

        # send the POST request
        response = requests.post(settings.LOGGING_URL, data=json_payload, headers=headers)

        # Check the response status code
        response.raise_for_status()

        # If the status code is 200 (OK), return the JSON response
        if response.status_code == 200:
            return response.json()
        else:
            print ({"error": f"Unexpected status code: {response.status_code}"})

    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        print ({"error": f"Request Exception: {e}"})

    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print ({"error": f"JSON Decode Error: {e}"})

    except Exception as e:
        # Handle other unexpected errors
        print ({"error": f"Unexpected Error: {e}"})

def log_event(message:str, level:str):
    send_post_request(settings.LOGGING_URL, {"message":message, "level":level})