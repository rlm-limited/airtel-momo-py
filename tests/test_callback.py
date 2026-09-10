import asyncio
import json

import pytest

from airtel_momo import CallbackHandler, parse_callback
from airtel_momo.errors import CallbackParseError
from airtel_momo.models.callback_body import CallbackBody
from airtel_momo.models.callback_status_code import CallbackStatusCode, callback_status_description

# The sample payload from the Airtel documentation, verbatim
SAMPLE = {
    "transaction": {
        "id": "BBZMiscxy",
        "message": "Paid RWF 5,000 to MeshPower Ltd Charge RWF 140, Trans ID MP210603.1234.L06941.",
        "status_code": "TS",
        "airtel_money_id": "MP210603.1234.L06941",
    }
}


def test_parse_doc_sample():
    """The documented sample payload parses and round-trips unchanged"""
    body = parse_callback(json.dumps(SAMPLE).encode())

    assert isinstance(body, CallbackBody)
    assert body.transaction.id == "BBZMiscxy"
    assert body.transaction.airtel_money_id == "MP210603.1234.L06941"
    assert body.transaction.status_code == "TS"
    assert body.transaction.message.startswith("Paid RWF 5,000")
    assert body.to_dict() == SAMPLE


def test_parse_accepts_bytes_str_and_mapping():
    """All three input shapes a web framework might hand over produce the same result"""
    from_bytes = parse_callback(json.dumps(SAMPLE).encode())
    from_str = parse_callback(json.dumps(SAMPLE))
    from_dict = parse_callback(SAMPLE)

    assert from_bytes.to_dict() == from_str.to_dict() == from_dict.to_dict() == SAMPLE


def test_status_code_resolution():
    """TS and TF resolve to the documented meanings"""
    assert CallbackStatusCode.parse("TS") is CallbackStatusCode.TRANSACTION_SUCCESS
    assert CallbackStatusCode.parse("TF") is CallbackStatusCode.TRANSACTION_FAILED

    assert CallbackStatusCode.TRANSACTION_SUCCESS.succeeded is True
    assert CallbackStatusCode.TRANSACTION_FAILED.succeeded is False

    assert CallbackStatusCode.TRANSACTION_SUCCESS.description == "Transaction Success"
    assert callback_status_description("TF") == "Transaction Failed"

    # str-enum equality with the raw wire value
    assert CallbackStatusCode.TRANSACTION_SUCCESS == "TS"


def test_failed_transaction_payload():
    """A TF callback parses and reports failure"""
    payload = {
        "transaction": {
            "id": "BBZMiscxy",
            "message": "Transaction failed",
            "status_code": "TF",
            "airtel_money_id": "MP210603.1234.L06941",
        }
    }
    body = parse_callback(payload)
    code = CallbackStatusCode.parse(body.transaction.status_code)

    assert code is CallbackStatusCode.TRANSACTION_FAILED
    assert code.succeeded is False


def test_unknown_status_code_still_parses():
    """An undocumented status code must not break parsing, matching ResponseCode's tolerance"""
    payload = {"transaction": dict(SAMPLE["transaction"], status_code="XX")}
    body = parse_callback(payload)

    assert body.transaction.status_code == "XX"
    assert CallbackStatusCode.parse("XX") is None
    assert callback_status_description("XX") is None


@pytest.mark.parametrize(
    "payload",
    [
        b"not json at all",
        b"[]",
        b'"a string"',
        b"{}",
        json.dumps({"transaction": {"id": "x"}}).encode(),
        json.dumps({"nottransaction": {}}).encode(),
    ],
)
def test_malformed_payloads_rejected(payload):
    """Unparseable bodies raise CallbackParseError and handle() turns them into a 400"""
    with pytest.raises(CallbackParseError):
        parse_callback(payload)

    calls = []
    result = CallbackHandler(calls.append).handle(payload)

    assert result.status_code == 400
    assert result.ok is False
    assert result.error
    assert result.transaction is None
    assert calls == [], "the registered function must not run for a rejected payload"


def test_handle_dispatches_once_and_accepts():
    """A valid callback is dispatched exactly once and answered with 200"""
    seen = []
    result = CallbackHandler(seen.append).handle(json.dumps(SAMPLE).encode())

    assert result.status_code == 200
    assert result.ok is True
    assert result.body == {"status": "ok"}
    assert result.transaction is not None
    assert result.transaction.id == "BBZMiscxy"

    assert len(seen) == 1
    assert seen[0].transaction.airtel_money_id == "MP210603.1234.L06941"


def test_application_errors_propagate():
    """An exception from the registered function bubbles out so Airtel retries delivery"""

    def boom(body):
        raise RuntimeError("database unavailable")

    with pytest.raises(RuntimeError, match="database unavailable"):
        CallbackHandler(boom).handle(json.dumps(SAMPLE).encode())


def test_ahandle_with_async_function():
    """ahandle() awaits a coroutine function"""
    seen = []

    async def on_payment(body):
        await asyncio.sleep(0)
        seen.append(body)

    result = asyncio.run(CallbackHandler(on_payment).ahandle(json.dumps(SAMPLE).encode()))

    assert result.status_code == 200
    assert len(seen) == 1
    assert seen[0].transaction.id == "BBZMiscxy"


def test_ahandle_with_sync_function():
    """ahandle() also accepts a plain function, so async apps can use either"""
    seen = []
    result = asyncio.run(CallbackHandler(seen.append).ahandle(json.dumps(SAMPLE).encode()))

    assert result.status_code == 200
    assert len(seen) == 1


def test_ahandle_rejects_malformed():
    """The async path applies the same 400 contract"""
    result = asyncio.run(CallbackHandler(lambda body: None).ahandle(b"not json"))

    assert result.status_code == 400
    assert result.ok is False


def test_handle_rejects_coroutine_function():
    """Passing an async function to the sync handle() fails loudly rather than never awaiting it"""

    async def on_payment(body):
        pass

    with pytest.raises(TypeError, match="ahandle"):
        CallbackHandler(on_payment).handle(json.dumps(SAMPLE).encode())


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
