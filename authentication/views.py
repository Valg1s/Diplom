from django.shortcuts import render ,Http404,redirect

from games.models import Statement , Tournament


def accept_statements(request,id):
    if request.method == "GET":
        statement = Statement.get_by_id(id)
        context = {'statement': statement}
        return render(request,"admin_adds/accept.html",context)
    elif request.method == "POST":
        method = request.POST['method']

        statement = Statement.get_by_id(id)

        status = 2

        if method == "Accept":
            statement.tournament.add_team(statement.team)
            status = 1

        statement.status = status
        statement.save()

        return redirect("/admin/games/statement/")
    else:
        return Http404


def delete_team(request,id):
    if request.method == "GET":
        tournament = Tournament.get_by_id(id)
        teams = tournament.teams.all()
        context = {
            "tournament":tournament,
            "teams": teams,
        }

        return render(request, "admin_adds/remove.html", context)
    elif request.method == "POST":
        teams = request.POST.getlist('team')
        tournament = Tournament.get_by_id(id)
        if len(teams) == len(tournament.get_all_teams()):
            tournament.delete_all_teams()
        else:
            for team in teams:
                try:
                    tournament.delete_team_by_id(int(team))
                except Exception as e:
                    print(e)

        return redirect("/admin/games/tournament/")
    else:
        return Http404


