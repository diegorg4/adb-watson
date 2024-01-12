import json
import requests

from settings import LABEL_ERROR, LOGGING_URL

def post_request(url: str, payload: dict, headers:dict={}, verbose:bool=True) -> None:

    try:

        json_payload = json.dumps(payload)
        
        response = requests.post(url, data=json_payload, headers=headers)

        response.raise_for_status()

        if verbose:
            print(f"Reponse from {url}: {response.text}")

        else:
            print(f"Status from {url}: {response.status_code}")
        
        return response.text

    except Exception as e:

        print(f"An exception ocurred from {url}: {str(e)}", LABEL_ERROR)

        raise
