from pydub import AudioSegment
from os import remove


async def m4a_to_mp3(input_file: int):
    sound = AudioSegment.from_file(f"bot_brain\\misc\\files\\{input_file}.m4a")
    sound.export(f"bot_brain\\misc\\files\\{input_file}.mp3", format="mp3")
    remove(f"bot_brain\\misc\\files\\{input_file}.m4a")
