from openai import OpenAI

TRANSCRIPTION_MODEL = "whisper-1"
COMPLETIONS_MODEL = "gpt-3.5-turbo-1106"

client = OpenAI()


def transcribe_audio(audio_file) -> str:
    transcript = client.audio.transcriptions.create(
        model = TRANSCRIPTION_MODEL,
        file = audio_file
    )
    
    return transcript


def post_process_transcription(input_text: str) -> str:
    """prompt gpt to correct any possible transcription discrepencies"""
    reponse = client.chat.completions.create(
        model=COMPLETIONS_MODEL,
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
        ]
    )
    return reponse['choices'][0]['message']['content']


def call_chat_completions(input_text: str) -> str:
    """evaluates whether or not the customer issue has been resolved"""
    response = client.chat.completions.create(
    model=COMPLETIONS_MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
        ]
    )
    return response['choices'][0]['message']['content']
