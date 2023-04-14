from django import forms
from django.utils import timezone


class UserForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Електронна пошта"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))


class ChangePasswordForm(forms.Form):
    password_1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Новий пароль"}))
    password_2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Повторіть новий пароль",
                                                                   'data-confirm-password': 'password_1'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password_1')
        password2 = cleaned_data.get('password_2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі різні чи один з них відсутній")

        return cleaned_data


class StatementForm(forms.Form):
    coach = forms.CharField(label="Тренер:",widget=forms.TextInput(attrs={'readonly':'readonly',"class":"blocked__input"}))
    team = forms.CharField(label="Команда:",widget=forms.TextInput(attrs={'readonly':'readonly',"class":"blocked__input"}))
    tournament = forms.CharField(label="Турнір:", widget=forms.TextInput(attrs={'readonly': 'readonly',"class":"blocked__input"}))
    context = forms.CharField(label="Повідомлення:", widget=forms.Textarea(attrs={"placeholder":"Ваше повідомлення",
                                                                                  'rows':4, 'cols':15}))


class CreateTeamForm(forms.Form):
    logo = forms.ImageField(label="Логотип")
    name = forms.CharField(label="Назва команди",widget=forms.TextInput(attrs={"placeholder":"Назва команди"}))
    year = forms.IntegerField(label="Рік створення", min_value=1850,
                              max_value=int(timezone.now().year),
                              widget=forms.NumberInput(attrs={"placeholder":"Рік створення"}))
