import requests
from dotenv import load_dotenv
from os import getenv
import sys

load_dotenv(override=True)

def create_api_key(x_reference_id):
    """
    Creates an API Key for an existing API User.
    Returns: tuple (api_key, success_boolean, error_message)
    """
    subscription_key = getenv("PRIMARY_KEY")

    if not subscription_key:
        return None, False, "Missing PRIMARY_KEY in .env"

    url = f"https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/{x_reference_id}/apikey"

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    try:
        response = requests.post(url=url, headers=headers)
        if response.status_code == 201:
            return response.json().get('apiKey'), True, None
        else:
            return None, False, response.text
    except Exception as e:
        return None, False, str(e)

if __name__ == "__main__":
    ref_id = getenv("X_REFERENCE_ID")
    print(f"Creating API Key for X_REFERENCE_ID: {ref_id}")
    key, success, error = create_api_key(ref_id)
    if success:
        print(f"API Key created successfully: {key}")
    else:
        print(f"Failed to create API key. Error: {error}")
