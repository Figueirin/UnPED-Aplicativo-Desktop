
import customtkinter as ctk
from tkinter import messagebox
from services.persistencia import salvar_comandas

class DetalhePedidoFrame(ctk.CTkFrame):
    def __init__(self, master, app_instance):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance
        self.comanda = None
        self.selected_category = None
        self.buffer = {}  # Carrinho temporário: { produto_id: quantidade }

        # Configurar layout principal (1 linha, 2 colunas com proporção)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=4)  # Lado Esquerdo: Seletor de Categorias/Produtos
        self.grid_columnconfigure(1, weight=3)  # Lado Direito: Carrinho (Buffer) e Consumo Atual

        # --- COLUNA 0: Seletor Mobile-Style ---
        self.col0_frame = ctk.CTkFrame(self)
        self.col0_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        # Botão de Voltar para o Dashboard
        self.btn_voltar = ctk.CTkButton(
            self.col0_frame, text="← Voltar ao Dashboard", fg_color="transparent",
            text_color=("#1f6aa5", "#1f6aa5"), hover_color=("gray90", "gray30"),
            command=lambda: self.app.selecionar_aba("dashboard")
        )
        self.btn_voltar.pack(anchor="w", padx=15, pady=(15, 5))

        self.lbl_seletor_titulo = ctk.CTkLabel(
            self.col0_frame, text="Lançamento - Comanda #0",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5", anchor="w"
        )
        self.lbl_seletor_titulo.pack(fill="x", padx=20, pady=(5, 10))

        # Scrollable Frame para o painel de seleção de itens/categorias
        self.scroll_selector = ctk.CTkScrollableFrame(self.col0_frame)
        self.scroll_selector.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # --- COLUNA 1: Carrinho (Buffer) & Consumo Atual ---
        self.col1_frame = ctk.CTkFrame(self)
        self.col1_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")

        # Divisão da Coluna 1 em duas linhas (linha 0 = Buffer/Cart, linha 1 = Consumo)
        self.col1_frame.grid_rowconfigure((0, 1), weight=1, uniform="equal")
        self.col1_frame.grid_columnconfigure(0, weight=1)

        # -- SUB-SEÇÃO A: Buffer de Envio (Itens a Lançar) --
        self.buffer_frame = ctk.CTkFrame(self.col1_frame)
        self.buffer_frame.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="nsew")

        self.lbl_buffer_titulo = ctk.CTkLabel(
            self.buffer_frame, text="Itens a Enviar",
            font=ctk.CTkFont(family="Outfit", size=15, weight="bold"),
            text_color="#1f6aa5", anchor="w"
        )
        self.lbl_buffer_titulo.pack(side="top", fill="x", padx=15, pady=10)

        self.btn_enviar_pedido = ctk.CTkButton(
            self.buffer_frame, text="Enviar Pedidos (0)", fg_color="gray", state="disabled",
            font=ctk.CTkFont(weight="bold"), command=self.enviar_buffer
        )
        self.btn_enviar_pedido.pack(side="bottom", fill="x", padx=15, pady=(0, 15))

        self.scroll_buffer = ctk.CTkScrollableFrame(self.buffer_frame)
        self.scroll_buffer.pack(side="top", fill="both", expand=True, padx=15, pady=(0, 10))

        # -- SUB-SEÇÃO B: Consumo Atual (Persistido) --
        self.consumo_frame = ctk.CTkFrame(self.col1_frame)
        self.consumo_frame.grid(row=1, column=0, padx=15, pady=(10, 15), sticky="nsew")

        self.lbl_consumo_titulo = ctk.CTkLabel(
            self.consumo_frame, text="Consumo Registrado",
            font=ctk.CTkFont(family="Outfit", size=15, weight="bold"),
            text_color="#1f6aa5", anchor="w"
        )
        self.lbl_consumo_titulo.pack(fill="x", padx=15, pady=10)

        self.scroll_consumo = ctk.CTkScrollableFrame(self.consumo_frame)
        self.scroll_consumo.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def carregar_comanda(self, numero_comanda):
        self.comanda = self.app.service.buscar_comanda(numero_comanda)
        if not self.comanda:
            messagebox.showerror("Erro", "Comanda não encontrada!")
            self.app.selecionar_aba("dashboard")
            return

        self.buffer = {}  # Reinicia o carrinho temporário
        self.selected_category = None
        self.atualizar_view()

    def atualizar_view(self):
        if not self.comanda:
            return

        # Atualiza Títulos
        self.lbl_seletor_titulo.configure(text=f"Lançamento - Comanda #{self.comanda.numero} ({self.comanda.cliente_nome})")

        # 1. Desenhar a Coluna da Esquerda (Categorias ou Produtos da categoria)
        self.desenhar_seletor()

        # 2. Desenhar a Coluna da Direita (Buffer e Consumo atual)
        self.desenhar_buffer_carrinho()
        self.desenhar_consumo_registrado()

    def mudar_categoria(self, categoria):
        self.selected_category = categoria
        self.desenhar_seletor()

    def desenhar_seletor(self):
        # Limpar área do seletor
        for widget in self.scroll_selector.winfo_children():
            widget.destroy()

        if self.selected_category is None:
            # --- VISAO DE CATEGORIAS ---
            lbl_instrucao = ctk.CTkLabel(
                self.scroll_selector, text="Selecione uma Categoria:",
                font=ctk.CTkFont(size=13, weight="bold"), anchor="w"
            )
            lbl_instrucao.pack(fill="x", padx=10, pady=(5, 10))

            # Extrai categorias únicas cadastradas
            categorias = sorted(list(set(p.categoria for p in self.app.cardapio.produtos)))

            if not categorias:
                lbl_aviso = ctk.CTkLabel(
                    self.scroll_selector, text="Nenhum produto/categoria cadastrado no cardápio.",
                    font=ctk.CTkFont(size=12, slant="italic"), text_color="gray"
                )
                lbl_aviso.pack(pady=40)
                return

            # Grid de Categorias (2 colunas)
            grid_cat = ctk.CTkFrame(self.scroll_selector, fg_color="transparent")
            grid_cat.pack(fill="both", expand=True)
            grid_cat.grid_columnconfigure((0, 1), weight=1, uniform="equal")

            for idx, cat in enumerate(categorias):
                row = idx // 2
                col = idx % 2

                btn = ctk.CTkButton(
                    grid_cat, text=cat.upper(), height=65,
                    font=ctk.CTkFont(weight="bold", size=13),
                    fg_color="#1f6aa5", hover_color="#1a5885",
                    command=lambda c=cat: self.mudar_categoria(c)
                )
                btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        else:
            # --- VISAO DE PRODUTOS ---
            header_sub = ctk.CTkFrame(self.scroll_selector, fg_color="transparent")
            header_sub.pack(fill="x", padx=5, pady=(5, 10))

            btn_back = ctk.CTkButton(
                header_sub, text="← Categorias", width=90, height=28,
                fg_color="gray", hover_color="dimgray",
                command=lambda: self.mudar_categoria(None)
            )
            btn_back.pack(side="left")

            lbl_cat_nome = ctk.CTkLabel(
                header_sub, text=f" Categoria: {self.selected_category}",
                font=ctk.CTkFont(size=14, weight="bold"), anchor="w"
            )
            lbl_cat_nome.pack(side="left", padx=10)

            # Filtra produtos da categoria
            produtos = [p for p in self.app.cardapio.produtos if p.categoria == self.selected_category]

            # Grid de Produtos (2 colunas)
            grid_prod = ctk.CTkFrame(self.scroll_selector, fg_color="transparent")
            grid_prod.pack(fill="both", expand=True)
            grid_prod.grid_columnconfigure((0, 1), weight=1, uniform="equal")

            for idx, prod in enumerate(produtos):
                row = idx // 2
                col = idx % 2

                btn_text = f"{prod.nome}\nR$ {prod.preco:.2f}"
                btn = ctk.CTkButton(
                    grid_prod, text=btn_text, height=65,
                    font=ctk.CTkFont(weight="bold", size=12),
                    fg_color="#1f6aa5", text_color="white",
                    hover_color="#1a5885",
                    command=lambda p=prod: self.adicionar_ao_buffer(p)
                )
                btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

    def adicionar_ao_buffer(self, produto):
        self.buffer[produto.id] = self.buffer.get(produto.id, 0) + 1
        self.desenhar_buffer_carrinho()

    def alterar_quantidade_buffer(self, produto_id, diff):
        if produto_id in self.buffer:
            self.buffer[produto_id] += diff
            if self.buffer[produto_id] <= 0:
                self.buffer.pop(produto_id)
            self.desenhar_buffer_carrinho()

    def desenhar_buffer_carrinho(self):
        # Limpar widgets do scroll do buffer
        for widget in self.scroll_buffer.winfo_children():
            widget.destroy()

        if not self.buffer:
            lbl_aviso = ctk.CTkLabel(
                self.scroll_buffer, text="Carrinho vazio.\nClique nos produtos para adicionar.",
                font=ctk.CTkFont(size=12, slant="italic"), text_color="gray"
            )
            lbl_aviso.pack(pady=30)
            self.btn_enviar_pedido.configure(text="Enviar Pedidos (0)", fg_color="gray", state="disabled")
            return

        total_itens = 0
        for prod_id, qtd in self.buffer.items():
            total_itens += qtd
            produto = self.app.cardapio.buscar_produto(prod_id)
            if not produto:
                continue

            card = ctk.CTkFrame(self.scroll_buffer, fg_color=("gray95", "gray25"))
            card.pack(fill="x", padx=5, pady=3)

            lbl = ctk.CTkLabel(
                card, text=f"{qtd}x {produto.nome}",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            lbl.pack(side="left", padx=10, pady=5)

            # Botões de controle de quantidade
            ctrl_frame = ctk.CTkFrame(card, fg_color="transparent")
            ctrl_frame.pack(side="right", padx=10, pady=5)

            btn_dec = ctk.CTkButton(
                ctrl_frame, text="-", width=24, height=24, fg_color="#d32f2f", hover_color="#b71c1c",
                command=lambda pid=prod_id: self.alterar_quantidade_buffer(pid, -1)
            )
            btn_dec.pack(side="left", padx=2)

            btn_inc = ctk.CTkButton(
                ctrl_frame, text="+", width=24, height=24, fg_color="#2e7d32", hover_color="#1b5e20",
                command=lambda pid=prod_id: self.alterar_quantidade_buffer(pid, 1)
            )
            btn_inc.pack(side="left", padx=2)

        # Habilitar botão de enviar
        self.btn_enviar_pedido.configure(
            text=f"Enviar Pedidos ({total_itens})",
            fg_color="#2e7d32", hover_color="#1b5e20",
            state="normal"
        )

    def desenhar_consumo_registrado(self):
        # Limpar widgets do scroll do consumo registrado
        for widget in self.scroll_consumo.winfo_children():
            widget.destroy()

        if not self.comanda or not self.comanda.itens:
            lbl_aviso = ctk.CTkLabel(
                self.scroll_consumo, text="Nenhum item consumido ainda.",
                font=ctk.CTkFont(size=12, slant="italic"), text_color="gray"
            )
            lbl_aviso.pack(pady=30)
            return

        for item in self.comanda.itens:
            card = ctk.CTkFrame(self.scroll_consumo, fg_color=("gray95", "gray25"))
            card.pack(fill="x", padx=5, pady=3)

            lbl_desc = ctk.CTkLabel(
                card, text=f"{item.quantidade} x {item.produto.nome}",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            lbl_desc.pack(side="left", padx=10, pady=8)

            # Botão de transferência (Apenas para Gerente/Administrador)
            if self.app.usuario.cargo in ["Gerente", "Administrador"]:
                btn_transf = ctk.CTkButton(
                    card, text="Transferir", fg_color="#d97706", hover_color="#b45309", width=80, height=24,
                    command=lambda i=item: self.abrir_dialogo_transferencia(i)
                )
                btn_transf.pack(side="right", padx=10, pady=8)

            lbl_sub = ctk.CTkLabel(
                card, text=f"R$ {item.calc_subtotal():.2f}",
                font=ctk.CTkFont(size=12)
            )
            lbl_sub.pack(side="right", padx=10, pady=8)

    def abrir_dialogo_transferencia(self, item_comanda):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Transferir Item")
        dialog.geometry("380x280")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.focus_force()

        lbl_titulo = ctk.CTkLabel(
            dialog, text="Transferência de Item",
            font=ctk.CTkFont(family="Outfit", size=16, weight="bold"),
            text_color="#1f6aa5"
        )
        lbl_titulo.pack(pady=(20, 15))

        lbl_info = ctk.CTkLabel(
            dialog, text=f"Item: {item_comanda.produto.nome} (Qtd. Max: {item_comanda.quantidade})",
            font=ctk.CTkFont(size=12)
        )
        lbl_info.pack(anchor="w", padx=30, pady=(0, 10))

        # Entrada de Quantidade a transferir
        lbl_qtd = ctk.CTkLabel(dialog, text="Quantidade a Transferir", font=ctk.CTkFont(size=11))
        lbl_qtd.pack(anchor="w", padx=30)
        entry_qtd = ctk.CTkEntry(dialog, width=320)
        entry_qtd.insert(0, str(item_comanda.quantidade))
        entry_qtd.pack(padx=30, pady=(0, 10))

        # Dropdown de comanda de destino
        lbl_dest = ctk.CTkLabel(dialog, text="Comanda de Destino", font=ctk.CTkFont(size=11))
        lbl_dest.pack(anchor="w", padx=30)

        # Filtra comandas ativas exceto a atual
        comandas_destino = [str(num) for num in self.app.service.comandas_ativas.keys() if num != self.comanda.numero]
        if not comandas_destino:
            comandas_destino = ["Nenhuma outra comanda aberta"]

        combo_dest = ctk.CTkOptionMenu(dialog, values=comandas_destino, width=320)
        combo_dest.pack(padx=30, pady=(0, 20))

        def confirmar():
            dest_str = combo_dest.get()
            if dest_str == "Nenhuma outra comanda aberta":
                messagebox.showerror("Erro", "Não há nenhuma outra comanda aberta para receber o item!", parent=dialog)
                return

            try:
                dest_num = int(dest_str)
                qtd_transferir = int(entry_qtd.get().strip())
                if qtd_transferir <= 0 or qtd_transferir > item_comanda.quantidade:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", f"A quantidade deve ser um número inteiro de 1 a {item_comanda.quantidade}!", parent=dialog)
                return

            dest_comanda = self.app.service.buscar_comanda(dest_num)
            if not dest_comanda:
                messagebox.showerror("Erro", "Comanda de destino inválida!", parent=dialog)
                return

            # Efetuar a transferência
            # 1. Adicionar ao destino
            dest_comanda.adicionar_item(item_comanda.produto, qtd_transferir)

            # 2. Deduzir da comanda atual
            item_comanda.quantidade -= qtd_transferir
            if item_comanda.quantidade <= 0:
                self.comanda.itens.remove(item_comanda)

            # Salvar
            salvar_comandas(self.app.service.comandas_ativas)

            messagebox.showinfo("Sucesso", f"Transferido(s) {qtd_transferir}x {item_comanda.produto.nome} para comanda #{dest_num}!", parent=dialog)
            dialog.destroy()
            self.atualizar_view()

        btn_confirmar = ctk.CTkButton(dialog, text="Confirmar Transferência", height=35, command=confirmar)
        btn_confirmar.pack(padx=30, fill="x")

    def enviar_buffer(self):
        if not self.comanda or not self.buffer:
            return

        # Lança os produtos do buffer na comanda oficial
        for prod_id, qtd in self.buffer.items():
            produto = self.app.cardapio.buscar_produto(prod_id)
            if produto:
                self.comanda.adicionar_item(produto, qtd)

        # Salva o arquivo de comandas JSON
        salvar_comandas(self.app.service.comandas_ativas)

        # Limpa o buffer local
        self.buffer = {}

        messagebox.showinfo("Sucesso", "Pedido enviado e registrado com sucesso!")
        self.app.selecionar_aba("dashboard")
