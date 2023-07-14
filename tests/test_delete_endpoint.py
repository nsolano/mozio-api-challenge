"""
Test module for the delete_endpoint module.
"""

from unittest.mock import patch

import pytest

from api.delete_endpoint import DeleteRide
from errors.errors import DeleteFailedError


@pytest.fixture(name="mock_requests_delete")
def mock_requests_delete_fixture():
    """
    Fixture to mock the requests.post function.
    """
    with patch("connections.api_connections.requests.delete") as mock_delete:
        yield mock_delete

def test_delete_ride_valid_response(mock_requests_delete):
    """
    Test the delete_ride method with a valid response.
    """
    mock_response = mock_requests_delete.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"cancelled": "1",
                                       "refunded": "1"}

    reservation_id = "123"
    response = DeleteRide.delete_ride(reservation_id)

    assert response == {"cancelled": "1",
                                       "refunded": "1"}


@pytest.mark.parametrize(
        "response",
        [None, {}]
    )
def test_delete_ride_invalid_response(response, mock_requests_delete):
    """
    Test the delete_ride method with an invalid response.
    """
    mock_response = mock_requests_delete.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = response

    reservation_id = "123"

    with pytest.raises(DeleteFailedError):
        response = DeleteRide.delete_ride(reservation_id)
