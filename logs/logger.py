""" 
Module generated for manage the logs
"""

import logging


class ErrorLogger:
    """
    Logger class for recording and handling error messages in the application.
    """

    def __init__(self):
        self.logger = self.setup_logger()

    def setup_logger(self):
        """
        Set up the logger with appropriate configuration.
        Returns:
            logging.Logger: The configured logger instance.
        """
        logger = logging.getLogger("error_logger")
        logger.setLevel(logging.ERROR)

        # Create file handler and set level to ERROR
        file_handler = logging.FileHandler("logs/error_log.log")
        file_handler.setLevel(logging.ERROR)

        # Create formatter and add it to the handler
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(file_handler)

        return logger

    def log_error(self, message):
        """
        Log an error message.
        Args:
            message (str): The error message to log.
        """
        self.logger.error(message)
