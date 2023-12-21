"""main script"""
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from src.db_operations import insert_into_database
from src.llm_logic import (
	transcribe_audio,
	call_completions,
)
from src.file_ops import (
    archive_file,
    upload_to_blob_storage
)

load_dotenv()

logging.info("initializing variables.")

# OpenAI constants
TRANSCRIPTION_MODEL = "whisper-1"
COMPLETIONS_MODEL = "gpt-3.5-turbo-1106"
client = OpenAI(
	api_key = f"{os.environ.get("OPENAI_API_KEY")}"
)
IS_ISSUE_RESOLVED_PROMPT=os.environ.get("IS_ISSUE_RESOLVED_PROMPT")
# UPSET_CUSTOMER_PROMPT=os.environ.get("UPSET_CUSTOMER_PROMPT")
OFFERING_PROMPT=os.environ.get("OFFERING_PROMPT")

# Azure Blob Storage
AZ_BLOB_STORAGE_CONN_STR = os.environ.get("AZURE_STORAGE_ACCOUNT_CONNECTION_STRING_1")
AZ_CONTAINER = "containerprojectjoe"

# others
CALL_LOGS_DIR = "call_logs/"
CALL_LOGS_FILE = "Customer Service Sample Call - Product Refund.mp4"
CALL_LOGS_FILEPATH = f"{CALL_LOGS_DIR}/{CALL_LOGS_FILE}"
ARCHIVE_DIR = "call_logs_archive/"
ARCHIVE_FILEPATH = f"{ARCHIVE_DIR}/{CALL_LOGS_FILE}"

# logging variables
LOG_DIR = "logs"
DATE_NOW = datetime.now().strftime("%Y/%B/%d")
TIME_NOW = datetime.now().strftime("%H%M%S")
LOGGING_DIR = os.path.join(LOG_DIR, DATE_NOW)
os.makedirs(LOGGING_DIR, exist_ok = True)

# Initlaize logging
logger = logging.getLogger("main.py")
LOG_FILE_PATH = os.path.join(LOGGING_DIR, f"{TIME_NOW}_gpt_powered_pipeline.log")
logging.basicConfig(
    filename = LOG_FILE_PATH,
    level = logging.INFO,
    format = "%(asctime)s : %(name)s : %(levelname)s : %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
)


def main():
    """
    transcribes audio files to text, from that, a few features columns for analysis are parsed: 
    (is_resolved/gift_given/customer_upset).
    Results are then inserted into a sqlite database & processed files are
    archived/uploaded to blob storage
    """
    logging.info("running main().")
    transcription = transcribe_audio(
		client,
  		TRANSCRIPTION_MODEL,
		CALL_LOGS_FILEPATH
	)
    is_resolved = call_completions(
        client,
		COMPLETIONS_MODEL,
		IS_ISSUE_RESOLVED_PROMPT,
		0,
		transcription
	)
    # is_upset = call_completions(
    #     client,
	# 	COMPLETIONS_MODEL,
	# 	UPSET_CUSTOMER_PROMPT,
	# 	transcription,
	# 	0
	# )
    is_gift_given = call_completions(
        client,
		COMPLETIONS_MODEL,
		OFFERING_PROMPT,
		0,
		transcription
	)
    time_processed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_into_database(
		respondant_id = 1,
		agent_id = 1,
		is_resolved = is_resolved,
		feature_columns = is_gift_given,
		call_logs = transcription,
		timestamp = time_processed
	)
    archive_file(CALL_LOGS_FILEPATH, ARCHIVE_DIR)
    # upload_to_blob_storage(AZ_CONTAINER, AZ_BLOB_STORAGE_CONN_STR, CALL_LOGS_FILEPATH)
    logging.debug("finished running main().")

if __name__ == "__main__":
    main()
