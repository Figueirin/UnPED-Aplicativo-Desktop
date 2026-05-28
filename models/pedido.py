from models.cliente import Cliente
from models.pedido_item import PedidoItem

class Pedido:
    """
    Representa a comanda ativa de consumo de um cliente específico no estabelecimento.
    Esta classe demonstra os conceitos de Associação (com Cliente) e Composição (com PedidoItem).
    """
    def __init__(self, num_comanda, cliente):
        """
        Construtor da classe Pedido.
        
        Parâmetros:
        - num_comanda (int): Número identificador único da comanda física.
        - cliente (Cliente): Objeto do tipo Cliente associado a esta comanda.
        """
        self.cliente = cliente  # Associação de classes
        self.comanda = num_comanda
        self.itens = []         # Composição: Lista contendo objetos da classe PedidoItem

    def adicionar_item(self, produto, qtd=1):
        """
        Adiciona itens à comanda ativa.
        Se o produto já constar na comanda, apenas atualiza a quantidade para evitar linhas duplicadas.
        
        Parâmetros:
        - produto (Produto): O objeto Produto selecionado.
        - qtd (int): Quantidade a ser adicionada.
        """
        # Varre a lista de itens atuais para buscar duplicatas
        for item in self.itens:
            if item.produto.nome.lower() == produto.nome.lower():
                item.quantidade += qtd
                return

        # Se for um item inédito nesta comanda, instancia um novo PedidoItem
        novo_item = PedidoItem(produto, qtd)
        self.itens.append(novo_item)
    
    def calcular_total(self):
        """
        Calcula o subtotal acumulado de consumo somando os subtotais de todas as linhas de itens.
        
        Retorna:
        - float: O valor acumulado dos itens consumidos (sem taxa de serviço).
        """
        total = 0
        for item in self.itens:
            total += item.calc_subtotal()
        return total

    def to_dict(self):
        """
        Converte a comanda e sua lista de itens em um dicionário estruturado.
        Utilizado pela camada de persistência para salvar os pedidos em arquivos JSON.
        """
        return {
            "Comanda": self.comanda,
            "Cliente": self.cliente.nome,
            "Items": [item.to_dict() for item in self.itens]
        }
    
    def __str__(self):
        """
        Gera a representação visual formatada (extrato de consumo parcial ou final) da comanda.
        Inclui o cálculo da taxa de serviço opcional (10%) e o total geral.
        """
        subtotal = self.calcular_total()
        taxa = subtotal * 0.10
        total_geral = subtotal + taxa
        
        extrato = f"Comanda {self.comanda} | Cliente: {self.cliente.nome}\n"
        extrato += "=====================================\n"

        # Adiciona a linha de detalhamento de cada item consumido
        for item in self.itens:
            extrato += f"{item}\n"

        extrato += f"Subtotal: R$ {subtotal:.2f}\n"
        extrato += f"Taxa de Servico (10%): R$ {taxa:.2f}\n"
        extrato += "=====================================\n"
        extrato += f"Total: R$ {total_geral:.2f}"

        return extrato
