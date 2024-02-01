"""file_handler.py

Contains class that handles a single file.
"""

# python native
import sys, os
from pathlib import Path
from typing import Type, Any

# in project
from .file_extension import FileExtension
from .useful_methods import *


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
    file_exists():
        determines if file already exists
    is_empty():
        determines if file is empty
    read():
        opens file and returns its data
    write(data):
        writes to file
    """

    def __init__(self, fn: str, 
                 extension: Type[FileExtension], 
                 dir: str='data') -> None:
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
        self.extention = extension(self.path)
        if not self.file_exists():
            if self.create_file():
                print_internal(f'{self.path} created successfully')
            else:
                print_internal(f'error creating file {self.path}')


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
                with open(self.path, 'a+'):
                    val = True

        except IOError as e:
            handle_error(e, 'FileHandler.create_file()', 
                         'error creating file')

        except Exception as e:
            handle_error(e, 'FileHandler.create_file()', 
                         'erroneous error creating file')

        finally:
            return val
        

    def file_exists(self) -> bool:
        """
        Determines if file exists.

        Returns
        -------
        bool
            True,  if file exists |
            False, otherwise
        """

        return os.path.isfile(self.path)
    

    def is_empty(self) -> bool:
        """
        Determins if file is empty.

        Returns
        -------
        bool
            True,  if file is empty |
            False, otherwise
        """

        return os.stat(self.path).st_size == 0
    

    def read(self) -> Any | None:
        """
        Opens file and returns its data.

        Returns
        -------
        Any
            the data held in the file | 
            None, if file is empty
        """

        return self.extention.read() if not self.is_empty() else None
    

    def write(self, data: Any) -> bool:
        """
        Writes data to file.

        Parameters
        ----------
        data : Any
            data to write to the file
        
        Returns
        -------
        bool
            True,  if the data was written to the file successfully |
            False, otherwise
        """

        return self.extention.write(data)