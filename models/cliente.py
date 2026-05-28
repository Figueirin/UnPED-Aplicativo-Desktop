class Cliente:
    def __init__(self,  nome):
        self.nome = nome

    def __str__(self):
        return (f"O nome do cliente eh {self.nome}")