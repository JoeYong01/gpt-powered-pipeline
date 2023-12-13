"""contains functions responsible for file operations"""
import os
import zlib

def compress_file(
    source_file_path: str,
    compression_level: int = 5
) -> bytes:
    """
    Takes in a file & compresses it

    Args:
        source_file_path (str): source filepath 
        compression_level (int, optional): (0 - 9). Defaults to 5

    Returns:
        IO: returns a compressed file
    """
    with open(source_file_path, 'rb') as source_file:
        file_data = source_file.read()
        compressed_data = zlib.compress(file_data, compression_level)
        return compressed_data


def decompress_file(
    source_path: str,
    source_file: str
) -> None:
    """
    decompresses a file

    Args:
        source_path (str): _description_
        source_file (str): _description_
        destination_path (str): _description_
    """
    with open(source_path + source_file, "rb") as file:
        compressed_data = file.read()
        decompressed_data = zlib.decompress(compressed_data)
        return decompressed_data


def archive_file(
    source_path: str,
    source_file: str,
    destination_path: str
) -> None:
    """
    archives a file to a destination

    Args:
        source_path (str): path of the source directory
        source_file_path (str): file to be compressed
        destination_path (str): target directory of archived file
    """
    source_filepath = source_path + source_file
    destination_filepath = destination_path + "compressed-" + source_file
    compressed_file = compress_file(source_filepath)
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    with open(destination_filepath, "wb") as file:
        file.write(compressed_file)
        os.remove(source_filepath)


def unarchive_file(
    source_path: str,
    source_file: str,
    destination_path: str
) -> None:
    """_summary_

    Args:
        source_path (str): path of the source directory
        source_file_path (str): file to be decompressed
        destination_path (str): target directory to write the file to
    """
    source_file_path = source_path + source_file
    destination_filepath = destination_path + source_file.replace("compressed-", "")
    decompressed_file = decompress_file(source_path, source_file)
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    with open(destination_filepath, "wb") as file:
        file.write(decompressed_file)
        os.remove(source_file_path)
