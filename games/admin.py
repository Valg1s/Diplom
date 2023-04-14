from django.contrib import admin
from django.shortcuts import render
from django.utils.html import format_html
from django.template.loader import render_to_string


from .models import Game,Tournament, Statement
from team.models import Team
from . import views

class TournamentAdmin(admin.ModelAdmin):
    list_display = ("__str__","delete_team")
    ordering = ("-date_of_start", "-date_of_end",)
    search_fields = ("tournament_name",)

    readonly_fields = ("teams",)
    fieldsets = (
        (None, {"fields": ("tournament_name", ("date_of_start", "date_of_end",))}),
        ("Додавати тільки по заявках",{"fields": ("teams",)})
    )

    def delete_team(self,obj):
        if obj.teams.all():
            context = {
                "redirect_to": 'custom_admin:remove',
                "parameter": obj.tournament_id,
                "text": "Відсторонити команду",
            }
        elif not obj.teams.all():
            context = {"text":"Команди відсутні"}
        return format_html(render_to_string("admin_adds/admin_button.html",context=context))

    delete_team.short_description = "Відсторонення команди"


class GameAdmin(admin.ModelAdmin):
    list_filter = ("date_of_game",)
    ordering = ("-date_of_game",)

    fieldsets = (
        (None, {"fields":("game_place",("first_team","second_team",),"date_of_game","tournament")}),
        ("Необов'язкові поля(Заповнювати після гри)",{"fields":("winner","store",("set_first_team","set_second_team"))}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("game_place","first_team","second_team","date_of_game","tournament")

        return self.readonly_fields + ("winner", "store","set_first_team","set_second_team")

    def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
        if obj:
            context["adminform"].form.fields["winner"].queryset = Team.objects.filter(team_id=obj.first_team.team_id)  | Team.objects.filter(team_id=obj.second_team.team_id)
        return super(GameAdmin, self).render_change_form(request, context, add, change, form_url, obj)


class StatementAdmin(admin.ModelAdmin):
    list_display = ("__str__","accept_stat",)
    list_filter = ("tournament",)
    readonly_fields = ("coach","team","tournament","context","date","status")

    def accept_stat(self,obj):
        if obj.status == 0:
            context = {
                "redirect_to": 'custom_admin:accept',
                "parameter": obj.statement_id,
                "text": "Відреагувати на заяву",
            }
        elif obj.status != 0:
            context = {"text":"Вже розглянута"}
        return format_html(render_to_string("admin_adds/admin_button.html",context=context))

    accept_stat.short_description = "Дії з заявами"



admin.site.register(Game,GameAdmin)
admin.site.register(Tournament,TournamentAdmin)
admin.site.register(Statement,StatementAdmin)