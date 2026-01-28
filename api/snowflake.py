"""Snowflake ID API."""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from models import ApiResponse, SnowflakeIdResponse
from api.base import BaseApi

if TYPE_CHECKING:
    from client import IdBuilderClient


class SnowflakeApi(BaseApi):
    """API for getting snowflake configuration."""

    def __init__(self, client: IdBuilderClient, key: str) -> None:
        """Initialize the API.

        Args:
            client: The parent IdBuilderClient.
            key: The configuration key for this ID type.
        """
        super().__init__(client)
        self._key = key

    def get_config(self) -> SnowflakeIdResponse:
        """Get the snowflake configuration for local ID generation.

        The returned configuration can be used to create a local
        SnowflakeGenerator that generates IDs without network calls.

        Returns:
            SnowflakeIdResponse with worker_id, epoch, worker_bits, sequence_bits.

        Raises:
            IdBuilderError: If the request fails.
        """
        url = f"{self._client.base_url}/v1/id/snowflake?key={quote(self._key)}"
        data = self._request(url)

        response_data = data.get("data", {})
        response = ApiResponse[SnowflakeIdResponse](
            code=data.get("code", 0),
            message=data.get("message", ""),
            data=SnowflakeIdResponse(
                worker_id=response_data.get("worker_id", 0),
                epoch=response_data.get("epoch", 0),
                worker_bits=response_data.get("worker_bits", 0),
                sequence_bits=response_data.get("sequence_bits", 0),
            )
            if response_data
            else None,
        )

        return self._handle_response(response, self._key)
