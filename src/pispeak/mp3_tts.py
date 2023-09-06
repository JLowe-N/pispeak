from gtts import gTTS

def text_to_speech(text):
    output = gTTS(text=text, lang="en", tld="com", slow=False)
    output.save("output.mp3")
