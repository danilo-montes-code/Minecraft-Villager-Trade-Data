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

    Methods
    -------
    open():
        opens the file and returns its data


    """

    def __init__(self) -> None:
        """
        Creates FileExtension instance.
        """
        pass
    
    
    @abstractmethod
    def open(self) -> Any:
        """
        Opens the file and returns the data held within.
        """
        pass

    
    @abstractmethod
    def write(self) -> bool:
        """
        Writes to the file.
        """
        pass