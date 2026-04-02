from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, label='Name')
    last_name = forms.CharField(max_length=150, label='Surname')
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']