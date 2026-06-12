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
        # Validação do ID
        try:
            id_val = int(id_produto)
            if id_val <= 0:
                raise ValueError("O ID do produto deve ser maior que zero.")
        except (TypeError, ValueError) as e:
            raise ValueError(f"ID inválido para o produto: {id_produto}") from e

        # Validação do Nome
        if not isinstance(nome_produto, str) or not nome_produto.strip():
            raise ValueError("O nome do produto não pode ser vazio ou conter apenas espaços.")

        # Validação do Preço
        try:
            preco_val = float(preco)
            if preco_val <= 0:
                raise ValueError("O preço do produto deve ser maior que zero.")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Preço inválido para o produto: {preco}") from e

        # Validação da Categoria
        if not isinstance(categoria, str) or not categoria.strip():
            raise ValueError("A categoria do produto não pode ser vazia ou conter apenas espaços.")

        self.id = id_val
        self.nome = nome_produto.strip()
        self.preco = preco_val
        self.categoria = categoria.strip()

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