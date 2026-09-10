from __future__ import annotations

from enum import StrEnum


class CallbackStatusCode(StrEnum):
    """Transaction status codes carried by the inbound payment callback.

    This is a separate scheme from the DP008000010xx codes in ``ResponseCode``, which belong to the
    synchronous USSD Push response. The callback only ever carries TS or TF.

    ``CallbackTransaction.status_code`` stays a plain ``str``, so use :meth:`parse` to resolve a
    value without raising on one Airtel has not documented.
    """

    TRANSACTION_SUCCESS = "TS"
    TRANSACTION_FAILED = "TF"

    @classmethod
    def parse(cls, value: object) -> CallbackStatusCode | None:
        """Resolve a raw ``status_code``, returning None if it is not a known code"""
        try:
            return cls(value)
        except ValueError:
            return None

    @property
    def succeeded(self) -> bool:
        """Whether this code means the transaction completed successfully"""
        return self is CallbackStatusCode.TRANSACTION_SUCCESS

    @property
    def description(self) -> str:
        """The meaning of this code, as documented by Airtel"""
        return _DESCRIPTIONS[self]


_DESCRIPTIONS: dict[CallbackStatusCode, str] = {
    CallbackStatusCode.TRANSACTION_SUCCESS: "Transaction Success",
    CallbackStatusCode.TRANSACTION_FAILED: "Transaction Failed",
}


def callback_status_description(value: object) -> str | None:
    """The documented meaning of a raw ``status_code``, or None if it is not a known code"""
    code = CallbackStatusCode.parse(value)
    return None if code is None else code.description
