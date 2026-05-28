from models.cliente import Cliente
from models.pedido import Pedido

class PedidoService:
    def __init__(self):
        self.pedidos_ativos = {}

    def abrir_comanda(self, num_comanda, nome_cliente):
        if num_comanda in self.pedidos_ativos:
            print(f"A comanda {num_comanda} ja esta aberta no nome {self.pedidos_ativos[num_comanda].cliente.nome}")

            return False

        else:
            cliente = Cliente(nome_cliente)
            novo_pedido = Pedido(num_comanda, cliente)
            self.pedidos_ativos[num_comanda] = novo_pedido
            print(f"Comanda {num_comanda} aberta para {nome_cliente}")

            return True

    def buscar_comandas(self, num_comanda):
        if num_comanda in self.pedidos_ativos:
            return self.pedidos_ativos[num_comanda]
    
        return None

    def fechar_comanda(self, num_comanda):
        if num_comanda in self.pedidos_ativos:
            return self.pedidos_ativos.pop(num_comanda)
        
        return None

    def listar_comandas_ativas(self):
        if not self.pedidos_ativos:
            print("Nenhuma comanda aberta no momento")
            return

        print("=== Comandas Abertas ===")
        for num_comanda, pedido in self.pedidos_ativos.items():
            print(f"Comanda num {num_comanda} | Cliente: {pedido.cliente.nome} | Total Atual R$ {pedido.calcular_total():.2f}")

