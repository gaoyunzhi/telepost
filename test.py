#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telepost
import time
import plain_db
import asyncio
import webgram
from telethon import types
from telegram_util import matchKey

existing = plain_db.load('existing')
channel = 'twitter_translate'

def test():
    post = telepost.getPost(channel, existing, min_time=1, max_time = time.time()) # get the first post outside existing ones
    print(post)
    posts = telepost.getPosts(channel, min_time=1, max_time = time.time() - 24 * 10 * 60 * 60)
    print(next(posts))

async def run():
    # credential file need to contain telegram_api_hash, telegram_api_id and telegram_user_password
    post_id = 1392
    post_size = 2
    filenames = await telepost.getImages(channel, post_id, post_size)
    print(filenames)
    await telepost.exitTelethon()

async def testImagesV2():
    post_id = 1392
    src_id = 1374186417
    client = await telepost.getTelethonClient()
    src = await client.get_entity(src_id)
    post = await client.get_messages(src, ids=post_id)
    filenames = await telepost.getImagesV2(src, post)
    print(filenames)
    await telepost.exitTelethon()

async def testGetPostTelethon():
    client = await telepost.getTelethonClient()
    dialogs = await client.get_dialogs()
    low_priority_chat = await client.get_entity(1310793327)
    chat = await client.get_entity(1386450222)
    posts = await telepost.getPostsTelethon(1386450222, 2637)
    for post in posts[::-1]:
        if not post.raw_text:
            continue
        if type(post.media).__name__ in ['MessageMediaPhoto', 'MessageMediaDocument']:
            result = await client.edit_message(chat, post.id, text = '(high priority) ' + post.text)
        else:
            ...
            await client.send_message(low_priority_chat, post.text)
    await telepost.exitTelethon()

async def testPinnedMessage():
    client = await telepost.getTelethonClient()
    await client.get_dialogs()
    chat = await client.get_entity(1386450222)
    to_chat = await client.get_entity(1197072284)
    messages = await client.get_messages(chat, filter=types.InputMessagesFilterPinned(), limit=500)
    print(len(messages))
    for message in messages:
        if not message.raw_text:
            continue
        print(message.raw_text)
        if matchKey(message.raw_text, ['已完成', '已翻译']):
            print('here')
            result = await client.unpin_message(chat, message.id)
            print(result)
    await telepost.exitTelethon()

def testAsync():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    r = loop.run_until_complete(testImagesV2())
    loop.close()

def testGetText():
    post = webgram.getPost('twitter_translate', 1218)
    print(telepost.getText(post.text))

if __name__=='__main__':
    testAsync()
    # test()
    # testGetText()