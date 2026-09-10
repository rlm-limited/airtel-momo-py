from http import HTTPStatus
from typing import Any

import httpx

from .. import errors
from ..client import AuthenticatedClient, Client
from ..models.oauth_2_token_body import Oauth2TokenBody
from ..models.oauth_2_token_response import Oauth2TokenResponse
from ..types import Response


def _get_kwargs(
    *,
    body: Oauth2TokenBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Accept"] = "*/*"

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/oauth2/token",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Oauth2TokenResponse | None:
    if response.status_code == 200:
        response_200 = Oauth2TokenResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Oauth2TokenResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: Oauth2TokenBody,
) -> Response[Oauth2TokenResponse]:
    """OAuth2

     This API is used to get the bearer token. The output of this API contains access_token that will be
    used as bearer token for the API that we will be going to call.

    Args:
        body (Oauth2TokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Oauth2TokenResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: Oauth2TokenBody,
) -> Oauth2TokenResponse | None:
    """OAuth2

     This API is used to get the bearer token. The output of this API contains access_token that will be
    used as bearer token for the API that we will be going to call.

    Args:
        body (Oauth2TokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Oauth2TokenResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: Oauth2TokenBody,
) -> Response[Oauth2TokenResponse]:
    """OAuth2

     This API is used to get the bearer token. The output of this API contains access_token that will be
    used as bearer token for the API that we will be going to call.

    Args:
        body (Oauth2TokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Oauth2TokenResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: Oauth2TokenBody,
) -> Oauth2TokenResponse | None:
    """OAuth2

     This API is used to get the bearer token. The output of this API contains access_token that will be
    used as bearer token for the API that we will be going to call.

    Args:
        body (Oauth2TokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Oauth2TokenResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
