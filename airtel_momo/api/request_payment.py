from http import HTTPStatus
from typing import Any

import httpx

from .. import errors
from ..client import AuthenticatedClient, Client
from ..models.request_payment_body import RequestPaymentBody
from ..models.request_payment_response_200 import RequestPaymentResponse200
from ..types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: RequestPaymentBody,
    authorization: str,
    x_country: str,
    x_currency: str,
    x_signature: str | Unset = UNSET,
    x_key: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Accept"] = "*/*"

    headers["X-Country"] = x_country

    headers["X-Currency"] = x_currency

    headers["Authorization"] = authorization

    if not isinstance(x_signature, Unset):
        headers["x-signature"] = x_signature

    if not isinstance(x_key, Unset):
        headers["x-key"] = x_key

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/merchant/v2/payments/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> RequestPaymentResponse200 | None:
    if response.status_code == 200:
        response_200 = RequestPaymentResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[RequestPaymentResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RequestPaymentBody,
    authorization: str,
    x_country: str,
    x_currency: str,
    x_signature: str | Unset = UNSET,
    x_key: str | Unset = UNSET,
) -> Response[RequestPaymentResponse200]:
    """Payments - USSD Push

     This API is used to request a payment from a consumer(Payer). The consumer(payer) will be asked to
    authorize the payment. After authorization, the transaction will be executed.

    Note: Do not send country code in msisdn.

    Note: Airtel returns HTTP 200 for business failures as well, with status.success set to false and the
    outcome in status.response_code. A 200 does not mean the payment succeeded - check
    parsed.status.success, and resolve status.response_code with models.ResponseCode. A successful USSD
    push typically returns DP00800001006 (In process), not DP00800001001 (Success), because the payment
    is only complete once the consumer enters their PIN.

    Args:
        authorization (str): Authorization bearer token.
        x_country (str): Transaction country.
        x_currency (str): Transaction currency.
        x_signature (str | Unset): Encrypted payload.
        x_key (str | Unset): Encrypted AES key and iv.
        body (RequestPaymentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RequestPaymentResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
        authorization=authorization,
        x_country=x_country,
        x_currency=x_currency,
        x_signature=x_signature,
        x_key=x_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: RequestPaymentBody,
    authorization: str,
    x_country: str,
    x_currency: str,
    x_signature: str | Unset = UNSET,
    x_key: str | Unset = UNSET,
) -> RequestPaymentResponse200 | None:
    """Payments - USSD Push

     This API is used to request a payment from a consumer(Payer). The consumer(payer) will be asked to
    authorize the payment. After authorization, the transaction will be executed.

    Note: Do not send country code in msisdn.

    Note: Airtel returns HTTP 200 for business failures as well, with status.success set to false and the
    outcome in status.response_code. A 200 does not mean the payment succeeded - check
    parsed.status.success, and resolve status.response_code with models.ResponseCode. A successful USSD
    push typically returns DP00800001006 (In process), not DP00800001001 (Success), because the payment
    is only complete once the consumer enters their PIN.

    Args:
        authorization (str): Authorization bearer token.
        x_country (str): Transaction country.
        x_currency (str): Transaction currency.
        x_signature (str | Unset): Encrypted payload.
        x_key (str | Unset): Encrypted AES key and iv.
        body (RequestPaymentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RequestPaymentResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
        authorization=authorization,
        x_country=x_country,
        x_currency=x_currency,
        x_signature=x_signature,
        x_key=x_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RequestPaymentBody,
    authorization: str,
    x_country: str,
    x_currency: str,
    x_signature: str | Unset = UNSET,
    x_key: str | Unset = UNSET,
) -> Response[RequestPaymentResponse200]:
    """Payments - USSD Push

     This API is used to request a payment from a consumer(Payer). The consumer(payer) will be asked to
    authorize the payment. After authorization, the transaction will be executed.

    Note: Do not send country code in msisdn.

    Note: Airtel returns HTTP 200 for business failures as well, with status.success set to false and the
    outcome in status.response_code. A 200 does not mean the payment succeeded - check
    parsed.status.success, and resolve status.response_code with models.ResponseCode. A successful USSD
    push typically returns DP00800001006 (In process), not DP00800001001 (Success), because the payment
    is only complete once the consumer enters their PIN.

    Args:
        authorization (str): Authorization bearer token.
        x_country (str): Transaction country.
        x_currency (str): Transaction currency.
        x_signature (str | Unset): Encrypted payload.
        x_key (str | Unset): Encrypted AES key and iv.
        body (RequestPaymentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RequestPaymentResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
        authorization=authorization,
        x_country=x_country,
        x_currency=x_currency,
        x_signature=x_signature,
        x_key=x_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: RequestPaymentBody,
    authorization: str,
    x_country: str,
    x_currency: str,
    x_signature: str | Unset = UNSET,
    x_key: str | Unset = UNSET,
) -> RequestPaymentResponse200 | None:
    """Payments - USSD Push

     This API is used to request a payment from a consumer(Payer). The consumer(payer) will be asked to
    authorize the payment. After authorization, the transaction will be executed.

    Note: Do not send country code in msisdn.

    Note: Airtel returns HTTP 200 for business failures as well, with status.success set to false and the
    outcome in status.response_code. A 200 does not mean the payment succeeded - check
    parsed.status.success, and resolve status.response_code with models.ResponseCode. A successful USSD
    push typically returns DP00800001006 (In process), not DP00800001001 (Success), because the payment
    is only complete once the consumer enters their PIN.

    Args:
        authorization (str): Authorization bearer token.
        x_country (str): Transaction country.
        x_currency (str): Transaction currency.
        x_signature (str | Unset): Encrypted payload.
        x_key (str | Unset): Encrypted AES key and iv.
        body (RequestPaymentBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RequestPaymentResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            authorization=authorization,
            x_country=x_country,
            x_currency=x_currency,
            x_signature=x_signature,
            x_key=x_key,
        )
    ).parsed
