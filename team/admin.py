from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django import forms
from django.forms.widgets import SelectMultiple

from .models import Team
from authentication.models import CustomUser


class TeamAdminForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=SelectMultiple(attrs={'readonly': 'readonly'}),
    )
    available_players = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role=2, player=None),
        widget=SelectMultiple,
        required=False,
    )

    class Meta:
        model = Team
        fields = '__all__'


class TeamAdmin(admin.ModelAdmin):
    search_fields = ("team_name",)
    list_filter = ("year_of_create",)
    ordering = ("-team_id",)

    form = TeamAdminForm

    readonly_fields = ("team_name","year_of_create","logo","players")

    fieldsets = (
        ("Змінити тренера", {"fields": ("team_coach",)}),
        ("Додати гравців",{"fields": ("players","available_players")}),
        ("Тільки для перегляду", {"fields": ("team_name", "year_of_create", "logo")}),
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['available_players'].label = 'Доступні гравці'
        return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj:
            # Заполняем поле available_players только свободными игроками
            context = {'available_players': CustomUser.objects.filter(role=2, player=None)}
        else:
            context = {}
        if extra_context is not None:
            context.update(extra_context)
        return super().change_view(request, object_id, form_url=form_url, extra_context=context)

    def save_model(self, request, obj, form, change):
        # Получаем список выбранных игроков из формы
        selected_players = form.cleaned_data.get('available_players', [])
        # Добавляем выбранных игроков в поле players объекта команды
        for player in selected_players:
            obj.add_players(player)
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False

    def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
        if obj:
            selected_coach = CustomUser.objects.filter(user_id = obj.team_coach.user_id)
            cont = context["adminform"].form.fields

            cont["team_coach"].queryset = selected_coach.union(CustomUser.objects.filter(role=1, coach=None))
        return super(TeamAdmin, self).render_change_form(request, context, add, change, form_url, obj)


admin.site.register(Team,TeamAdmin)
