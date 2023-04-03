from django import forms
from .models import Estoque, EstoqueItem


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = '__all__'


class EstoqueItemForm(forms.ModelForm):
    class Meta:
        model = EstoqueItem
        fields = '__all__'
