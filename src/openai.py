from openai import OpenAI

COMPLETIONS_MODEL = "gpt-3.5-turbo-1106"

client = OpenAI()

def call_chat_completions(input_text: str) -> str:
    """_summary_

    Args:
        input_text (str): _description_

    Returns:
        str: _description_
    """
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