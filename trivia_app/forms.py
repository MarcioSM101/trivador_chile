# trivia_app/forms.py

from django import forms
from .models import Pregunta

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['texto', 'categoria', 'resp_correcta', 'resp_incorrecta1', 'resp_incorrecta2', 'resp_incorrecta3']
