import csv
import io

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.http import JsonResponse, HttpResponseRedirect

from .forms import ProdutoForm
from .models import Produto


class ProdutoList(ListView):
    model = Produto
    template_name = 'produto_list.html'
    paginate_by = 10


def produto_detail(request, pk):
    template_name = 'produto_detail.html'
    obj = Produto.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)


def produto_add(request):
    template_name = 'produto_form.html'
    return render(request, template_name)


class ProdutoCreate(CreateView):
    #Ok
    model = Produto
    template_name = 'produto_form.html'
    form_class = ProdutoForm


class ProdutoUpdate(UpdateView):
    model = Produto
    template_name = 'produto_form.html'
    form_class = ProdutoForm


def produto_json(request, pk):
    produto = Produto.objects.filter(pk=pk)
    data = [item.to_dict_json() for item in produto]
    return JsonResponse({'data': data})

def save_data(data):
    """
    Cria objetos Produto a partir dos dados lidos do arquivo CSV e salva esses objetos no banco de dados usando o método bulk_create do ORM do Django
    """
    produtos = []
    for item in data:
        # Extrai os valores das colunas do dicionário
        produto = item.get('produto')
        ncm = item.get('ncm')
        importado = True if item.get('importado') == 'True' else False
        preco = item.get('preco')
        estoque = item.get('estoque')
        estoque_minimo = item.get('estoque_minimo')
        # Cria um objeto Produto com os valores extraídos
        produto_obj = Produto(
            produto=produto,
            ncm=ncm,
            importado=importado,
            preco=preco,
            estoque=estoque,
            estoque_minimo=estoque_minimo
        )
        produtos.append(produto_obj)
    # Cria todos os objetos Produto de uma vez usando o método bulk_create do ORM do Django
    Produto.objects.bulk_create(produtos)

def import_csv(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        file = myfile.read().decode('latin-1')
        reader = csv.DictReader(io.StringIO(file))
        data = [row for row in reader]
        save_data(data)
        return HttpResponseRedirect(reverse('produto:produto_list'))
    template_name = 'produto_import.html'
    return render(request, template_name)
