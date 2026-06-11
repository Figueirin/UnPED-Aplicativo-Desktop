class Usuario:

    """
    Classe pai de todo o sistema de usuario
    """
    def __init__ (self, username, senha, nome, cargo):
        self.username = username
        self.senha = senha
        self.nome = nome
        self.cargo = cargo

    def to_dict(self):
        
        return{
            "username": self.username,
            "senha": self.senha,
            "nome": self.nome,
            "cargo": self.cargo
        }

class Garcom(Usuario):
    """
    classe filha de Usuario - Ja define o colaborador como Garçom
    """

    def __init__(self, username, senha, nome):

        super().__init__(username, senha, nome, "Garcom")
        
class Gerente(Usuario):
    """
    classe filha de Usuario - Ja define o colaborador como Gerente
    """
    def __init__(self, username, senha, nome):

        super().__init__(username, senha, nome, "Gerente")