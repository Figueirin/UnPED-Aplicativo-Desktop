import customtkinter as ctk
from tkinter import messagebox
from services.persistencia import salvar_comandas

class DetalhePedidoFrame(ctk.CTkFrame):
    def __init__(self, master, app_instance):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance
        self.comanda = None

        # Layout principal (1 linha, 2 colunas para colocar form na esquerda e lista na direita)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Formulário de lançamento
        self.grid_columnconfigure(1, weight=1)  # Lista de itens lançados

        # --- LADO ESQUERDO: Formulário de Lançamento ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        # Botão de Voltar
        self.btn_voltar = ctk.CTkButton(
            self.form_frame, text="← Voltar ao Dashboard", fg_color="transparent",
            text_color=("#1f6aa5", "#1f6aa5"), hover_color=("gray90", "gray30"),
            command=lambda: self.app.selecionar_aba("dashboard")
        )
        self.btn_voltar.pack(anchor="w", padx=15, pady=(15, 5))

        self.lbl_comanda_titulo = ctk.CTkLabel(
            self.form_frame, text="Lançar Itens - Comanda #0",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5", anchor="w"
        )
        self.lbl_comanda_titulo.pack(fill="x", padx=20, pady=(5, 15))

        # Painel do Lançador
        self.launcher_panel = ctk.CTkFrame(self.form_frame, fg_color=("gray95", "gray25"))
        self.launcher_panel.pack(fill="x", padx=20, pady=(0, 20))

        self.lbl_add_titulo = ctk.CTkLabel(
            self.launcher_panel, text="Lançar Novo Item",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.lbl_add_titulo.pack(anchor="w", padx=15, pady=(10, 5))

        # Dropdown de Produtos
        self.lbl_prod = ctk.CTkLabel(self.launcher_panel, text="Selecionar Produto", font=ctk.CTkFont(size=11))
        self.lbl_prod.pack(anchor="w", padx=15)
        
        self.produtos_map = {}
        self.combo_produtos = None
        self.atualizar_produtos_dropdown()

        # Entrada de Quantidade
        self.lbl_qtd = ctk.CTkLabel(self.launcher_panel, text="Quantidade", font=ctk.CTkFont(size=11))
        self.lbl_qtd.pack(anchor="w", padx=15, pady=(5, 0))
        self.entry_qtd = ctk.CTkEntry(self.launcher_panel, placeholder_text="Ex: 1", width=100)
        self.entry_qtd.insert(0, "1")
        self.entry_qtd.pack(anchor="w", padx=15, pady=(0, 15))

        # Botão Lançar
        self.btn_lancar = ctk.CTkButton(
            self.launcher_panel, text="Confirmar Lançamento",
            command=self.lancar_item
        )
        self.btn_lancar.pack(anchor="w", padx=15, pady=(0, 15))

        # --- LADO DIREITO: Consumo Atual da Comanda ---
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")

        self.lbl_consumo_titulo = ctk.CTkLabel(
            self.list_frame, text="Consumo Atual da Comanda",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5", anchor="w"
        )
        self.lbl_consumo_titulo.pack(fill="x", padx=20, pady=20)

        self.scroll_itens = ctk.CTkScrollableFrame(self.list_frame, label_text="Itens Consumidos")
        self.scroll_itens.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def atualizar_produtos_dropdown(self):
        if self.combo_produtos:
            self.combo_produtos.destroy()

        self.produtos_map = {f"[{p.id}] {p.nome} - R$ {p.preco:.2f}": p for p in self.app.cardapio.produtos}
        opcoes = list(self.produtos_map.keys())

        if not opcoes:
            opcoes = ["Nenhum produto cadastrado"]

        self.combo_produtos = ctk.CTkOptionMenu(self.launcher_panel, values=opcoes, width=280)
        # Inserir o dropdown logo abaixo do label de produto
        self.combo_produtos.pack(padx=15, pady=(0, 10), fill="x", after=self.lbl_prod)

    def carregar_comanda(self, numero_comanda):
        self.comanda = self.app.service.buscar_comanda(numero_comanda)
        if not self.comanda:
            messagebox.showerror("Erro", "Comanda não encontrada!")
            self.app.selecionar_aba("dashboard")
            return

        self.atualizar_produtos_dropdown()
        self.atualizar_view()

    def atualizar_view(self):
        if not self.comanda:
            return

        # Atualizar Título
        self.lbl_comanda_titulo.configure(text=f"Lançar Itens - Comanda #{self.comanda.numero} ({self.comanda.cliente_nome})")

        # Limpar e recarregar lista de itens
        for widget in self.scroll_itens.winfo_children():
            widget.destroy()

        for item in self.comanda.itens:
            item_frame = ctk.CTkFrame(self.scroll_itens, fg_color=("gray95", "gray25"))
            item_frame.pack(fill="x", padx=5, pady=3)

            lbl_desc = ctk.CTkLabel(
                item_frame,
                text=f"{item.quantidade} x {item.produto.nome}",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            lbl_desc.pack(side="left", padx=10, pady=8)

            lbl_sub = ctk.CTkLabel(
                item_frame,
                text=f"R$ {item.calc_subtotal():.2f}",
                font=ctk.CTkFont(size=12)
            )
            lbl_sub.pack(side="right", padx=10, pady=8)

    def lancar_item(self):
        if not self.comanda:
            return

        prod_selecionado = self.combo_produtos.get()
        if prod_selecionado == "Nenhum produto cadastrado" or prod_selecionado not in self.produtos_map:
            messagebox.showerror("Erro", "Selecione um produto válido!")
            return

        produto = self.produtos_map[prod_selecionado]
        
        try:
            qtd = int(self.entry_qtd.get().strip())
            if qtd <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "A quantidade deve ser um número inteiro maior que zero!")
            return

        self.comanda.adicionar_item(produto, qtd)
        salvar_comandas(self.app.service.comandas_ativas)

        self.entry_qtd.delete(0, "end")
        self.entry_qtd.insert(0, "1")

        messagebox.showinfo("Sucesso", f"{qtd}x {produto.nome} lançado(s) com sucesso!")
        self.atualizar_view()
