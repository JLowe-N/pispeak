from bs4 import BeautifulSoup
import feedparser
import sqlite3
import os

URLS = ['https://forum.devtalk.com/latest.rss',
        'https://feeds.npr.org/1001/rss.xml',
        'https://projects-raspberry.com/news-updates/raspberry-pi-news/feed/',
        ]

if os.path.exists('feeddata.db'):
    read_articles = True
else:
    read_articles = False
    print("feeddata.db database doesn't exist, creating a new database file")
    conn = sqlite3.connect('feeddata.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE NewsFeeds(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        link TEXT
    );""")
    conn.commit()
    conn.close()

conn = sqlite3.connect("feeddata.db")
c = conn.cursor()

for url in URLS:
    feed = feedparser.parse(url)

    for entry in feed["entries"]:
        title = entry.get("title")
        link = entry.get("link")
        description = BeautifulSoup(entry.get("description"), "lxml").text

        c.execute("SELECT link FROM NewsFeeds WHERE link=?", [link])
        link_exists = c.fetchone()
        if link_exists:
            # Record already exists in the database
            pass
        else:
            newdata = (title, link)
            c.execute("INSERT INTO NewsFeeds (title, link) VALUES (?,?)", newdata)
            print("Added to DB: " + title)
conn.commit()
conn.close()
