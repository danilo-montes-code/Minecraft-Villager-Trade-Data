"""file_extension.py

Contains a class that handles file IO for a specific file format.
Class is written as an abstract class.
"""

# python native
import os
from abc import ABC, abstractmethod
from typing import Any


class FileExtension(ABC):
    """
    A class that handles file IO for a specific file format.
    
    Attributes
    ----------
    fn : str
        filename of the file

    Methods
    -------
    open():
        opens the file and returns its data
    write(data):
        writes data to file
    """

    def __init__(self, fn: str) -> None:
        """
        Creates FileExtension instance.

        Parameters
        ----------
        fn : str
            filename of the desired file
        """
        
        self.fn = fn
    
    
    @abstractmethod
    def read(self) -> Any:
        """
        Opens the file and returns the data held within.
        """
        pass

    
    @abstractmethod
    def write(self, data: Any) -> bool:
        """
        Writes to the file.
        """
        pass