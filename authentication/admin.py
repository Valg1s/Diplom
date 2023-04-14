from django.contrib import admin
from django.core.mail import get_connection,EmailMessage
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
            None, {"fields": ("last_name", "first_name", "middle_name", "role","date_of_birth")}
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
                last_name=obj.last_name, middle_name=obj.middle_name, role=obj.role,date_of_birth=obj.date_of_birth
            )

            with get_connection(
                                host=settings.EMAIL_HOST,
                                port=settings.EMAIL_PORT,
                                username=settings.EMAIL_HOST_USER,
                                password=settings.EMAIL_HOST_PASSWORD,
                                use_tls=settings.EMAIL_USE_TLS
            ) as connection:
                subject = "Реєстрація у волейбольній лізі"
                message = f"Добрий день, {obj.last_name} {obj.first_name}!\n\nВаш аккаунт був успішно зареєстрований" \
                          f" на сайті волейбольної ліги!\nЩоб увійти в аккаунт,Вам потрібно перейти" \
                          f" за посиланням: <тут повинне бути посилання>.\nВведіть" \
                          f" Вашу пошту,на яку прийшов цей лист,та пароль standartpassword ,після чого ви зможете" \
                          f" змінити його.\n\nДякую за вашу участь!"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [obj.email]

                EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()

        else:
            obj.save()
        return obj


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PlayerStatistic, PlayerStatisticAdmin)
