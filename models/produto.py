class Produto:
    """
    Representa um item individual disponível no cardápio do estabelecimento.
    Esta classe encapsula as propriedades básicas de um produto (ID, nome, preço e categoria).
    """
    def __init__(self, id_produto, nome_produto, preco, categoria):
        """
        Construtor da classe Produto.
        
        Parâmetros:
        - id_produto (int): Identificador numérico único do produto.
        - nome_produto (str): Nome de exibição do produto.
        - preco (float): Preço de venda unitário do produto.
        - categoria (str): Categoria à qual o produto pertence (ex: Bebidas, Salgados, etc.).
        """
        self.id = id_produto
        self.nome = nome_produto
        self.preco = preco
        self.categoria = categoria

    def to_dict(self):
        """
        Converte o objeto do tipo Produto em um dicionário Python.
        Útil para o processo de serialização e persistência de dados em arquivos JSON.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "categoria": self.categoria
        }
    
    def __str__(self):
        """
        Retorna a representação textual formatada do produto.
        """
        return f"[{self.id}] | {self.nome} | R${self.preco:.2f}"