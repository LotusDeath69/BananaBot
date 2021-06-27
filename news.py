import feedparser

def latestUpdate():
  data = feedparser.parse('https://hypixel.net/forums/skyblock-patch-notes.158/index.rss')
  