from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('get-sentiments', views.getSentiments, name="get-sentiments"),
]