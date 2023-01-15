from django.shortcuts import render ,Http404,redirect

from games.models import Statement

def accept_statements(request,id):
    if request.method == "GET":
        statement = Statement.get_by_id(id)
        context = {'statement': statement}
        return render(request,"admin_adds/accept.html",context)
    elif request.method == "POST":
        method = request.POST['method']

        id = request.POST['statement_id']
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
