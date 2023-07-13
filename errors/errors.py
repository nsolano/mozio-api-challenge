""" 
Module generated for custom errors
"""

class APINotRespondingError(Exception):
    """
    Custom exception class for api not responding errors.
    Raised when the API is not responding."""

class APIBadRequestError(Exception):
    """
    Custom exception class for a bad request error.
    Raised when the API returns a status code of 400."""

class APIInvalidKeyError(Exception):
    """
    Custom exception class for an invalid key.
    Raised when the API returns a status code of 403."""

class APINonFieldError(Exception):
    """
    Custom exception class for a non-field error.
    Raised when the API returns a status code different than 400 and 403."""

class SearchNotValidError(Exception):
    """
    Custom exception class for a search not valid.
    Raised when the API returns a not valid ID."""

class FieldNotFalseError(Exception):
    """
    Custom exception class for the field more_coming.
    Raised more_coming never returned False."""
