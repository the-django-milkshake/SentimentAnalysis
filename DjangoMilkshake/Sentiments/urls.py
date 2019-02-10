from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('tweet-sentiments/<query>', views.tweetSentiments, name="tweet-sentiments"),
    path('chart', views.chart, name="chart"),
    path('news/<query>', views.newsSentiments, name="news"),
]