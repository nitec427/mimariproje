"""
Usage: 
>>> read_files(folder_name)
>>> read_files("unprocessed")
>>> read_files("inprogress")

The code is reading files from the given folder. You can import this code and use in any way you wish.


"""


"""PEP Standard: Please define all imports at the top of your code in Python not the place you want to use. It is both efficient and easy to use."""


import os
import pathlib
import typing
from unidecode import unidecode
path_type = typing.Union[str, pathlib.Path]

def read_files(directory: path_type ):
    """
    Parameters
    ----------
    directory: files will be read from this folder
    Returns
    -------
    file_count (int): Return the number of files in all of the subdirectories
    imgs_path (List[str]): Return path for all files that are relevant
    """
    directory = os.path.join("static","images",directory)
    file_count = 0
    imgs_path = []
    for root, directories, files in os.walk(directory):
        file_count+= len(files)
        for dir in directories:
            # if the folders are uppercase turn them into lowercase and make them English compliant
            os.rename(os.path.join(root, dir), os.path.join(root, unidecode(dir.lower())))
        for name in sorted(files):
            imgs_path.append(os.path.join(root, name))
        
    return file_count, imgs_path

_, paths = read_files('unprocessed')
