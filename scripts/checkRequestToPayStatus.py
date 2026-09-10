import requests
from dotenv import load_dotenv
from os import getenv
import json
import sys
import os

# Import the helper from createAccessToken
from createAccessToken import get_access_token
load_dotenv(override=True)


def get_request_to_pay_status(reference_id):
    """
    Retrieves the status of a Request To Pay transaction.
    Returns: dict with response data or None
    """
    subscription_key = getenv("PRIMARY_KEY")

    if not subscription_key:
        print("Error: Missing PRIMARY_KEY in .env")
        return None

    token = get_access_token()
    if not token:
        return None

    url = f"https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay/{reference_id}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Target-Environment": "sandbox",
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve Status. Code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"Request Error: {e}")
        return None

if __name__ == "__main__":
    # Ensure the script can find 'createAccessToken' if run from scripts/
    sys.path.append(os.path.dirname(__file__))
    
    ref_id = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not ref_id:
        print("Usage: python3 checkRequestToPayStatus.py <reference_id>")
    else:
        status_data = get_request_to_pay_status(ref_id)
        if status_data:
            print("Transaction Status:")
            print(json.dumps(status_data, indent=2))
