from models.cardapio import Cardapio
from models.produto import Produto
from services.pedido_service import PedidoService
from utils.menu import exibir_menu, obter_float, obter_inteiro, lancar_item

def main():
    service = PedidoService()
    cardapio = Cardapio()

    cardapio.add_produto(Produto("Cafe", 4.50))
    cardapio.add_produto(Produto("Pao de Queijo", 6.00))
    cardapio.add_produto(Produto("Coca-Cola", 5.50))
    cardapio.add_produto(Produto("Suco de Laranja", 7.00))
    cardapio.add_produto(Produto("Salgado Assado", 8.50))
    cardapio.add_produto(Produto("Bolo de Cenoura", 6.50))
    cardapio.add_produto(Produto("Torta de Frango", 9.00))
    cardapio.add_produto(Produto("Agua Mineral", 3.00))
    
    while True:
        opcao = exibir_menu()

        if opcao == "1":
            num = obter_inteiro("Numero da Comanda:")
            nome = input("Nome do cliente: ")

            if not nome.strip():
                print("Erro... O nome do cliente nao pode ser vazio")

            else:
                sucesso = service.abrir_comanda(num, nome)

                if sucesso:
                    deseja_pedido = input("Deseja fazer um pedido? s/n").strip().lower()

                    if deseja_pedido == "s":

                        pedido = service.buscar_comandas(num)
                        lancar_item(pedido, cardapio)
        
        elif opcao == "2":
            num = obter_inteiro("Numero da comanda: ")
            pedido = service.buscar_comandas(num)

            if pedido:
                lancar_item(pedido, cardapio)
            else:
                print("Comanda não encontrada!")

        elif opcao == "3":
            num = obter_inteiro("Numero da comanda: ")
            pedido = service.buscar_comandas(num)

            if pedido:
                print("\n" + str(pedido))

            else:
                print("Comanda nao encontrada")

        elif opcao == '4':
            num = obter_inteiro("Numero da comanda para fechar: ")
            pedido = service.fechar_comanda(num)

            if pedido:
                print("\n === Comanda Fechada com sucesso ===")
                print(pedido)

            else:
                print("Comanda não encontrada!")

        elif opcao == '5':
            print("\n === Cardapio ===")
            cardapio.listar_produtos()

        elif opcao == '6':
            nome = input("Nome do novo produto: ")

            if not nome.strip():
                print("O nome do produto nao pode ser vazio")

            else:
                preco = obter_float("Preço: ")

                if preco <= 0:
                    print("O valor do produto nao pode ser =< 0");

                else:
                    cardapio.add_produto(Produto(nome, preco))
                    print(f"Produto {nome} cadastrado com sucesso")

        elif opcao == '0':
            print("Encerrado sistema...")
            break

        else:
            print("Opção inválida, tente novamente")

if __name__ == "__main__":
    main()