"""file_txt.py

Contains a class that handles txt file IO.
"""

# python native
from typing import Any

# in project
from .file_extension import FileExtension
from .useful_methods import *


class TxtFile(FileExtension):
    """
    Class that handles txt file IO.

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
        Creates TxtFile instance.

        Attributes
        ----------
        fn : str
            filename of the desired file
        """

        super().__init__(fn)


    def read(self) -> list[str] | None:
        """
        Opens txt file and returns its data.

        Returns
        -------
        list[str]
            the data contained in the file | 
            None is there was an error
        """

        data = None
        try:
            with open(self.fn, 'r') as f:
                data = f.readlines()

        except IOError as e:
            handle_error(e, 'TxtFile.open()',
                         'error opening file')

        except Exception as e:
            handle_error(e, 'TxtFile.open()', 
                         'erroneous error opening file')

        finally:
            return data
        

    def write(self, data: list[str]) -> bool:
        """
        Writes data to txt file.

        Parameters
        ----------
        data : list[str]
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
                f.writelines(line + '\n' for line in data)
                saved = True
        
        except Exception as e:
            handle_error(e, 'TxtFile.write()', 'error writing to file')

        finally:
            return saved