from django.contrib import admin
from django.contrib.auth import logout
from django.urls import re_path

from . import views

app_name="news"

urlpatterns = [
    re_path(r"^$",views.main, name="main"),
    re_path(r"^news/(?P<news_id>\d+)$", views.spec_news, name="spec_news"),
    re_path(r"^login/$", views.auth, name="auth"),
    re_path(r"^change_password/$", views.change_password, name="change_password"),
    re_path(r"^logout/$", views.logout_view,name="logout"),
    re_path(r"^news/(?P<news_id>\d+)/statements/$", views.send_statement, name="statement"),
]