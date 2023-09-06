from bs4 import BeautifulSoup
import feedparser
import sqlite3
import os
from typing import Tuple, TypedDict, List

URLS = [
    "https://forum.devtalk.com/latest.rss",
    "https://feeds.npr.org/1001/rss.xml",
    "https://projects-raspberry.com/news-updates/raspberry-pi-news/feed/",
]

DB_NAME = "feeddata.db"


def initialize_db(db_name: str) -> None:
    if not os.path.exists(db_name):
        print(f"{db_name} database doesn't exist, creating a new database file")
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute(
            """CREATE TABLE NewsFeeds(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT
        );"""
        )
        conn.commit()
        conn.close()


def retrieve_feeds(db_name: str, urls: List) -> List:
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    story_count = 0
    unseen_feeds = []
    for url in urls:
        feed = feedparser.parse(url)

        for entry in feed["entries"]:
            print(entry)
            title = entry.get("title")
            link = entry.get("link")
            description = BeautifulSoup(entry.get("description"), "lxml").text

            c.execute("SELECT link FROM NewsFeeds WHERE link=?", [link])
            link_exists = c.fetchone()
            print(link_exists)
            print(bool(link_exists))
            if link_exists:
                # Record already exists in the database
                pass
            else:
                newdata = (title, link)
                c.execute(
                    "INSERT INTO NewsFeeds (title, link) VALUES (?,?)", newdata)
                story_count += 1
                unseen_feeds.append((title, link, description))
    conn.commit()
    conn.close()
    return unseen_feeds

# TODO define custom type or class to describe feed tuple


class FeedText(TypedDict):
    tts_feed: str
    story_collection: str


def feed_text(feed_stories: List[Tuple[str, str, str]]) -> FeedText:
    tts_feed = ""
    story_collection = ""
    for story in feed_stories:
        title, link, description = story
        tts_feed += title + "\n" + description + "\n"
        story_collection += title + "\n" + description + "\n" + link + "\n"
    return {
        "tts_feed": tts_feed,
        "story_collection": story_collection
    }


def feed_pull() -> dict:
    initialize_db(DB_NAME)
    unseen_feeds = retrieve_feeds(DB_NAME, URLS)
    return feed_text(unseen_feeds)
