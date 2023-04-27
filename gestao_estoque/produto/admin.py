import csv
from datetime import datetime

import xlwt
from django.contrib import admin
from django.http import HttpResponse

from .models import Produto, Categoria

MDATA = datetime.now().strftime('%Y-%m-%d')
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
    actions = ('export_as_csv', 'export_as_xls',)

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

    def export_as_xls(self, request, queryset):
        meta = self.model._meta
        columns = ('Produto', 'NCM', 'Importado',
                  'Preco', 'Estoque', 'Estoque minimo', 'Categoria')

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}_{}.xls"'.format(meta, MDATA)

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(self.model.__name__)

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        default_style = xlwt.XFStyle()

        rows = queryset.values_list('produto', 'ncm', 'importado', 'preco', 'estoque', 'estoque_minimo', 'categoria__categoria')
        for row, rowdata in enumerate(rows):
            row_num += 1
            for col_num, col in enumerate(rowdata):
                ws.write(row_num, col_num, col, default_style)

        wb.save(response)
        return response

    export_as_xls.short_description = 'Exportar para XLS'


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
    )
    search_fields = ('categoria',)