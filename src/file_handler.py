"""file_handler.py
"""

import sys, os

SCRIPT_ROOT = sys.path[0]
FILE_PATH_VILLAGER_DATA = os.path.join(SCRIPT_ROOT, 'data', 'villager-data.json')
FILE_PATH_OUTPUT = os.path.join(SCRIPT_ROOT, 'data', 'data-output.txt')
DEVELOPING = True
MAX_WIDTH = 80

class FileHandler():

    def __init__(self, path:str='test') -> None:
        self.path = path