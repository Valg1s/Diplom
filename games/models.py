from django.db import models
from django.utils import timezone

from authentication.models import CustomUser
from team.models import Team

STATUS_CHOICE = (
    (0,"Не розглянута"),
    (1,"Схвалено"),
    (2,"Відхилено"),
)

class Tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    tournament_name = models.CharField(null=False, max_length=128, verbose_name="Назва турніру")
    date_of_start = models.DateField(null=False, verbose_name="Дата початку")
    date_of_end = models.DateField(null=False, verbose_name="Дата кінця")
    teams = models.ManyToManyField(Team, related_name="teams_of_tournament", null=True,blank=True, verbose_name="Команди - учасники")

    class Meta:
        verbose_name_plural = 'Турніри'
        verbose_name = "турнір"

    def __str__(self):
        return f"{self.tournament_id}| {self.tournament_name}: {self.date_of_start} -- {self.date_of_end}"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.tournament_id})"

    @staticmethod
    def get_by_id(id):
        tournament = Tournament.objects.filter(tournament_id=id)[0]

        if tournament:
            return tournament
        else:
            raise "Турнір не знайдено"

    @staticmethod
    def delete_by_id(id):
        if Tournament.objects.filter(tournament_id=id).delete()[0] == 0:
            return True
        else:
            raise "Турнір не знайдено"

    @staticmethod
    def create(name, date_of_start, date_of_end):

        tournament = Tournament(tournament_name=name, date_of_start=date_of_start, date_of_end=date_of_end)

        tournament.save()

        return True

    def update(self, name=None, date_of_start=None, date_of_end=None):
        if name:
            self.tournament_name = name
        if date_of_start:
            self.date_of_start = date_of_start
        if date_of_end:
            self.date_of_end = date_of_end

        self.save()

        return True

    @staticmethod
    def get_all():
        return Tournament.objects.all()

    def add_team(self, teams):
        if type(teams) == "list":
            for team in teams:
                self.teams.add(team)
        else:
            self.teams.add(teams)

        self.save()

    def delete_team_by_id(self, id):
        team = self.teams.get(team_id=id)

        self.teams.remove(team)
        return None

    def delete_all_teams(self):
        self.teams.clear()

        return True

    def get_all_teams(self):
        return self.teams.all()

class Statement(models.Model):
    statement_id = models.AutoField(primary_key=True)
    coach = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,related_name="coach_statements",verbose_name="Тренер")
    team = models.ForeignKey(Team,on_delete=models.DO_NOTHING,related_name="team_statements",verbose_name="Команда")
    tournament = models.ForeignKey(Tournament,on_delete=models.DO_NOTHING,related_name="tournament_statements",verbose_name="Турнір")
    context = models.CharField(max_length=1024,verbose_name="Повідомлення")
    date = models.DateField(verbose_name="Дата")
    status = models.IntegerField(default=0 , choices=STATUS_CHOICE,verbose_name="Статус заяви")

    class Meta:
        verbose_name = "заяву"
        verbose_name_plural = 'Заяви'

    def __str__(self):
        return f"{self.statement_id}| {self.tournament.tournament_name} -- {self.team.team_name}"

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.statement_id})'

    @staticmethod
    def get_by_id(id):
        stat = Statement.objects.filter(statement_id=id)[0]

        if stat:
            return stat
        else:
            raise "Заяву не знайдено"

    @staticmethod
    def delete_by_id(id):
        if Statement.objects.filter(statement_id=id).delete()[0] == 0:
            return True
        else:
            raise "Заяву не знайдено"

    @staticmethod
    def create(coach,team,tournament,context):
        if coach and team and tournament and context:
            date = timezone.now()
            statement = Statement(coach = coach,team = team,tournament= tournament,context =context, date=date)
            statement.save()

            return True
        else:
            return False

    def to_dict(self):
        return {
            "id": self.statement_id,
            "coach": self.coach,
            "team": self.team,
            "tournament": self.tournament,
            "context": self.context,
            "date": self.date,
        }

    def update(self, context = None):
        if context:
            self.context = context

        self.save()

        return None


    @staticmethod
    def get_all():
        return Statement.objects.all()

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_place = models.CharField(null=False,max_length=128, verbose_name="Місце проведення")
    first_team = models.ForeignKey(Team, related_name="team_1", on_delete=models.DO_NOTHING, verbose_name="Команда 1")
    second_team = models.ForeignKey(Team, related_name="team_2", on_delete=models.DO_NOTHING, verbose_name="Команда 2")
    winner = models.ForeignKey(Team, related_name="winner", on_delete=models.DO_NOTHING, verbose_name="Переможець",
                               null=True)
    store = models.CharField(null=True, max_length=64, verbose_name="Рахунок")
    date_of_game = models.DateTimeField(verbose_name="Дата проведення")
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING, verbose_name="Турнір(Назва турніру чи товариська гра)")

    class Meta:
        verbose_name_plural = 'Ігри'
        verbose_name = "гру"

    def __str__(self):
        return f"{self.game_id}| {self.first_team.team_name} - {self.second_team.team_name} : {self.store}"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.game_id})"

    @staticmethod
    def get_by_id(id):
        game = Game.objects.filter(game_id=id)[0]

        if game:
            return game
        else:
            raise "Гру не знайдено"

    @staticmethod
    def delete_by_id(id):
        if Game.objects.filter(game_id=id).delete()[0] == 0:
            return True
        else:
            raise "Гру не знайдено"

    @staticmethod
    def create(place, team_1, team_2, date_of_game, tournament):

        game = Game(game_place=place, first_team=team_1,
                    second_team=team_2, date_of_game=date_of_game, tournament=tournament)

        game.save()

        return True

    def update(self, place=None, team_1=None, team_2=None, date_of_game=None, tournament=None, winner=None, store=None):
        if place:
            self.game_place = place
        if team_1:
            self.first_team = team_1
        if team_2:
            self.second_team = team_2
        if date_of_game:
            self.date_of_game = date_of_game
        if tournament:
            self.tournament = tournament
        if winner:
            self.winner = winner
        if store:
            self.store = store

        self.save()

        return True

    @staticmethod
    def get_all():
        return Game.objects.all()


