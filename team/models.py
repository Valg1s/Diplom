from datetime import datetime

from django.db import models
from django.utils import timezone

from authentication.models import CustomUser


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(null=False, max_length=128, verbose_name="Назва команди")
    team_coach = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Тренер",related_name="coach")
    year_of_create = models.IntegerField(null=False, default=int(datetime.now().year), verbose_name="Рік створення")
    players = models.ManyToManyField(CustomUser, null=True,blank=True, verbose_name="Гравці",related_name="player")
    logo = models.ImageField(null=True, default="default_logo.png",verbose_name="Логотип")

    class Meta:
        verbose_name_plural = 'Команди'
        verbose_name = "команду"

    def __str__(self):
        return f"{self.team_id}| {self.team_name}"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.team_id})"

    @staticmethod
    def get_by_id(id):
        team = Team.objects.filter(team_id=id)[0]

        if team:
            return team
        else:
            raise "Команду не знайдено"

    @staticmethod
    def delete_by_id(id):
        if Team.objects.filter(team_id=id).delete()[0] == 0:
            return True
        else:
            raise "Команду не знайдено"

    @staticmethod
    def create(name, coach, year=None, logo=None):
        coach = CustomUser.get_by_id(coach)

        team = Team(team_name=name, team_coach=coach, year_of_create=year, logo=logo)

        team.save()

        return True

    def add_players(self,players):
        if type(players) == "list":
            for player in players:
                self.players.add(player)
        else:
            self.players.add(players)

    def update(self,name=None,coach = None,year = None,logo = None):
        if name:
            self.team_name = name
        if coach:
            if type(coach) == "int":
                coach = CustomUser.get_by_id(coach)

            self.team_coach = coach
        if year:
            self.year_of_create = year

        if logo:
            self.logo = logo

        self.save()

    def delete_player_by_id(self,id):
        for player in self.players:
            if player.user_id == id:
                self.players.remove(player)
                break
        return None

    def delete_all_players(self):
        self.players.clear()

        return True

    @staticmethod
    def get_all():
        return Team.objects.all()

