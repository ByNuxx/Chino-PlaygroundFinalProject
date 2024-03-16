from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import logout_then_login
from .forms import SignUpForm
from accounts.models import Profile

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')  # Redirecciona a la página principal
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def cerrar_sesion(request):
    return logout_then_login(request)

@login_required
def about_view(request):
    if request.method == 'POST':
        perfil_usuario, created = Profile.objects.get_or_create(user=request.user)

        perfil_usuario.nombre = request.POST.get('nombre')
        perfil_usuario.apellido = request.POST.get('apellido')
        perfil_usuario.descripcion = request.POST.get('descripcion')
        perfil_usuario.nacionalidad = request.POST.get('nacionalidad')

        perfil_usuario.save()

        return redirect('about')

    else:
        perfil_usuario, created = Profile.objects.get_or_create(user=request.user)

        return render(request, 'inicio/about.html', {'perfil_usuario': perfil_usuario})