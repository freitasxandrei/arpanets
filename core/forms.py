from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    gender = forms.CharField(max_length=10)
    age = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'password', 'gender', 'age']
