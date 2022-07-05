from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Link


class AddLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('url', )

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields= ['username', 'email', 'password1', 'password2']