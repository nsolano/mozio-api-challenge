"""
Test module for the reservations_poll_endpoint module.
"""

from unittest.mock import patch

import pytest

from connections.api_connections import MozioClient
from api.reservations_poll_endpoint import BookPoll
from errors.errors import FieldNotChangedError, SearchNotValidError, StatusFailedError

@pytest.fixture(name="mock_requests_get")
def mock_requests_get_fixture():
    """
    Fixture to mock the requests.get function.
    """
    with patch("connections.api_connections.requests.get") as mock_get:
        yield mock_get


@pytest.fixture(name="client")
def client_fixture():
    """
    Fixture to create an instance of MozioClient.
    """
    return MozioClient()


def test_poll_book_results(mock_requests_get, client):
    """
    Test the poll_book_results method.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "completed",
        "reservations": [{"confirmation_number": "123",
                          "id":"567"
                          }]
    }

    search_id = "456"

    response = BookPoll.poll_book_results(search_id, client)

    assert response == {
        "status": "completed",
        "reservations": [{"confirmation_number": "123",
                          "id":"567"
                          }]
    }


def test_get_poll_result_reservations(mock_requests_get):
    """
    Test the get_poll_result_reservations method with a valid search ID.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "completed",
        "reservations": [{"confirmation_number": "123",
                          "id":"567"
                          }]
    }

    search_id = "456"
    status = "pending"

    response = BookPoll.get_poll_result_reservations(search_id, status)
    assert response == ('completed', '123', '567')


def test_get_poll_result_reservations_timeout(mock_requests_get):
    """
    Test the get_poll_result_reservations method with a timeout.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "pending",
        "reservations": [{"confirmation_number": "123",
                          "id":"567"
                          }]
    }

    search_id = "456"
    status = "pending"

    with pytest.raises(FieldNotChangedError):
        BookPoll.get_poll_result_reservations(search_id, status)

@pytest.mark.parametrize(
        "status",
        [None, ""]
    )
def test_get_poll_result_reservations_invalid_status(status, mock_requests_get):
    """
    Test the get_poll_result_reservations method with an invalid status.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": status,
        "reservations": [{"confirmation_number": "123",
                          "id":"567"
                          }]
    }

    search_id = "456"
    status = "pending"

    with pytest.raises(SearchNotValidError):
        BookPoll.get_poll_result_reservations(search_id, status)

@pytest.mark.parametrize(
        "confirmation_number",
        [None, "0"]
    )
def test_get_poll_result_reservations_invalid_confirmation_number\
(confirmation_number, mock_requests_get):
    """
    Test the get_poll_result_reservations method with an invalid
    confirmation number.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "completed",
        "reservations": [{"confirmation_number": confirmation_number,
                          "id":"567"
                          }]
    }

    search_id = "456"
    status = "pending"

    with pytest.raises(SearchNotValidError):
        BookPoll.get_poll_result_reservations(search_id, status)


def test_get_poll_result_reservations_failed_status(mock_requests_get):
    """
    Test get_poll_result_reservations method with a failed status.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "failed",
        "reservations": [{"confirmation_number": "456",
                          "id":"567"
                          }]
    }

    search_id = "456"
    status = "pending"

    with pytest.raises(StatusFailedError):
        BookPoll.get_poll_result_reservations(search_id, status)
