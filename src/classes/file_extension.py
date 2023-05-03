"""file_extension.py

Contains a class that handles file IO for a specific file format.
Class is written as an abstract class.
"""

from abc import ABC, abstractmethod
from typing import Any

DEVELOPING = True

class FileExtension(ABC):
    """
    A class that handles file io for a specific file format.
    
    Attributes
    ----------
    ext : str
        the extension of the file

    Methods
    -------
    """

    def __init__(self, ext: str) -> None:
        """
        Creates FileExtension instance.

        Parameters
        ----------
        ext : str
            the extension of the file

        """

        self.ext = ext


    @abstractmethod
    def open(self) -> Any:
        """Opens the file and returns the data held within.
        """

        pass

    def handle_error(self, error: Exception, function: str, default_error: str) -> None:
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

        self.etc()
        return
    

    def etc() -> None:
        """Displays prompt to user to press Enter to continue"""

        input('Press Enter to continue\n')
        return