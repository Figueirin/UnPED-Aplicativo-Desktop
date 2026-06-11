from models.item_comanda import ItemComanda

class Comanda:
    """
    Representa a comanda ativa de consumo de um cliente no estabelecimento.
    Demonstra o conceito de Composição (com ItemComanda).
    """
    def __init__(self, numero, cliente_nome):
        self.numero = numero
        self.cliente_nome = cliente_nome  # Agora guardamos apenas o nome como string direta!
        self.itens = []                   # Composição: Lista contendo objetos da classe ItemComanda

    def adicionar_item(self, produto, qtd=1):
        """
        Adiciona itens à comanda ativa.
        Se o produto já constar na comanda, apenas atualiza a quantidade para evitar linhas duplicadas.
        """
        # Varre a lista de itens atuais para buscar duplicatas
        for item in self.itens:
            if item.produto.nome.lower() == produto.nome.lower():
                item.quantidade += qtd
                return

        # Se for um item inédito, instancia um novo ItemComanda
        novo_item = ItemComanda(produto, qtd)
        self.itens.append(novo_item)
    
    def calcular_total(self):
        """
        Calcula o subtotal acumulado de consumo somando os subtotais de todas as linhas de itens.
        """
        total = 0
        for item in self.itens:
            total += item.calc_subtotal()
        return total

    def to_dict(self):
        """
        Converte a comanda e sua lista de itens em um dicionário estruturado.
        Utilizado pela camada de persistência para salvar os dados em arquivos JSON.
        """
        return {
            "Comanda": self.numero,
            "Cliente": self.cliente_nome,
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
        
        extrato = f"Comanda {self.numero} | Cliente: {self.cliente_nome}\n"
        extrato += "=====================================\n"

        # Adiciona a linha de detalhamento de cada item consumido
        for item in self.itens:
            extrato += f"{item}\n"

        extrato += f"Subtotal: R$ {subtotal:.2f}\n"
        extrato += f"Taxa de Servico (10%): R$ {taxa:.2f}\n"
        extrato += "=====================================\n"
        extrato += f"Total: R$ {total_geral:.2f}"

        return extrato
