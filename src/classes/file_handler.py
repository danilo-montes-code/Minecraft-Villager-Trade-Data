"""file_handler.py

Contains class that handles a file.
"""

# python native
import sys, os
from pathlib import Path
from typing import TextIO


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
    dir : str, default='data'
        directory to put files in
    
    Methods
    -------

    """

    def __init__(self, fn: str, dir: str='data') -> None:
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