from django import forms
from .models import Produto, Categoria


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
