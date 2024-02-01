"""useful_methods.py

Contains various functions for use across different files.
"""

# python native
from typing import Any


# constants
DEVELOPING = True


def handle_error(error: Exception, 
                 function: str, default_error: str) -> None:
    """
    Displays error message and what function the error occurred in.
    Either displays the full error message or just the error text,
    depending on whether the script is being developed or not.

    Parameters
    ----------
    error : Exception
        the exception that was raised
    function : str
        the name of the function that the expection was raised in
    default_error : str
        the error message to be displayed to the user, non-technical
        such that the user can more obviously know what to do
    """

    if DEVELOPING:
        print_internal('Error in function: ' + function)
        print_internal(type(error))
        print_internal(error)
    else:
        print_internal(default_error)

    etc()
    return


def etc() -> None:
    """
    Displays prompt to user to press Enter to continue.
    """

    input('Press Enter to continue\n')
    return


def print_internal(text: Any, display_error_notice: bool) -> None:
    """
    Prints a message with an indent indicating an internal message,
    a message that appears during setup of the script.

    Parameters
    ----------
    text : Any
        the data to display
    """

    if display_error_notice:
        print(f'[ERROR] {text}')
    else:
        print(f'] {text}')
    return