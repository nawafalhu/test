from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    pass

class RegistrationForm(UserCreationForm):
    class meta:
        model = User
        field =['username','email','password 1','password 2']
        