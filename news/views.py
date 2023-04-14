import json

from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone

from authentication.models import CustomUser, PlayerStatistic
from games.models import Statement, Tournament, Game
from team.models import Team
from .forms import UserForm, ChangePasswordForm, StatementForm, CreateTeamForm
from .models import News


# Create your views here.


def is_ajax(request):
    # Func for checking request ajax or no
    return request.headers.get('Content-Type') == 'application/json'


def main(request):
    context = {
        "news_list": News.get_all().order_by("-date_of_pub"),
    }

    return render(request, "news.html", context)


def spec_news(request, news_id):
    news = News.get_by_id(news_id)
    stat = False

    if news.tournament:
        if request.user.is_authenticated:
            if request.user.role == 1 and request.user.coach.exists():
                coach = CustomUser.get_by_id(request.user.user_id)
                tournament = news.tournament

                if not Statement.objects.filter(coach=coach, tournament=tournament).first():
                    stat = True

    context = {
        "news": News.get_by_id(news_id),
        "stat": stat,
    }

    return render(request, "spec_news.html", context)


def auth(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                user = authenticate(request, username=email, password=password)
            except Exception:
                user = None

            if user:
                login(request, user, backend=settings.AUTHENTICATION_BACKENDS[1])

                if user.check_password("standartpassword"):
                    return redirect("news:change_password")

                return redirect("news:main")

            form.add_error("email", "Не зівпало")

    else:
        form = UserForm()

    context = {
        "form": form,
    }

    return render(request, "auth/login.html", context)


@login_required(login_url="/login/")
def change_password(request):
    if request.user.check_password("standartpassword"):
        if request.method == "POST":
            form = ChangePasswordForm(request.POST)

            if form.is_valid():
                password_1 = form.cleaned_data.get('password_1')
                password_2 = form.cleaned_data.get('password_2')

                if password_1 == password_2:
                    user = CustomUser.get_by_id(request.user.user_id)

                    user.set_password(password_1)
                    user.save()

                    return redirect("news:auth")
                else:
                    form.add_error("password_1", "Поля не однакові")

        else:
            form = ChangePasswordForm()

        context = {
            "form": form
        }

        return render(request, "auth/change_password.html", context)
    else:
        return redirect("news:main")


@login_required(login_url="/login/")
def logout_view(request):
    logout(request)

    return redirect("news:auth")


@login_required(login_url="/login/")
def send_statement(request, news_id):
    coach = CustomUser.get_by_id(request.user.user_id)
    team = coach.coach.first()
    tournament = News.get_by_id(news_id).tournament

    if request.method == "POST":
        form = StatementForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["context"]

            Statement.create(coach, team, tournament, message)

            return redirect(f"/news/{news_id}")

    else:
        form = StatementForm({
            "coach": f"{coach.last_name} {coach.first_name} {coach.middle_name}",
            "team": team.team_name,
            "tournament": tournament.tournament_name
        })

    context = {
        "form": form,
    }

    return render(request, "statements.html", context)


def create_team(request):
    if request.user.role == 1 and not request.user.coach.exists():
        if request.method == "POST":
            form = CreateTeamForm(request.POST, request.FILES)

            if form.is_valid():
                name = form.cleaned_data['name']
                logo = form.cleaned_data['logo']
                year = form.cleaned_data['year']
                coach_id = request.user.user_id

                Team.create(name=name, coach=coach_id, year=year, logo=logo)

                return redirect("news:main")

        else:
            form = CreateTeamForm()

        context = {
            "form": form,
        }

        return render(request, "create_team.html", context)
    else:
        return redirect("news:main")


def my_team(request):
    if request.user.role == 1 and not request.user.coach.exists():
        return redirect("news:create_team")
    elif request.user.role == 2 and not request.user.player.exists():
        return redirect("news:main")
    else:
        user = CustomUser.get_by_id(request.user.user_id)
        if request.user.role == 1:
            team = Team.objects.filter(team_coach_id=user).first()
        else:
            team = Team.objects.filter(players=user).first()

        if request.method == "POST":
            if is_ajax(request):
                body_unicode = request.body.decode('utf-8')
                received_json = json.loads(body_unicode)

                if received_json['method'] == 'delete':
                    player = CustomUser.get_by_id(received_json['player_id'])

                    team.players.remove(player)

                if received_json['method'] == 'change_data':
                    email = received_json["email_field"]
                    password_1 = received_json["password_1"]
                    password_2 = received_json["password_2"]

                    cur_user = CustomUser.get_by_id(request.user.user_id)

                    if cur_user.email != email:
                        cur_user.email = email
                    if password_1:
                        if password_1 == password_2:
                            cur_user.set_password(password_1)

                    cur_user.save()

                return HttpResponse()
            else:
                pass

        team_name = team.team_name
        coach = f" {team.team_coach.last_name} {team.team_coach.first_name} {team.team_coach.middle_name}"
        year = team.year_of_create
        logo = f"media/{team.logo}"

        players = []

        now = timezone.now()

        user_age = now.year - request.user.date_of_birth.year - (
                (now.month, now.day) < (request.user.date_of_birth.month,
                                        request.user.date_of_birth.day)),

        for player in team.players.all().order_by("date_of_birth"):
            players.append({
                "player_id": player.user_id,
                "full_name": f"{player.last_name} {player.first_name} {player.middle_name}",
                "date_of_birth": player.date_of_birth,
                "age": now.year - player.date_of_birth.year - ((now.month, now.day) < (player.date_of_birth.month,
                                                                                       player.date_of_birth.day)),
                "player_stat": PlayerStatistic.objects.filter(player=player).order_by("-year").first(),
            })

        context = {
            "team_name": team_name,
            "coach": coach,
            "year": year,
            "logo": logo,
            "players": players,
            "user_age": user_age[0],
            "tournaments": team.teams_of_tournament.all()
        }

        return render(request, "my_team.html", context)


def tournament(request, tournament_id):
    tournament = Tournament.get_by_id(tournament_id)

    teams = tournament.teams.all()
    games = Game.objects.filter(tournament=tournament).all()

    context = {
        'tournament_name': tournament.tournament_name,
        "teams": teams,
        "games": games,
    }

    return render(request, "tournament.html", context)
