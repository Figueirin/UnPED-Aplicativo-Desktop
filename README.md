# UnPED - Sistema de Comandas para Bares e Restaurantes

Este projeto é um sistema de comandas para restaurantes e bares, desenvolvido como projeto prático para a matéria de Programação Orientada a Objetos (OO) da Universidade de Brasília (UnB). 

O objetivo do sistema é gerenciar comandas no terminal: abrir comandas associando o número a um cliente, lançar itens do cardápio nas comandas, exibir o extrato de consumo e fechar comandas calculando o total a pagar. Além disso, os dados são salvos em arquivos JSON para não sumirem toda vez que o programa é fechado.

---

## 🏗️ Como o projeto está organizado (Estrutura de Pastas)

Para manter o código organizado e evitar arquivos gigantes, separamos o projeto em módulos/pastas lógicas:

- `models/`: Contém as classes que representam as entidades do negócio.
  - `cliente.py`: Representa o cliente (guarda o nome).
  - `produto.py`: Representa um item do cardápio (nome e preço).
  - `pedido_item.py`: Representa a linha do pedido (produto associado à quantidade pedida).
  - `pedido.py`: É a comanda física (associa o cliente, número da comanda e a lista de itens consumidos).
  - `cardapio.py`: Gerencia a lista de produtos disponíveis.
- `services/`: Contém as regras de funcionamento do negócio e persistência.
  - `pedido_service.py`: Controla o estado das comandas ativas (abrir, buscar, listar e fechar comanda).
  - `persistencia.py`: Cuida de ler e gravar os dados nos arquivos JSON.
- `utils/`: Funções utilitárias.
  - `menu.py`: Cuida da parte visual do console e das funções de validação de input.
- `data/`: Pasta onde os arquivos JSON (`cardapio.json` e `pedidos.json`) ficam salvos.
- `main.py`: Ponto de entrada do programa que roda o loop do menu.

---

## 🧠 Conceitos de OO aplicados no trabalho (Para avaliação do Professor)

### 1. Associação e Composição de Objetos
* **Associação:** A classe `Pedido` guarda uma referência direta ao objeto `Cliente` associado (passado no construtor). Não duplicamos os dados do cliente dentro do pedido, apenas apontamos para ele.
* **Composição:** O `Pedido` é composto por uma lista de objetos `PedidoItem`. Cada `PedidoItem` associa um objeto `Produto` à sua respectiva quantidade pedida.

### 2. Delegação de Responsabilidade
Para calcular o valor de uma linha da comanda (`PedidoItem`), a classe não acessa o preço diretamente de forma solta. Ela chama o método `calc_subtotal()`, que por sua vez delega a consulta de preço ao objeto `Produto` (`self.produto.preco * self.quantidade`). O mesmo ocorre quando o `Pedido` calcula o total geral chamando `calc_subtotal()` de cada item.

### 3. Encapsulamento e Métodos Especiais
* Sobrescrevemos o método especial `__str__` nas classes (`Cliente`, `Produto`, `PedidoItem` e `Pedido`) para personalizar a exibição deles em formato de texto amigável na tela.
* O menu principal (`main.py`) não sabe como o `PedidoService` guarda as comandas (que é via dicionário na memória). A lógica interna de busca e remoção está totalmente encapsulada dentro do serviço.

### 4. Tratamento de Exceções e Edge Cases
Para evitar que o programa sofra travamento (crash) no console por entradas inválidas, implementamos:
* Loops com `try/except ValueError` para garantir que campos que precisam ser números (como quantidade, número de comanda e preço) não quebrem se o usuário digitar letras ou símbolos.
* Validação para impedir que comandas com números duplicados sejam abertas ao mesmo tempo.
* Validação para impedir o cadastro de produtos ou quantidades menores ou iguais a zero (valores negativos).

---

## 💾 Persistência de Dados (JSON)
Criamos um sistema de serialização em arquivos JSON dentro de `services/persistencia.py`. 
Toda alteração de estado no sistema (cadastrar produto, abrir comanda, adicionar item ou pagar conta) dispara automaticamente um salvamento nos arquivos `.json` da pasta `data/`. Quando o programa inicia, ele lê esses arquivos e reconstrói as classes e suas associações em memória.

---

## 🚀 Como executar o projeto

Basta clonar o repositório, abrir a pasta raiz no terminal e rodar:

```bash
python main.py
```
