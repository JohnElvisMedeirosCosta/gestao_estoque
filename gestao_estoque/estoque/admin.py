from django.contrib import admin
from .models import Estoque, EstoqueItem


class EstoqueItemInline(admin.TabularInline):
    model = EstoqueItem
    extra = 0


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'nf',
    )
    search_fields = ('nf',)
    list_filter = ('funcionario',)
    date_hierarchy = 'created'
    inlines = (EstoqueItemInline,)
