import requests
from uuid import uuid4
from dotenv import load_dotenv
from os import getenv
import json
import sys
import os

# Import the helper from createAccessToken
from createAccessToken import get_access_token

def request_to_pay(amount="100", currency="EUR", party_id="0783089337", payer_message="MP EV", payee_note="MP EV"):
    """
    Triggers a Request To Pay transaction.
    Returns: tuple (transaction_ref_id, success_boolean, response_json)
    """
    load_dotenv(override=True)
    subscription_key = getenv("PRIMARY_KEY")

    if not subscription_key:
        print("Error: Missing PRIMARY_KEY in .env")
        return None, False, None

    token = get_access_token()
    if not token:
        return None, False, None

    # Generate unique IDs for this specific transaction
    transaction_ref_id = str(uuid4())
    external_id = str(uuid4())

    url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Callback-Url": "https://evstaging.meshpower.co.rw/payment/callback/mtn",
        "X-Reference-Id": transaction_ref_id,
        "X-Target-Environment": "sandbox",
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/json"
    }

    data = {
        "amount": amount,
        "currency": currency,
        "externalId": external_id,
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": party_id
        },
        "payerMessage": payer_message,
        "payeeNote": payee_note
    }

    try:
        response = requests.post(url=url, headers=headers, json=data)
        if response.status_code == 202:
            return transaction_ref_id, True, None
        else:
            return transaction_ref_id, False, response.text
    except Exception as e:
        return None, False, str(e)

if __name__ == "__main__":
    # Ensure the script can find 'createAccessToken' if run from scripts/
    sys.path.append(os.path.dirname(__file__))
    
    amount = sys.argv[1] if len(sys.argv) > 1 else "100"
    
    print(f"Triggering Request to Pay: {amount} EUR for 0783089337")
    ref_id, success, error_msg = request_to_pay(amount=amount)

    if success:
        print("Request to Pay accepted (Pending authorization)")
        print(f"Transaction Reference ID (X-Reference-Id): {ref_id}")
    else:
        print(f"Failed to Request to Pay. Error: {error_msg}")
