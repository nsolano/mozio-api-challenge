"""
Test module for the api_connections module.
"""

from unittest.mock import patch

import pytest

from errors.errors import (APIBadRequestError, APIInvalidKeyError,
                            APINonFieldError, APINotRespondingError)
from connections.api_connections import MozioClient


@pytest.fixture(name="mock_requests_post")
def mock_requests_post_fixture():
    """
    Fixture to mock the requests.post function.
    """
    with patch("connections.api_connections.requests.post") as mock_post:
        yield mock_post


@pytest.fixture(name="client")
def client_fixture():
    """
    Fixture to create an instance of MozioClient.
    """
    return MozioClient()


def test_connect_with_valid_method(mock_requests_post, client):
    """
    Test the connect method with a valid HTTP method.
    """
    mock_response = mock_requests_post.return_value
    mock_response.status_code = 201
    mock_response.json.return_value = {}

    response = client.connect(method="post", endpoint="/example", payload={})

    assert response.status_code == 201


def test_connect_with_invalid_method(client):
    """
    Test the connect method with an invalid HTTP method.
    """
    with pytest.raises(ValueError):
        client.connect(method="invalid", endpoint="/example", payload={})


def test_connect_with_bad_request(mock_requests_post, client):
    """
    Test the connect method with a bad request response.
    """
    mock_response = mock_requests_post.return_value
    mock_response.status_code = 400
    mock_response.json.return_value = {"specific_param": "Bad Request"}

    with pytest.raises(APIBadRequestError):
        client.connect(method="post", endpoint="/example", payload={})


def test_connect_with_invalid_key(mock_requests_post, client):
    """
    Test the connect method with an invalid API key response.
    """
    mock_response = mock_requests_post.return_value
    mock_response.status_code = 403

    with pytest.raises(APIInvalidKeyError):
        client.connect(method="post", endpoint="/example", payload={})


def test_connect_with_non_field_error(mock_requests_post, client):
    """
    Test the connect method with a non-field error response.
    """
    mock_response = mock_requests_post.return_value
    mock_response.status_code = 404

    with pytest.raises(APINonFieldError):
        client.connect(method="post", endpoint="/example", payload={})


def test_connect_with_not_responding(mock_requests_post, client):
    """
    Test the connect method when the API is not responding.
    """
    mock_requests_post.side_effect = TimeoutError

    with pytest.raises(APINotRespondingError):
        client.connect(method="post", endpoint="/example", payload={})
