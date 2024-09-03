from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Pregunta, Juego, Like
from .models import Pregunta, Categoria  
from .forms import PreguntaForm
from django.utils import timezone
import random
from django.contrib import messages
from .forms import CustomUserCreationForm


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
    # Paso 1: Selección de categoría
    if request.method == 'GET' and 'categoria' not in request.session:
        categorias = Categoria.objects.all()
        return render(request, 'trivia_app/seleccionar_categoria.html', {'categorias': categorias})

    # Paso 2: Mostrar preguntas después de seleccionar una categoría
    elif request.method == 'POST' and 'categoria' not in request.session:
        categoria_id = request.POST.get('categoria')
        if not categoria_id:
            return redirect('home')  # Redirige si no hay categoría seleccionada

        categoria = get_object_or_404(Categoria, id=categoria_id)

        # Obtener preguntas aleatorias de la categoría seleccionada
        preguntas = list(Pregunta.objects.filter(categoria=categoria))
        random.shuffle(preguntas)
        preguntas = preguntas[:4]

        # Guardar la categoría seleccionada y las preguntas en la sesión
        request.session['categoria'] = categoria.id
        request.session['preguntas_ids'] = [pregunta.id for pregunta in preguntas]

        # Mostrar las preguntas al usuario
        return render(request, 'trivia_app/jugar.html', {'preguntas': preguntas, 'categoria': categoria})

    # Paso 3: Guardar el juego después de responder preguntas
    elif request.method == 'POST' and 'categoria' in request.session:
        preguntas_ids = request.session.get('preguntas_ids', [])
        if not preguntas_ids:
            return redirect('home')

        preguntas = Pregunta.objects.filter(id__in=preguntas_ids)
        puntaje = 0
        for pregunta in preguntas:
            respuesta_usuario = request.POST.get(f'respuesta_{pregunta.id}')
            if respuesta_usuario == pregunta.resp_correcta:
                puntaje += 1

        # Guardar el juego con el puntaje
        Juego.objects.create(
            usuario=request.user,
            puntaje=puntaje,
            fecha=timezone.now()
        )

        # Limpiar la sesión después de guardar el juego
        del request.session['categoria']
        del request.session['preguntas_ids']

        return redirect('home')

    # Si algo sale mal, redirigir al inicio
    return redirect('home')


@login_required
def like_resultado(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    Like.objects.get_or_create(usuario=request.user, juego=juego)
    return redirect('home')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def preguntas(request):
    """
    Vista que muestra todas las preguntas, accesible solo para superusuarios.
    """
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        preguntas = Pregunta.objects.filter(categoria_id=categoria_id)
    else:
        preguntas = Pregunta.objects.all()
    
    categorias = Categoria.objects.all()
    return render(request, 'trivia_app/preguntas.html', {'preguntas': preguntas, 'categorias': categorias})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
