from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error

def update_tags():
    mp3_file = EasyID3("faster.mp3")
    mp3_file["title"] = "Sample Title"
    mp3_file["artist"] = "Content Creator"
    mp3_file["album"] = "PiSpeak Project"
    mp3_file.save()

    mp3_file = MP3("output.mp3", ID3=ID3)
    mp3_file.tags.add(
        APIC(
            mime="image/png",
            type=3,
            desc="PiSpeak Project",
            data=open("home.png", "rb").read(),
        )
    )
    mp3_file.save()
