"""runs tests against file_ops source code"""
import os
from dotenv import load_dotenv
from src.file_ops import (
	compress_file,
	decompress_file,
	upload_to_blob_storage,
	archive_file,
	unarchive_file,
)

load_dotenv()
# this is bugged
AZURE_BLOB_STORAGE_CONN_STR = os.environ.get('AZURE_STORAGE_ACCOUNT_CONNECTION_STRING_1')

def test_compress_file() -> None:
    """tests to see if it returns a compressed data"""
    data = compress_file('tests/audio_test/How to Pronounce Hello.mp4')
    assert data is not None


def test_deompress_file() -> None:
    """tests to see if it returns decompressed data"""
    data = decompress_file('tests/audio_test/compressed-How to Pronounce Hello.mp4')
    assert data is not None


def test_upload_to_blob_storage() -> None:
    """tests to see if it uploads the blobs correctly (and then removes it & returns True)"""
    result = upload_to_blob_storage(
        container_name = 'containerprojectjoe',
        connection_string = AZURE_BLOB_STORAGE_CONN_STR,
        file_path = 'tests/audio_test/compressed-How to Pronounce Hello.mp4',
        is_test = True
    )
    assert result is True


def test_archive_file() -> None:
    """
    tests to see if it archive the file correctly 
    (and then removes the file & dir created & returns True)
    """
    result = archive_file(
        file_path = 'tests/audio_test/How to Pronounce Hello.mp4',
        destination_path = 'tests/archive_audio_tests/',
        is_test = True
    )
    assert result is True


def test_unarchive_file() -> None:
    """
    test to see if it unarchives the file correctly 
    (and then removes the file & dir created & returns True)
    """
    result = unarchive_file(
        file_path = 'tests/audio_test/compressed-How to Pronounce Hello.mp4',
        destination_path = 'tests/unarchived_audio_tests/',
        is_test = True
    )
    assert result is True
