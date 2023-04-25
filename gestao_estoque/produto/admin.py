from django.contrib import admin
from .models import Produto, Categoria


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'importado',
        'ncm',
        'preco',
        'estoque',
        'estoque_minimo',
    )
    search_fields = ('produto',)
    list_filter = ('importado',)

    class Media:
        js = (
            'https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.min.js',
            '/static/js/estoque_admin.js',
        )


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )
    search_fields = ('categoria',)