import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from src.db_operations import insert_into_database
from src.llm_logic import (
	transcribe_audio,
	call_completions,
)
from src.file_ops import archive_file


load_dotenv()

# OpenAI constants
TRANSCRIPTION_MODEL = "whisper-1"
COMPLETIONS_MODEL = "gpt-3.5-turbo-1106"
client = OpenAI(
	api_key = f"{os.environ.get("OPENAI_API_KEY")}"
)
IS_ISSUE_RESOLVED_PROMPT=os.environ.get("IS_ISSUE_RESOLVED_PROMPT")
UPSET_CUSTOMER_PROMPT=os.environ.get("UPSET_CUSTOMER_PROMPT")
OFFERING_PROMPT=os.environ.get("OFFERING_PROMPT")

# others
CALL_LOGS_DIR = "call_logs/"
CALL_LOGS_FILE = "Customer Service Sample Call - Product Refund.mp4"
CALL_LOGS_FILEPATH = f"{CALL_LOGS_DIR}/{CALL_LOGS_FILE}"
ARCHIVE_DIR = "call_logs_archive/"
ARCHIVE_FILEPATH = f"{ARCHIVE_DIR}/{CALL_LOGS_FILE}"


def main():
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
    archive_file(CALL_LOGS_DIR, CALL_LOGS_FILE, ARCHIVE_DIR)
    

if __name__ == "__main__":
    main()
    
"""
This call is now being recorded. Parker Scarves, how may I help you? I bought a scarf online for my wife, and it turns out they shipped the wrong color. Oh, I am so sorry, sir. I got it for her birthday, 
which is tonight, and now I'm not 100% sure what I need to do. Okay, let me see if I can help you. Do you have the item number of the Parker Scarf? I don't think so. It's called a New Yorker, I think. Excellent. Okay. What color did you want the New Yorker in? Blue. The one they shipped was light blue. I wanted the darker one. Did you want navy blue or royal blue? What's the difference there? The royal blue is a bit brighter. That's the one I want. Okay. What zip code are you located in? 19406. Okay. It appears that we do not, or I'm sorry, that we do have that item in stock at Karen's Boutique at the Hunter Mall. Is that close by? It is. It's right by my office. 
Okay. What is your name, sir? Charlie Johnson. Charlie Johnson? Is that J-O-H-N-S-O-N? Yes, ma'am. And Mr. Johnson, do you have the Parker Scarf in light blue with you now? I do. They shipped it to my office. It just came in not that long ago. Okay. What I will do is make arrangements with Karen's Boutique for you to exchange the Parker Scarf at no additional cost. And in addition, I was able to look up your order in our system, and I'm going to send out a special gift to you to make up for the inconvenience. Oh, excellent. Thank you so much. You're welcome. And thank you for calling Parker Scarf, and I hope your wife enjoys her birthday gift. Oh, thank you. Thank you very much. You're very welcome. Goodbye. Bye-bye.
"""