import customtkinter as ctk
from tkinter import messagebox
from services.persistencia import salvar_comandas

class DetalhePedidoFrame(ctk.CTkFrame):
    def __init__(self, master, app_instance):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance
        self.comanda = None
        self.pago_acumulado = 0.0

        # Layout principal (1 linha, 2 colunas)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Itens e adição
        self.grid_columnconfigure(1, weight=1)  # Extrato e Pagamento

        # --- COLUNA 0: Itens & Lançamentos ---
        self.col0_frame = ctk.CTkFrame(self)
        self.col0_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        # Cabeçalho da Coluna 0
        self.btn_voltar = ctk.CTkButton(
            self.col0_frame, text="← Voltar ao Dashboard", fg_color="transparent",
            text_color=("#1f6aa5", "#1f6aa5"), hover_color=("gray90", "gray30"),
            command=lambda: self.app.selecionar_aba("dashboard")
        )
        self.btn_voltar.pack(anchor="w", padx=15, pady=(15, 5))

        self.lbl_comanda_titulo = ctk.CTkLabel(
            self.col0_frame, text="Comanda #0 | Cliente: -",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5", anchor="w"
        )
        self.lbl_comanda_titulo.pack(fill="x", padx=20, pady=(5, 15))

        # Adicionar Item Form
        self.add_item_frame = ctk.CTkFrame(self.col0_frame, fg_color=("gray95", "gray25"))
        self.add_item_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.lbl_add_titulo = ctk.CTkLabel(
            self.add_item_frame, text="Lançar Item no Pedido",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.lbl_add_titulo.pack(anchor="w", padx=15, pady=(10, 5))

        # Dropdown de Produtos
        self.lbl_prod = ctk.CTkLabel(self.add_item_frame, text="Produto", font=ctk.CTkFont(size=11))
        self.lbl_prod.pack(anchor="w", padx=15)
        
        self.produtos_map = {}
        self.atualizar_produtos_dropdown()

        # Input Quantidade
        self.lbl_qtd = ctk.CTkLabel(self.add_item_frame, text="Quantidade", font=ctk.CTkFont(size=11))
        self.lbl_qtd.pack(anchor="w", padx=15, pady=(5, 0))
        self.entry_qtd = ctk.CTkEntry(self.add_item_frame, placeholder_text="Ex: 1", width=100)
        self.entry_qtd.insert(0, "1")
        self.entry_qtd.pack(anchor="w", padx=15, pady=(0, 15))

        # Botão de Lançar
        self.btn_lancar = ctk.CTkButton(
            self.add_item_frame, text="Lançar Item",
            command=self.lancar_item
        )
        self.btn_lancar.pack(anchor="w", padx=15, pady=(0, 15))

        # Título da lista de consumo
        self.lbl_consumo_titulo = ctk.CTkLabel(
            self.col0_frame, text="Consumo Atual:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.lbl_consumo_titulo.pack(anchor="w", padx=20, pady=(10, 5))

        # Lista de Itens Consumidos (Scrollable)
        self.scroll_itens = ctk.CTkScrollableFrame(self.col0_frame)
        self.scroll_itens.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # --- COLUNA 1: Extrato & Fechamento ---
        self.col1_frame = ctk.CTkFrame(self)
        self.col1_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")

        self.lbl_extrato_titulo = ctk.CTkLabel(
            self.col1_frame, text="Extrato / Fechamento de Conta",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5", anchor="w"
        )
        self.lbl_extrato_titulo.pack(fill="x", padx=20, pady=20)

        # Monospace Text Box to show receipt
        self.txt_extrato = ctk.CTkTextbox(
            self.col1_frame, font=ctk.CTkFont(family="Courier", size=12),
            wrap="none", state="disabled"
        )
        self.txt_extrato.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # Painel de Fechamento de Conta
        self.checkout_frame = ctk.CTkFrame(self.col1_frame, fg_color=("gray95", "gray25"))
        self.checkout_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.lbl_pago_acumulado = ctk.CTkLabel(
            self.checkout_frame, text="Valor Pago: R$ 0.00",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.lbl_pago_acumulado.pack(anchor="w", padx=15, pady=(10, 2))

        self.lbl_falta_troco = ctk.CTkLabel(
            self.checkout_frame, text="Falta pagar: R$ 0.00",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#d32f2f"
        )
        self.lbl_falta_troco.pack(anchor="w", padx=15, pady=(0, 10))

        # Entrada de Valor Pago
        self.lbl_valor_pago = ctk.CTkLabel(self.checkout_frame, text="Registrar Pagamento (R$)", font=ctk.CTkFont(size=11))
        self.lbl_valor_pago.pack(anchor="w", padx=15)

        self.entry_pagamento = ctk.CTkEntry(self.checkout_frame, placeholder_text="Ex: 50.00", width=150)
        self.entry_pagamento.pack(anchor="w", padx=15, pady=(0, 10))

        self.btn_pagar = ctk.CTkButton(
            self.checkout_frame, text="Adicionar Pagamento",
            command=self.registrar_pagamento
        )
        self.btn_pagar.pack(anchor="w", padx=15, pady=(0, 10))

        # Botão Fechar Comanda (Completo)
        self.btn_fechar_comanda = ctk.CTkButton(
            self.checkout_frame, text="Encerrar Comanda", fg_color="gray", state="disabled",
            command=self.concluir_fechamento
        )
        self.btn_fechar_comanda.pack(fill="x", padx=15, pady=(5, 15))

    def atualizar_produtos_dropdown(self):
        # Limpar dropdown antigo se existir
        if hasattr(self, "combo_produtos"):
            self.combo_produtos.destroy()

        self.produtos_map = {f"[{p.id}] {p.nome} - R$ {p.preco:.2f}": p for p in self.app.cardapio.produtos}
        opcoes = list(self.produtos_map.keys())

        if not opcoes:
            opcoes = ["Nenhum produto cadastrado"]

        self.combo_produtos = ctk.CTkOptionMenu(self.add_item_frame, values=opcoes, width=250)
        self.combo_produtos.pack(padx=15, pady=(0, 10), fill="x")

    def carregar_comanda(self, numero_comanda):
        self.comanda = self.app.service.buscar_comanda(numero_comanda)
        if not self.comanda:
            messagebox.showerror("Erro", "Comanda não encontrada!")
            self.app.selecionar_aba("dashboard")
            return

        self.pago_acumulado = 0.0
        self.atualizar_produtos_dropdown()
        self.atualizar_view()

    def atualizar_view(self):
        if not self.comanda:
            return

        # 1. Título e cabeçalho
        self.lbl_comanda_titulo.configure(text=f"Comanda #{self.comanda.numero} | Cliente: {self.comanda.cliente_nome}")

        # 2. Atualizar lista de itens consumidos
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
            lbl_desc.pack(side="left", padx=10, pady=5)

            lbl_sub = ctk.CTkLabel(
                item_frame,
                text=f"R$ {item.calc_subtotal():.2f}",
                font=ctk.CTkFont(size=12)
            )
            lbl_sub.pack(side="right", padx=10, pady=5)

        # 3. Atualizar Extrato Textbox (Receipt format)
        self.txt_extrato.configure(state="normal")
        self.txt_extrato.delete("1.0", "end")
        self.txt_extrato.insert("1.0", str(self.comanda))
        self.txt_extrato.configure(state="disabled")

        # 4. Atualizar Valores de Pagamento
        subtotal = self.comanda.calcular_total()
        taxa = subtotal * 0.10
        total_geral = subtotal + taxa

        self.lbl_pago_acumulado.configure(text=f"Valor Pago: R$ {self.pago_acumulado:.2f}")

        falta = total_geral - self.pago_acumulado
        if falta > 0:
            self.lbl_falta_troco.configure(
                text=f"Falta pagar: R$ {falta:.2f}",
                text_color="#d32f2f"
            )
            self.btn_fechar_comanda.configure(fg_color="gray", state="disabled")
        else:
            troco = abs(falta)
            self.lbl_falta_troco.configure(
                text=f"Troco a devolver: R$ {troco:.2f}" if troco > 0 else "Conta quitada!",
                text_color="#2e7d32"
            )
            self.btn_fechar_comanda.configure(fg_color="#2e7d32", state="normal")

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

    def registrar_pagamento(self):
        if not self.comanda:
            return

        pag_str = self.entry_pagamento.get().strip()
        try:
            valor = float(pag_str)
            if valor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor de pagamento válido maior que zero!")
            return

        self.pago_acumulado += valor
        self.entry_pagamento.delete(0, "end")
        self.atualizar_view()

    def concluir_fechamento(self):
        if not self.comanda:
            return

        subtotal = self.comanda.calcular_total()
        taxa = subtotal * 0.10
        total_geral = subtotal + taxa
        troco = self.pago_acumulado - total_geral

        # Confirmação final
        msg = f"Deseja realmente fechar e encerrar a comanda #{self.comanda.numero}?"
        if troco > 0:
            msg += f"\nTroco a ser devolvido: R$ {troco:.2f}"

        if not messagebox.askyesno("Fechar Comanda", msg):
            return

        # Executa fechamento no serviço (pop)
        self.app.service.fechar_comanda(self.comanda.numero)
        salvar_comandas(self.app.service.comandas_ativas)

        messagebox.showinfo("Sucesso", f"Comanda #{self.comanda.numero} encerrada com sucesso!")
        self.comanda = None
        self.app.selecionar_aba("dashboard")
