from django.contrib import admin

from .models import Team

class TeamAdmin(admin.ModelAdmin):
    search_fields = ("team_name",)
    list_filter = ("year_of_create",)
    ordering = ("-team_id",)

    readonly_fields = ("team_name","team_coach","year_of_create","players","logo")

    fieldsets = (
        ("Тільки для перегляду", {"fields": ("team_name","team_coach","year_of_create","players","logo")}),
    )

admin.site.register(Team,TeamAdmin)
