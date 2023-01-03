from django.contrib import admin

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ("email",)
    list_filter = ('role',)
    readonly_fields = ("email","password","created_at","updated_at")
    fieldsets = (
        (
          None, {"fields":("last_name","first_name","middle_name","role")}
        ),
        (
        "Тільки для перегляду", {"fields":("email","password","created_at","updated_at")}
        ),
        (
            "Права, можливості та стан", {"fields":("is_superuser","is_staff","is_active")}
        )
    )

admin.site.register(CustomUser, CustomUserAdmin)
