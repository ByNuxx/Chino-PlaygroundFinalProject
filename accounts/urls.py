from django.urls import path
from . import views
from .views import AboutView
from django.contrib.auth.views import LogoutView
from .views import ProfileView, ProfileEditView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about/', AboutView.as_view(), name='about'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)