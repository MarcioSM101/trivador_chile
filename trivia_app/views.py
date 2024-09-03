from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Pregunta, Juego, Like
from .models import Pregunta, Categoria  
from .forms import PreguntaForm
import random


def home(request):
    # Lógica para obtener los 5 mejores juegos
    juegos = Juego.objects.order_by('-puntaje')[:5]
    fecha_filtrada = request.GET.get('fecha', None)
    if fecha_filtrada:
        juegos = Juego.objects.filter(fecha=fecha_filtrada).order_by('-puntaje')[:5]

    # Verificar si el usuario está autenticado antes de obtener los likes
    if request.user.is_authenticated:
        juegos_liked_by_user = Like.objects.filter(usuario=request.user).values_list('juego_id', flat=True)
    else:
        juegos_liked_by_user = []  # Si el usuario no está autenticado, no hay likes

    context = {
        'juegos': juegos,
        'juegos_liked_by_user': juegos_liked_by_user,
        'fecha_filtrada': fecha_filtrada,
    }
    return render(request, 'trivia_app/home.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def crear_pregunta(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías

    if request.method == 'POST':
        form = PreguntaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('preguntas')  # Redirige a la lista de preguntas después de crear una nueva
    else:
        form = PreguntaForm()
    
    return render(request, 'trivia_app/crear_pregunta.html', {'form': form, 'categorias': categorias})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def eliminar_pregunta(request, pregunta_id):
    """
    Vista para eliminar una pregunta específica, accesible solo para superusuarios.
    """
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    pregunta.delete()
    return redirect('preguntas')

@login_required
def jugar(request):
    if request.method == 'POST':
        # Obtener la categoría seleccionada por el usuario
        categoria_id = request.POST.get('categoria')
        categoria = get_object_or_404(Categoria, id=categoria_id)
        
        # Obtener preguntas aleatorias de la categoría seleccionada
        preguntas = list(Pregunta.objects.filter(categoria=categoria))
        random.shuffle(preguntas)
        preguntas = preguntas[:4]  # Seleccionar solo 4 preguntas
        
        return render(request, 'trivia_app/jugar.html', {'preguntas': preguntas, 'categoria': categoria})
    
    else:
        # Mostrar formulario de selección de categoría
        categorias = Categoria.objects.all()
        return render(request, 'trivia_app/seleccionar_categoria.html', {'categorias': categorias})

@login_required
def like_resultado(request, juego_id):
    """
    Vista para dar 'like' a un resultado de juego específico.
    """
    juego = get_object_or_404(Juego, id=juego_id)
    Like.objects.get_or_create(usuario=request.user, juego=juego)
    return redirect('home')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def preguntas(request):
    """
    Vista que muestra todas las preguntas, accesible solo para superusuarios.
    """
    preguntas = Pregunta.objects.all()
    return render(request, 'trivia_app/preguntas.html', {'preguntas': preguntas})


def signup(request):
    """
    Vista de registro de usuarios.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio después de registrarse
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
