import xlwt
from datetime import datetime
from django.http import HttpResponse

from gestao_estoque.produto.models import Produto

MDATA = datetime.now().strftime('%Y-%m-%d')

def export_xls(model, filename, queryset, columns):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    default_style = xlwt.XFStyle()

    rows = queryset
    for row, rowdata in enumerate(rows):
        row_num += 1
        for col_num, col in enumerate(rowdata):
            ws.write(row_num, col_num, col, default_style)

    wb.save(filename)
    return response


def exportar_produtos_xls():
    model = 'Produto'
    filename = 'produtos_exportados.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}-{MDATA}.{_filename[1]}'
    queryset = Produto.objects.all().values_list('produto', 'ncm', 'importado', 'preco', 'estoque', 'estoque_minimo')
    columns = ['Produto', 'NCM', 'Importado', 'Preço', 'Estoque', 'Estoque Mínimo']
    response = export_xls(model, filename_final, queryset, columns)
    return response

