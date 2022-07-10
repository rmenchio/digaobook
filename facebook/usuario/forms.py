import email
from django import forms
from . import models
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self, *args, **kwargs):
        pass


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Confirmar senha'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password','password2', 'email')

    def clean(self, *args, **kwargs):
        pass