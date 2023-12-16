"""contains functions responsible for file operations"""
import os
import zlib
from azure.storage.blob import BlobServiceClient
from datetime import datetime

def compress_file(
    file_path: str,
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
    with open(file_path, 'rb') as source_file:
        file_data = source_file.read()
        compressed_data = zlib.compress(file_data, compression_level)
        return compressed_data


def decompress_file(
    file_path: str
) -> None:
    """
    decompresses a file

    Args:
        file_path (str): full path to the file
    """
    with open(file_path, "rb") as file:
        compressed_data = file.read()
        decompressed_data = zlib.decompress(compressed_data)
        return decompressed_data


def upload_to_blob_storage(
    container_name: str,
    connection_string: str,
    file_path: str,
    is_test: bool = False
) -> None:
    """
    uploads a file to Azure Blob Storage

    Args:
        container_name (str): Name of container to upload to
        connection_string (str): Azure Storage Account connection string
        file_path (str): full path to the file
        is_test (bool, optional): Used to pytest testing. Defaults to False
    """
    filename = os.path.basename(file_path)
    blob_dir = datetime.now().strftime("%Y/%b/%d")
    # blobs are case & space sensitive!
    blob_name = os.path.join(blob_dir, filename).lower().strip().replace("  ", " ")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)
    with open(file_path, "rb") as f:
        blob_client.upload_blob(f)
    # if its a test, just delete the blob & return True to indicate that its working
    if is_test:
        blob_client.delete_blob()
        return True
    else:
        os.remove(file_path)


def archive_file(
    file_path: str,
    destination_path: str,
    is_test: bool = False
) -> None:
    """
    archives a file to a destination

    Args:
        file_path (str): full path to the file
        destination_path (str): target directory of archived file
        is_test (bool, optional): Used to pytest testing. Defaults to False
    """
    filename = os.path.basename(file_path)
    compressed_filename = "compressed-" + filename
    destination_filepath = os.path.join(destination_path, compressed_filename)
    compressed_file = compress_file(file_path)
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    with open(destination_filepath, "wb") as file:
        file.write(compressed_file)
    # if its a test then just rm the created dir/files & return True to indicate its working
    if is_test:
        os.remove(destination_filepath)
        os.removedirs(destination_path)
        return True
    else:
        os.remove(file_path)


def unarchive_file(
    file_path: str,
    destination_path: str,
    is_test: bool = False
) -> None:
    """_summary_

    Args:
        file_path (str): full path to the file
        destination_path (str): target directory to write the file to
        is_test (bool, optional): Used to pytest testing. Defaults to False
    """
    filename = os.path.basename(file_path)
    decompressed_filename = filename.replace("compressed-", "")
    destination_filepath = os.path.join(destination_path, decompressed_filename)
    decompressed_file = decompress_file(file_path)
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    with open(destination_filepath, "wb") as file:
        file.write(decompressed_file)
    if is_test:
        os.remove(destination_filepath)
        os.removedirs(destination_path)
        return True
    else:
        os.remove(file_path)
