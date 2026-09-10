import requests
from dotenv import load_dotenv
from os import getenv
from uuid import uuid4
import sys

load_dotenv(override=True)

def create_api_user():
    """
    Creates an API User in the MTN MoMo Sandbox.
    Returns: tuple (x_reference_id, success_boolean, error_message)
    """
    subscription_key = getenv("PRIMARY_KEY")
    callback_host = getenv("PROVIDER_CALLBACK_HOST")
    x_reference_id = getenv("X_REFERENCE_ID")

    if not subscription_key:
        return None, False, "Missing PRIMARY_KEY in .env"

    if not x_reference_id:
        exit("Error: X_REFERENCE_ID must be provided either in .env or as an argument")

    if not callback_host:
        exit("Error: PROVIDER_CALLBACK_HOST must be provided either in .env or as an argument")

    url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser"

    headers = {
        "X-Reference-Id": x_reference_id,
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    data = {
        "providerCallbackHost": callback_host
    }

    try:
        response = requests.post(url=url, headers=headers, json=data)
        if response.status_code == 201:
            return x_reference_id, True, None
        else:
            return x_reference_id, False, response.text
    except Exception as e:
        return x_reference_id, False, str(e)

if __name__ == "__main__":
    ref_id = getenv("X_REFERENCE_ID")
    callback_host = getenv("PROVIDER_CALLBACK_HOST")
    print(f"Creating API User with X_REFERENCE_ID: {ref_id}")
    ref_id, success, error = create_api_user()
    if success:
        print(f"User ID created successfully: {ref_id}")
    else:
        print(f"Failed to create user ID. Error: {error}")
