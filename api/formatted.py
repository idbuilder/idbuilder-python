"""Formatted ID API."""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from models import ApiResponse, FormattedIdResponse
from api.base import BaseApi

if TYPE_CHECKING:
    from client import IdBuilderClient


class FormattedApi(BaseApi):
    """API for generating formatted string IDs."""

    def __init__(self, client: IdBuilderClient, key: str) -> None:
        """Initialize the API.

        Args:
            client: The parent IdBuilderClient.
            key: The configuration key for this ID type.
        """
        super().__init__(client)
        self._key = key

    def generate(self, count: int = 1) -> list[str]:
        """Generate multiple formatted string IDs.

        Args:
            count: Number of IDs to generate (default: 1, max: 1000).

        Returns:
            A list of generated formatted string IDs.

        Raises:
            IdBuilderError: If the request fails.
        """
        if count < 1:
            raise ValueError("count must be at least 1")
        if count > 1000:
            raise ValueError("count must not exceed 1000")

        url = f"{self._client.base_url}/v1/id/formatted?key={quote(self._key)}&size={count}"
        data = self._request(url)

        response = ApiResponse[FormattedIdResponse](
            code=data.get("code", 0),
            message=data.get("message", ""),
            data=FormattedIdResponse(ids=data.get("data", {}).get("ids", []))
            if data.get("data")
            else None,
        )

        return self._handle_response(response, self._key).ids

    def generate_one(self) -> str:
        """Generate a single formatted string ID.

        Returns:
            A single generated formatted string ID.

        Raises:
            IdBuilderError: If the request fails.
        """
        return self.generate(1)[0]
