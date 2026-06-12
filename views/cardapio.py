import customtkinter as ctk
from tkinter import messagebox
from models.produto import Produto
from services.persistencia import salvar_cardapio

class CardapioFrame(ctk.CTkFrame):
    def __init__(self, master, app_instance):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance

        # Layout principal (1 coluna, grid configurado)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Cabeçalho: Título e Botão
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(10, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.header_label = ctk.CTkLabel(
            self.header_frame, text="Cardápio do Estabelecimento",
            font=ctk.CTkFont(family="Outfit", size=22, weight="bold"),
            text_color="#1f6aa5"
        )
        self.header_label.grid(row=0, column=0, sticky="w")

        # Botão para cadastrar produto (Visível/Habilitado para Gerente e Administrador)
        self.btn_novo_produto = ctk.CTkButton(
            self.header_frame, text="+ Cadastrar Produto",
            font=ctk.CTkFont(weight="bold"),
            command=self.abrir_dialogo_cadastro
        )
        self.btn_novo_produto.grid(row=0, column=1, sticky="e")

        # Scroll Frame ocupando toda a área útil
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

        self.atualizar_lista()

    def atualizar_lista(self):
        # Limpar widgets do scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not self.app.cardapio.produtos:
            lbl_vazio = ctk.CTkLabel(
                self.scroll_frame, text="Nenhum produto cadastrado no cardápio.\nClique no botão acima para cadastrar o primeiro!",
                font=ctk.CTkFont(size=14, slant="italic"),
                text_color="gray"
            )
            lbl_vazio.pack(pady=50)
            return

        # Agrupar produtos por categoria
        categorias = {}
        for produto in self.app.cardapio.produtos:
            cat = produto.categoria
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(produto)

        # Renderizar categorias e itens
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

                # Truncar o nome do produto se necessário
                nome_exibido = p.nome
                if len(nome_exibido) > 25:
                    nome_exibido = nome_exibido[:22] + "..."

                lbl_prod_info = ctk.CTkLabel(
                    prod_card,
                    text=f"[{p.id}] {nome_exibido}",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    anchor="w"
                )
                lbl_prod_info.pack(side="left", padx=15, pady=8)

                # Botão de remoção (Lado Direito)
                btn_remover = ctk.CTkButton(
                    prod_card, text="Remover", fg_color="#d32f2f", hover_color="#b71c1c", width=70, height=24,
                    command=lambda pid=p.id: self.remover_produto(pid)
                )
                btn_remover.pack(side="right", padx=15, pady=8)

                lbl_prod_preco = ctk.CTkLabel(
                    prod_card,
                    text=f"R$ {p.preco:.2f}",
                    font=ctk.CTkFont(size=12),
                    anchor="e"
                )
                lbl_prod_preco.pack(side="right", padx=5, pady=8)

    def remover_produto(self, produto_id):
        produto = self.app.cardapio.buscar_produto(produto_id)
        if not produto:
            return

        # Verifica se o produto está em uso em alguma comanda ativa no momento
        for comanda in self.app.service.comandas_ativas.values():
            for item in comanda.itens:
                if item.produto.id == produto_id:
                    messagebox.showerror(
                        "Erro", 
                        f"Não é possível remover o produto '{produto.nome}' porque ele está atualmente lançado na Comanda #{comanda.numero}!"
                    )
                    return

        if not messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o produto '{produto.nome}' do cardápio?"):
            return

        self.app.cardapio.produtos = [p for p in self.app.cardapio.produtos if p.id != produto_id]
        salvar_cardapio(self.app.cardapio)

        messagebox.showinfo("Sucesso", f"Produto '{produto.nome}' removido com sucesso!")
        self.atualizar_lista()

    def abrir_dialogo_cadastro(self):
        # Criar janela Toplevel para o cadastro
        dialog = ctk.CTkToplevel(self)
        dialog.title("Cadastrar Produto")
        dialog.geometry("380x420")
        dialog.resizable(False, False)
        dialog.grab_set()  # Torna modal
        dialog.focus_force()

        lbl_titulo = ctk.CTkLabel(
            dialog, text="Cadastrar Novo Produto",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5"
        )
        lbl_titulo.pack(pady=(20, 15))

        # Campo Nome
        lbl_nome = ctk.CTkLabel(dialog, text="Nome do Produto (Max 30 caracteres)", font=ctk.CTkFont(size=12))
        lbl_nome.pack(anchor="w", padx=30)
        entry_nome = ctk.CTkEntry(dialog, placeholder_text="Ex: Suco de Uva", width=320)
        entry_nome.pack(padx=30, pady=(0, 10))

        # Campo Preço
        lbl_preco = ctk.CTkLabel(dialog, text="Preço Unitário (R$)", font=ctk.CTkFont(size=12))
        lbl_preco.pack(anchor="w", padx=30)
        entry_preco = ctk.CTkEntry(dialog, placeholder_text="Ex: 9.90", width=320)
        entry_preco.pack(padx=30, pady=(0, 10))

        # Obter categorias existentes de forma única
        categorias_existentes = sorted(list(set(p.categoria for p in self.app.cardapio.produtos)))
        opcoes_dropdown = categorias_existentes + ["Criar nova categoria..."]

        # Campo Categoria
        lbl_cat = ctk.CTkLabel(dialog, text="Categoria", font=ctk.CTkFont(size=12))
        lbl_cat.pack(anchor="w", padx=30)

        # Entrada de Texto adicional para nova categoria (inicialmente invisível)
        entry_nova_cat = ctk.CTkEntry(dialog, placeholder_text="Digite a nova categoria (Max 20 chars)...", width=320)

        def ao_selecionar_categoria(opcao):
            if opcao == "Criar nova categoria...":
                entry_nova_cat.pack(padx=30, pady=(5, 10), before=btn_cadastrar)
            else:
                entry_nova_cat.pack_forget()

        # Dropdown
        dropdown_cat = ctk.CTkOptionMenu(
            dialog, values=opcoes_dropdown, width=320, command=ao_selecionar_categoria
        )
        dropdown_cat.pack(padx=30, pady=(0, 10))

        # Pré-selecionar a primeira categoria existente, ou a opção de criar nova se vazio
        if categorias_existentes:
            dropdown_cat.set(categorias_existentes[0])
        else:
            dropdown_cat.set("Criar nova categoria...")
            ao_selecionar_categoria("Criar nova categoria...")

        def cadastrar():
            nome = entry_nome.get().strip()
            preco_str = entry_preco.get().strip()
            opcao_cat = dropdown_cat.get()

            # Resolver Categoria
            if opcao_cat == "Criar nova categoria...":
                categoria = entry_nova_cat.get().strip()
            else:
                categoria = opcao_cat

            if not nome or not preco_str or not categoria:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!", parent=dialog)
                return

            if len(nome) > 30:
                messagebox.showerror("Erro", "O nome do produto não pode exceder 30 caracteres!", parent=dialog)
                return

            if len(categoria) > 20:
                messagebox.showerror("Erro", "A categoria não pode exceder 20 caracteres!", parent=dialog)
                return

            if len(preco_str) > 10:
                messagebox.showerror("Erro", "O preço digitado é excessivamente longo!", parent=dialog)
                return

            try:
                preco = float(preco_str)
                if preco <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Digite um preço decimal válido e maior que zero!", parent=dialog)
                return

            # Evita Duplicados
            nome_low = nome.lower()
            for p in self.app.cardapio.produtos:
                if p.nome.lower() == nome_low:
                    messagebox.showerror("Erro", f"O produto '{nome}' já está cadastrado!", parent=dialog)
                    return

            # Auto-gerar ID
            novo_id = max([p.id for p in self.app.cardapio.produtos], default=0) + 1

            # Adicionar e persistir
            novo_produto = Produto(novo_id, nome, preco, categoria)
            self.app.cardapio.add_produto(novo_produto)
            salvar_cardapio(self.app.cardapio)

            messagebox.showinfo("Sucesso", f"'{nome}' cadastrado com sucesso!", parent=dialog)
            dialog.destroy()
            self.atualizar_lista()

        btn_cadastrar = ctk.CTkButton(dialog, text="Salvar Produto", height=35, command=cadastrar)
        btn_cadastrar.pack(padx=30, pady=(15, 0), fill="x")
