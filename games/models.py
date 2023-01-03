from django.db import models

from team.models import Team

class Game(models.Model):
    game_id = models.AutoField(primary_key = True)
    game_place = models.CharField(null=False, verbose_name="Місце проведення")
    first_team = models.ForeignKey(Team,related_name="team_1",on_delete=models.DO_NOTHING, verbose_name="Команда 1")
    second_team = models.ForeignKey(Team,related_name="team_2",on_delete=models.DO_NOTHING,verbose_name="Команда 2")
    winner = models.ForeignKey(Team,related_name="winner",on_delete=models.DO_NOTHING,verbose_name="Переможець",null=True)
    store = models.CharField(null=True,max_length=64 , verbose_name="Рахунок")
    date_of_game = models.DateTimeField(verbose_name="Дата проведення")
    tournament = models.CharField(null=False,max_length=128, verbose_name="Тип турниру")



