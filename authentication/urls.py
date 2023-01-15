from django.contrib import admin
from django.urls import re_path , include,path

from . import views

app_name = "custom_admin"

urlpatterns = [
    re_path(r'accept/(?P<id>\d+)$', views.accept_statements , name="accept")
]