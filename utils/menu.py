def exibir_menu():
    print("\n UnPED - Comandas")
    print("1- Abrir Comanda")
    print("2- Adicionar item a Comanda")
    print("3- Ver extrato")
    print("4- Fechar Comanda")
    print("5- Mostrar Cardapio")
    print("6- Cadastrar Produto")
    print("7- Listar comandas abertas")
    print("0- Sair")

    opcao = input("Escolha uma Opcao ")
    return opcao

def obter_inteiro(mensagem):
    while True:
        try:
            return(int(input(mensagem)))
        except ValueError:
            print("Digite um numero valido")
        
def obter_float(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Digite um numero valido")

def lancar_item(pedido, cardapio):

    while True:
        print("\n=== Cardapio ===")
        cardapio.listar_produtos()
        nome_prod = input("Digite o nome do produto que deseja: ")
        produto = cardapio.buscar_produto(nome_prod)

        if produto:
            qtd = obter_inteiro(f"Quantidade de {produto.nome}: ")
            
            if qtd <= 0:
                print("Quantidade deve ser maior que zero")

            else:
                pedido.adicionar_item(produto, qtd)
                print("Item adicionado")

        else:
            print("Produto nao encontrado")

        mais_itens = input("Deseja adicionar mais um item? s/n: ").strip().lower()

        if mais_itens != 's':
            break

                