import requests
from dotenv import load_dotenv
from os import getenv
import json
import sys

load_dotenv(override=True)

def get_api_user_details(x_reference_id):
    """
    Retrieves information for an API User.
    Returns: dict with user details or None
    """
    subscription_key = getenv("PRIMARY_KEY")

    if not subscription_key:
        print("Error: Missing PRIMARY_KEY in .env")
        return None

    url = f"https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/{x_reference_id}"

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch user. Status: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"Request Error: {e}")
        return None

if __name__ == "__main__":
    ref_id = getenv("X_REFERENCE_ID")
    print(f"Fetching details for API User: {ref_id}")
    details = get_api_user_details(ref_id)
    if details:
        print(json.dumps(details, indent=2))
