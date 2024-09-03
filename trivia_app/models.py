from django.db import models
from django.contrib.auth.models import User
import random

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    texto = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    resp_correcta = models.CharField(max_length=255)
    resp_incorrecta1 = models.CharField(max_length=255)
    resp_incorrecta2 = models.CharField(max_length=255)
    resp_incorrecta3 = models.CharField(max_length=255)

   
    def get_respuestas_aleatorias(self):
        respuestas = [self.resp_correcta, self.resp_incorrecta1, self.resp_incorrecta2, self.resp_incorrecta3]
        random.shuffle(respuestas)
        return respuestas
    
    def __str__(self):
        return self.texto

class Juego(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    puntaje = models.IntegerField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.puntaje} puntos"

class Like(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'juego')
