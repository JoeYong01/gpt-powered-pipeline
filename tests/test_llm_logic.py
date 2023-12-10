import os
from dotenv import load_dotenv
from openai import OpenAI
from src.llm_logic import transcribe_audio

TRANSCRIPTION_MODEL = "whisper-1"
COMPLETIONS_MODEL = "gpt-3.5-turbo-1106"

load_dotenv()
client = OpenAI(
	api_key = f"{os.environ.get("OPENAI_API_KEY")}"
)

def test_transcribe_audio() -> None:
    transcription = transcribe_audio(
        client,
        TRANSCRIPTION_MODEL,
        "src/tests/audio_test/How to Pronounce Hello.mp4"
    )
    assert transcription is not None
