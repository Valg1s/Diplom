from django import forms

from authentication.models import CustomUser


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
    coach = forms.CharField(label="Тренер:",widget=forms.TextInput(attrs={'readonly':'readonly'}))
    team = forms.CharField(label="Команда:",widget=forms.TextInput(attrs={'readonly':'readonly'}))
    tournament = forms.CharField(label="Турнір:", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    context = forms.CharField(label="Повідомлення:", widget=forms.Textarea(attrs={"placeholder":"Ваше повідомлення",
                                                                                  'rows':4, 'cols':15}))