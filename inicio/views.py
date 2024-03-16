from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def crear_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.autor = request.user
            blog.save()
            return redirect('lista_blogs')
    else:
        form = BlogForm()
    return render(request, 'inicio/crear_blog.html', {'form': form})

def listar_blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'inicio/listar_blogs.html', {'blogs': blogs})

def ver_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    return render(request, 'inicio/ver_blog.html', {'blog': blog})

def eliminar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.autor == request.user:
        blog.delete()
        return redirect('lista_blogs')
    else:
        return render(request, 'error_permiso.html')

def inicio(request):
    return render(request, 'inicio/inicio.html')

def editar_perfil(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('inicio')  
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'accounts/editar_perfil.html', {'form': form})

def cambiar_contraseña(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('inicio')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/cambiar_contraseña.html', {'form': form})
