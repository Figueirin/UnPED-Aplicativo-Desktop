from models.produto import Produto
from services.persistencia import salvar_cardapio, salvar_comandas

def exibir_menu():
    """
    Exibe o menu de opções do terminal CLI e captura a escolha do usuário.
    
    Retorna:
    - str: A opção selecionada pelo usuário.
    """
    print("\n UnPED - Comandas")
    print("1- Abrir Comanda")
    print("2- Adicionar item a Comanda")
    print("3- Ver extrato")
    print("4- Fechar Comanda")
    print("5- Mostrar Cardapio")
    print("6- Cadastrar Produto")
    print("7- Listar comandas abertas")
    print("0- Sair")

    opcao = input("Escolha uma Opcao: ")
    return opcao

def obter_inteiro(mensagem):
    """
    Função utilitária para capturar e validar entradas de números inteiros do usuário.
    Trata exceções do tipo ValueError para impedir falhas de execução no sistema.
    """
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Erro: Digite um número inteiro válido!")
        
def obter_float(mensagem):
    """
    Função utilitária para capturar e validar entradas de valores decimais (preços).
    Garante que o valor inserido seja conversível para float.
    """
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Erro: Digite um preço/número decimal válido!")

def lancar_item(comanda, cardapio):
    """
    Loop interativo que permite ao garçom adicionar vários itens seguidos à comanda,
    sem a necessidade de retornar ao menu principal do sistema a cada adição.
    """
    while True:
        print("\n=== Cardapio ===")
        cardapio.listar_produtos()
        
        # O garçom pode digitar o ID numérico ou o Nome do produto
        termo = input("Digite o nome ou ID do produto que deseja: ")
        produto = cardapio.buscar_produto(termo)

        if produto:
            qtd = obter_inteiro(f"Quantidade de {produto.nome}: ")
            if qtd <= 0:
                print("Erro: A quantidade deve ser maior que zero!")
            else:
                comanda.adicionar_item(produto, qtd)
                print(f"{qtd}x {produto.nome} adicionado(s) com sucesso!")
        else:
            print("Produto não encontrado no cardápio!")

        # Pergunta se o garçom deseja continuar na mesma rotina de lançamentos
        mais_itens = input("Deseja adicionar mais um item? s/n: ").strip().lower()
        if mais_itens != 's':
            break

def fluxo_abrir_comanda(service, cardapio):
    """
    Ação do menu: Inicia o fluxo para abertura de uma nova comanda.
    Permite também o lançamento imediato de itens caso o usuário deseje.
    """
    num = obter_inteiro("Numero da comanda: ")
    nome = input("Nome do cliente: ")

    if not nome.strip():
        print("O nome nao pode ser vazio")
    else:
        # Tenta abrir no gerenciador (que bloqueia números duplicados)
        sucesso = service.abrir_comanda(num, nome)

        if sucesso:
            # Salva o estado atualizado das comandas ativas no JSON
            salvar_comandas(service.comandas_ativas)
            deseja_pedido = input("Deseja fazer mais algum pedido? s/n: ").strip().lower()

            if deseja_pedido == 's':
                comanda = service.buscar_comanda(num)
                lancar_item(comanda, cardapio)
                salvar_comandas(service.comandas_ativas)

def fluxo_adicionar_item(service, cardapio):
    """
    Ação do menu: Localiza uma comanda ativa e lança um ou mais itens nela.
    """
    num = obter_inteiro("Numero da Comanda: ")
    comanda = service.buscar_comanda(num)

    if comanda:
        lancar_item(comanda, cardapio)
        salvar_comandas(service.comandas_ativas)
    else:
        print("Comanda nao encontrada")

def fluxo_ver_extrato(service, cardapio):
    """
    Ação do menu: Imprime o extrato de consumo atual de uma comanda na tela.
    A formatação de exibição é delegada para o método __str__ da classe Comanda.
    """
    num = obter_inteiro("Numero da comanda: ")
    comanda = service.buscar_comanda(num)

    if comanda:
        print("\n" + str(comanda))
    else:
        print("Comanda nao encontrada")

def fluxo_fechar_comanda(service, cardapio):
    """
    Ação do menu: Encerra o consumo de uma comanda e realiza a cobrança.
    Apresenta a taxa de serviço (10%) e gerencia um loop de pagamentos interativos
    até que o valor total seja quitado, devolvendo troco se necessário.
    """
    num = obter_inteiro("Numero da comanda para fechamento: ")
    # Pop da comanda na memória de ativos (remove do sistema)
    comanda = service.fechar_comanda(num)

    if not comanda:
        print("\n === Comanda nao encontrada! ===")
        return 

    # Cálculos financeiros da conta
    subtotal = comanda.calcular_total()
    taxa = subtotal * 0.10
    total_geral = subtotal + taxa

    # Exibição do extrato de fechamento formatado
    print(f"\n === Fechamento de comanda {comanda.numero} ===")
    print(f"Cliente: {comanda.cliente_nome}")
    print("========================================")
    for item in comanda.itens:
        print(item)
    print("========================================")
    print(f"Subtotal: R$ {subtotal:.2f}")
    print(f"Taxa de Servico (10%): R$ {taxa:.2f}")
    print("========================================")
    print(f"Total Geral: R$ {total_geral:.2f}")
    print("========================================")

    pago_acumulado = 0.0
    # Loop de pagamentos cumulativos (pode receber valores parciais de várias pessoas)
    while pago_acumulado < total_geral:
        falta = total_geral - pago_acumulado
        valor_pago = obter_float(f"Valor a pagar (Falta R$ {falta:.2f}): R$ ")

        if valor_pago <= 0:
            print("Erro: O valor de pagamento deve ser maior que zero")
            continue
        pago_acumulado += valor_pago
        print(f"Total pago ate agora: R$ {pago_acumulado:.2f}")

    # Atualiza o arquivo JSON em disco removendo a comanda quitada
    salvar_comandas(service.comandas_ativas)

    # Exibição dos resultados finais de encerramento
    troco = pago_acumulado - total_geral
    print("\n === Comanda Fechada com Sucesso ===")
    if troco > 0:
        print(f"Troco: R$ {troco:.2f}")
    print("Obrigado pela preferência e volte sempre!")

def fluxo_listar_cardapio(service, cardapio):
    """
    Ação do menu: Imprime o cardápio cadastrado por categorias.
    """
    print("\n === Cardapio ===")
    cardapio.listar_produtos()

def fluxo_cadastrar_produto(service, cardapio):
    """
    Ação do menu: Adiciona um novo produto ao catálogo do cardápio geral.
    Pergunta nome, preço e categoria, gerando o ID identificador de forma automática.
    """
    nome = input("Nome do produto a ser adicionado: ").strip()
    if not nome:
        print("O nome do produto nao pode ser vazio")
        return

    # Evita que o mesmo produto seja cadastrado com outro ID (duplicatas de nome)
    nome_low = nome.lower()
    for p in cardapio.produtos:
        if p.nome.lower() == nome_low:
            print(f"Erro: O produto '{p.nome}' já está cadastrado com o ID {p.id}!")
            return

    preco = obter_float("Preço: ")
    if preco <= 0:
        print("O valor do produto não pode ser =< 0")
        return

    categoria = input("Digite a categoria do produto: ").strip()
    if not categoria:
        categoria = "Geral"

    # Auto-geração do ID incrementado com base no maior ID cadastrado atual
    novo_id = max([p.id for p in cardapio.produtos], default=0) + 1
    
    # Cria o produto na memória e salva no JSON
    cardapio.add_produto(Produto(novo_id, nome, preco, categoria))
    salvar_cardapio(cardapio)

    print(f"'{nome}' cadastrado com ID {novo_id} na categoria '{categoria}'!")

def fluxo_listar_comandas_ativas(service, cardapio):
    """
    Ação do menu: Lista todas as comandas abertas no momento com seus respectivos subtotais.
    """
    service.listar_comandas_ativas()