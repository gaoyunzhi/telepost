#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telepost
import album_sender
import yaml
from telegram.ext import Updater

with open('credential') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
tele = Updater(CREDENTIALS['bot_token'], use_context=True)
chat = tele.bot.get_chat(CREDENTIALS['channel'])

def test(url):
	result = telepost.get(url)
	print(result)
	album_sender.send_v2(chat, result)
	
if __name__=='__main__':
	test('https://www.reddit.com/r/Feminism/comments/lwz97t/dump_the_dimorphism_between_female_and_male_brain/')