"""
Module for polling the reservation using the Mozio API.
"""

import time

from connections.api_connections import MozioClient
from errors.errors import FieldNotChangedError, SearchNotValidError, StatusFailedError


class BookPoll:
    """
    Class for polling book results using the Mozio API.
    """

    @staticmethod
    def poll_book_results(search_id: str, client: object):
        """
        Poll the book results for a specific search ID using the Mozio API.

        Args:
            search_id (str): The ID of the search to poll results for.
            client (object): The MozioClient object for making API requests.

        Returns:
            dict: The search results in a dictionary format.

        """
        endpoint = f"/reservations/{search_id}/poll/"
        response = client.connect(method="get", endpoint=endpoint, payload=None)
        search_results = response.json()
        return search_results

    @staticmethod
    def get_poll_result_reservations(search_id: str, status: str) -> tuple:
        """
        Get the poll result ID for a specific search ID using the Mozio API.

        Args:
            search_id (str): The ID of the search to get the poll result ID.
            status (str): The status of the reservation.

        Returns:
            Tuple[str, str, str]: A tuple containing the reservations 
            the final status, the reservation id and the confirmation number.

         Raises:
            FieldNotChangedError: If the 'status' field never changes.

        """
        timeout = 20
        client = MozioClient()
        start_time = time.time()
        # poll results
        while status == 'pending':
            time.sleep(2)  # check every two seconds for new comming searches
            search_results = BookPoll.poll_book_results(search_id, client)
            status = search_results.get("status", 'pending')
            # Check if the timeout has been reached
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                raise FieldNotChangedError("The field status never changed")

        reservations = search_results.get("reservations", [{}])
        confirmation_number = reservations[0].get("confirmation_number", "0")
        reservation_id = reservations[0].get("id", "0")
        BookPoll.handle_errors(status, confirmation_number)
        del client
        return status, confirmation_number, reservation_id

    @staticmethod
    def handle_errors(status: str, confirmation_number: str) -> None:
        """
        Evaluates if there is a status from the response of the Mozio API.

        Args:
            status (str): The status from the API response.

        Raises:
            SearchNotValidError: If the status or 
            confirmation_number is not valid.
            StatusFailedError: If status failed
        """
        if not status or status == "":
            raise SearchNotValidError(
                f"Failed to get a valid status:\
                    Status: {status}"
            )

        if status == "failed":
            raise StatusFailedError(f"API responded with status: {status}")

        if not confirmation_number or confirmation_number == "0":
            raise SearchNotValidError(
                f"Failed to get a confirmation_number:\
                    Reservation: {confirmation_number}"
            )
