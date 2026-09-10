from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Oauth2TokenBody")


@_attrs_define
class Oauth2TokenBody:
    """
    Attributes:
        client_id (str): The client_id is a public identifier for apps. It must also be unique across all clients that
            the authorization server handles. This is equivalent to consumer key displayed under keys section of application
            listing. Example: c02e9e46-db9d-4faf-b91a-94f88bbe688c.
        client_secret (str): The client_secret is a secret known only to the application and the authorization server.
            This is equivalent to consumer secret displayed under keys section of application listing. Example:
            ab672211-4197-4c11-ba79-b29ce2034ca2.
        grant_type (str): The Client Credential grant type is used by confidential and public clients to fetch access
            token. Example: client_credentials.
    """

    client_id: str
    client_secret: str
    grant_type: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        client_secret = self.client_secret

        grant_type = self.grant_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": grant_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_id = d.pop("client_id")

        client_secret = d.pop("client_secret")

        grant_type = d.pop("grant_type")

        oauth_2_token_body = cls(
            client_id=client_id,
            client_secret=client_secret,
            grant_type=grant_type,
        )

        oauth_2_token_body.additional_properties = d
        return oauth_2_token_body

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
