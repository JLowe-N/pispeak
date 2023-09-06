import feed_pull
import mp3_tts
import mp3_tagging
import mp3_move

new_feeds = feed_pull.feed_pull()
tts_feed = new_feeds.get("tts_feed")
story_collection = new_feeds.get("story_collection")
print(tts_feed)
print(new_feeds)
mp3_tts.text_to_speech(tts_feed)
mp3_tagging.update_tags()
mp3_move()
