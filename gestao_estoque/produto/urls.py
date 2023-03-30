from django.urls import path
from gestao_estoque.produto import views as v


app_name = 'produto'

urlpatterns = [
    path('', v.produto_list, name='index'),
]
