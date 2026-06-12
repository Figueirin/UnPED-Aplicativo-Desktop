# UnPED - Sistema de Comandas para Bares e Restaurantes (Versão GUI)

Este projeto é um sistema de comandas ("comandas de consumo") para restaurantes e bares, desenvolvido como projeto prático para a matéria de Programação Orientada a Objetos (OO) da Universidade de Brasília (UnB).

A aplicação foi modernizada para utilizar uma interface gráfica enriquecida (GUI) em **Python 3.14** com a biblioteca `customtkinter`, simulando um terminal de PDV (Ponto de Venda) completo com restrições de acesso por cargos (Garçom, Gerente, Administrador) e persistência robusta em arquivos JSON.

---

## 🏗️ Estrutura de Pastas do Projeto

Para manter o código organizado e garantir o **Princípio da Responsabilidade Única (SRP)**, o projeto foi estruturado da seguinte forma:

*   **`models/`**: Representa as entidades de domínio do negócio.
    *   [produto.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/models/produto.py): Representa um item do cardápio com validação estrita de ID, nome, preço e categoria.
    *   [item_comanda.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/models/item_comanda.py): Representa a linha de consumo (associa um `Produto` a uma quantidade).
    *   [comanda.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/models/comanda.py): Representa a comanda ativa do cliente (agrupa número, nome do cliente, itens e gera extrato).
    *   [cardapio.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/models/cardapio.py): Gerencia a lista de produtos disponíveis.
    *   [usuario.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/models/usuario.py): Define a hierarquia de usuários do sistema (`Garcom`, `Gerente` e `Administrador`).
*   **`services/`**: Camada de lógica de controle e persistência de dados.
    *   [comanda_service.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/services/comanda_service.py): Gerencia o estado das comandas em execução na memória.
    *   [persistencia.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/services/persistencia.py): Serializa e desserializa os dados de cardápio, comandas e usuários em arquivos JSON com segurança.
*   **`views/`**: Telas e componentes da interface gráfica.
    *   [login.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/views/login.py): Autenticação, visualização de senha e fallback de registro de Admin inicial em caso de perda de banco de dados.
    *   [dashboard.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/views/dashboard.py): Grid de visualização rápida de comandas ativas e abertura de novas contas.
    *   [detalhe_pedido.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/views/detalhe_pedido.py): Lançador de pedidos PDV Mobile-style (buffer de pedidos e transferência de itens restrita a cargos gerenciais).
    *   [cardapio.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/views/cardapio.py): Cadastro de produtos e exclusão segura.
    *   [usuarios.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/views/usuarios.py): Cadastro e remoção de operadores do sistema.
    *   [fechar_comanda.py](file:///c:/Users/Renato/Documents/Antigravity/UnB/OO/UnPED/views/fechar_comanda.py): Fechamento interativo da conta, recebimentos parciais e cálculo automático de troco.
*   **`data/`**: Arquivos JSON persistentes (`cardapio.json`, `comandas.json` e `usuarios.json`).
*   **`app.py`**: Ponto de entrada (bootstrapper) principal do sistema em modo gráfico.

---

## 📊 Modelagem UML (Diagrama de Classes)

O diagrama abaixo descreve a nova estrutura de classes do UnPED, seus respectivos atributos, métodos e tipos de relacionamentos.

```mermaid
classDiagram
    direction TB
    
    class Usuario {
        +str username
        +str senha
        +str nome
        +str cargo
        +to_dict() dict
    }
    class Garcom {
        +__init__(username, senha, nome)
    }
    class Gerente {
        +__init__(username, senha, nome)
    }
    class Administrador {
        +__init__(username, senha, nome)
    }
    Usuario <|-- Garcom
    Usuario <|-- Gerente
    Usuario <|-- Administrador

    class Produto {
        +int id
        +str nome
        +float preco
        +str categoria
        +__init__(id_produto, nome_produto, preco, categoria)
        +to_dict() dict
        +__str__() str
    }
    
    class ItemComanda {
        +Produto produto
        +int quantidade
        +__init__(produto, qtd)
        +calc_subtotal() float
        +to_dict() dict
        +__str__() str
    }
    
    class Comanda {
        +int numero
        +str cliente_nome
        +list itens
        +__init__(numero, cliente_nome)
        +adicionar_item(produto, qtd)
        +calcular_total() float
        +to_dict() dict
        +__str__() str
    }
    
    class Cardapio {
        +list produtos
        +__init__()
        +add_produto(produto) bool
        +listar_produtos()
        +buscar_produto(termo) Produto
    }
    
    class ComandaService {
        +dict comandas_ativas
        +__init__()
        +abrir_comanda(numero, cliente_nome) bool
        +buscar_comanda(numero) Comanda
        +fechar_comanda(numero) Comanda
        +listar_comandas_ativas()
    }

    %% Relacionamentos
    ItemComanda --> Produto : "Associação (1..1)"
    Comanda *-- ItemComanda : "Composição (0..*)"
    Cardapio o-- Produto : "Agregação (0..*)"
    ComandaService o-- Comanda : "Agregação (0..*)"
```

---

## 🧠 Conceitos de OO aplicados ao projeto

### 1. Associação, Agregação e Composição
*   **Associação:** A classe `ItemComanda` possui uma associação direta a um objeto do tipo `Produto` para consultar seu preço e dados.
*   **Agregação:** A classe `Cardapio` agrega objetos do tipo `Produto`. Se o cardápio for limpo ou reinstanciado, a existência conceitual dos produtos cadastrados pode continuar de forma independente.
*   **Composição (Relação Forte):** A classe `Comanda` é composta de objetos `ItemComanda`. Quando uma comanda é encerrada e removida da memória, todas as suas linhas de consumo (`ItemComanda`) associadas deixam de existir, mantendo a integridade do ciclo de vida.

### 2. Herança e Polimorfismo
*   A classe base `Usuario` define atributos comuns a todos os operadores. As classes filhas `Garcom`, `Gerente` e `Administrador` herdam essa estrutura básica.
*   **Polimorfismo Baseado em Regras de Acesso:** A interface gráfica se comporta de forma polimórfica ao ocultar abas e botões reativos da sidebar baseando-se no cargo do usuário ativo (ex: apenas Gerente/Admin visualiza aba de Cardápio; apenas Administrador visualiza Usuários; e opções críticas como transferência de itens dependem da verificação dinâmica do cargo).

### 3. Encapsulamento & Validação Fail-Fast (Defensive Coding)
*   **Validação Estrita:** Em vez de depender apenas do tratamento de dados na interface (views), as validações foram inseridas diretamente no construtor dos modelos. Instanciar um produto com preço negativo, um item de comanda com quantidade zerada, ou uma comanda com cliente vazio dispara um `ValueError` imediatamente. Isso protege o banco de dados contra corrupções em qualquer nível de integração.

---

## 🛡️ Mecanismos de Segurança Implementados

1.  **Salvaguarda contra perda de banco de dados:** Se o arquivo `usuarios.json` for deletado ou corrompido, a tela de login detecta a falha e se transforma em uma tela de cadastro inicial de Administrador do sistema, efetuando o login automático logo após a persistência bem-sucedida.
2.  **Proteção de integridade no Cardápio:** O sistema impede a remoção de qualquer produto que esteja atualmente lançado em alguma comanda ativa, alertando o operador e evitando itens órfãos/valores nulos na inicialização seguinte.
3.  **Controle de estouro de Grid (UI):** Limitações físicas de caracteres nos campos de formulário (ex: nome do cliente limitado a 25 caracteres, produto a 30) e truncagem por reticências (`...`) impedem que entradas longas quebrem as proporções e ocultem botões de ação na interface.
4.  **Arredondamento Financeiro:** Utilização de `round(falta, 2)` na apuração de saldo devedor de comandas, prevenindo que imprecisões decimais da especificação de ponto flutuante (IEEE 754) impeçam o fechamento correto de contas quitadas.

---

## 🚀 Como executar o projeto

Certifique-se de ter o Python 3.10+ instalado em sua máquina.

```bash
# 1. Clone o repositório
git clone https://github.com/Figueirin/UnPED

# 2. Acesse a pasta do projeto
cd UnPED

# 3. Instale a biblioteca CustomTkinter (caso ainda não possua)
pip install customtkinter

# 4. Execute a aplicação em modo gráfico
python app.py
```

*Nota: A versão para linha de comando original pode ser executada por `python main.py`.*
