from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestao_estoque.core.urls')),
    path('produto/', include('gestao_estoque.produto.urls')),
    path('estoque/', include('gestao_estoque.estoque.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
]
