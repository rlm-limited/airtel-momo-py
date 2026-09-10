"""Contains shared errors types that can be raised from API functions"""


class UnexpectedStatus(Exception):
    """Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True"""

    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content

        super().__init__(
            f"Unexpected status code: {status_code}\n\nResponse content:\n{content.decode(errors='ignore')}"
        )


class CallbackParseError(Exception):
    """Raised when an inbound Airtel callback body cannot be parsed

    Retrying an unparseable payload cannot help, so callers should answer it with a 4xx rather than
    a 5xx that would make Airtel redeliver it.
    """

    def __init__(self, message: str, content: bytes | str | None = None):
        self.content = content

        super().__init__(message)


__all__ = ["CallbackParseError", "UnexpectedStatus"]
