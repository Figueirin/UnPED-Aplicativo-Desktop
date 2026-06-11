import customtkinter as ctk
from tkinter import messagebox
from services.persistencia import salvar_comandas

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, app_instance):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance

        # Layout principal (1 linha, 1 coluna)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Cabeçalho: Título e Botão Nova Comanda
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(10, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.header_label = ctk.CTkLabel(
            self.header_frame, text="Painel de Comandas Abertas",
            font=ctk.CTkFont(family="Outfit", size=22, weight="bold"),
            text_color="#1f6aa5"
        )
        self.header_label.grid(row=0, column=0, sticky="w")

        self.btn_nova_comanda = ctk.CTkButton(
            self.header_frame, text="+ Abrir Nova Comanda",
            font=ctk.CTkFont(weight="bold"),
            command=self.abrir_dialogo_nova_comanda
        )
        self.btn_nova_comanda.grid(row=0, column=1, sticky="e")

        # Scroll Frame para conter o grid/lista de comandas
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

        self.atualizar()

    def atualizar(self):
        # Limpar widgets anteriores
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        comandas = list(self.app.service.comandas_ativas.values())

        if not comandas:
            lbl_vazio = ctk.CTkLabel(
                self.scroll_frame, text="Nenhuma comanda aberta no momento.\nClique no botão acima para abrir uma nova!",
                font=ctk.CTkFont(size=14, slant="italic"),
                text_color="gray"
            )
            lbl_vazio.pack(pady=50)
            return

        # Container interno para grid das comandas (3 colunas dinâmicas)
        self.grid_container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.grid_container.pack(fill="both", expand=True)
        self.grid_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        for idx, c in enumerate(comandas):
            # Criar um card para cada comanda
            row = idx // 3
            col = idx % 3

            card = ctk.CTkFrame(self.grid_container, border_width=1, border_color=("gray80", "gray30"))
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card.grid_columnconfigure(0, weight=1)

            # Número da Comanda & Cliente
            lbl_num = ctk.CTkLabel(
                card, text=f"Comanda #{c.numero}",
                font=ctk.CTkFont(family="Outfit", size=16, weight="bold"),
                text_color="#1f6aa5"
            )
            lbl_num.grid(row=0, column=0, padx=15, pady=(15, 2), sticky="w")

            lbl_cliente = ctk.CTkLabel(
                card, text=f"Cliente: {c.cliente_nome}",
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w"
            )
            lbl_cliente.grid(row=1, column=0, padx=15, pady=2, sticky="w")

            # Subtotal parcial
            subtotal = c.calcular_total()
            lbl_valor = ctk.CTkLabel(
                card, text=f"Subtotal: R$ {subtotal:.2f}",
                font=ctk.CTkFont(size=12, slant="italic"),
                text_color="gray"
            )
            lbl_valor.grid(row=2, column=0, padx=15, pady=(2, 15), sticky="w")

            # Botões de ação
            btn_ver = ctk.CTkButton(
                card, text="Ver / Lançar", height=28,
                command=lambda num=c.numero: self.app.ir_para_detalhes(num)
            )
            btn_ver.grid(row=3, column=0, padx=15, pady=(0, 8), sticky="ew")

            btn_fechar = ctk.CTkButton(
                card, text="Fechar Conta", height=28, fg_color="#2e7d32", hover_color="#1b5e20",
                command=lambda num=c.numero: self.app.ir_para_fechamento(num)
            )
            btn_fechar.grid(row=4, column=0, padx=15, pady=(0, 15), sticky="ew")

    def abrir_dialogo_nova_comanda(self):
        # Cria uma janela Toplevel estilizada para pedir os dados da nova comanda
        dialog = ctk.CTkToplevel(self)
        dialog.title("Nova Comanda")
        dialog.geometry("350x280")
        dialog.resizable(False, False)
        dialog.grab_set()  # Torna a janela modal
        dialog.focus_force()

        lbl_titulo = ctk.CTkLabel(
            dialog, text="Abertura de Comanda",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5"
        )
        lbl_titulo.pack(pady=(20, 15))

        # Campo Número
        lbl_num = ctk.CTkLabel(dialog, text="Número da Comanda (Apenas Inteiro)", font=ctk.CTkFont(size=12))
        lbl_num.pack(anchor="w", padx=30)
        entry_num = ctk.CTkEntry(dialog, placeholder_text="Ex: 10", width=290)
        entry_num.pack(padx=30, pady=(0, 10))

        # Campo Nome do Cliente
        lbl_nome = ctk.CTkLabel(dialog, text="Nome do Cliente", font=ctk.CTkFont(size=12))
        lbl_nome.pack(anchor="w", padx=30)
        entry_nome = ctk.CTkEntry(dialog, placeholder_text="Ex: Renato", width=290)
        entry_nome.pack(padx=30, pady=(0, 20))

        def confirmar():
            num_str = entry_num.get().strip()
            nome = entry_nome.get().strip()

            if not num_str or not nome:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!", parent=dialog)
                return

            try:
                num = int(num_str)
                if num <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "O número da comanda deve ser um inteiro válido maior que zero!", parent=dialog)
                return

            # Tenta abrir a comanda
            sucesso = self.app.service.abrir_comanda(num, nome)
            if sucesso:
                salvar_comandas(self.app.service.comandas_ativas)
                messagebox.showinfo("Sucesso", f"Comanda #{num} aberta para {nome}!", parent=dialog)
                dialog.destroy()
                self.atualizar()
                self.app.ir_para_detalhes(num)
            else:
                messagebox.showerror("Erro", f"A comanda #{num} já está ativa no sistema!", parent=dialog)

        btn_confirmar = ctk.CTkButton(dialog, text="Abrir Comanda", height=35, command=confirmar)
        btn_confirmar.pack(padx=30, fill="x")