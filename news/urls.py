from django.urls import re_path
from django.views.generic import TemplateView


from . import views

app_name="news"

urlpatterns = [
    re_path(r"^$",views.main, name="main"),
    re_path(r"^news/(?P<news_id>\d+)$", views.spec_news, name="spec_news"),
    re_path(r"^login/$", views.auth, name="auth"),
    re_path(r"^change_password/$", views.change_password, name="change_password"),
    re_path(r"^logout/$", views.logout_view,name="logout"),
    re_path(r"^news/(?P<news_id>\d+)/statements/$", views.send_statement, name="statement"),
    re_path(r"^create_team/$", views.create_team,name= "create_team"),
    re_path(r"^my_team/$",views.my_team,name="my_team"),
    re_path(r"^my_team/tournament/(?P<tournament_id>\d+)",views.tournament, name="tournament"),
    re_path(r"^FAQ/$",TemplateView.as_view(template_name="FAQ.html"), name="FAQ"),
]