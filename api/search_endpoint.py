"""
Module for searching rides using the Mozio API.
"""
from dataclasses import dataclass
from connections.api_connections import MozioClient

from errors.errors import SearchNotValidError


@dataclass
class RideSearchParams:
    """
    Data class for ride search parameters.

    Params:
        start_address (str): The starting address for the ride.
        end_address (str): The ending address for the ride.
        mode (str): The mode of the ride (e.g., 'one_way', 'round_trip', etc.).
        pickup_datetime (str): The pickup date and time for the ride.
        num_passengers (int): The number of passengers for the ride.
        currency (str): The currency to use for pricing information.
        campaign (str): The campaign information for the ride.
    """

    start_address: str
    end_address: str
    mode: str
    pickup_datetime: str
    num_passengers: int
    currency: str
    campaign: str


class Search:
    """
    Class for searching rides using the Mozio API.
    """

    @staticmethod
    def search_ride(params: RideSearchParams) -> str:
        """
        Search for rides using the Mozio API.

        Args:
            params (RideSearchParams): The parameters for the ride search.  

        Returns:
            str: The search ID for the ride.

        """
        client = MozioClient()
        endpoint = "/search/"
        payload = {
            "start_address": params.start_address,
            "end_address": params.end_address,
            "mode": params.mode,
            "pickup_datetime": params.pickup_datetime,
            "num_passengers": params.num_passengers,
            "currency": params.currency,
            "campaign": params.campaign,
        }

        response = client.connect(
            method="post",
            endpoint=endpoint,
            payload=payload)

        search_id = response.json().get("search_id", "0")

        Search.handle_errors(search_id)

        del client

        return search_id

    @staticmethod
    def handle_errors(search_id: str) -> None:
        """
        Evaluates if there is a valid ID from the response of the Mozio API.

        Args:
            search_id (str): The ID from the API response.

        Raises:
            SearchNotValidError: If the ID is not valid.
        """
        if not search_id or search_id =='0':
            raise SearchNotValidError(
                f"Failed to get a valid search id:\
                    ID: {search_id}"
                )
