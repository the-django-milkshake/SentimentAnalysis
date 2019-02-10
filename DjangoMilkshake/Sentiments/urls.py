from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('timeline', views.home_timeline, name="timeline"),
    path('chart', views.chart, name="chart"),
]