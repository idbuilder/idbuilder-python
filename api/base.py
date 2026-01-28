"""Base API class with common HTTP functionality."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, TypeVar
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from error import (
    ApiError,
    ConfigNotFoundError,
    ForbiddenError,
    HttpError,
    RateLimitedError,
    SequenceExhaustedError,
    UnauthorizedError,
)
from models import ApiResponse

if TYPE_CHECKING:
    from client import IdBuilderClient

T = TypeVar("T")


class BaseApi:
    """Base class for API implementations."""

    def __init__(self, client: IdBuilderClient) -> None:
        """Initialize the base API.

        Args:
            client: The parent IdBuilderClient.
        """
        self._client = client

    def _request(self, url: str) -> dict[str, Any]:
        """Make an HTTP GET request.

        Args:
            url: The URL to request.

        Returns:
            The parsed JSON response.

        Raises:
            IdBuilderError: If the request fails.
        """
        headers = {"Content-Type": "application/json"}

        if self._client.key_token:
            headers["Authorization"] = self._client.key_token

        request = Request(url, headers=headers, method="GET")

        try:
            with urlopen(request, timeout=self._client.timeout) as response:
                body = response.read().decode("utf-8")
                return json.loads(body)
        except HTTPError as e:
            status_code = e.code
            try:
                body = e.read().decode("utf-8")
                data = json.loads(body)
            except (json.JSONDecodeError, UnicodeDecodeError):
                data = {}

            if status_code == 401:
                raise UnauthorizedError(data.get("message", "unauthorized"))
            elif status_code == 403:
                raise ForbiddenError(data.get("message", "forbidden"))
            elif status_code == 429:
                raise RateLimitedError(data.get("message", "rate limited"))
            else:
                raise HttpError(status_code, data.get("message", str(e)))
        except URLError as e:
            raise HttpError(None, str(e.reason))
        except TimeoutError:
            raise HttpError(None, "request timeout")

    def _handle_response(self, response: ApiResponse[T], key: str) -> T:
        """Handle API response and extract data.

        Args:
            response: The API response.
            key: The configuration key (for error messages).

        Returns:
            The response data.

        Raises:
            IdBuilderError: If the response indicates an error.
        """
        if response.is_success():
            if response.data is None:
                raise ApiError(response.code, "response data is null")
            return response.data

        code = response.code
        message = response.message

        if code == 3001:
            raise ConfigNotFoundError(key)
        elif code == 4003:
            raise SequenceExhaustedError(key)
        else:
            raise ApiError(code, message)
