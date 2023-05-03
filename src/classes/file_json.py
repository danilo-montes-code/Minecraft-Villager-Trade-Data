"""file_json.py

Contains a class that handles JSON file IO.
"""

from file_extension import FileExtension
from typing import Any
import json


class JSONFile(FileExtension):
    """
    Class that handles JSON file IO.
    """

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
            self.handle_error(e, 'open()', 'error opening file')
            data = None

        except Exception as e:
            self.handle_error(e, 'open()', 'erroneous error opening file')
            data = None

        finally:
            return data
