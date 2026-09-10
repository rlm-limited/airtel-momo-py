__version__ = "1.1.1"
"""A client library for accessing Airtel Money"""

from .callback import CallbackHandler, CallbackResult, parse_callback
from .client import AuthenticatedClient, Client

STAGING_BASE_URL = "https://openapiuat.airtel.co.rw"
PRODUCTION_BASE_URL = "https://openapi.airtel.co.rw"

__all__ = (
    "PRODUCTION_BASE_URL",
    "STAGING_BASE_URL",
    "AuthenticatedClient",
    "CallbackHandler",
    "CallbackResult",
    "Client",
    "parse_callback",
)
