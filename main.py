from models.cardapio import Cardapio
from models.produto import Produto
from services.pedido_service import PedidoService
from utils.menu import exibir_menu, obter_float, obter_inteiro, lancar_item

def main():
    # Instanciamos os gerenciadores globais (Serviços e Cardápio da loja)
    service = PedidoService()
    cardapio = Cardapio()

    # Carga inicial do Cardápio (produtos de demonstração)
    cardapio.add_produto(Produto("Cafe", 4.50))
    cardapio.add_produto(Produto("Pao de Queijo", 6.00))
    cardapio.add_produto(Produto("Coca-Cola", 5.50))
    cardapio.add_produto(Produto("Suco de Laranja", 7.00))
    cardapio.add_produto(Produto("Salgado Assado", 8.50))
    cardapio.add_produto(Produto("Bolo de Cenoura", 6.50))
    cardapio.add_produto(Produto("Torta de Frango", 9.00))
    cardapio.add_produto(Produto("Agua Mineral", 3.00))
    
    # Loop Principal do Sistema
    while True:
        opcao = exibir_menu()

        if opcao == "1":
            # Abertura de nova comanda
            num = obter_inteiro("Numero da Comanda: ")
            nome = input("Nome do cliente: ")

            if not nome.strip():
                print("Erro... O nome do cliente nao pode ser vazio")

            else:
                sucesso = service.abrir_comanda(num, nome)

                # Se abrir com sucesso, oferece o lançamento imediato de itens
                if sucesso:
                    deseja_pedido = input("Deseja fazer um pedido? s/n: ").strip().lower()

                    if deseja_pedido == "s":
                        pedido = service.buscar_comandas(num)
                        lancar_item(pedido, cardapio)
        
        elif opcao == "2":
            # Adiciona item a uma comanda já existente
            num = obter_inteiro("Numero da comanda: ")
            pedido = service.buscar_comandas(num)

            if pedido:
                lancar_item(pedido, cardapio)
            else:
                print("Comanda não encontrada!")

        elif opcao == "3":
            # Visualização do extrato de consumo atual de uma comanda
            num = obter_inteiro("Numero da comanda: ")
            pedido = service.buscar_comandas(num)

            if pedido:
                print("\n" + str(pedido)) # O str(pedido) chama automaticamente o método __str__ da classe Pedido
            else:
                print("Comanda nao encontrada")

        elif opcao == '4':
            # Pagamento e encerramento (fechamento) de comanda
            num = obter_inteiro("Numero da comanda para fechar: ")
            pedido = service.fechar_comanda(num)

            if pedido:
                print("\n === Comanda Fechada com sucesso ===")
                print(pedido)
            else:
                print("Comanda não encontrada!")

        elif opcao == '5':
            # Exibição do Cardápio completo cadastrado na memória
            print("\n === Cardapio ===")
            cardapio.listar_produtos()

        elif opcao == '6':
            # Cadastro de novo produto no Cardápio Geral do estabelecimento
            nome = input("Nome do novo produto: ")

            if not nome.strip():
                print("O nome do produto nao pode ser vazio")

            else:
                preco = obter_float("Preço: ")

                if preco <= 0:
                    print("O valor do produto nao pode ser =< 0")
                else:
                    cardapio.add_produto(Produto(nome, preco))
                    print(f"Produto {nome} cadastrado com sucesso")

        elif opcao == '7':
            # Listagem resumida de todas as comandas abertas com valor corrente
            service.listar_comandas_ativas()

        elif opcao == '0':
            print("Encerrado sistema...")
            break

        else:
            print("Opção inválida, tente novamente")

if __name__ == "__main__":
    main()