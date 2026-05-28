from models.cliente import Cliente
from models.pedido import Pedido

class PedidoService:
    """
    Camada de Serviço (Service Layer) / Controlador.
    Gerencia a lógica de negócios e o estado de todas as comandas abertas na memória.
    """
    def __init__(self):
        # Dicionário de comandas ativas: { num_comanda: objeto_pedido }
        self.pedidos_ativos = {}

    def abrir_comanda(self, num_comanda, nome_cliente):
        # Bloqueio de duplicados: se a comanda já estiver aberta, cancela a operação
        if num_comanda in self.pedidos_ativos:
            print(f"A comanda N.º {num_comanda} | Esta aberta no nome {self.pedidos_ativos[num_comanda].cliente.nome}")
            return False

        else:
            # Caso contrário, instancia o cliente, o pedido e insere no dicionário
            cliente = Cliente(nome_cliente)
            novo_pedido = Pedido(num_comanda, cliente)
            self.pedidos_ativos[num_comanda] = novo_pedido
            print(f"Comanda: {num_comanda} | Nome: {nome_cliente}")
            return True

    def buscar_comandas(self, num_comanda):
        # Busca direta no dicionário por chave (Busca O(1) ultra-rápida, sem loops!)
        if num_comanda in self.pedidos_ativos:
            return self.pedidos_ativos[num_comanda]
    
        return None

    def fechar_comanda(self, num_comanda):
        # Remove a comanda ativa pelo número (chave) e retorna o pedido fechado
        if num_comanda in self.pedidos_ativos:
            return self.pedidos_ativos.pop(num_comanda)
        
        return None

    def listar_comandas_ativas(self):
        # Lista detalhada de todas as comandas abertas com seus respectivos totais parciais
        if not self.pedidos_ativos:
            print("Nenhuma comanda aberta no momento")
            return

        print("=== Comandas Abertas ===")
        for num_comanda, pedido in self.pedidos_ativos.items():
            print(f"Comanda Nº {num_comanda} | Cliente: {pedido.cliente.nome} | Total Atual R$ {pedido.calcular_total():.2f}")

