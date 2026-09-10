from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.callback_transaction import CallbackTransaction


T = TypeVar("T", bound="CallbackBody")


@_attrs_define
class CallbackBody:
    """The body Airtel POSTs to the merchant's callback URL once a payment reaches a final state.

    Example:
        {'transaction': {'id': 'BBZMiscxy', 'message': 'Paid RWF 5,000 to TECHNOLOGIES LIMITED Charge RWF 140,
            Trans ID MP210603.1234.L06941.', 'status_code': 'TS', 'airtel_money_id': 'MP210603.1234.L06941'}}

    Attributes:
        transaction (CallbackTransaction): Transaction detail.
    """

    transaction: CallbackTransaction
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transaction = self.transaction.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transaction": transaction,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.callback_transaction import CallbackTransaction

        d = dict(src_dict)
        transaction = CallbackTransaction.from_dict(d.pop("transaction"))

        callback_body = cls(
            transaction=transaction,
        )

        callback_body.additional_properties = d
        return callback_body

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
