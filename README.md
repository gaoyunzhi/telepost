# telepost

Get post from telegram and make ready to repost it to other places (twitter / douban / reddit).

## usage

```
import telepost
import time
import plain_db

existing = plain_db.load('existing')
channel = 'twitter_translate'

post = telepost.getPost(channel, existing, min_time=1, max_time = time.time()) # get the first post outside existing ones

posts = telepost.getPosts(channel, min_time=1, max_time = time.time())

# credential file need to contain telegram_api_hash, telegram_api_id and telegram_user_password
post_id = 1392
post_size = 2
filenames = await telepost.getImages(channel, post_id, post_size)
await telepost.exitTelethon()
```

## how to install

`pip3 install telepost`