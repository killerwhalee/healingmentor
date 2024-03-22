from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from common.models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("image", "fullname", "classname")
