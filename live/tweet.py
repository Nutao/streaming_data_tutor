import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import Stream
from tweepy import OAuthHandler
from tweepy import Stream
import socket
import sys
import requests
import requests_oauthlib
import json
import time


import numpy as np
import pandas as pd
import configparser
from requests_oauthlib import OAuth1Session
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
bearer_token= 'AAAAAAAAAAAAAAAAAAAAAB0bmwEAAAAA6xI7rw4xaLveDiG6glwgo9emZPI%3DWG8JZwIt9ABxANElHDui9qU7IoOBNykbjlap6mAckU6AP6lKOC'
client_id= config['twitter']['client_id']
client_secret= config['twitter']['client_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']


# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
# user tweets
user = 'veritasium'
limit=300

tweets = tweepy.Cursor(api.user_timeline, screen_name=user, count=200, tweet_mode='extended').items(limit)

# tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode='extended')

# create DataFrame
columns = ['User', 'Tweet']
data = []

for tweet in tweets:
    data.append([tweet.user.screen_name, tweet.full_text])

df = pd.DataFrame(data, columns=columns)

print(df)
my_auth = requests_oauthlib.OAuth1(api_key, api_key_secret,access_token, access_token_secret)

# # oauth = OAuth1Session(api_key,
# #                       client_secret=api_key_secret,
# #                       resource_owner_key=access_token,
# #                       resource_owner_secret=access_token_secret)

def get_tweets():
  url = ' https://api.twitter.com/1.1/search/tweets.json?q=%23python&result_type=recent'
  # query_data = [('language', 'en'), ('locale', '-130,-20,100,50'),('track','#')]
  # query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
  response = requests.get(url, auth=my_auth, stream=True)
  print(url, response)
  return response

import random

word_list = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]

random_word = random.choice(word_list)

get_tweets()
def send_tweets_to_spark(http_resp, tcp_connection):
  for line in http_resp.iter_lines():
      full_tweet = json.loads(line)
      for tweet in full_tweet['statuses']:
        send_data=""
        tweet_text=tweet['entities']['hashtags']
        texts=[]
        for tweet_dict in tweet_text:
          texts.append(tweet_dict['text'])
        texts.append(random.choice(word_list))
        texts_str = '\n'.join(texts) + '\n'
       

        # 将字符串转换为字节串
        data_to_send = texts_str.encode('utf-8')
        tcp_connection.send(data_to_send)
        time.sleep(5)  #
      
        print(tweet_text)
        print ("------------------------------------------")
        
    # except:
    #   e = sys.exc_info()[0]
    #   print("Error: %s" % e)


      

TCP_IP = "localhost"
TCP_PORT = 9999
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")

conn, addr = s.accept()
print("Connected... Starting getting tweets.")
for _ in range(5):
  resp = get_tweets()
  send_tweets_to_spark(resp, conn)

