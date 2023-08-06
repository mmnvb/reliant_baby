from pydub import AudioSegment
from os import remove


async def m4a_to_mp3(file: int, author: str, title: str):
    sound = AudioSegment.from_file(f"temp/{file}.m4a")
    sound.export(f"temp/{file}.mp3", format="mp3",
                 tags={'artist': f"{author}",
                       'album': 'ReliantBaby',
                       'title': f"{title}"})
    remove(f"temp/{file}.m4a")


async def ogg_to_mp3(file: int, author: str):
    def match_target_amplitude(sound_self, target_dbfs):
        change_in_dBFS = target_dbfs - sound.dBFS
        return sound_self.apply_gain(change_in_dBFS)

    sound = AudioSegment.from_file(f"temp/{file}.ogg")
    normalized = match_target_amplitude(sound, -20.0)
    normalized.export(f"temp/{file}.mp3", format="mp3",
                      tags={'artist': f"{author}",
                            'album': 'ReliantBaby',
                            'title': f"audio"})
    remove(f"temp/{file}.ogg")
