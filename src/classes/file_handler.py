"""file_handler.py

Contains class that handles a single file.
"""

# python native
import sys, os
from pathlib import Path

# in project
from file_extension import FileExtension
from useful_methods import *


# constants
SCRIPT_ROOT = sys.path[0]


class FileHandler:
    """
    A class that handles a single file's input and output.

    Attributes
    ----------
    fn : str
        filename of the desired file
    extension : FileExtension
        handles file IO based on extension type
    
    Methods
    -------
    @staticmethod
    create_dir(path='data'):
        creates directory from the root directory at given path
    create_file():
        creates file at the location of the fn attribute
    """

    def __init__(self, fn: str, 
                 extension: FileExtension, dir: str='data') -> None:
        """
        Creates FileHandler instance.

        Parameters
        ----------
        fn : str
            filename of the desired file
        extension : FileExtension
            handles file IO based on extension type
        dir : str, default='data'
            directory to put files in
        """

        self.path = os.path.join(SCRIPT_ROOT, dir, fn)
        self.extention = extension


    @staticmethod
    def create_dir(path: str = 'data') -> bool: 
        """
        Create directory from the root of the script.

        Parameters
        ----------
        path : str
            path of the directory to be created

        Returns
        -------
        bool
            True,  if directory was created successfully or if \
                   directory already exists |
            False, otherwise
        """

        created = False
        try:
            Path(path).mkdir()
            created = True

        except FileExistsError as e:
            created = True

        except Exception as e:
            handle_error(e, 'FileHandler.create_dir()', 
                        'erroneous error creating data directory')

        finally:
            return created


    def create_file(self) -> bool:
        """
        Creates file at path specified in attribute.

        Returns
        -------
        bool
            True,  if file was created successfully |
            False, otherwise
        """

        val = False
        try:
            if FileHandler.create_dir():
                with open(self.path, 'w'):
                    val = True
                    print('file created successfully')

        except IOError as e:
            handle_error(e, 'FileHandler.create_file()', 
                         'error creating file')

        except Exception as e:
            handle_error(e, 'FileHandler.create_file()', 
                         'erroneous error creating file')

        finally:
            return val