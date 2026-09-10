from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_data import PaymentData
    from ..models.status import Status


T = TypeVar("T", bound="RequestPaymentResponse200")


@_attrs_define
class RequestPaymentResponse200:
    """
    Example:
        {'data': {'transaction': {'id': False, 'status': 'SUCCESS'}}, 'status': {'code': '200', 'message': 'SUCCESS',
            'result_code': 'ESB000010', 'response_code': 'DP00800001006', 'success': True}}

    Attributes:
        data (PaymentData | Unset): Ussd Payment Response.
        status (Status | Unset): Status Response.
    """

    data: PaymentData | Unset = UNSET
    status: Status | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        status: dict[str, Any] | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.payment_data import PaymentData
        from ..models.status import Status

        d = dict(src_dict)
        _data = d.pop("data", UNSET)
        data: PaymentData | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = PaymentData.from_dict(_data)

        _status = d.pop("status", UNSET)
        status: Status | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = Status.from_dict(_status)

        request_payment_response_200 = cls(
            data=data,
            status=status,
        )

        request_payment_response_200.additional_properties = d
        return request_payment_response_200

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
