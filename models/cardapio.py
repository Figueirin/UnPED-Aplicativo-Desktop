from models.produto import Produto

class Cardapio:
    """
    Gerencia a coleção de produtos à venda no bar/restaurante.
    """
    def __init__(self):
        # Inicializa a lista vazia de produtos cadastrados no sistema
        self.produtos = []

    def add_produto(self, produto):
        # Cadastra um novo produto no cardápio
        self.produtos.append(produto)
    
    def listar_produtos(self):
        # Exibe todos os produtos do cardápio um a um
        for produto in self.produtos:
            print(produto)

    def buscar_produto(self, nome_produto):
        # Busca um produto na lista pelo nome (case-insensitive) e retorna o objeto Produto
        for produto in self.produtos:
            if produto.nome.lower() == nome_produto.lower():
                return produto
    
        return None

