from bs4 import BeautifulSoup
import feedparser

URLS = [
    "https://forum.devtalk.com/latest.rss",
    "https://feeds.npr.org/1001/rss.xml",
    "https://projects-raspberry.com/news-updates/raspberry-pi-news/feed/",
]

for url in URLS:
    feed = feedparser.parse(url)

    for entry in feed["entries"]:
        title = entry.get("title")
        link = entry.get("link")
        description = BeautifulSoup(entry.get("description"), "lxml").text
        print(title + "\n" + link + "\n" + description + "\n\n")
