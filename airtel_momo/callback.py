"""Handling of the inbound payment callback Airtel POSTs to the merchant's own URL.

Everything under ``airtel_momo.api`` is an outbound call to Airtel; this module is the inbound
half. A USSD Push returns while the payment is still pending (``DP00800001006``, In process), and
the final outcome only arrives later as a POST to the callback URL registered for the merchant.

The handler is deliberately framework-agnostic - it takes the raw request body and hands back a
status code and a body, leaving the host application to build its own HTTP response.

Wiring it into an application::

    from airtel_momo import CallbackHandler
    from airtel_momo.models import CallbackBody, CallbackStatusCode

    def on_payment(body: CallbackBody) -> None:
        txn = body.transaction
        if CallbackStatusCode.parse(txn.status_code) is CallbackStatusCode.TRANSACTION_SUCCESS:
            mark_paid(txn.id, airtel_money_id=txn.airtel_money_id)
        else:
            mark_failed(txn.id, reason=txn.message)

    handler = CallbackHandler(on_payment)

Django::

    @csrf_exempt
    def airtel_callback(request):
        result = handler.handle(request.body)
        return JsonResponse(result.body, status=result.status_code)

Flask::

    @app.post("/payment/callback/airtel")
    def airtel_callback():
        result = handler.handle(request.get_data())
        return jsonify(result.body), result.status_code

FastAPI (with an async ``on_payment``)::

    @app.post("/payment/callback/airtel")
    async def airtel_callback(request: Request):
        result = await handler.ahandle(await request.body())
        return JSONResponse(result.body, status_code=result.status_code)

Two things this module deliberately does not do:

- **Authenticate the caller.** Airtel's docs specify only ``Content-Type`` on this request - there
  is no signature or shared secret (``x-signature`` / ``x-key`` are for outbound calls). Protect the
  endpoint at the application or proxy layer: an unguessable path, an IP allowlist, or similar.
- **Deduplicate.** Delivery is at-least-once, so the same callback may arrive more than once. Make
  ``on_payment`` idempotent, keyed on ``transaction.id`` or ``airtel_money_id``.

Exceptions raised by the registered function propagate untouched, so a failure on the application's
side becomes a 5xx and Airtel retries delivery. Only an unparseable body is converted into a
result, with status 400.
"""

from __future__ import annotations

import inspect
import json
from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from attrs import define, field

from .errors import CallbackParseError
from .models.callback_body import CallbackBody
from .models.callback_transaction import CallbackTransaction

CallbackFunc = Callable[[CallbackBody], None]
AsyncCallbackFunc = Callable[[CallbackBody], Awaitable[None]]


def parse_callback(payload: bytes | str | Mapping[str, Any]) -> CallbackBody:
    """Parse a raw Airtel callback body into a CallbackBody

    Accepts the raw request body as ``bytes`` (what most web frameworks hand you), as ``str``, or as
    an already-decoded mapping.

    Args:
        payload: The raw callback body.

    Raises:
        CallbackParseError: If the payload is not valid JSON, is not a JSON object, or is missing
            any of the mandatory fields.

    Returns:
        CallbackBody
    """
    if isinstance(payload, Mapping):
        data: Any = payload
    else:
        if isinstance(payload, bytes):
            try:
                text = payload.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise CallbackParseError(f"Callback body is not valid UTF-8: {exc}", payload) from exc
        else:
            text = payload

        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise CallbackParseError(f"Callback body is not valid JSON: {exc}", payload) from exc

    if not isinstance(data, Mapping):
        raise CallbackParseError(
            f"Callback body must be a JSON object, got {type(data).__name__}",
            payload if isinstance(payload, bytes | str) else None,
        )

    try:
        return CallbackBody.from_dict(data)
    except KeyError as exc:
        raise CallbackParseError(
            f"Callback body is missing mandatory field {exc}",
            payload if isinstance(payload, bytes | str) else None,
        ) from exc
    except (AttributeError, TypeError) as exc:
        raise CallbackParseError(f"Callback body has an unexpected shape: {exc}", None) from exc


@define
class CallbackResult:
    """The outcome of handling one callback

    Attributes:
        status_code: 200 when the callback was accepted, 400 when the body could not be parsed.
        body: A small acknowledgement body. Airtel does not document a required ack payload, so
            returning this verbatim is safe, as is ignoring it and answering with a bare 200.
        transaction: The parsed transaction, or None when the body could not be parsed.
        error: The parse failure message, or None when the callback was accepted.
    """

    status_code: int
    body: dict[str, Any]
    transaction: CallbackTransaction | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        """Whether the callback was accepted"""
        return self.error is None


@define
class CallbackHandler:
    """Dispatches inbound Airtel callbacks to an application-supplied function

    Attributes:
        func: Called with the parsed CallbackBody once a callback is accepted. May be a plain
            function or a coroutine function; a coroutine function requires ahandle().
    """

    func: CallbackFunc | AsyncCallbackFunc = field()

    def handle(self, payload: bytes | str | Mapping[str, Any]) -> CallbackResult:
        """Parse a callback body and dispatch it to the registered function

        Exceptions raised by the registered function propagate, so the application answers with a
        5xx and Airtel retries delivery. An unparseable body is returned as a 400 result instead.

        Args:
            payload: The raw callback body.

        Raises:
            TypeError: If the registered function is a coroutine function; use ahandle() instead.

        Returns:
            CallbackResult
        """
        if inspect.iscoroutinefunction(self.func):
            raise TypeError(
                f"{getattr(self.func, '__name__', self.func)!r} is a coroutine function; "
                "use 'await handler.ahandle(payload)' instead of 'handler.handle(payload)'"
            )

        try:
            body = parse_callback(payload)
        except CallbackParseError as exc:
            return _rejected(exc)

        self.func(body)  # type: ignore[arg-type]

        return _accepted(body)

    async def ahandle(self, payload: bytes | str | Mapping[str, Any]) -> CallbackResult:
        """Parse a callback body and dispatch it to the registered function, awaiting if needed

        Accepts both a coroutine function and a plain function, so an async application can use
        either. Behaves like handle() in every other respect.

        Args:
            payload: The raw callback body.

        Returns:
            CallbackResult
        """
        try:
            body = parse_callback(payload)
        except CallbackParseError as exc:
            return _rejected(exc)

        result = self.func(body)
        if inspect.isawaitable(result):
            await result

        return _accepted(body)


def _accepted(body: CallbackBody) -> CallbackResult:
    return CallbackResult(
        status_code=200,
        body={"status": "ok"},
        transaction=body.transaction,
    )


def _rejected(exc: CallbackParseError) -> CallbackResult:
    message = str(exc)
    return CallbackResult(
        status_code=400,
        body={"status": "error", "message": message},
        error=message,
    )


__all__ = [
    "AsyncCallbackFunc",
    "CallbackFunc",
    "CallbackHandler",
    "CallbackResult",
    "parse_callback",
]
