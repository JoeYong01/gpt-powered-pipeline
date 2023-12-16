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
    client,
    model: str,
    prompt: str,
    temperature: int,
    input_text: str
) -> bool:
    """Evaluates whether the prompt against the input text & returns a boolean value"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content
