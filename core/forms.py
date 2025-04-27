from django import forms # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from .models import User

class RegisterForm(UserCreationForm):
    gender = forms.CharField(max_length=10, label='Gênero')
    age = forms.IntegerField(label='Idade')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'gender', 'age']
        