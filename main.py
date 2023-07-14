"""
Main script for performing a search and polling the results using the Mozio API.
"""

from json.decoder import JSONDecodeError

from requests.exceptions import RequestException

from api.delete_endpoint import DeleteRide
from api.reservations_endpoint import Book, RideBookParams
from api.reservations_poll_endpoint import BookPoll
from api.search_endpoint import RideSearchParams, Search
from api.search_poll_endpoint import SearchPoll
from errors.errors import (APIBadRequestError, APIInvalidKeyError,
                           APINonFieldError, APINotRespondingError,
                           DeleteFailedError, FieldNotChangedError,
                           FieldNotFalseError, SearchNotValidError,
                           StatusFailedError)
from logs.logger import ErrorLogger

LOGGER = ErrorLogger()


def perform_search() -> str:
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


def perform_booking(search_id: str, result_id: str) -> str:
    """
    Perform a booking using the Mozio API.

    Returns:
        str: The status.
    """
    book = Book()
    ride_params = RideBookParams(
        search_id,
        result_id,
        email="example@example.com",
        country_code_name="US",
        phone_number="8776665543",
        first_name="Johannu",
        last_name="Doe",
        airline="AA",
        flight_number="125",
        customer_special_instructions="Pick the cheapest vehicle available.",
        provider={"name": "Dummy External Provider"},
    )
    status = book.book_ride(ride_params)
    return status


def poll_search_results(search_id: str) -> str:
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


def poll_book_results(search_id: str, status: str) -> tuple:
    """
    Poll book results using the Mozio API.

    Args:
        search_id (str): The ID of the search to poll results.
        status (str): The status of the reservation.

    Returns:
        Tuple[str, str, str]: A tuple containing the reservations
        the final status, the reservation id and the confirmation number.
    """
    book_poll = BookPoll()
    (
        status,
        confirmation_number,
        reservation_id,
    ) = book_poll.get_poll_result_reservations(search_id, status)
    return status, confirmation_number, reservation_id


def perform_delete(reservation_id: str) -> str:
    """
    Poll book results using the Mozio API.

    Args:
        search_id (str): The ID of the search to poll results.
        status (str): The status of the reservation.

    Returns:
        str: The result ID.
    """
    response = DeleteRide.delete_ride(reservation_id)
    return response


def main():
    """
    Main function to perform the search and poll the results.
    """
    try:
        print("-- Performing the ride search --")
        search_id = perform_search()
        print(f"Completed with search ID: {search_id}")
        print("-- Polling the search --")
        result_id = poll_search_results(search_id)
        print(f"Completed with result ID: {result_id}")
        print("-- Polling the reservation --")
        status = perform_booking(search_id, result_id)
        print(f"Completed with the status: {status}")
        status, confirmation_number, reservation_id = poll_book_results(
            search_id, status
        )
        print(f"Completed with the confirmation number: {confirmation_number}")
        print("-- Deleting the reservation --")
        delete = perform_delete(reservation_id)
        print(f"Completed with the response: {delete}")
    except APIBadRequestError as err:
        print(f"Bad Request: {err}")
        LOGGER.log_error(err)
    except APIInvalidKeyError as err:
        print(f"Invalid API Key: {err}")
        LOGGER.log_error(err)
    except APINonFieldError as err:
        print(f"Non-Field Error: {err}")
        LOGGER.log_error(err)
    except APINotRespondingError as err:
        print(f"API Not Responding: {err}")
        LOGGER.log_error(err)
    except DeleteFailedError as err:
        print(f"Delete Failed: {err}")
        LOGGER.log_error(err)
    except FieldNotChangedError as err:
        print(f"Field Not Changed: {err}")
        LOGGER.log_error(err)
    except FieldNotFalseError as err:
        print(f"Field Not False: {err}")
        LOGGER.log_error(err)
    except SearchNotValidError as err:
        print(f"Search Not Valid: {err}")
        LOGGER.log_error(err)
    except StatusFailedError as err:
        print(f"Status Failed: {err}")
        LOGGER.log_error(err)
    except IndexError as err:
        print(f"Index exceded: {err}")
        LOGGER.log_error(err)
    except JSONDecodeError as err:
        print(f"Bad JSON: {err}")
        LOGGER.log_error(err)
    except RequestException as err:
        print(f"Bad JSON: {err}")
        LOGGER.log_error(err)


if __name__ == "__main__":
    main()
