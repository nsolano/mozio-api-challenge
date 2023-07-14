"""
Test module for the reservations_endpoint module.
"""

from unittest.mock import patch

import pytest

from api.reservations_endpoint import RideBookParams, Book
from errors.errors import SearchNotValidError, StatusFailedError


@pytest.fixture(name="mock_requests_post")
def mock_requests_post_fixture():
    """
    Fixture to mock the requests.post function.
    """
    with patch("connections.api_connections.requests.post") as mock_post:
        yield mock_post

@pytest.fixture(name="ride_params")
def ride_params_fixture():
    """
    Fixture to mock the RideBookParams class.
    """
    params = RideBookParams(
        search_id="123456789",
        result_id="987654321",
        email="example@example.com",
        country_code_name="US",
        phone_number="1234567890",
        first_name="John",
        last_name="Doe",
        airline="Airline Name",
        flight_number="123",
        customer_special_instructions="Please deliver to front desk.",
        provider={"name": "Provider Name", "id": "provider123"},
    )
    return params


def test_book_ride_valid_response(ride_params, mock_requests_post):
    """
    Test the book_ride method with a valid response.
    """
    mock_response = mock_requests_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "pending"}
    status = Book.book_ride(ride_params)

    assert status == "pending"

@pytest.mark.parametrize(
        "status",
        [None, ""]
    )
def test_book_ride_invalid_response(status, ride_params, mock_requests_post):
    """
    Test the book_ride method with an invalid response.
    """
    mock_response = mock_requests_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": status}

    with pytest.raises(SearchNotValidError):
        Book.book_ride(ride_params)


def test_book_ride_failed_response(ride_params, mock_requests_post):
    """
    Test the book_ride method with an invalid response.
    """
    mock_response = mock_requests_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "failed"}

    with pytest.raises(StatusFailedError):
        Book.book_ride(ride_params)
