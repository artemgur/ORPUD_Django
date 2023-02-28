from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm

from web.models import User


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Пароль еще раз')

    button_text = 'Зарегистрироваться'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "password", "password2")


# class CreateNoteForm(forms.ModelForm):
#     button_text = 'Создать'
#     class Meta:
#         model = Note
#         fields = ['title', 'text']

class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

    button_text = 'Войти'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        user = authenticate(**cleaned_data)
        if user is None:
            self.add_error(None, "Неверное имя пользователя или пароль")
        else:
            login(self.request, user)


class TranslatedPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(TranslatedPasswordChangeForm, self).__init__(user, *args, **kwargs)
        self.fields['old_password'].label = 'Текущий пароль:'
        self.fields['new_password1'].label = 'Новый пароль:'
        self.fields['new_password2'].label = 'Новый пароль еще раз:'
