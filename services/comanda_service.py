from models.comanda import Comanda

class ComandaService:
    """
    Camada de Serviço (Service Layer) / Controlador.
    Gerencia a lógica de negócios e o estado de todas as comandas abertas na memória RAM.
    """
    def __init__(self):
        # Dicionário de comandas ativas: { numero_comanda: objeto_comanda }
        self.comandas_ativas = {}

    def abrir_comanda(self, numero, cliente_nome):
        # Bloqueio de duplicados: se a comanda já estiver aberta, cancela a operação
        if numero in self.comandas_ativas:
            print(f"A comanda N.º {numero} | Está aberta no nome {self.comandas_ativas[numero].cliente_nome}")
            return False

        # Instancia a comanda e insere no dicionário
        nova_comanda = Comanda(numero, cliente_nome)
        self.comandas_ativas[numero] = nova_comanda
        print(f"Comanda: {numero} | Nome: {cliente_nome}")
        return True

    def buscar_comanda(self, numero):
        # Busca direta no dicionário por chave (Busca O(1) ultra-rápida, sem loops!)
        if numero in self.comandas_ativas:
            return self.comandas_ativas[numero]
        return None

    def fechar_comanda(self, numero):
        # Remove a comanda ativa pelo número (chave) e retorna o objeto fechado
        if numero in self.comandas_ativas:
            return self.comandas_ativas.pop(numero)
        return None

    def listar_comandas_ativas(self):
        # Lista detalhada de todas as comandas abertas com seus respectivos totais parciais
        if not self.comandas_ativas:
            print("Nenhuma comanda aberta no momento")
            return

        print("=== Comandas Abertas ===")
        for numero, comanda in self.comandas_ativas.items():
            print(f"Comanda Nº {numero} | Cliente: {comanda.cliente_nome} | Total Atual R$ {comanda.calcular_total():.2f}")
