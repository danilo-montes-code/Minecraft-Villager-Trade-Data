"""file_yaml.py

Contains a class that handles  YAML file IO.
"""

# python native
import yaml
from typing import Any

# in project
from .file_extension import FileExtension
from .useful_methods import *


class YAMLFile(FileExtension):
    """
    Class that handles YAML file IO.

    Attributes
    ----------
    fn : str
        filename of the file
    
    Methods
    -------
    read():
        opens the file and returns its data
    write(data):
        writes data to file
    """

    def __init__(self, fn: str) -> None:
        """
        Creates YAMLFile instance.

        Attributes
        ----------
        fn : str
            filename of the desired file
        """

        super().__init__(fn)


    def read(self) -> dict | None:
        """
        Opens YAML file and returns its data.

        Returns
        -------
        dict
            the data contained in the file | 
            None is there was an error
        """

        data = None
        try:
            with open(self.fn, 'r') as f:
                data = yaml.safe_load(f)

        except IOError as e:
            handle_error(e, 'YAMLFile.open()',
                         'error opening file')

        except Exception as e:
            handle_error(e, 'YAMLFile.open()', 
                         'erroneous error opening file')

        finally:
            return data
        

    def write(self, data: dict[str, Any]) -> bool:
        """
        Writes data to YAML file.

        Parameters
        ----------
        data : dict[str, Any]
            the data to write to the file

        Returns
        -------
        bool
            True,  if the data was written to the file |
            False, otherwise
        """

        saved = False
        try: 
            with open(self.fn, 'w') as f:
                yaml.dump(data, f)
                saved = True
        
        except Exception as e:
            handle_error(e, 'YAMLFile.write()', 'error writing to file')

        finally:
            return saved