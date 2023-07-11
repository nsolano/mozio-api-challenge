"""
Module for polling search results using the Mozio API.
"""

import time

from connections.api_connections import MozioClient

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

        """
        more_comming = False
        counter = 0
        client = MozioClient()
        while not more_comming and counter < 11:
            time.sleep(2)  # check every two seconds for new comming searches
            search_results = SearchPoll.poll_search_results(search_id, client)
            more_comming = search_results.get("more_coming", False)
            counter += 1
        results = search_results.get("results", [])
        result_id = results[0].get("result_id", "0")
        del client
        return result_id
