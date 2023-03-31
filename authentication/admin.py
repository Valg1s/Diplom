from django.contrib import admin
from django.core.mail import get_connection,send_mail
from django.conf import settings

from .models import CustomUser, PlayerStatistic

#CONNECTION = get_connection()


class PlayerStatisticAdmin(admin.ModelAdmin):
    list_filter = ("year", "player",)
    fieldsets = (
        (None, {"fields": ("player", "year",)}),
        ("Статистика гравця", {"fields": ("games", "points", "defence")})
    )

    def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
        if not obj:
            context["adminform"].form.fields["player"].queryset = CustomUser.objects.filter(role=2)
        return super(PlayerStatisticAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("player", "year",)

        return self.readonly_fields


class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ("email",)
    list_filter = ('role',)
    readonly_fields = ("created_at", "updated_at", "password")

    fieldsets = (
        (
            None, {"fields": ("last_name", "first_name", "middle_name", "role")}
        ),
        (
            "Конфіденційні дані", {"fields":("email",)}
        ),
        (
            "Тільки для перегляду", {"fields": ("created_at", "updated_at","password",)}
        ),
        (
            "Права, можливості та стан", {"fields": ("is_superuser", "is_staff", "is_active")}
        )
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("email",)

        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj = CustomUser.objects.create_user(
                email=obj.email, password="standartpassword", first_name=obj.first_name,
                last_name=obj.last_name, middle_name=obj.middle_name, role=obj.role
            )

            '''send_mail(
                subject='Реєстрація у Волейбольній Лізі',
                message=f'Добрий день, {obj.last_name} {obj.first_name}!Ви були успішно зареєстровані у базі даних Ліги.'
                f' Ви можете зайти за допомогою вашої пошти: {obj.email} та паролем "standartpassword".'
                f' Дякую за реєстрацію! ',
                from_email='kursworkvolleyballleague@gmail.com',
                recipient_list=[obj.email],
                fail_silently=False,
                auth_user='kursworkvolleyballleague@gmail.com',
                auth_password='Strongpassword123',
                connection=None,
                html_message=None,
            )'''

        else:
            obj.save()
        return obj


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PlayerStatistic, PlayerStatisticAdmin)
