from django.contrib import admin
from .models import Estoque, EstoqueItem, EstoqueEntrada, EstoqueSaida


class EstoqueItemInline(admin.TabularInline):
    model = EstoqueItem
    extra = 0


@admin.register(EstoqueEntrada)
class EstoqueEntradaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'nf', 'funcionario',)
    search_fields = ('nf',)
    list_filter = ('funcionario',)
    date_hierarchy = 'created'
    inlines = (EstoqueItemInline,)


@admin.register(EstoqueSaida)
class EstoqueSaidaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'nf', 'funcionario',)
    search_fields = ('nf',)
    list_filter = ('funcionario',)
    date_hierarchy = 'created'
    inlines = (EstoqueItemInline,)
