from django.core.management.base import BaseCommand
from trivia_app.models import Categoria
import json
import os

class Command(BaseCommand):
    help = 'Carga categorías desde un archivo JSON'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(__file__), '../../../data/categorias.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            categorias_data = json.load(file)
            for categoria in categorias_data:
                Categoria.objects.get_or_create(nombre=categoria['nombre'])
        self.stdout.write(self.style.SUCCESS('Categorías cargadas exitosamente.'))
