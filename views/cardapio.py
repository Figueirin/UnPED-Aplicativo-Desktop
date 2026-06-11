import customtkinter as ctk
from tkinter import messagebox
from models.produto import Produto
from services.persistencia import salvar_cardapio

class CardapioFrame(ctk.CTkFrame):
    def __init__(self, master, app_instance):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance

        # Configurar layout grid (1 linha, 2 colunas)
        # Se for Gerente, divide a tela entre o formulário de cadastro e a lista.
        # Se for Garçom, o cardápio ocupa a tela inteira (embora a aba esteja bloqueada na sidebar, caso venha a acessar).
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # Lado Esquerdo: Formulário de Cadastro de Produto (Apenas para Gerente)
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        self.lbl_titulo_form = ctk.CTkLabel(
            self.form_frame, text="Cadastrar Novo Produto",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5"
        )
        self.lbl_titulo_form.pack(pady=20, padx=20, anchor="w")

        # Nome do Produto
        self.lbl_nome = ctk.CTkLabel(self.form_frame, text="Nome do Produto", font=ctk.CTkFont(size=12))
        self.lbl_nome.pack(anchor="w", padx=20, pady=(10, 2))
        self.entry_nome = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: Suco de Laranja", width=220)
        self.entry_nome.pack(padx=20, pady=(0, 10), fill="x")

        # Preço
        self.lbl_preco = ctk.CTkLabel(self.form_frame, text="Preço Unitário (R$)", font=ctk.CTkFont(size=12))
        self.lbl_preco.pack(anchor="w", padx=20, pady=(10, 2))
        self.entry_preco = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: 8.50", width=220)
        self.entry_preco.pack(padx=20, pady=(0, 10), fill="x")

        # Categoria
        self.lbl_categoria = ctk.CTkLabel(self.form_frame, text="Categoria", font=ctk.CTkFont(size=12))
        self.lbl_categoria.pack(anchor="w", padx=20, pady=(10, 2))
        self.entry_categoria = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: Bebidas", width=220)
        self.entry_categoria.pack(padx=20, pady=(0, 20), fill="x")

        # Botão Cadastrar
        self.btn_cadastrar = ctk.CTkButton(
            self.form_frame, text="Cadastrar Produto", height=35,
            command=self.cadastrar_produto
        )
        self.btn_cadastrar.pack(padx=20, pady=(0, 20), fill="x")

        # Lado Direito: Visualização do Cardápio
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")

        self.lbl_titulo_lista = ctk.CTkLabel(
            self.list_frame, text="Cardápio do Estabelecimento",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5"
        )
        self.lbl_titulo_lista.pack(pady=20, padx=20, anchor="w")

        self.scroll_frame = ctk.CTkScrollableFrame(self.list_frame, label_text="Produtos Disponíveis")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.atualizar_lista()

    def atualizar_lista(self):
        # Limpar widgets do scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Agrupar produtos por categoria
        categorias = {}
        for produto in self.app.cardapio.produtos:
            cat = produto.categoria
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(produto)

        # Renderizar categorias e itens de forma elegante
        for categoria, produtos in categorias.items():
            # Rótulo da Categoria
            cat_label = ctk.CTkLabel(
                self.scroll_frame, text=categoria.upper(),
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#1f6aa5", anchor="w"
            )
            cat_label.pack(fill="x", padx=10, pady=(15, 5))

            # Separador visual
            sep = ctk.CTkFrame(self.scroll_frame, height=2, fg_color="gray")
            sep.pack(fill="x", padx=10, pady=(0, 10))

            # Lista de produtos na categoria
            for p in produtos:
                prod_card = ctk.CTkFrame(self.scroll_frame, fg_color=("gray95", "gray25"))
                prod_card.pack(fill="x", padx=10, pady=3)

                lbl_prod_info = ctk.CTkLabel(
                    prod_card,
                    text=f"[{p.id}] {p.nome}",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    anchor="w"
                )
                lbl_prod_info.pack(side="left", padx=15, pady=8)

                lbl_prod_preco = ctk.CTkLabel(
                    prod_card,
                    text=f"R$ {p.preco:.2f}",
                    font=ctk.CTkFont(size=12),
                    anchor="e"
                )
                lbl_prod_preco.pack(side="right", padx=15, pady=8)

    def cadastrar_produto(self):
        nome = self.entry_nome.get().strip()
        preco_str = self.entry_preco.get().strip()
        categoria = self.entry_categoria.get().strip()

        if not nome or not preco_str:
            messagebox.showerror("Erro", "Nome e Preço são obrigatórios!")
            return

        # Validar Preço
        try:
            preco = float(preco_str)
            if preco <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Digite um preço decimal válido e maior que zero!")
            return

        if not categoria:
            categoria = "Geral"

        # Validar Duplicatas de nome
        nome_low = nome.lower()
        for p in self.app.cardapio.produtos:
            if p.nome.lower() == nome_low:
                messagebox.showerror("Erro", f"O produto '{nome}' já está cadastrado!")
                return

        # Auto-geração do ID incrementado
        novo_id = max([p.id for p in self.app.cardapio.produtos], default=0) + 1

        # Adicionar e salvar
        novo_produto = Produto(novo_id, nome, preco, categoria)
        self.app.cardapio.add_produto(novo_produto)
        salvar_cardapio(self.app.cardapio)

        # Limpar campos
        self.entry_nome.delete(0, "end")
        self.entry_preco.delete(0, "end")
        self.entry_categoria.delete(0, "end")

        messagebox.showinfo("Sucesso", f"'{nome}' cadastrado com sucesso!")
        self.atualizar_lista()
