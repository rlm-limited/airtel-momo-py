import os

import pytest
from dotenv import load_dotenv

from airtel_momo import STAGING_BASE_URL, Client
from airtel_momo.api import authenticate
from airtel_momo.models.oauth_2_token_body import Oauth2TokenBody
from airtel_momo.models.oauth_2_token_response import Oauth2TokenResponse

load_dotenv()


def test_authenticate_success():
    """Test OAuth2 token creation successfully using airtel_momo"""
    client_id = os.getenv("AIRTEL_CLIENT_ID", "").replace('"', "").replace("'", "")
    client_secret = os.getenv("AIRTEL_CLIENT_SECRET", "").replace('"', "").replace("'", "")

    if not all([client_id, client_secret]):
        pytest.skip("Credentials missing in .env")

    client = Client(base_url=STAGING_BASE_URL)

    response = authenticate.sync_detailed(
        client=client,
        body=Oauth2TokenBody(
            client_id=client_id,
            client_secret=client_secret,
            grant_type="client_credentials",
        ),
    )

    if response.status_code == 200:
        assert isinstance(response.parsed, Oauth2TokenResponse)
        assert response.parsed.access_token is not None
        print(f"\n[SUCCESS] Access Token: {response.parsed.access_token[:15]}...")
        print(f"Token Type: {response.parsed.token_type}, Expires In: {response.parsed.expires_in}")
    else:
        print(f"\n[ERROR] Status Code: {response.status_code}")
        print(f"Response Content: {response.content.decode()}")
        pytest.fail(f"Failed to create access token: {response.status_code}")


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
