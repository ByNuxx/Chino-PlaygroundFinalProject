from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CrearBlogView

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('crear/', CrearBlogView.as_view(), name='crear_blog'),
    path('listar/', views.listar_blogs, name='lista_blogs'),
    path('eliminar_blog/<int:blog_id>/', views.eliminar_blog, name='eliminar_blog'),
    path('<int:blog_id>/', views.ver_blog, name='ver_blog'),
    path('editar_blog/<int:blog_id>/', views.editar_blog, name='editar_blog'),
    path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)