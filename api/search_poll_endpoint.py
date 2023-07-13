"""
Module for polling search results using the Mozio API.
"""

import time

from connections.api_connections import MozioClient
from errors.errors import FieldNotFalseError, SearchNotValidError


class SearchPoll:
    """
    Class for polling search results using the Mozio API.
    """

    @staticmethod
    def poll_search_results(search_id: str, client: object):
        """
        Poll the search results for a specific search ID using the Mozio API.

        Args:
            search_id (str): The ID of the search to poll results for.
            client (object): The MozioClient object for making API requests.

        Returns:
            dict: The search results in a dictionary format.

        """
        endpoint = f"/search/{search_id}/poll/"
        response = client.connect(method="get", endpoint=endpoint, payload=None)
        search_results = response.json()
        return search_results

    @staticmethod
    def get_poll_result_id(search_id: str):
        """
        Get the poll result ID for a specific search ID using the Mozio API.

        Args:
            search_id (str): The ID of the search to get the poll result ID for.

        Returns:
            str: The poll result ID for the search.

         Raises:
            FieldNotFalseError: If the 'more_coming' field never returns False.

        """
        more_comming = False
        timeout = 20
        client = MozioClient()
        start_time = time.time()
        # poll results
        while not more_comming:
            time.sleep(2)  # check every two seconds for new comming searches
            search_results = SearchPoll.poll_search_results(search_id, client)
            more_comming = search_results.get("more_coming", False)
            # Check if the timeout has been reached
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                raise FieldNotFalseError("The field more_comming never returned False")

        results = search_results.get("results", [{}])
        result_id = results[0].get("result_id", "0")
        SearchPoll.handle_errors(result_id)
        del client
        return result_id

    @staticmethod
    def handle_errors(result_id: str) -> None:
        """
        Evaluates if there is a valid ID from the response of the Mozio API.

        Args:
            result_id (str): The ID from the API response.

        Raises:
            SearchNotValidError: If the ID is not valid.
        """
        if not result_id or result_id == "0":
            raise SearchNotValidError(
                f"Failed to get a valid search id:\
                    ID: {result_id}"
            )
