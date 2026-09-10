import os
import uuid

import pytest
from dotenv import load_dotenv

from airtel_momo import STAGING_BASE_URL, Client
from airtel_momo.api import authenticate, request_payment
from airtel_momo.models.oauth_2_token_body import Oauth2TokenBody
from airtel_momo.models.request_payment_body import RequestPaymentBody
from airtel_momo.models.request_payment_response_200 import RequestPaymentResponse200
from airtel_momo.models.response_code import ResponseCode, response_code_reason
from airtel_momo.models.subscriber import Subscriber
from airtel_momo.models.transaction import Transaction

load_dotenv()


def get_token():
    """Fetch an OAuth2 access token for the USSD push test"""
    client_id = os.getenv("AIRTEL_CLIENT_ID", "").replace('"', "").replace("'", "")
    client_secret = os.getenv("AIRTEL_CLIENT_SECRET", "").replace('"', "").replace("'", "")

    if not all([client_id, client_secret]):
        return None

    client = Client(base_url=STAGING_BASE_URL)
    response = authenticate.sync_detailed(
        client=client,
        body=Oauth2TokenBody(
            client_id=client_id,
            client_secret=client_secret,
            grant_type="client_credentials",
        ),
    )
    return response.parsed.access_token if response.status_code == 200 else None


def test_request_payment_success():
    """Test USSD Push payment request successfully using airtel_momo"""
    msisdn = os.getenv("AIRTEL_TEST_MSISDN", "").replace('"', "").replace("'", "")

    if not msisdn:
        pytest.skip("AIRTEL_TEST_MSISDN not set - skipping live USSD push")

    token = get_token()

    if not token:
        pytest.skip("Credentials missing in .env")

    client = Client(base_url=STAGING_BASE_URL)

    transaction_id = str(uuid.uuid4())

    body = RequestPaymentBody(
        reference="Testing transaction",
        subscriber=Subscriber(
            country="RW",
            currency="RWF",
            msisdn=msisdn,
        ),
        transaction=Transaction(
            amount=1000,
            country="RW",
            currency="RWF",
            id=transaction_id,
        ),
    )

    response = request_payment.sync_detailed(
        client=client,
        body=body,
        authorization=f"Bearer {token}",
        x_country="RW",
        x_currency="RWF",
    )

    if response.status_code == 200:
        assert isinstance(response.parsed, RequestPaymentResponse200)
        print(f"\n[SUCCESS] USSD push sent. Transaction ID: {transaction_id}")
        print(f"Status Code: {response.parsed.status.code}, Message: {response.parsed.status.message}")
        code = response.parsed.status.response_code
        print(f"Response Code: {code} ({response_code_reason(code)}), Success: {response.parsed.status.success}")
        # A USSD push that reached the handset is pending until the consumer enters their PIN
        assert ResponseCode.parse(code) is not ResponseCode.FORBIDDEN, "x-signature and payload did not match"
    else:
        print(f"\n[ERROR] Status Code: {response.status_code}")
        print(f"Response Content: {response.content.decode()}")
        pytest.fail(f"Failed to request payment: {response.status_code}")


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
