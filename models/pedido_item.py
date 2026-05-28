from models.produto import Produto

class PedidoItem:
    """
    Representa uma linha de consumo do pedido.
    Associa um objeto Produto a uma quantidade comprada.
    """
    def __init__(self, produto, qtd = 1):
        # Associação de Objetos: guardamos o objeto Produto completo
        self.produto = produto
        self.quantidade = qtd

    def calc_subtotal(self):
        # Delegação: o PedidoItem delega o preço ao produto e multiplica pela quantidade
        return self.produto.preco * self.quantidade

    def to_dict(self):
        # Serialização: converte a linha do pedido em dicionário para salvar no JSON
        return{
            "produto": self.produto.to_dict(),
            "quantidade": self.quantidade
        }

    def __str__(self):
        # Exibição bonita do item e seu subtotal (ex: 2 x Cafe (Subtotal: R$ 9.00))
        return f"{self.quantidade} x {self.produto.nome} (Subtotal: R$ {self.calc_subtotal():.2f})"
