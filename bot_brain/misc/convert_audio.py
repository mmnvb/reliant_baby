from pydub import AudioSegment
from os import remove


async def m4a_to_mp3(file: int, author: str, title: str):
    sound = AudioSegment.from_file(f"temp/{file}.m4a")
    sound.export(f"temp/{file}.mp3", format="mp3",
                 tags={'artist': f"{author}",
                       'album': 'ReliantBaby',
                       'title': f"{title}"})
    remove(f"temp/{file}.m4a")
