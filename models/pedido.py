from models.cliente import Cliente
from models.pedido_item import PedidoItem

class Pedido:
    """
    Representa a comanda ativa no estabelecimento.
    Composição de Objetos: agrega um objeto Cliente e uma lista de objetos PedidoItem.
    """
    def __init__(self, num_comanda, cliente):
        self.cliente = cliente  # Associação: objeto do tipo Cliente
        self.comanda = num_comanda
        self.itens = []         # Composição: lista de objetos do tipo PedidoItem

    def adicionar_item(self, produto, qtd = 1):
        # Evita itens duplicados agrupando quantidades iguais
        for item in self.itens:
            if item.produto.nome.lower() == produto.nome.lower():
                item.quantidade += qtd
                return

        # Se for um item inédito na comanda, cria e adiciona
        novo_item = PedidoItem(produto, qtd)
        self.itens.append(novo_item)
    
    def calcular_total(self):
        # Soma o subtotal de todas as linhas de pedido
        total = 0
        for item in self.itens:
            total += item.calc_subtotal()
        
        return total

    def to_dict(self):
        # Converte a comanda para dicionário visando salvamento JSON
        return {
            "Comanda": self.comanda,
            "Cliente": self.cliente.nome,
            "Items":[item.to_dict() for item in self.itens]
        }
    
    def __str__(self):
        # Gera o extrato visual formatado da comanda
        extrato = f"comanda {self.comanda} | Cliente: {self.cliente.nome}\n"
        extrato += "=======================================\n"

        for item in self.itens:
            extrato += f"{item}\n" 
        
        extrato += "========================================\n"
        extrato += f"total: R$ {self.calcular_total():.2f}"
        return extrato

