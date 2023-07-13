"""
Test module for the search_endpoint module.
"""

from unittest.mock import patch

import pytest

from api.search_endpoint import RideSearchParams, Search
from errors.errors import SearchNotValidError


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
    Fixture to mock the requests.post function.
    """
    params = RideSearchParams(
    start_address="123 Main St",
    end_address="456 Elm St",
    mode="car",
    pickup_datetime="2023-07-15 10:00",
    num_passengers=2,
    currency="USD",
    campaign="summer-special",
    )
    return params


def test_search_ride_valid_response(ride_params, mock_requests_post):
    """
    Test the search_ride method with a valid response.
    """
    mock_response = mock_requests_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"search_id": "123"}
    search_id = Search.search_ride(ride_params)

    assert search_id == "123"

@pytest.mark.parametrize(
        "search_id",
        ["0", None]
    )
def test_search_ride_invalid_response(search_id, ride_params, mock_requests_post):
    """
    Test the search_ride method with an invalid response.
    """
    mock_response = mock_requests_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"search_id": search_id}

    with pytest.raises(SearchNotValidError):
        Search.search_ride(ride_params)
