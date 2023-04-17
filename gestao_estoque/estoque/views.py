from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.views.generic import ListView, DetailView

from gestao_estoque.produto.models import Produto

from .forms import EstoqueItemForm, EstoqueForm
from .models import Estoque, EstoqueItem, EstoqueSaida, EstoqueEntrada


class EstoqueEntradaList(ListView):
    model = EstoqueEntrada
    template_name = 'estoque_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Entrada'
        context['url_add'] = 'estoque:estoque_entrada_add'
        context['url_detail'] = 'estoque:estoque_entrada_detail'
        return context


class EstoqueDetail(DetailView):
    model = Estoque
    template_name = 'estoque_detail.html'


def dar_baixa_estoque(form):
    # Pega os produtos a partir da instância do formulário (Estoque)
    produtos = form.estoques.all()
    for item in produtos:
        produto = Produto.objects.get(pk=item.produto.pk)
        produto.estoque = item.saldo
        produto.save()
    print('Estoque atualizado com sucesso!')


def estoque_add(request, template_name, movimento, url):
    estoque_form = Estoque()
    item_estoque_formset = inlineformset_factory(
        Estoque,
        EstoqueItem,
        form=EstoqueItemForm,
        extra=0,
        min_num=1,
        validate_min=True,
    )
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque_form, prefix='main')
        formset = item_estoque_formset(request.POST, instance=estoque_form, prefix='estoque')
        if form.is_valid() and formset.is_valid():
            form = form.save()
            form.movimento = movimento
            form.save()
            formset.save()
            dar_baixa_estoque(form)
            return {'pk': form.pk}
    else:
        form = EstoqueForm(instance=estoque_form, prefix='main')
        formset = item_estoque_formset(instance=estoque_form, prefix='estoque')

    context = {'form': form, 'formset': formset}
    return context


def estoque_entrada_add(request):
    template_name = 'estoque_entrada_form.html'
    movimento = 'e'
    url = 'estoque:estoque_detail'
    context = estoque_add(request, template_name, movimento, url)
    if context.get('pk'):
        return HttpResponseRedirect(resolve_url(url, context.get('pk')))
    return render(request, template_name, context)


class EstoqueSaidaList(ListView):
    model = EstoqueSaida
    template_name = 'estoque_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Saida'
        context['url_add'] = 'estoque:estoque_saida_add'
        context['url_detail'] = 'estoque:estoque_saida_detail'
        return context


class EstoqueSaidaDetail(DetailView):
    model = EstoqueSaida
    template_name = 'estoque_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_list'] = 'estoque:estoque_saida_list'
        return context

def estoque_saida_add(request):
    template_name = 'estoque_saida_form.html'
    movimento = 's'
    url = 'estoque:estoque_detail'
    context = estoque_add(request, template_name, movimento, url)
    if context.get('pk'):
        return HttpResponseRedirect(resolve_url(url, context.get('pk')))
    return render(request, template_name, context)
