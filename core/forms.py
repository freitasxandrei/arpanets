from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    gender = forms.CharField(max_length=10, label='Gênero')
    age = forms.IntegerField(label='Idade')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'gender', 'age']

    