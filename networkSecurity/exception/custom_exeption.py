import sys
from networkSecurity.logging.logger import logging


class NetworkSecurityException(Exception):
    """
    Custom Exception class for the Network Security project.
    It captures the error message, line number, and filename
    where the exception occurred.
    """

    def __init__(self, error_message: str, error_details: sys):
        """
        Constructor to initialize the custom exception.

        Parameters:
        -----------
        error_message : str
            The error message from the exception.

        error_details : sys
            The sys module is passed to extract detailed
            information about the exception (line number, filename).
        """
        self.error_message = str(error_message)

        # Extract traceback information
        _, _, exc_tb = error_details.exc_info()
        self.lineno = exc_tb.tb_lineno               # Line number where error occurred
        self.filename = exc_tb.tb_frame.f_code.co_filename  # File where error occurred

    def __str__(self):
        """
        Return a string representation of the exception
        including filename, line number, and error message.
        """
        error_msg = (
            f"Error occurred in Python script [{self.filename}] "
            f"at line number [{self.lineno}] "
            f"with error message: [{self.error_message}]"
        )
        logging.error(error_msg)  # Log to file/console
        return error_msg  # Return string for printing


if __name__ == "__main__":
    try:
        logging.info("Entering the try block")
        a = 1 / 0  # This will raise ZeroDivisionError
        print("This line will not be printed")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
