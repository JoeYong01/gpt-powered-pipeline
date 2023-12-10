def transcribe_audio(client: str, model: str, audio_file) -> str:
    """transcribes audio/speech to text using whisper"""
    with open(audio_file, "rb") as file:
        transcript = client.audio.transcriptions.create(
            model = model,
            file = file
        )
    
    return transcript


def post_process_transcription(client: str, model: str, input_text: str) -> str:
    """prompt gpt to correct any possible transcription discrepencies"""
    response = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
        ]
    )
    return response['choices'][0]['message']['content']


def call_chat_completions(client: str, model: str, input_text: str) -> str:
    """evaluates whether or not the customer issue has been resolved"""
    response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
        ]
    )
    return response['choices'][0]['message']['content']
