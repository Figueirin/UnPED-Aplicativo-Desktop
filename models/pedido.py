from models.cliente import Cliente
from models.pedido_item import PedidoItem

class Pedido:
    def __init__(self, num_comanda, cliente):
        self.cliente = cliente
        self.comanda = num_comanda
        self.itens = []

    def adicionar_item(self, produto, qtd = 1):
        for item in self.itens:
            if item.produto.nome.lower() == produto.nome.lower():
                item.quantidade += qtd
                return

        novo_item = PedidoItem(produto, qtd)
        self.itens.append(novo_item)
    
    def calcular_total(self):
        total = 0
        for item in self.itens:
            total += item.calc_subtotal()
        
        return total

    def to_dict(self):
        return {
            "Comanda": self.comanda,
            "Cliente": self.cliente.nome,
            "Items":[item.to_dict() for item in self.itens]
        }
    
    def __str__(self):
        extrato = f"comanda {self.comanda} | Cliente: {self.cliente.nome}\n"
        extrato += "=======================================\n"

        for item in self.itens:
            extrato += f"`{item}\n"
        
        extrato += "========================================\n"
        extrato += f"total: R$ {self.calcular_total():.2f}"
        return extrato



