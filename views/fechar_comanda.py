import customtkinter as ctk
from tkinter import messagebox
from services.persistencia import salvar_comandas

class FecharComandaFrame(ctk.CTkFrame):
    def __init__(self, master, app_instance):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance
        self.comanda = None
        self.pago_acumulado = 0.0

        # Layout principal (1 linha, 2 colunas: extrato na esquerda, painel de pagamento na direita)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Extrato (Cupom)
        self.grid_columnconfigure(1, weight=1)  # Caixa de Pagamento

        # --- COLUNA 0: Extrato (Cupom Fiscal) ---
        self.extrato_frame = ctk.CTkFrame(self)
        self.extrato_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        # Botão de Voltar
        self.btn_voltar = ctk.CTkButton(
            self.extrato_frame, text="← Voltar ao Dashboard", fg_color="transparent",
            text_color=("#1f6aa5", "#1f6aa5"), hover_color=("gray90", "gray30"),
            command=lambda: self.app.selecionar_aba("dashboard")
        )
        self.btn_voltar.pack(anchor="w", padx=15, pady=(15, 5))

        self.lbl_extrato_titulo = ctk.CTkLabel(
            self.extrato_frame, text="Extrato Parcial/Final",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5", anchor="w"
        )
        self.lbl_extrato_titulo.pack(fill="x", padx=20, pady=(5, 15))

        # Caixa de texto com fonte mono para exibir a Comanda (Cupom)
        self.txt_extrato = ctk.CTkTextbox(
            self.extrato_frame, font=ctk.CTkFont(family="Courier", size=12),
            wrap="none", state="disabled"
        )
        self.txt_extrato.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # --- COLUNA 1: Caixa de Pagamento ---
        self.pagamento_frame = ctk.CTkFrame(self)
        self.pagamento_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")

        self.lbl_pag_titulo = ctk.CTkLabel(
            self.pagamento_frame, text="Registrar Pagamentos",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5", anchor="w"
        )
        self.lbl_pag_titulo.pack(fill="x", padx=20, pady=20)

        self.checkout_panel = ctk.CTkFrame(self.pagamento_frame, fg_color=("gray95", "gray25"))
        self.checkout_panel.pack(fill="x", padx=20, pady=(0, 20))

        # Rótulos de Valores
        self.lbl_pago_acumulado = ctk.CTkLabel(
            self.checkout_panel, text="Total Pago: R$ 0.00",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.lbl_pago_acumulado.pack(anchor="w", padx=15, pady=(15, 2))

        self.lbl_falta_troco = ctk.CTkLabel(
            self.checkout_panel, text="Falta pagar: R$ 0.00",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#d32f2f"
        )
        self.lbl_falta_troco.pack(anchor="w", padx=15, pady=(0, 15))

        # Entrada de Valor Pago
        self.lbl_valor_pago = ctk.CTkLabel(self.checkout_panel, text="Valor do Pagamento (R$)", font=ctk.CTkFont(size=12))
        self.lbl_valor_pago.pack(anchor="w", padx=15)

        self.entry_pagamento = ctk.CTkEntry(self.checkout_panel, placeholder_text="Ex: 50.00", width=180)
        self.entry_pagamento.pack(anchor="w", padx=15, pady=(0, 10))

        self.btn_pagar = ctk.CTkButton(
            self.checkout_panel, text="Registrar Pagamento",
            command=self.registrar_pagamento
        )
        self.btn_pagar.pack(anchor="w", padx=15, pady=(0, 15))

        # Botão Fechar Comanda (Completo)
        self.btn_fechar_comanda = ctk.CTkButton(
            self.checkout_panel, text="Encerrar Conta", fg_color="gray", state="disabled",
            height=35, command=self.concluir_fechamento
        )
        self.btn_fechar_comanda.pack(fill="x", padx=15, pady=(5, 15))

    def carregar_comanda(self, numero_comanda):
        self.comanda = self.app.service.buscar_comanda(numero_comanda)
        if not self.comanda:
            messagebox.showerror("Erro", "Comanda não encontrada!")
            self.app.selecionar_aba("dashboard")
            return

        self.pago_acumulado = 0.0
        self.atualizar_view()

    def atualizar_view(self):
        if not self.comanda:
            return

        # Atualizar Cupom
        self.txt_extrato.configure(state="normal")
        self.txt_extrato.delete("1.0", "end")
        self.txt_extrato.insert("1.0", str(self.comanda))
        self.txt_extrato.configure(state="disabled")

        # Atualizar Valores de Pagamento
        subtotal = self.comanda.calcular_total()
        taxa = subtotal * 0.10
        total_geral = subtotal + taxa

        self.lbl_pago_acumulado.configure(text=f"Total Pago: R$ {self.pago_acumulado:.2f}")

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

    def registrar_pagamento(self):
        if not self.comanda:
            return

        pag_str = self.entry_pagamento.get().strip()
        try:
            valor = float(pag_str)
            if valor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor de pagamento válido maior que zero!", parent=self)
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

        msg = f"Deseja fechar e encerrar a comanda #{self.comanda.numero}?"
        if troco > 0:
            msg += f"\nTroco a ser devolvido: R$ {troco:.2f}"

        if not messagebox.askyesno("Fechar Comanda", msg, parent=self):
            return

        # Executa fechamento no serviço e salva
        self.app.service.fechar_comanda(self.comanda.numero)
        salvar_comandas(self.app.service.comandas_ativas)

        messagebox.showinfo("Sucesso", f"Comanda #{self.comanda.numero} encerrada com sucesso!", parent=self)
        self.comanda = None
        self.app.selecionar_aba("dashboard")
