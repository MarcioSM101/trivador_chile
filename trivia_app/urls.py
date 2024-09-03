from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Esta línea hace que 'home' sea la vista predeterminada
    path('preguntas/', views.preguntas, name='preguntas'),
    path('preguntas/crear/', views.crear_pregunta, name='crear_pregunta'),
    path('juego/', views.jugar, name='jugar'),
    path('like/<int:juego_id>/', views.like_resultado, name='like_resultado'),
    path('preguntas/eliminar/<int:pregunta_id>/', views.eliminar_pregunta, name='eliminar_pregunta'),
    path('signup/', views.signup, name='signup'),  # Ruta para el registro
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Ruta para el login
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Ruta para el logout
]
