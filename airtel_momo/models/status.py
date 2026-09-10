from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Status")


@_attrs_define
class Status:
    """Status Response.

    Attributes:
        code (str | Unset): Status code, HTTP status code. Example: 200.
        message (str | Unset): The descriptive message of the response/action. Example: SUCCESS.
        result_code (str | Unset): Application specific code to identify the error and success response. This will be
            different for the type of error and success. Deprecated. Please use response_code field for new error code.
            Example: ESB000010.
        response_code (str | Unset): Product specific code to identify the error and success response. This will be
            different for the type of error and success. Left as a str because Airtel may return codes beyond the
            documented set; see ResponseCode and response_code_reason() to resolve one. Example: DP00800001006.
        success (bool | Unset): true if no error else false.
    """

    code: str | Unset = UNSET
    message: str | Unset = UNSET
    result_code: str | Unset = UNSET
    response_code: str | Unset = UNSET
    success: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        result_code = self.result_code

        response_code = self.response_code

        success = self.success

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if message is not UNSET:
            field_dict["message"] = message
        if result_code is not UNSET:
            field_dict["result_code"] = result_code
        if response_code is not UNSET:
            field_dict["response_code"] = response_code
        if success is not UNSET:
            field_dict["success"] = success

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code", UNSET)

        message = d.pop("message", UNSET)

        result_code = d.pop("result_code", UNSET)

        response_code = d.pop("response_code", UNSET)

        success = d.pop("success", UNSET)

        status = cls(
            code=code,
            message=message,
            result_code=result_code,
            response_code=response_code,
            success=success,
        )

        status.additional_properties = d
        return status

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
