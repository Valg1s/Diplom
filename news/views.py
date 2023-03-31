from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

from .models import News
from games.models import Statement
from authentication.models import CustomUser
from .forms import UserForm, ChangePasswordForm, StatementForm


def main(request):
    context = {
        "news_list": News.get_all(),
    }

    return render(request, "news.html", context)


def spec_news(request, news_id):
    news = News.get_by_id(news_id)
    stat = False

    if news.tournament:
        if request.user.is_active:
            if request.user.role == 1:
                coach = CustomUser.get_by_id(request.user.user_id)
                tournament = news.tournament

                if Statement.objects.filter(coach=coach, tournament=tournament).first():
                    stat = True

                print(Statement.objects.filter(coach=coach, tournament=tournament).first())

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

            user = authenticate(request, username=email, password=password)

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
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            password_1 = form.cleaned_data.get('password_1')
            password_2 = form.cleaned_data.get('password_2')

            if password_1 == password_2:
                user = CustomUser.get_by_id(request.user.user_id)

                user.set_password(password_1)
                user.save()

                return redirect("news:main")
            else:
                form.add_error("password_1", "Поля не однакові")

        else:
            print(form.errors)

    else:
        form = ChangePasswordForm()

    context = {
        "form": form
    }

    return render(request, "auth/change_password.html", context)


def logout_view(request):
    logout(request)

    return redirect("news:auth")


def send_statement(request, news_id):
    coach = CustomUser.get_by_id(request.user.user_id)
    team = coach.coach.first()
    tournament = News.get_by_id(news_id).tournament

    if request.method == "POST":
        form = StatementForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data["context"]

            Statement.create(coach, team, tournament, message)

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
