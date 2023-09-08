import os


def text_to_speech(text, engine="coqui") -> None:
    if not text:
        print("No new feeds to convert.")
        return
    
    if engine == "gtts":
        from gtts import gTTS
        output = gTTS(text=text, lang="en", tld="com", slow=False)
        output.save("output.mp3")
    elif engine == "coqui":
        import torch
        from TTS.api import TTS

        # Get device
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # List available 🐸TTS models and choose the first one
        # model_name = TTS().list_models()

        # Init TTS
        tts = TTS("tts_models/en/jenny/jenny").to(device)
        tts.tts_to_file(text=text, file_path="output.wav")
    else:
        raise ValueError("Text to speech engine must be either 'gtts' or 'cocqui'")

    # -filter:a atempo - speed up playback & reduce filesize
    # -ar input sample rate for mp3 conversion
    # -ac audio channels: 2 (stereo)
    # -b:a 192k --- constant bitrate quality of 192kbps
    os.system('ffmpeg -i output.wav -filter:a "atempo=1.5" -ar 44100 -ac 2 -b:a 192k compressed.mp3')
    
    os.remove('output.mp3')
    os.rename('faster.mp3', 'output.mp3')
