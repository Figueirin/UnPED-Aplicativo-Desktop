from models.produto import Produto

class PedidoItem:
    def __init__(self, produto, qtd = 1):
        self.produto = produto
        self.quantidade = qtd

    def calc_subtotal(self):
        return self.produto.preco * self.quantidade

    def to_dict(self):
        return{
            "produto": self.produto.to_dict(),
            "quantidade": self.quantidade
        }

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome} (Subtotal: R$ {self.calc_subtotal():.2f})"


