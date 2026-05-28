class Produto:
    """
    Representa um item do cardápio (Café, Pão de Queijo, etc.).
    Guarda as informações gerais do produto (nome e preço de venda).
    """
    def __init__(self, nome_produto, preco):
        self.nome = nome_produto
        self.preco = preco

    def to_dict(self):
        # Converte o objeto para um dicionário simples (usado para salvar em JSON mais tarde)
        return {
            "nome": self.nome,
            "preco": self.preco
        }
    
    def __str__(self):
        # Mostra o produto formatado com duas casas decimais no preço (ex: Café R$4.50)
        return f"{self.nome} R${self.preco:.2f}"

    