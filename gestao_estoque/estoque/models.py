from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from gestao_estoque.core.models import TimeStampedModel
from gestao_estoque.produto.models import Produto
from gestao_estoque.estoque.managers import EstoqueSaidaManager, EstoqueEntradaManager

MOVIMENTO = (
    ('e', 'Entrada'),
    ('s', 'Saída'),
)


class Estoque(TimeStampedModel):
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
    nf = models.PositiveIntegerField('nota fiscal', null=True, blank=True)
    movimento = models.CharField(max_length=1, choices=MOVIMENTO)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.nf, self.created.strftime('%d-%m-%Y'))

    def get_absolute_url(self):
        return reverse_lazy('estoque:estoque_entrada_detail', kwargs={'pk': self.pk})

    def nf_formated(self):
        return str(self.nf).zfill(6)


class EstoqueEntrada(Estoque):
    objects = EstoqueEntradaManager()
    class Meta:
        proxy = True
        verbose_name = 'estoque entrada'
        verbose_name_plural = 'estoque entrada'


class EstoqueSaida(Estoque):
    objects = EstoqueSaidaManager()
    class Meta:
        proxy = True
        verbose_name = 'estoque saida'
        verbose_name_plural = 'estoque saida'


class EstoqueItem(models.Model):
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='estoques')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    saldo = models.PositiveIntegerField()

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return f'{self.pk} - {self.estoque.pk} - {self.produto}'
