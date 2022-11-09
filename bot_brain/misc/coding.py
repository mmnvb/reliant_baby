
def encode(text: str):
    print("encoding...")
    return text.removeprefix('https://')


def decode(text):
    print("decoding...")
    return "https://"+text
