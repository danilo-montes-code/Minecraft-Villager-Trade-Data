"""file_json.py

Contains a class that handles JSON file IO.
"""

# python native
import json
from typing import Any

# in project
from file_extension import FileExtension
from useful_methods import *


class JSONFile(FileExtension):
    """
    Class that handles JSON file IO.
    """

    def __init__(self) -> None:
        """
        Creates JSONFile instance.
        """
        super().__init__()


    def open(self, file : str) -> Any:
        """Opens JSON file and returns its data
        
        Parameters
        ----------
        file : str
            path to file to open
        """

        try:
            with open(file, 'r') as f:
                data = json.load(f)

        except IOError as e:
            handle_error(e, 'open()', 'error opening file')
            data = None

        except Exception as e:
            handle_error(e, 'open()', 'erroneous error opening file')
            data = None

        finally:
            return data
