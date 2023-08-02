from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import Usuario


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email')
