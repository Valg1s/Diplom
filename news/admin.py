from django.contrib import admin
from django import forms

from .models import News

class NewsForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = News
        fields = '__all__'



class NewsModel(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ("date_of_pub",)
    form = NewsForm
    ordering = ("-date_of_pub",)

    readonly_fields = ("date_of_pub",)

    fieldsets = (
        (None, {"fields": ("title","content","photo_content")}),
        ("Тільки для перегляду",{"fields": ("date_of_pub",)})
    )

admin.site.register(News,NewsModel)

