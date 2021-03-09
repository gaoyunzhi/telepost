#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telepost
import time
import plain_db
import asyncio

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

def testAsync():
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	r = loop.run_until_complete(run())
	loop.close()
	
if __name__=='__main__':
	testAsync()
	test()