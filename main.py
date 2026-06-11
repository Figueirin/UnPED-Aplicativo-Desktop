from models.cardapio import Cardapio
from services.comanda_service import ComandaService
from utils.menu import exibir_menu
from services.persistencia import carregar_cardapio, carregar_comandas
from utils.menu import (fluxo_listar_comandas_ativas, fluxo_cadastrar_produto, fluxo_listar_cardapio, fluxo_fechar_comanda, fluxo_ver_extrato, fluxo_adicionar_item, fluxo_abrir_comanda)

def main():
    """
    Função principal de inicialização do sistema UnPED.
    Responsável por instanciar os controladores, carregar os dados persistidos em disco (JSON)
    e gerenciar a execução do loop principal através do dicionário de ações mapeadas.
    """
    # Instanciamos os gerenciadores de estado globais (Serviços e Cardápio do estabelecimento)
    service = ComandaService()
    cardapio = Cardapio()

    # Recupera o cardápio e as comandas ativas salvas nos arquivos JSON correspondentes
    carregar_cardapio(cardapio)
    carregar_comandas(service, cardapio)

    acoes = {
        "1": fluxo_abrir_comanda,
        "2": fluxo_adicionar_item,
        "3": fluxo_ver_extrato,
        "4": fluxo_fechar_comanda,
        "5": fluxo_listar_cardapio,
        "6": fluxo_cadastrar_produto,
        "7": fluxo_listar_comandas_ativas
    }

    # Loop Principal do Ciclo de Vida do Sistema
    while True:
        opcao = exibir_menu()

        if opcao == '0':
            print("Encerrando Sistema...")
            break

        elif opcao in acoes:
            acoes[opcao](service, cardapio)

        else:
            print("Opção invalida, tente novamente")

if __name__ == "__main__":
    main()