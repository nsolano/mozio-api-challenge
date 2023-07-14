"""
Module for deleting the reservation using the Mozio API.
"""

from connections.api_connections import MozioClient
from errors.errors import DeleteFailedError


class DeleteRide:
    """
    Class for deleting the ride reservation using the Mozio API.
    """

    @staticmethod
    def delete_ride(reservation_id: str)-> dict:
        """
        Poll the book results for a specific search ID using the Mozio API.

        Args:
            search_id (str): The ID of the search to poll results for.
            client (object): The MozioClient object for making API requests.

        Returns:
            dict: The search results in a dictionary format.

        """
        client = MozioClient()
        endpoint = f"/reservations/{reservation_id}/"
        response = client.connect(method="delete", endpoint=endpoint, payload=None)
        results = response.json()
        DeleteRide.handle_errors(results)
        return results


    @staticmethod
    def handle_errors(results:str) -> None:
        """
        Evaluates if there is a status from the response of the Mozio API.

        Args:
            status (str): The status from the API response.

        Raises:
            SearchNotValidError: If the status or 
            confirmation_number is not valid.
            StatusFailedError: If status failed
        """
        if not results or results == {}:
            raise DeleteFailedError(
                f"Failed to delete the ride:\
                    Results: {results}"
            )
