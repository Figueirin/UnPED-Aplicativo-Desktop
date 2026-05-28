class Cliente:
    """
    Representa o cliente (consumidor) no sistema.
    Responsável apenas por armazenar informações da pessoa física.
    """
    def __init__(self, nome):
        # Define o nome do cliente (atributo público)
        self.nome = nome

    def __str__(self):
        # Representação em string do objeto Cliente (usado no print(cliente))
        return f"O nome do cliente eh {self.nome}"