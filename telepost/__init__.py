#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'telepost'

import yaml
import webgram
import time
from telethon import TelegramClient
from telegram_util import isUrl

# TODO: may need async getTextMarkdown

with open('credential') as f:
    credential = yaml.load(f, Loader=yaml.FullLoader)

Day = 24 * 60 * 60

def getPosts(channel, min_time = None, max_time = None):
    if not min_time:
        min_time = time.time() - 2 * Day
    if not max_time:
        max_time = time.time() - Day
    posts = webgram.getPosts(channel)[1:]
    for post in posts:
        if post.time < max_time:
            yield post
    while posts and posts[0].time > min_time:
        pivot = posts[0].post_id
        posts = webgram.getPosts(channel, posts[0].post_id, 
            direction='before', force_cache=True)[1:]
        for post in posts:
            if post.time < max_time:
                yield post

def getPost(channel, existing_file, min_time = None, max_time = None):
    for post in getPosts(channel, min_time, max_time):
        key = 'https://t.me/' + post.getKey()
        if existing_file.get(key):
            continue
        return post

async def getChannelImp(client, channel):
    if channel not in credential['id_map']:
        entity = await client.get_entity(channel)
        credential['id_map'][channel] = entity.id
        with open('credential', 'w') as f:
            f.write(yaml.dump(credential, sort_keys=True, indent=2, allow_unicode=True))
        return entity
    return await client.get_entity(credential['id_map'][channel])
        
channels_cache = {}
async def getChannel(client, channel):
    if channel in channels_cache:
        return channels_cache[channel]
    channels_cache[channel] = await getChannelImp(client, channel)
    return channels_cache[channel]

client_cache = {}
async def getTelethonClient():
    if 'client' in client_cache:
        return client_cache['client']
    client = TelegramClient('session_file', credential['telegram_api_id'], credential['telegram_api_hash'])
    await client.start(password=credential['telegram_user_password'])
    client_cache['client'] = client   
    return client_cache['client']

async def getImages(channel, post_id, post_size):
    client = await getTelethonClient()
    entity = await getChannel(client, channel)
    posts = await client.get_messages(entity, min_id=post_id - 1, max_id = post_id + post_size)
    result = []
    for post in posts[::-1]:
        fn = await post.download_media('tmp/')
        result.append(fn)
    return result

async def exitTelethon():
    if 'client' in client_cache:
        await client_cache['client'].disconnect()

def getText(soup):
    for item in soup.find_all('a'):
        if item.get('href') and not isUrl(item.text):
                item.replace_with('\n\n' + item.get('href') + '\n\n')
    for item in soup.find_all('br'):
        item.replace_with('\n')
    result = soup.text.strip()
    for _ in range(5):
        result = result.replace('\n\n\n', '\n\n')
    return result