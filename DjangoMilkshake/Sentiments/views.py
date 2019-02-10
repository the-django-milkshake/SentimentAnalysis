from django.shortcuts import render
# from django.contrib.auth import login, authenticate
from django.http import HttpResponse
import requests
import json
import tweepy
from tweepy.auth import OAuthHandler
from textblob import TextBlob
from langdetect import detect

# Create your views here.


def home(request):

    return HttpResponse("welcome to home")


def home_timeline(request):
    auth = OAuthHandler('XRCnQ49KVWgy0IsN5QYBTn5Zm', 'P6UwYNbfboKQfrr51P3HLjp88Mq32SxNcQt7zsFKDdAZdXrAoW')
    auth.set_access_token('912853951984238592-BODZqgKvgD0QdKD5Rz1grMGPCDFiZm4', 'proz3qXFAR7Ie8YOylG86z0uERL8orw0HcClAA2X4CN6t')

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    public_tweets = []

    for tweet in tweepy.Cursor(api.home_timeline).items(5):
        blob = TextBlob(tweet.text)
        senti = blob.sentiment.polarity
        sub = blob.sentiment.subjectivity
        lang = detect(tweet.text)
        public_tweets.append({'tweet':tweet, 'subjectivity':sub, 'language':lang})


    return render(request, 'public_tweets.html', {'public_tweets': public_tweets})