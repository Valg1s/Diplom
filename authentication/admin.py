from django.contrib import admin

from .models import CustomUser, PlayerStatistic


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


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PlayerStatistic, PlayerStatisticAdmin)
