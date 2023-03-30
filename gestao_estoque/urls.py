from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestao_estoque.core.urls')),
    path('produto/', include('gestao_estoque.produto.urls')),
]
