# coding: UTF-8

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import os
import time

import settings
import twitter

CK = settings.CONSUMER_KEY    # Consumer Key
CS = settings.CONSUMER_SECRET # Consumer Secret
AT = settings.ACCESS_TOKEN    # Access Token
AS = settings.ACCESS_SECRET   # Accesss Token Secert

auth = twitter.OAuth(consumer_key=CK, consumer_secret=CS, token=AT, token_secret=AS)

picsDir = "/Users/chihiro/src/skirt/pics"

# ツイート本文
#message = "養老院 #養老院"

t = twitter.Twitter(auth=auth)

class ChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print('%s is created' % filename)
        self.tweet(filepath)

    def on_modified(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print('%s is updated' % filename)

    def on_deleted(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print('%s is deleted' % filename)

    def tweet(self, path):
        messages = []
        result = t.search.tweets(q="instagram.com,#")
        for status in result["statuses"]:
            for hashtag in status["entities"]["hashtags"]:
                messages.append(hashtag["text"])
                if len(messages) == 10:
                	break;
            else:
                continue
            break
        with open(path, "rb") as image_file:
            image_data=image_file.read()
        message = "#" + " #".join(messages)
        pic_upload = twitter.Twitter(domain = 'upload.twitter.com',auth = auth)
        id_img1 = pic_upload.media.upload(media = image_data)["media_id_string"]
        t.statuses.update(status = message, media_ids = ",".join([id_img1]))


if __name__ in '__main__':
    print("-- start --")
    while 1:
        event_handler = ChangeHandler()
        observer = Observer()
        observer.schedule(event_handler, picsDir, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()