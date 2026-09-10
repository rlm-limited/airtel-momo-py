from __future__ import annotations

from enum import StrEnum


class ResponseCode(StrEnum):
    """Product specific codes returned in ``status.response_code``.

    Airtel may return codes that are not listed here, so ``Status.response_code`` stays a plain
    ``str``. Use :meth:`parse` to resolve a code without raising on an unknown one.
    """

    AMBIGUOUS = "DP00800001000"
    SUCCESS = "DP00800001001"
    INCORRECT_PIN = "DP00800001002"
    EXCEEDS_WITHDRAWAL_AMOUNT_LIMIT = "DP00800001003"
    INVALID_AMOUNT = "DP00800001004"
    TRANSACTION_ID_IS_INVALID = "DP00800001005"
    IN_PROCESS = "DP00800001006"
    NOT_ENOUGH_BALANCE = "DP00800001007"
    REFUSED = "DP00800001008"
    DO_NOT_HONOR = "DP00800001009"
    TRANSACTION_NOT_PERMITTED_TO_PAYEE = "DP00800001010"
    TRANSACTION_TIMED_OUT = "DP00800001024"
    TRANSACTION_NOT_FOUND = "DP00800001025"
    FORBIDDEN = "DP00800001026"
    TRANSACTION_EXPIRED = "DP00800001029"

    @classmethod
    def parse(cls, value: object) -> ResponseCode | None:
        """Resolve a raw ``status.response_code`` value, returning None if it is not a known code"""
        try:
            return cls(value)
        except ValueError:
            return None

    @property
    def reason(self) -> str:
        """The expected error reason for this code, as documented by Airtel"""
        return _REASONS[self]

    @property
    def description(self) -> str:
        """The description for this code, as documented by Airtel"""
        return _DESCRIPTIONS[self]


_REASONS: dict[ResponseCode, str] = {
    ResponseCode.AMBIGUOUS: "Ambiguous",
    ResponseCode.SUCCESS: "Success",
    ResponseCode.INCORRECT_PIN: "Incorrect Pin",
    ResponseCode.EXCEEDS_WITHDRAWAL_AMOUNT_LIMIT: (
        "Exceeds withdrawal amount limit(s) / Withdrawal amount limit exceeded"
    ),
    ResponseCode.INVALID_AMOUNT: "Invalid Amount",
    ResponseCode.TRANSACTION_ID_IS_INVALID: "Transaction ID is invalid",
    ResponseCode.IN_PROCESS: "In process",
    ResponseCode.NOT_ENOUGH_BALANCE: "Not enough balance",
    ResponseCode.REFUSED: "Refused",
    ResponseCode.DO_NOT_HONOR: "Do not honor",
    ResponseCode.TRANSACTION_NOT_PERMITTED_TO_PAYEE: "Transaction not permitted to Payee",
    ResponseCode.TRANSACTION_TIMED_OUT: "Transaction Timed Out",
    ResponseCode.TRANSACTION_NOT_FOUND: "Transaction Not Found",
    ResponseCode.FORBIDDEN: "Forbidden",
    ResponseCode.TRANSACTION_EXPIRED: "Transaction Expired",
}

_DESCRIPTIONS: dict[ResponseCode, str] = {
    ResponseCode.AMBIGUOUS: (
        "The transaction is still processing and is in ambiguous state. "
        "Please do the transaction enquiry to fetch the transaction status."
    ),
    ResponseCode.SUCCESS: "Transaction is successful.",
    ResponseCode.INCORRECT_PIN: "Incorrect pin has been entered.",
    ResponseCode.EXCEEDS_WITHDRAWAL_AMOUNT_LIMIT: "The User has exceeded their wallet allowed transaction limit.",
    ResponseCode.INVALID_AMOUNT: "The amount User is trying to transfer is less than the minimum amount allowed.",
    ResponseCode.TRANSACTION_ID_IS_INVALID: "User didn't enter the pin.",
    ResponseCode.IN_PROCESS: "Transaction in pending state. Please check after sometime.",
    ResponseCode.NOT_ENOUGH_BALANCE: "User wallet does not have enough money to cover the payable amount.",
    ResponseCode.REFUSED: "The transaction was refused.",
    ResponseCode.DO_NOT_HONOR: "This is a generic refusal that has several possible causes.",
    ResponseCode.TRANSACTION_NOT_PERMITTED_TO_PAYEE: (
        "Payee is already initiated for churn or barred or not registered on Airtel Money platform."
    ),
    ResponseCode.TRANSACTION_TIMED_OUT: "The transaction was timed out.",
    ResponseCode.TRANSACTION_NOT_FOUND: "The transaction was not found.",
    ResponseCode.FORBIDDEN: "X-signature and payload did not match.",
    ResponseCode.TRANSACTION_EXPIRED: "Transaction has been expired.",
}


def response_code_reason(value: object) -> str | None:
    """The documented reason for a raw ``status.response_code``, or None if it is not a known code"""
    code = ResponseCode.parse(value)
    return None if code is None else code.reason


def response_code_description(value: object) -> str | None:
    """The documented description for a raw ``status.response_code``, or None if it is not a known code"""
    code = ResponseCode.parse(value)
    return None if code is None else code.description
