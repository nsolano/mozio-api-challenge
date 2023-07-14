"""
Test module for the search_poll_ednpoint module.
"""

from unittest.mock import patch

import pytest

from connections.api_connections import MozioClient
from api.search_poll_endpoint import SearchPoll
from errors.errors import FieldNotFalseError, SearchNotValidError

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


def test_poll_search_results(mock_requests_get, client):
    """
    Test the poll_search_results method.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "more_coming": False,
        "results": [{"result_id": "123"}]
    }

    search_id = "456"

    response = SearchPoll.poll_search_results(search_id, client)

    assert response == {
        "more_coming": False,
        "results": [{"result_id": "123"}]
    }


def test_get_poll_result_id_valid_result(mock_requests_get):
    """
    Test the get_poll_result_id method with a valid result ID.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "more_coming": False,
        "results": [{"result_id": "123"}]
    }

    search_id = "456"

    response = SearchPoll.get_poll_result_id(search_id)
    assert response == "123"


def test_get_poll_result_id_timeout(mock_requests_get):
    """
    Test the get_poll_result_id method with a timeout.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "more_coming": True,
        "results": []
    }

    search_id = "789"

    with pytest.raises(FieldNotFalseError):
        SearchPoll.get_poll_result_id(search_id)

@pytest.mark.parametrize(
        "results",
        [{"result_id": "0"}, {"result_id": None}]
    )
def test_get_poll_result_id_invalid_result(results, mock_requests_get):
    """
    Test the get_poll_result_id method with an invalid result ID.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "more_coming": False,
        "results": [results]
    }

    search_id = "123"

    with pytest.raises(SearchNotValidError):
        SearchPoll.get_poll_result_id(search_id)
