# Generated by Django 4.1.7 on 2023-04-13 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstoqueEntrada',
            fields=[
            ],
            options={
                'verbose_name': 'estoque entrada',
                'verbose_name_plural': 'estoque entrada',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('estoque.estoque',),
        ),
        migrations.CreateModel(
            name='EstoqueSaida',
            fields=[
            ],
            options={
                'verbose_name': 'estoque saida',
                'verbose_name_plural': 'estoque saida',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('estoque.estoque',),
        ),
        migrations.AlterField(
            model_name='estoqueitem',
            name='estoque',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estoques', to='estoque.estoque'),
        ),
    ]
