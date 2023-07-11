"""
Module for searching rides using the Mozio API.
"""

from connections.api_connections import MozioClient


class Search:
    """
    Class for searching rides using the Mozio API.
    """
    @staticmethod
    def search_ride(
        start_address: str,
        end_address: str,
        mode: str,
        pickup_datetime: str,
        num_passengers: int,
        currency: str,
        campaign: str,
    ):
        """
        Search for rides using the Mozio API.

        Args:
            start_address (str): The starting address for the ride.
            end_address (str): The ending address for the ride.
            mode (str): The mode of the ride (e.g., 'one_way', 'round_trip', etc.).
            pickup_datetime (str): The pickup date and time for the ride.
            num_passengers (int): The number of passengers for the ride.
            currency (str): The currency to use for pricing information.
            campaign (str): The campaign information for the ride.

        Returns:
            str: The search ID for the ride.

        """
        client = MozioClient()
        endpoint = "/search/"
        payload = {
            "start_address": start_address,
            "end_address": end_address,
            "mode": mode,
            "pickup_datetime": pickup_datetime,
            "num_passengers": num_passengers,
            "currency": currency,
            "campaign": campaign,
        }

        response = client.connect(method="post", endpoint=endpoint, payload=payload)
        search_id = response.json().get("search_id", "0")
        del client
        return search_id