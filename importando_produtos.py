import csv
from gestao_estoque.produto.models import Produto


class CsvToProduto:
    def __init__(self, filename):
        self.filename = filename

    def csv_to_list(self):
        """
        Lê o arquivo CSV e retorna uma lista de dicionários, onde cada dicionário representa uma linha do arquivo CSV
        """
        with open(self.filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            data = [row for row in reader]
        return data

    def save_data(self, data):
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

    def process(self):
        """
        Lê o arquivo CSV e cria objetos Produto a partir dos dados lidos, salvando-os no banco de dados
        """
        data = self.csv_to_list()
        self.save_data(data)

csv_to_produto = CsvToProduto('fix/produtos.csv')
csv_to_produto.process()

