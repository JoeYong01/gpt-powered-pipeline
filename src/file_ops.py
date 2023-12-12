import os
import shutil
import zlib
from typing import IO

def move_file(
    source_file_path: str,
    destination_path: str
) -> None:
    """
    Moves a file to a directory (creates if not exists) using shutil

    Args:
        source_file_path (str): path of the source file
        destination_path (str): target directory to move to
    """
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    
    shutil.move(source_file_path, destination_path)


def compress_file(
    source_file_path: str,
    compression_level: int = 5,
    window_size: int = 12
) -> IO:
    """
    Takes in a file & compresses it

    Args:
        source_file_path (str): path of the source file
        compression_level (int, optional): (0 - 9). Defaults to 5.
        window_size (int, optional): higher = better compression & higher memory usage (9 - 15). Defaults to 12.

    Returns:
        IO: returns a file object
    """
    ...

def archive_file(
    source_file_path: str,
    destination_file_path: str
) -> None:
    """
    archives a file to a destination

    Args:
        source_file_path (str): path of the source file
        destination_file_path (str): destination of the file
    """
    ...


archive_path = "call_logs_archive/"
os.makedirs(archive_path) if not os.path.exists(archive_path) else print('path exists')
shutil.copy("call_logs/Call Center Sample Calls E-Commerce Store.mp4", f"{archive_path}")
compress_file(f"{archive_path}Call Center Sample Calls E-Commerce Store.mp4")