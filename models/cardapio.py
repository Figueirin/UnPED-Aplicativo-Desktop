from models.produto import Produto

class Cardapio:
    def __init__(self):
        self.produtos = []

    def add_produto(self, produto):
        self.produtos.append(produto)
    
    def listar_produtos(self):
        for produto in self.produtos:
            print(produto)

    def buscar_produto(self, nome_produto):
        for produto in self.produtos:
            if produto.nome.lower() == nome_produto.lower():
                return produto
    
        return None

