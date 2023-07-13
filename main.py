"""
Main script for performing a search and polling the results using the Mozio API.
"""

from api.search_endpoint import RideSearchParams, Search
from api.search_poll_endpoint import SearchPoll


def perform_search():
    """
    Perform a search using the Mozio API.

    Returns:
        str: The search ID.
    """
    search = Search()
    ride_params = RideSearchParams(
        start_address="44 Tehama Street, San Francisco, CA, USA",
        end_address="SFO",
        mode="one_way",
        pickup_datetime="2023-12-01 15:30",
        num_passengers=2,
        currency="USD",
        campaign="Nelson Solano",
    )
    search_id = search.search_ride(ride_params)
    return search_id


def poll_search_results(search_id):
    """
    Poll search results using the Mozio API.

    Args:
        search_id (str): The ID of the search to poll results for.

    Returns:
        str: The result ID.
    """
    search_poll = SearchPoll()
    result_id = search_poll.get_poll_result_id(search_id)
    return result_id


def main():
    """
    Main function to perform the search and poll the results.
    """
    search_id = perform_search()
    result_id = poll_search_results(search_id)
    print(result_id)


if __name__ == "__main__":
    main()
    