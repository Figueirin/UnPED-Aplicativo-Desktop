from models.produto import Produto

class ItemComanda:
    """
    Representa uma linha de consumo da comanda.
    Associa um objeto Produto a uma quantidade comprada.
    """
    def __init__(self, produto, qtd=1):
        self.produto = produto
        self.quantidade = qtd

    def calc_subtotal(self):
        # Delegação: o ItemComanda delega o preço ao produto e multiplica pela quantidade
        return self.produto.preco * self.quantidade

    def to_dict(self):
        # Serialização: converte a linha em dicionário para salvar no JSON
        return {
            "produto": self.produto.to_dict(),
            "quantidade": self.quantidade
        }

    def __str__(self):
        # Exibição bonita do item e seu subtotal (ex: 2 x Cafe (Subtotal: R$ 9.00))
        return f"{self.quantidade} x {self.produto.nome} (Subtotal: R$ {self.calc_subtotal():.2f})"
