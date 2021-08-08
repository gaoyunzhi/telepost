#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'telepost'

import yaml
import webgram
import time
from telethon import TelegramClient
from telegram_util import isUrl
import copy

channels_cache = {}
client_cache = {}
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
    if 'id_map' not in credential:
        credential['id_map'] = {}
    if channel not in credential['id_map']:
        entity = await client.get_entity(channel)
        credential['id_map'][channel] = entity.id
        with open('credential', 'w') as f:
            f.write(yaml.dump(credential, sort_keys=True, indent=2, allow_unicode=True))
        return entity
    return await client.get_entity(credential['id_map'][channel])
        
async def getChannel(client, channel):
    if channel in channels_cache:
        return channels_cache[channel]
    channels_cache[channel] = await getChannelImp(client, channel)
    return channels_cache[channel]

async def getTelethonClient():
    if 'client' in client_cache:
        return client_cache['client']
    client = TelegramClient('session_file', credential['telegram_api_id'], credential['telegram_api_hash'])
    await client.start(password=credential['telegram_user_password'])
    client_cache['client'] = client   
    return client_cache['client']

async def getImagesV2(channel, post):
    client = await getTelethonClient()
    size = 10 if post.grouped_id else 1
    posts = await client.get_messages(channel, min_id=post.id - 1, max_id = post.id + size)
    result = []
    for tmp_post in posts[::-1]:
        if tmp_post.grouped_id != post.grouped_id or not post.media:
            continue
        fn = await tmp_post.download_media('tmp/')
        result.append(fn)
    return result

async def getImages(channel, post_id, post_size):
    client = await getTelethonClient()
    entity = await getChannel(client, channel)
    posts = await client.get_messages(entity, min_id=post_id - 1, max_id = post_id + post_size)
    result = []
    for post in posts[::-1]:
        fn = await post.download_media('tmp/')
        result.append(fn)
    return result

async def getPostsTelethon(channel, min_id, limit = 1000):
    client = await getTelethonClient()
    entity = await getChannel(client, channel)
    posts = await client.get_messages(entity, min_id=min_id - 1, max_id = min_id + limit)
    return posts

async def genText(channel, post_id):
    client = await getTelethonClient()
    entity = await getChannel(client, channel)
    post = await client.get_messages(entity, ids=post_id)
    if not post:
        return ''
    return post.text

async def exitTelethon():
    if 'client' in client_cache:
        await client_cache['client'].disconnect()
        return True
    return False

def getText(soup):
    soup = copy.copy(soup)
    for item in soup.find_all('a'):
        if item.get('href') and not isUrl(item.text):
            item.replace_with('\n\n' + item.get('href') + '\n\n')
    for item in soup.find_all('br'):
        item.replace_with('\n')
    result = soup.text.strip()
    for _ in range(5):
        result = result.replace('\n\n\n', '\n\n')
    return result