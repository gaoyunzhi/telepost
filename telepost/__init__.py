#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'reddit_2_album'

from telegram_util import AlbumResult as Result
import yaml
import os
import praw
import cached_url
from bs4 import BeautifulSoup
from PIL import Image

def getCredential():
    for root, _, files in os.walk("."):
        for file in files:
            if 'credential' in file.lower():
                try:
                    with open(os.path.join(root, file)) as f:  
                        credential = yaml.load(f, Loader=yaml.FullLoader)
                        credential['reddit_client_id']
                        return credential
                except:
                    ...

credential = getCredential()

reddit = praw.Reddit(
    client_id=credential['reddit_client_id'],
    client_secret=credential['reddit_client_secret'],
    password=credential['reddit_password'],
    user_agent="testscript",
    username=credential['reddit_username'],
    check_for_async=False,
)

def getGallery(url):
    content = cached_url.get(url, force_cache=True)
    soup = BeautifulSoup(content, 'html.parser')
    for item in soup.find_all('a'):
        if item.parent.name != 'figure':
            continue
        yield item['href'] 

def isWebpage(url):
    if url.endswith('mp4'):
        return False
    cached_url.get(url, mode='b', force_cache=True)
    try:
        Image.open(cached_url.getFilePath(url))
        return False
    except:
        return True

def get(path):
    try:
        reddit_id = path.split('/')[6] # may need to revisit
    except:
        reddit_id = path
    submission = reddit.submission(reddit_id)
    result = Result()
    result.url = path
    
    result.cap = submission.title
    if submission.selftext:
        result.cap += '\n\n%s' % submission.selftext

    if 'gallery' in submission.url.split('/'):
        result.imgs = list(getGallery(submission.url))
        return result

    # 'v.redd.it' in submission.url 
    # check if we want to deal with video

    if isWebpage(submission.url):
        result.cap += '\n\n' + submission.url
    else:
        result.imgs = [submission.url]
    return result