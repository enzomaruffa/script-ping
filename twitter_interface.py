# -*- coding: utf-8 -*-

__name__ = "twitter_interface"

import time
import datetime
import twitter

# ENV file stuff
import os
from os.path import join, dirname
from dotenv import load_dotenv
 
# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')
 
# Load file from the path.
load_dotenv(dotenv_path)

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token_key = os.getenv('ACCESS_TOKEN_KEY')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

api = twitter.Api(consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token_key=access_token_key,
                    access_token_secret=access_token_secret)

# ------------------

LAST_TWEET = None # Data do último tweet
MIN_TWEET_INTERVAL = 5
VIVO_USERNAME = "@vivobr"

# Checks if last tweet was before MIN_TWEET_INTERVAL
def check_last_tweet():
	now = datetime.datetime.now()
	
	#print("Last Tweet:", LAST_TWEET)

	if LAST_TWEET == None or (LAST_TWEET - now).total_seconds()/60 >= MIN_TWEET_INTERVAL:
		return True
	return False

def tweet(message):
	print("Tweeting right now!")
	global LAST_TWEET 
	LAST_TWEET = datetime.datetime.now()
	#print("Last tweet has been updated to:", LAST_TWEET)
	api.PostUpdate(message)

def tweet_bad_ping(result, bad_pings):
	message = "Poxa " + VIVO_USERNAME + "! Meu ping para o google (" +  str(result.host) + ") está em " + str(result.ping) + "ms. Isso aconteceu nas últimas " + str(bad_pings) + " tentativas de pingar. Arruma aí, pô ;-(."
	tweet(message)

def tweet_downtime(last_down, downtime):
	message = "Eita " + VIVO_USERNAME + "! Minha internet caiu pelos últimos " + str(downtime) + " segundos, ou seja, meio que desde " + str(last_down) + ". Tá foda viu ;-("
	tweet(message)



