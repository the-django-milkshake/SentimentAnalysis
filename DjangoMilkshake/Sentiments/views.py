from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
from django.http import HttpResponse
import requests
import json
import tweepy
from tweepy.auth import OAuthHandler
from textblob import TextBlob
from .fusioncharts import FusionCharts
from collections import OrderedDict
from .news import Analysis

# Create your views here.


def home(request):
    return render(request, 'index.html', {})


def getSentiments(request):
    auth = OAuthHandler('XRCnQ49KVWgy0IsN5QYBTn5Zm', 'P6UwYNbfboKQfrr51P3HLjp88Mq32SxNcQt7zsFKDdAZdXrAoW')
    auth.set_access_token('912853951984238592-BODZqgKvgD0QdKD5Rz1grMGPCDFiZm4', 'proz3qXFAR7Ie8YOylG86z0uERL8orw0HcClAA2X4CN6t')

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    public_tweets = []
    if request.method=='GET':
        query = request.GET.get('search',"congress")
        a = Analysis(query)
        full_analysis = a.run()
    else:
        return redirect('home')

    for tweet in tweepy.Cursor(api.search, q=query, result_type="recent", tweet_mode="extended", lang="en").items(20):
        blob = TextBlob(tweet.full_text)
        senti = blob.sentiment.polarity
        sub = blob.sentiment.subjectivity
        public_tweets.append({'tweet':tweet, 'subjectivity':sub})


    return render(request, 'search_result.html', {'public_tweets': public_tweets, 'full_analysis': full_analysis})


def chart(request):

    # Chart data is passed to the `dataSource` parameter, as dictionary in the form of key-value pairs.
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key-value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Countries With Most Oil Reserves [2017-18]"
    chartConfig["subCaption"] = "In MMbbl = One Million barrels"
    chartConfig["xAxisName"] = "Country"
    chartConfig["yAxisName"] = "Reserves (MMbbl)"
    chartConfig["numberSuffix"] = "K"
    chartConfig["theme"] = "fusion"

    # The `chartData` dict contains key-value pairs data
    chartData = OrderedDict()
    chartData["Venezuela"] = 200
    chartData["Saudi"] = 260
    chartData["Canada"] = 180
    chartData["Iran"] = 140
    chartData["Russia"] = 115
    chartData["UAE"] = 100
    chartData["US"] = 30
    chartData["China"] = 30


    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    # Convert the data in the `chartData` array into a format that can be consumed by FusionCharts.
    # The data for the chart should be in an array wherein each element of the array is a JSON object
    # having the `label` and `value` as keys.

    # Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)


    # Create an object for the column 2D chart using the FusionCharts class constructor
    # The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("column2d", "ex1" , "600", "400", "chart-1", "json", dataSource)

    return  render(request, 'chart.html', {'output' : column2D.render(), 'chartTitle': 'Simple Chart Using Array'})