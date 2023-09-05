from gtts import gTTS

test_text = "This is a test of TTS Conversion"

output = gTTS(text=test_text, lang="en", tld="com", slow=False)

output.save("output.mp3")
