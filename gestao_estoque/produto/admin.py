import csv

from django.contrib import admin
from django.http import HttpResponse

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
    actions = ('export_as_csv',)

    class Media:
        js = (
            'https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.min.js',
            '/static/js/estoque_admin.js',
        )

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = 'Exportar para CSV'


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )
    search_fields = ('categoria',)