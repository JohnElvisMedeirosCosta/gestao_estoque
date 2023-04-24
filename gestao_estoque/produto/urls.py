from django.urls import path
from gestao_estoque.produto import views as v


app_name = 'produto'

urlpatterns = [
    path('', v.ProdutoList.as_view(), name='produto_list'),
    path('categoria/', v.CategoriaList.as_view(), name='categoria_list'),
    path('<int:pk>/', v.produto_detail, name='produto_detail'),
    path('categoria/<int:pk>/', v.categoria_detail, name='categoria_detail'),
    path('add/', v.ProdutoCreate.as_view(), name='produto_add'),
    path('add/categoria/', v.CategoriaCreate.as_view(), name='categoria_add'),
    path('<int:pk>/update/', v.ProdutoUpdate.as_view(), name='produto_edit'),
    path('categoria/<int:pk>/update/', v.CategoriaUpdate.as_view(), name='categoria_edit'),
    path('<int:pk>/json/', v.produto_json, name='produto_json'),
    path('import/csv/', v.import_csv, name='import_csv'),
    path('export/csv/', v.export_csv, name='export_csv'),
    path('import/xls/', v.import_xls, name='import_xls'),
    path('export/xls/', v.export_xls, name='export_xls'),
]
