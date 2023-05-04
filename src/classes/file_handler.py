"""file_handler.py

Contains class that handles a file.
"""

# python native
import sys, os
from pathlib import Path
from typing import TextIO

# in project
from file_extension import FileExtension
from useful_methods import *


# constants
SCRIPT_ROOT = sys.path[0]
# FILE_PATH_VILLAGER_DATA = os.path.join(SCRIPT_ROOT, 'data', 'villager-data.json')
# FILE_PATH_OUTPUT = os.path.join(SCRIPT_ROOT, 'data', 'data-output.txt')
# DEVELOPING = True
MAX_WIDTH = 80


class FileHandler:
    """
    A class that handles file input and output.

    Attributes
    ----------
    fn : str
        filename of the desired file
    extension : FileExtension
        handles file IO based on extension type
    dir : str, default='data'
        directory to put files in
    
    Methods
    -------
    create_dir(path='data'):
        creates directory from the root directory at given path
    """

    def __init__(self, fn: str, 
                 extension: FileExtension, dir: str='data') -> None:
        """
        Creates FileHandler instance.

        Parameters
        ----------
        fn : str
            filename of the desired file
        dir : str, default='data'
            directory to put files in
        """

        self.path = os.path.join(SCRIPT_ROOT, dir, fn)
        self.extention = extension


    def create_dir(self, path: str = 'data') -> bool: 
        """Create directory from the root of the script

        Parameters
        ----------
        path : str
            path of the directory to be created

        Returns
        -------
        bool
            True,  if directory was created successfully \n
            False, otherwise
        """

        ret = False
        try:
            Path(path).mkdir()
            ret = True

        except FileExistsError as e:
            handle_error(e, 'create_dir()', 
                        'error creating data directory')

        except Exception as e:
            handle_error(e, 'create_dir()', 
                        'erroneous error creating data directory')

        finally:
            return ret


    def create_file(self) -> bool:
        """
        Creates file at path specified in attribute.

        Parameters
        ----------
        path : str
            path of the file to be created

        Returns
        -------
        bool
            True,  if file was created successfully \n
            False, otherwise
        """

        val = False

        try:
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