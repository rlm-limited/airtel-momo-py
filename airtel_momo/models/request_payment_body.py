from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.subscriber import Subscriber
    from ..models.transaction import Transaction


T = TypeVar("T", bound="RequestPaymentBody")


@_attrs_define
class RequestPaymentBody:
    """
    Example:
        {'reference': 'Testing transaction', 'subscriber': {'country': 'RW', 'currency': 'RWF', 'msisdn': '12****89'},
            'transaction': {'amount': 1000, 'country': 'RW', 'currency': 'RWF', 'id': 'random-unique-id'}}

    Attributes:
        reference (str): Reference for service / goods purchased.
        subscriber (Subscriber): Subscriber.
        transaction (Transaction): Transaction details.
    """

    reference: str
    subscriber: Subscriber
    transaction: Transaction
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reference = self.reference

        subscriber = self.subscriber.to_dict()

        transaction = self.transaction.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reference": reference,
                "subscriber": subscriber,
                "transaction": transaction,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.subscriber import Subscriber
        from ..models.transaction import Transaction

        d = dict(src_dict)
        reference = d.pop("reference")

        subscriber = Subscriber.from_dict(d.pop("subscriber"))

        transaction = Transaction.from_dict(d.pop("transaction"))

        request_payment_body = cls(
            reference=reference,
            subscriber=subscriber,
            transaction=transaction,
        )

        request_payment_body.additional_properties = d
        return request_payment_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
