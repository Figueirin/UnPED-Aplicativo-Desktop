import customtkinter as ctk
from tkinter import messagebox
from services.persistencia import carregar_usuario, salvar_usuario
from models.usuario import Garcom, Gerente, Administrador

class UsuariosFrame(ctk.CTkFrame):
    def __init__(self, master, app_instance):
        super().__init__(master, fg_color="transparent")
        self.app = app_instance

        # Configurar layout grid (1 linha, 2 colunas com proporções)
        self.grid_columnconfigure(0, weight=1)  # Formulário lateral
        self.grid_columnconfigure(1, weight=2)  # Lista de usuários
        self.grid_rowconfigure(0, weight=1)

        # Lado Esquerdo: Form de Cadastro
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        
        self.lbl_titulo_form = ctk.CTkLabel(
            self.form_frame, text="Cadastrar Novo Usuário",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5"
        )
        self.lbl_titulo_form.pack(pady=20, padx=20, anchor="w")

        # Campo Nome
        self.lbl_nome = ctk.CTkLabel(self.form_frame, text="Nome Completo", font=ctk.CTkFont(size=12))
        self.lbl_nome.pack(anchor="w", padx=20, pady=(10, 2))
        self.entry_nome = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: João da Silva", width=220)
        self.entry_nome.pack(padx=20, pady=(0, 10), fill="x")

        # Campo Username
        self.lbl_username = ctk.CTkLabel(self.form_frame, text="Nome de Usuário (Username)", font=ctk.CTkFont(size=12))
        self.lbl_username.pack(anchor="w", padx=20, pady=(10, 2))
        self.entry_username = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: joao.silva", width=220)
        self.entry_username.pack(padx=20, pady=(0, 10), fill="x")

        # Campo Senha
        self.lbl_senha = ctk.CTkLabel(self.form_frame, text="Senha de Acesso", font=ctk.CTkFont(size=12))
        self.lbl_senha.pack(anchor="w", padx=20, pady=(10, 2))

        self.senha_container = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.senha_container.pack(fill="x", padx=20, pady=(0, 10))

        self.entry_senha = ctk.CTkEntry(self.senha_container, placeholder_text="Mínimo 3 caracteres", show="*", width=170)
        self.entry_senha.pack(side="left", fill="x", expand=True)

        self.btn_show_senha = ctk.CTkButton(
            self.senha_container, text="👁", width=30, height=28, fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray80", "gray30"),
            command=self.toggle_senha
        )
        self.btn_show_senha.pack(side="right", padx=(5, 0))

        # Campo Cargo
        self.lbl_cargo = ctk.CTkLabel(self.form_frame, text="Cargo / Função", font=ctk.CTkFont(size=12))
        self.lbl_cargo.pack(anchor="w", padx=20, pady=(10, 2))
        self.option_cargo = ctk.CTkOptionMenu(self.form_frame, values=["Garcom", "Gerente", "Administrador"])
        self.option_cargo.pack(padx=20, pady=(0, 20), fill="x")

        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(
            self.form_frame, text="Cadastrar Usuário", height=35,
            command=self.cadastrar_usuario
        )
        self.btn_salvar.pack(padx=20, pady=(0, 20), fill="x")

        # Lado Direito: Lista de Usuários
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")

        self.lbl_titulo_lista = ctk.CTkLabel(
            self.list_frame, text="Usuários Cadastrados",
            font=ctk.CTkFont(family="Outfit", size=18, weight="bold"),
            text_color="#1f6aa5"
        )
        self.lbl_titulo_lista.pack(pady=20, padx=20, anchor="w")

        # Frame de scroll para a lista de usuários
        self.scroll_frame = ctk.CTkScrollableFrame(self.list_frame, label_text="Lista de Colaboradores")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Lista interna de usuários carregada da persistência
        self.usuarios = []
        self.atualizar_lista()

    def atualizar_lista(self):
        # Limpar widgets do scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.usuarios = carregar_usuario()

        for u in self.usuarios:
            user_card = ctk.CTkFrame(self.scroll_frame, fg_color=("gray90", "gray20"))
            user_card.pack(fill="x", padx=5, pady=5)

            # Informações do Usuário
            lbl_info = ctk.CTkLabel(
                user_card,
                text=f"Nome: {u.nome}\nUser: {u.username} | Cargo: {u.cargo}",
                justify="left",
                font=ctk.CTkFont(size=12)
            )
            lbl_info.pack(side="left", padx=10, pady=10)

            # Botão de Remoção com base na regra de negócio
            # Se for Administrador, impede a remoção desabilitando o botão
            if u.cargo == "Administrador":
                btn_remover = ctk.CTkButton(
                    user_card, text="Remover", fg_color="gray", state="disabled", width=80
                )
            else:
                btn_remover = ctk.CTkButton(
                    user_card, text="Remover", fg_color="#d32f2f", hover_color="#b71c1c", width=80,
                    command=lambda username=u.username: self.remover_usuario(username)
                )
            btn_remover.pack(side="right", padx=10, pady=10)

    def cadastrar_usuario(self):
        nome = self.entry_nome.get().strip()
        username = self.entry_username.get().strip().lower()
        senha = self.entry_senha.get().strip()
        cargo = self.option_cargo.get()

        if not nome or not username or not senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        if len(senha) < 3:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 3 caracteres!")
            return

        # Verifica se o nome de usuário já existe
        for u in self.usuarios:
            if u.username == username:
                messagebox.showerror("Erro", "Este Nome de Usuário já está cadastrado!")
                return

        # Instancia e adiciona o usuário
        if cargo == "Garcom":
            novo_usuario = Garcom(username, senha, nome)
        elif cargo == "Gerente":
            novo_usuario = Gerente(username, senha, nome)
        elif cargo == "Administrador":
            novo_usuario = Administrador(username, senha, nome)

        self.usuarios.append(novo_usuario)
        salvar_usuario(self.usuarios)
        
        # Limpar campos do form
        self.entry_nome.delete(0, "end")
        self.entry_username.delete(0, "end")
        self.entry_senha.delete(0, "end")

        messagebox.showinfo("Sucesso", f"Usuário {nome} cadastrado com sucesso!")
        self.atualizar_lista()

    def remover_usuario(self, username):
        # Confirmação antes de remover
        if not messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o usuário '{username}'?"):
            return

        # Filtra a lista removendo o usuário correspondente
        novos_usuarios = [u for u in self.usuarios if u.username != username]
        salvar_usuario(novos_usuarios)

        messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")
        self.atualizar_lista()

    def toggle_senha(self):
        if self.entry_senha.cget("show") == "*":
            self.entry_senha.configure(show="")
            self.btn_show_senha.configure(text="🔒")
        else:
            self.entry_senha.configure(show="*")
            self.btn_show_senha.configure(text="👁")
