from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    email2 = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]