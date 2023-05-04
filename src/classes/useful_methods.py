"""useful_methods.py

Contains various functions for use across different files.
"""

DEVELOPING = True

def handle_error(error: Exception, function: str, default_error: str) -> None:
    """Displays error message and what function the error occurred in.
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
        print('Error in function: ' + function)
        print(type(error))
        print(error)
    else:
        print(default_error)

    etc()
    return


def etc() -> None:
    """Displays prompt to user to press Enter to continue"""

    input('Press Enter to continue\n')
    return