def transcribe_audio(
    client: str,
    model: str,
    audio_file
) -> str:
    """transcribes audio/speech to text using whisper"""
    with open(audio_file, "rb") as file:
        transcript = client.audio.transcriptions.create(
            model = model,
            file = file,
            response_format='text'
        )
    return transcript

def call_completions(
    client: str,
    model: str,
    prompt:str,
    temperature: int,
    input_text: str
) -> bool:
    """evaluates whether or not the customer issue has been resolved"""
    response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": f"{prompt}"},
        {"role": "user", "content": f"{input_text}"}
        ],
    temperature=temperature
    )
    return response['choices'][0]['message']['content']
