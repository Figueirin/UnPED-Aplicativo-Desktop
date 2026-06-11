import json
import os
from models.produto import Produto
from models.comanda import Comanda
from models.usuario import Garcom, Gerente, Administrador

# Definição dos caminhos dos arquivos JSON salvos na pasta data/
CAMINHO_CARDAPIO = "data/cardapio.json"
CAMINHO_COMANDAS = "data/comandas.json"

# Garante que a pasta data/ exista antes de qualquer operação de leitura/escrita
os.makedirs("data", exist_ok=True)

def salvar_cardapio(cardapio):
    """
    Grava de forma persistente todos os produtos atuais do cardápio em um arquivo JSON.
    Recria o arquivo a cada salvamento para manter os dados sincronizados.
    """
    dados = [produto.to_dict() for produto in cardapio.produtos]
    with open(CAMINHO_CARDAPIO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_cardapio(cardapio):
    """
    Lê os produtos gravados no arquivo JSON e os cadastra na memória ao iniciar o sistema.
    Possui fallbacks (tratamentos) de segurança para manter a compatibilidade com arquivos JSON antigos.
    """
    if not os.path.exists(CAMINHO_CARDAPIO):
        return
    
    try:
        with open(CAMINHO_CARDAPIO, "r", encoding="utf-8") as f:
            dados = json.load(f)
            for item in dados:
                id_prod = item.get("id", len(cardapio.produtos) + 1)
                categoria = item.get("categoria", "Geral")
                
                # Instancia e registra o produto na memória
                produto = Produto(id_prod, item["nome"], item["preco"], categoria)
                cardapio.add_produto(produto)
    except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError, KeyError):
        # Ignora erros de leitura ou arquivo vazio para não quebrar a inicialização do programa
        pass

def salvar_comandas(comandas_ativas):
    """
    Salva a lista de comandas abertas ativas na memória no arquivo de comandas JSON.
    """
    dados = [comanda.to_dict() for comanda in comandas_ativas.values()]
    with open(CAMINHO_COMANDAS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_comandas(service, cardapio):
    """
    Carrega as comandas ativas salvas no arquivo JSON de volta para a memória RAM.
    Reconstrói os relacionamentos (Comandas e seus respectivos ItemComanda associados).
    """
    if not os.path.exists(CAMINHO_COMANDAS):
        return

    try:
        with open(CAMINHO_COMANDAS, "r", encoding="utf-8") as f:
            dados = json.load(f)

            for item_comanda in dados:
                num = item_comanda["Comanda"]
                nome_cliente = item_comanda["Cliente"]

                # 1. Abre novamente a comanda na memória RAM
                service.abrir_comanda(num, nome_cliente)
                comanda = service.buscar_comanda(num)

                # 2. Se a comanda abriu com sucesso, reconstrói seus itens de consumo
                if comanda:
                    for item in item_comanda["Items"]:
                        nome_prod = item["produto"]["nome"]
                        qtd = item["quantidade"]
                        # Busca o produto correspondente no cardápio carregado
                        produto = cardapio.buscar_produto(nome_prod)

                        if produto:
                            # Re-vincula o produto e quantidade à comanda
                            comanda.adicionar_item(produto, qtd)
    except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError, KeyError):
        # Passa reto em caso de arquivo vazio ou corrompido
        pass

def carregar_usuario():
    
    """
    Lê o arquivo de usuários JSON e cria as instâncias de Garcom ou Gerente correspondentes.
    Demonstra a instanciação polimórfica baseada em dados.
    """

    caminho = "data/usuarios.json"

    if not os.path.exists(caminho):
        return []

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
            usuarios = []

            for item in dados:
                username = item["username"]
                nome = item["nome"]
                senha = item["senha"]
                cargo = item["cargo"]

                if cargo == "Garcom":
                    usuarios.append(Garcom(username, senha, nome))
                
                elif cargo == "Gerente":
                    usuarios.append(Gerente(username, senha, nome))

                elif cargo == "Administrador":
                    usuarios.append(Administrador(username, senha, nome))

            return usuarios

    except (json.JSONDecodeError, FileNotFoundError, KeyError):
        return []

def salvar_usuario(usuarios):
    """
    Grava de forma persistente todos os usuários (Garcom e Gerente) de volta no arquivo JSON.
    """
    caminho = "data/usuarios.json"
    dados = [u.to_dict() for u in usuarios]
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)