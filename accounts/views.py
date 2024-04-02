from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import logout_then_login
from .forms import SignUpForm
from .forms import ProfileForm
from django.urls import reverse_lazy
from .models import Profile
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
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

class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'inicio/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        context['profile'] = profile
        context['profile_image_url'] = profile.foto_perfil.url if profile.foto_perfil else None
        return context

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return self.render_to_response({'profile': profile})
        else:
            return self.render_to_response({'form': form, 'user': request.user})
        
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'inicio/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        context['profile'] = profile
        context['profile_image_url'] = profile.image.url if profile.image else None
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('about')

    def get_object(self, queryset=None):
        return self.request.user.profile