"""
This module provides a client for interacting with the Mozio API.
"""

import requests

from errors.errors import (
    APIBadRequestError,
    APIInvalidKeyError,
    APINonFieldError,
    APINotRespondingError,
)
from config.config import API_KEY, BASE_URL, TIME_OUT


class MozioClient:
    """Client for interacting with the Mozio API."""

    def __init__(self):
        """Initialize the MozioClient instance."""
        self.headers = {"API-KEY": f"{API_KEY}"}
        self.url = ""
        self.request_methods = {
            "get": requests.get,
            "post": requests.post,
            "delete": requests.delete,
        }

    def connect(self,
                method: str,
                endpoint: str,
                payload: dict) -> requests.Response:
        """
        Send a request to the Mozio API.

        Args:
            method (str): The HTTP method for the request.
            endpoint (str): The API endpoint to connect to.
            payload (dict): The payload to include in the request body.

        Returns:
            requests.Response: The response from the API.

        Raises:
            ValueError: If the provided method is not allowed.
            APIBadRequestError: If the API responds with a bad request.
            APIInvalidKeyError: If the API key used is invalid.
            APINonFieldError: If the API responds with a non-field error.
            APINotRespondingError: If the API does not respond.
        """
        self.url = f"{BASE_URL}{endpoint}"
        allowed_methods = list(self.request_methods.keys())

        if not method.lower() in allowed_methods:
            raise ValueError(
                f"Invalid method '{method}'. \
                    Allowed methods: {', '.join(allowed_methods)}"
            )

        request_method = self.request_methods.get(method.lower(), False)

        try:
            response = request_method(
                url=self.url,
                headers=self.headers,
                json=payload,
                timeout=TIME_OUT,
            )
        except TimeoutError as ter:
            raise APINotRespondingError(
                f"API not responding to the given endpoint: \
                    Endpoint: {self.url}, Method: {method}"
            ) from ter

        self.handle_errors(response)

        return response

    def handle_errors(self, response: requests.Response) -> None:
        """
        Handle error responses from the Mozio API.

        Args:
            response (requests.Response): The response object from the API.

        Raises:
            APIBadRequestError: If the API responds with a bad request.
            APIInvalidKeyError: If the API key used is invalid.
            APINonFieldError: If the API responds with a non-field error.
        """
        if response.status_code == 400:
            raise APIBadRequestError(
                f"Bad Request. {response.json().get('specific_param', '')}"
            )

        if response.status_code == 403:
            raise APIInvalidKeyError(
                "The API key used does not have access permissions."
            )

        if response.status_code in range(404, 452):
            raise APINonFieldError(
                f"The API responded with a non-field error: {response}"
            )
