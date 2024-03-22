from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from payapp.models import CURRENCY_CHOICES


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "currency"]


class AdminRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]