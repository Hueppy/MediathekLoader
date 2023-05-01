import os
from datetime import datetime
from subprocess import Popen
from time import mktime

import feedparser
import ffmpeg
import json

class Config:
    def __init__(self):
        self.last_check = datetime.now().isoformat()
        self.feeds = list()

    def load(self):
        with open("config.json", "r") as file:
            props = json.load(fp=file)
            for prop in self.__dict__.keys():
                if prop in props:
                    self.__dict__[prop] = props[prop]

    def save(self):
        with open("config.json", "w") as file:
            json.dump(self.__dict__, fp=file, default=str, indent=4)


config = Config()
try:
    config.load()

    check = datetime.now()
    for feed in config.feeds:
        rss = feedparser.parse(feed["url"])

        for entry in rss.entries:
            entry_date = datetime.fromtimestamp(mktime(entry.published_parsed))

            if check >= entry_date > datetime.fromisoformat(config.last_check):
                link = entry.link
                if "mediandr" in link and "hevc" not in link:
                    link = link.replace(".mp4", ".hevc.mp4")

                stream = ffmpeg.input(link)
                stream = ffmpeg.output(stream, f'{feed["path"]}/Season {entry_date.year}/Episode {entry_date.date().isoformat()} WEBDL-1080p.mkv', c='copy')
                ffmpeg.run(stream)

    config.last_check = check.isoformat()

finally:
    config.save()
