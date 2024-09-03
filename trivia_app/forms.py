# trivia_app/forms.py

from django import forms
from .models import Pregunta
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['texto', 'categoria', 'resp_correcta', 'resp_incorrecta1', 'resp_incorrecta2', 'resp_incorrecta3']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
