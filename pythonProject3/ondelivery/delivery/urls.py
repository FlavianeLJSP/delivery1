from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('adicionar_ao_carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('login/', views.login_cliente, name='login_cliente'),  # Página de login
    path('registro/', views.registrar_cliente, name='registro_cliente'),  # Página de registro
    path('finalizar_pedido/', views.finalizar_pedido, name='finalizar_pedido'),  # URL para a finalização do pedido

]

# Serve arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
