"""contains functions responsible for file operations"""
import logging
import os
import zlib
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError
from datetime import datetime

logger = logging.getLogger("file_ops.py")

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
    logger.info("running function compress_file.")
    try:
        with open(file_path, 'rb') as source_file:
            file_data = source_file.read()
            compressed_data = zlib.compress(file_data, compression_level)
            logger.debug("returning compressed data.")
            return compressed_data
    except zlib.error as e:
        logger.exception("zlib error exception in compress_file: %s", e)
    except Exception as e:
        logger.exception("Exception in compress_file: %s", e)
    finally:
        logger.debug("context manager closed.")
    


def decompress_file(
    file_path: str
) -> None:
    """
    decompresses a file

    Args:
        file_path (str): full path to the file
    """
    logger.info("running function: decompress file.")
    try:
        with open(file_path, "rb") as file:
            compressed_data = file.read()
            decompressed_data = zlib.decompress(compressed_data)
            logger.debug("returning decompressed data.")
            return decompressed_data
    except zlib.error as e:
        logger.exception("zlib error exception in decompress_file: %s", e)
    except Exception as e:
        logger.exception("Exception in decompress_file: %s", e)
    finally:
        logger.debug("context manager closed.")


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
    logger.info("running function: upload_to_blob_storage")
    try:
        filename = os.path.basename(file_path)
        blob_dir = datetime.now().strftime("%Y/%b/%d")
        # blobs are case & space sensitive!
        blob_name = os.path.join(blob_dir, filename).lower().strip().replace("  ", " ")
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)
        with open(file_path, "rb") as f:
            blob_client.upload_blob(f)
            logger.debug("context manager closed.")
        # if its a test, just delete the blob & return True to indicate that its working
        if is_test:
            logger.debug("test detected, deleting uploaded Blob.")
            blob_client.delete_blob()
            return True
        else:
            logger.debug("removing local file after upload.")
            os.remove(file_path)
    except AzureError as e:
        logger.exception("Azure error in upload_to_blob_storage: %s", e)
    except Exception as e:
        logger.exception("Exception in upload_to_blob_storage: %s", e)


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
    logger.info("running function: archive_file.")
    try:
        filename = os.path.basename(file_path)
        compressed_filename = "compressed-" + filename
        destination_file_path = os.path.join(destination_path, compressed_filename)
        compressed_file = compress_file(file_path)
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        with open(destination_file_path, "wb") as file:
            file.write(compressed_file)
            logger.debug("context manager closed.")
        # if its a test then just rm the created files & return True to indicate its working
        if is_test:
            logger.debug("test detected, destination file path.")
            os.remove(destination_file_path)
            return True
        else:
            logger.debug("removing source file.")
            os.remove(file_path)
    except Exception as e:
        logger.exception("Exception in archive_file: %e", e)


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
    logger.info("running function: unarchive_file.")
    try:
        filename = os.path.basename(file_path)
        decompressed_filename = filename.replace("compressed-", "")
        destination_file_path = os.path.join(destination_path, decompressed_filename)
        decompressed_file = decompress_file(file_path)
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        with open(destination_file_path, "wb") as file:
            file.write(decompressed_file)
            logger.debug("context manager closed.")
        if is_test:
            logger.debug("test detected, removing destination file path")
            os.remove(destination_file_path)
            return True
        else:
            logger.debug("removing source file.")
            os.remove(file_path)
    except Exception as e:
        logger.exception("Exception in unarchive_file: %e", e)