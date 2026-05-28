def exibir_menu():
    # Desenha o menu do bar no console e captura a escolha
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
    # Tratamento de erro: repete a pergunta se o usuário digitar algo que não seja um número inteiro
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Erro: Digite um número inteiro válido!")
        
def obter_float(mensagem):
    # Tratamento de erro: garante a digitação correta de preços decimais (float)
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Erro: Digite um preço/número decimal válido!")

def lancar_item(pedido, cardapio):
    # Loop interativo para lançar vários itens à comanda de uma única vez sem voltar ao menu
    while True:
        print("\n=== Cardapio ===")
        cardapio.listar_produtos()
        nome_prod = input("Digite o nome do produto que deseja: ")
        produto = cardapio.buscar_produto(nome_prod)

        if produto:
            qtd = obter_inteiro(f"Quantidade de {produto.nome}: ")
            
            if qtd <= 0:
                print("Erro: A quantidade deve ser maior que zero!")

            else:
                pedido.adicionar_item(produto, qtd)
                print(f"{qtd}x {produto.nome} adicionado(s) com sucesso!")

        else:
            print("Produto não encontrado no cardápio!")

        # Pergunta se quer continuar na mesma rotina de lançamento
        mais_itens = input("Deseja adicionar mais um item? s/n: ").strip().lower()

        if mais_itens != 's':
            break  # Sai da rotina e retorna ao menu principal do main.py

                