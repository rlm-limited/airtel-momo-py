from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Subscriber")


@_attrs_define
class Subscriber:
    """Subscriber.

    Attributes:
        country (str): The country of the subscriber. Example: RW.
        msisdn (str): MSISDN without the country code of the subscriber from which the payment amount deducted.
        currency (str | Unset): The currency of the subscriber. Example: RWF.
    """

    country: str
    msisdn: str
    currency: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        country = self.country

        msisdn = self.msisdn

        currency = self.currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "country": country,
                "msisdn": msisdn,
            }
        )
        if currency is not UNSET:
            field_dict["currency"] = currency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        country = d.pop("country")

        msisdn = d.pop("msisdn")

        currency = d.pop("currency", UNSET)

        subscriber = cls(
            country=country,
            msisdn=msisdn,
            currency=currency,
        )

        subscriber.additional_properties = d
        return subscriber

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
