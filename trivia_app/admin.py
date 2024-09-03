# trivia_app/admin.py

from django.contrib import admin
from .models import Categoria, Pregunta, Juego, Like

admin.site.register(Categoria)
admin.site.register(Pregunta)
admin.site.register(Juego)
admin.site.register(Like)
