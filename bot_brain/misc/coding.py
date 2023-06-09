def encode(text: str):
    return text.removeprefix('https://')


def decode(text):
    return "https://"+text
