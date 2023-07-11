"""
This module provides a client for interacting with the Mozio API.
"""
import requests

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
            "patch": requests.patch,
            "delete": requests.delete,
        }

    def connect(self, method: str, endpoint: str, payload: dict) -> dict:
        """
        Send a request to the Mozio API.

        Args:
            method (str): The HTTP method for the request.
            endpoint (str): The API endpoint to connect to.
            payload (dict): The payload to include in the request body.

        Returns:
            requests.Response (dict): The response from the API.

        Raises:
            ValueError: If the provided method is not allowed.
        """
        self.url = f"{BASE_URL}{endpoint}"

        request_method = self.request_methods.get(method.lower(), False)

        if not request_method:
            allowed_methods = list(self.request_methods.keys())
            raise ValueError(
                f"Invalid method '{method}'.\
                Allowed methods: {', '.join(allowed_methods)}"
            )

        response = request_method(
            url=self.url,
            headers=self.headers,
            json=payload,
            timeout=TIME_OUT,
        )

        return response
