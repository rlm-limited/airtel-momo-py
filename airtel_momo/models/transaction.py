from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Transaction")


@_attrs_define
class Transaction:
    """Transaction details.

    Attributes:
        amount (float): Transaction amount which will be deducted from subscriber's wallet. Example: 1000.
        id (str): Partner unique transaction id to identify the transaction.
        country (str | Unset): The country in which the transaction is happening, basically used for cross border
            payments. For the same country, this field is not required.
        currency (str | Unset): The currency in which the transaction is happening, basically used for cross border
            payments. For the same country, this field is not required.
    """

    amount: float
    id: str
    country: str | Unset = UNSET
    currency: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        id = self.id

        country = self.country

        currency = self.currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "id": id,
            }
        )
        if country is not UNSET:
            field_dict["country"] = country
        if currency is not UNSET:
            field_dict["currency"] = currency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount = d.pop("amount")

        id = d.pop("id")

        country = d.pop("country", UNSET)

        currency = d.pop("currency", UNSET)

        transaction = cls(
            amount=amount,
            id=id,
            country=country,
            currency=currency,
        )

        transaction.additional_properties = d
        return transaction

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
