from pathlib import Path
import shutil
import os

mp3name = "faster.mp3"
mp3destination = os.path.join(Path.home(), "GoogleDrive", mp3name)
shutil.move(mp3name, mp3destination)
