"""
Module for booking rides using the Mozio API.
"""
from dataclasses import dataclass

from connections.api_connections import MozioClient
from errors.errors import SearchNotValidError, StatusFailedError


@dataclass
class RideBookParams:
    """
    Data class for the required parameters.

    Params:
        search_id (str): The ID of the search.
        result_id (str): The ID of the search result.
        email (str): The email address of the customer.
        country_code_name (str): The country code name.
        phone_number (str): The phone number of the customer.
        first_name (str): The first name of the customer.
        last_name (str): The last name of the customer.
        airline (str): The airline name.
        flight_number (str): The flight number.
        customer_special_instructions (str): Special instructions provided by the customer.
        provider (dict): The provider information.

    """

    search_id: str
    result_id: str
    email: str
    country_code_name: str
    phone_number: str
    first_name: str
    last_name: str
    airline: str
    flight_number: str
    customer_special_instructions: str
    provider: dict


class Book:
    """
    Class for searching rides using the Mozio API.
    """

    @staticmethod
    def book_ride(params: RideBookParams) -> str:
        """
        Reserve a rides using the Mozio API.

        Args:
            params (BookRideParam): The parameters for the ride reservation.

        Returns:
            str: The status of the reservation.

        """
        client = MozioClient()
        endpoint = "/reservations/"
        payload = {
            "search_id": params.search_id,
            "result_id": params.result_id,
            "email": params.email,
            "country_code_name": params.country_code_name,
            "phone_number": params.phone_number,
            "first_name": params.first_name,
            "last_name": params.last_name,
            "airline": params.airline,
            "flight_number": params.flight_number,
            "customer_special_instructions": params.customer_special_instructions,
            "provider": params.provider,
        }

        response = client.connect(method="post", endpoint=endpoint, payload=payload)

        status = response.json().get("status", "")

        Book.handle_errors(status)

        del client

        return status

    @staticmethod
    def handle_errors(status: str) -> None:
        """
        Evaluates if there is a status from the response of the Mozio API.

        Args:
            status (str): The status from the API response.

        Raises:
            SearchNotValidError: If the ID is not valid.
            StatusFailedErro: If status failed
        """
        if not status or status == "":
            raise SearchNotValidError(
                f"Failed to get a valid status:\
                    ID: {status}"
            )

        if status == "failed":
            raise StatusFailedError(f"API responded with status: {status}")
