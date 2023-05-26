import csv
import io
import os

from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from gestao_estoque.produto.actions.import_xls import import_xls as action_import_xls
from gestao_estoque.produto.actions.export_xls import exportar_produtos_xls as action_export_xls

from .forms import ProdutoForm, CategoriaForm
from .models import Produto, Categoria


class ProdutoList(ListView):
    model = Produto
    template_name = 'produto_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search')
        if search_term:
            queryset = queryset.filter(
                Q(produto__icontains=search_term)
            )
        return queryset


class CategoriaList(ListView):
    model = Categoria
    template_name = 'categoria_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('search')
        if search_term:
            queryset = queryset.filter(
                Q(categoria__icontains=search_term)
            )
        return queryset


def produto_detail(request, pk):
    template_name = 'produto_detail.html'
    obj = Produto.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)

def categoria_detail(request, pk):
    template_name = 'categoria_detail.html'
    obj = Categoria.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)

def produto_add(request):
    template_name = 'produto_form.html'
    return render(request, template_name)

class ProdutoCreate(CreateView):
    model = Produto
    template_name = 'produto_form.html'
    form_class = ProdutoForm

class CategoriaCreate(CreateView):
    model = Categoria
    template_name = 'categoria_form.html'
    form_class = CategoriaForm

class ProdutoUpdate(UpdateView):
    model = Produto
    template_name = 'produto_form.html'
    form_class = ProdutoForm

class CategoriaUpdate(UpdateView):
    model = Categoria
    template_name = 'Categoria_form.html'
    form_class = CategoriaForm

def produto_json(request, pk):
    produto = Produto.objects.filter(pk=pk)
    data = [item.to_dict_json() for item in produto]
    return JsonResponse({'data': data})

def save_data(data):
    """
    Cria objetos Produto a partir dos dados lidos do arquivo CSV e salva esses objetos no banco de dados usando o método bulk_create do ORM do Django
    """
    produtos = []
    categorias = []

    for item in data:
        categoria = item.get('categoria')

        if categoria:
            if categoria not in categorias:
                categorias.append(categoria)

    for categoria in categorias:
        categoria_obj = Categoria(categoria=categoria)
        categoria_obj.save()


    for item in data:
        # Extrai os valores das colunas do dicionário
        produto = item.get('produto')
        ncm = item.get('ncm')
        importado = True if item.get('importado') == 'True' else False
        preco = item.get('preco')
        estoque = item.get('estoque')
        estoque_minimo = item.get('estoque_minimo')
        _categoria = item.get('categoria')
        categoria = Categoria.objects.filter(categoria=_categoria).first()

        # Cria um objeto Produto com os valores extraídos
        produto_obj = Produto(
            produto=produto,
            ncm=ncm,
            importado=importado,
            preco=preco,
            estoque=estoque,
            estoque_minimo=estoque_minimo,
            categoria=categoria
        )
        produtos.append(produto_obj)

    # Cria todos os objetos Produto de uma vez usando o método bulk_create do ORM do Django
    Produto.objects.bulk_create(produtos)

def import_csv(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        data = [row for row in reader]
        save_data(data)
        return HttpResponseRedirect(reverse('produto:produto_list'))
    template_name = 'produto_import.html'
    return render(request, template_name)

def export_csv(request):
    header = ['produto', 'ncm', 'importado', 'preco', 'estoque', 'estoque_minimo']
    produtos = Produto.objects.all().values_list(*header)
    with open('fix/produtos_exportados.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(produtos)

    caminho_do_arquivo = os.path.join(settings.BASE_DIR, 'fix', 'produtos_exportados.csv')
    if os.path.exists(caminho_do_arquivo):
        messages.success(request, 'Produtos exportados com sucesso!')
        with open(caminho_do_arquivo, 'rb') as arquivo:
            response = HttpResponse(arquivo.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=produtos_exportados.csv'
            return response
    else:
        messages.error(request, 'Não foi possível exportar os produtos!')
        return HttpResponseRedirect(reverse('produto:produto_list'))

def import_xls(request):
    filename = 'fix/produtos.xls'
    action_import_xls(filename)
    messages.success(request, 'Produtos importados com sucesso!')
    return HttpResponseRedirect(reverse('produto:produto_list'))

def export_xls(request):
    action_export_xls()
    messages.success(request, 'Produtos exportados com sucesso!')
    return HttpResponseRedirect(reverse('produto:produto_list'))