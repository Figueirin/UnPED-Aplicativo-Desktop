class Produto:
    def __init__(self, nome_produto, preco):
        self.nome = nome_produto
        self.preco = preco

    def to_dict(self):
        return {

            "nome": self.nome,
            "preco": self.preco
        }
    
    def __str__(self):
        return (f"{self.nome} R${self.preco:.2f}")

    