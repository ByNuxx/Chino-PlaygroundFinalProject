from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class CrearBlogView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'inicio/crear_blog.html'
    success_url = reverse_lazy('lista_blogs')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

def listar_blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'inicio/listar_blogs.html', {'blogs': blogs})

def ver_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    return render(request, 'inicio/ver_blog.html', {'blog': blog})

def editar_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('ver_blog', blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'inicio/editar_blog.html', {'form': form})

def eliminar_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.autor == request.user:
        blog.delete()
        return redirect('lista_blogs')
    else:
        return render(request, 'error_permiso.html')

def inicio(request):
    return render(request, 'inicio/inicio.html')



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
