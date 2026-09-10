from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_transaction import PaymentTransaction


T = TypeVar("T", bound="PaymentData")


@_attrs_define
class PaymentData:
    """Ussd Payment Response.

    Attributes:
        transaction (PaymentTransaction | Unset): Ussd Payment Transaction.
    """

    transaction: PaymentTransaction | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transaction: dict[str, Any] | Unset = UNSET
        if not isinstance(self.transaction, Unset):
            transaction = self.transaction.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if transaction is not UNSET:
            field_dict["transaction"] = transaction

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.payment_transaction import PaymentTransaction

        d = dict(src_dict)
        _transaction = d.pop("transaction", UNSET)
        transaction: PaymentTransaction | Unset
        if isinstance(_transaction, Unset):
            transaction = UNSET
        else:
            transaction = PaymentTransaction.from_dict(_transaction)

        payment_data = cls(
            transaction=transaction,
        )

        payment_data.additional_properties = d
        return payment_data

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
