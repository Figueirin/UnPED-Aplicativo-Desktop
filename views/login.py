import customtkinter as ctk
from tkinter import messagebox
from services.persistencia import carregar_usuario, salvar_usuario
from app import App

class LoginWindow(ctk.CTk):
    def __init__(self, service, cardapio):
        super().__init__()
        
        self.service = service
        self.cardapio = cardapio
        
        # Carrega os usuários a partir do JSON
        self.usuarios = carregar_usuario()

        # Configurações da Janela de Login
        self.title("UnPED - Acesso do Colaborador")
        self.geometry("400x475")
        self.resizable(False, False)

        # Container Principal
        self.main_frame = ctk.CTkFrame(self, width=350, height=430)
        self.main_frame.pack(expand=True, padx=20, pady=20)
        self.main_frame.pack_propagate(False)

        # Roteamento de telas na inicialização
        if not self.usuarios:
            self.desenhar_registro_admin_inicial()
        else:
            self.desenhar_login_normal()

    def desenhar_login_normal(self):
        # Limpar main_frame de qualquer widget anterior
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Título da Tela
        self.title_label = ctk.CTkLabel(
            self.main_frame, text="UnPED Login", 
            font=ctk.CTkFont(family="Outfit", size=26, weight="bold"),
            text_color="#1f6aa5"
        )
        self.title_label.pack(pady=(35, 20))

        # Campo Usuário
        self.lbl_user = ctk.CTkLabel(self.main_frame, text="Nome de Usuário", font=ctk.CTkFont(size=12))
        self.lbl_user.pack(anchor="w", padx=30, pady=(10, 2))
        self.entry_user = ctk.CTkEntry(self.main_frame, placeholder_text="Ex: garcom1", width=290)
        self.entry_user.pack(padx=30, pady=(0, 15))

        # Campo Senha
        self.lbl_pass = ctk.CTkLabel(self.main_frame, text="Senha", font=ctk.CTkFont(size=12))
        self.lbl_pass.pack(anchor="w", padx=30, pady=(10, 2))

        self.pass_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.pass_container.pack(fill="x", padx=30, pady=(0, 30))

        self.entry_pass = ctk.CTkEntry(self.pass_container, placeholder_text="Senha", show="*", width=240)
        self.entry_pass.pack(side="left", fill="x", expand=True)

        self.btn_show_pass = ctk.CTkButton(
            self.pass_container, text="👁", width=30, height=28, fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray80", "gray30"),
            command=self.toggle_senha
        )
        self.btn_show_pass.pack(side="right", padx=(5, 0))

        # Botão Entrar
        self.btn_login = ctk.CTkButton(
            self.main_frame, text="Autenticar", height=40, width=290,
            command=self.tentar_login
        )
        self.btn_login.pack(padx=30)

    def desenhar_registro_admin_inicial(self):
        # Limpar main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Título da Tela
        self.title_label = ctk.CTkLabel(
            self.main_frame, text="Cadastrar Admin Inicial", 
            font=ctk.CTkFont(family="Outfit", size=20, weight="bold"),
            text_color="#1f6aa5"
        )
        self.title_label.pack(pady=(20, 10))

        # Informação de que é o administrador inicial
        self.lbl_aviso = ctk.CTkLabel(
            self.main_frame, 
            text="Nenhum usuário cadastrado no sistema.\nCadastre o administrador do sistema para iniciar.",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="gray"
        )
        self.lbl_aviso.pack(pady=(0, 15))

        # Campo Nome Completo
        self.lbl_admin_nome = ctk.CTkLabel(self.main_frame, text="Nome Completo", font=ctk.CTkFont(size=12))
        self.lbl_admin_nome.pack(anchor="w", padx=30, pady=(5, 2))
        self.entry_admin_nome = ctk.CTkEntry(self.main_frame, placeholder_text="Ex: Renato Rodrigues", width=290)
        self.entry_admin_nome.pack(padx=30, pady=(0, 10))

        # Campo Nome de Usuário (Username)
        self.lbl_admin_user = ctk.CTkLabel(self.main_frame, text="Nome de Usuário (Username)", font=ctk.CTkFont(size=12))
        self.lbl_admin_user.pack(anchor="w", padx=30, pady=(5, 2))
        self.entry_admin_user = ctk.CTkEntry(self.main_frame, placeholder_text="Ex: admin", width=290)
        self.entry_admin_user.pack(padx=30, pady=(0, 10))

        # Campo Senha
        self.lbl_admin_pass = ctk.CTkLabel(self.main_frame, text="Senha de Acesso", font=ctk.CTkFont(size=12))
        self.lbl_admin_pass.pack(anchor="w", padx=30, pady=(5, 2))

        self.pass_container_admin = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.pass_container_admin.pack(fill="x", padx=30, pady=(0, 20))

        # Guardamos a referência do campo de senha ativo para o botão de visualização
        self.entry_pass = ctk.CTkEntry(self.pass_container_admin, placeholder_text="Mínimo 3 caracteres", show="*", width=240)
        self.entry_pass.pack(side="left", fill="x", expand=True)

        self.btn_show_pass = ctk.CTkButton(
            self.pass_container_admin, text="👁", width=30, height=28, fg_color="transparent",
            text_color=("gray10", "gray90"), hover_color=("gray80", "gray30"),
            command=self.toggle_senha
        )
        self.btn_show_pass.pack(side="right", padx=(5, 0))

        # Botão Cadastrar
        self.btn_cadastrar_admin = ctk.CTkButton(
            self.main_frame, text="Criar Administrador", height=40, width=290,
            command=self.cadastrar_admin_inicial
        )
        self.btn_cadastrar_admin.pack(padx=30)

    def tentar_login(self):
        username = self.entry_user.get().strip()
        senha = self.entry_pass.get().strip()

        usuario_encontrado = None
        for u in self.usuarios:
            if u.username == username and u.senha == senha:
                usuario_encontrado = u
                break

        if usuario_encontrado:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario_encontrado.nome} ({usuario_encontrado.cargo})!")
            
            # Fecha a janela de login e abre a janela principal
            self.destroy()
            main_app = App(self.service, self.cardapio, usuario_encontrado)
            main_app.mainloop()
        else:
            messagebox.showerror("Acesso Negado", "Nome de usuário ou senha inválidos!")

    def cadastrar_admin_inicial(self):
        nome = self.entry_admin_nome.get().strip()
        username = self.entry_admin_user.get().strip().lower()
        senha = self.entry_pass.get().strip()

        if not nome or not username or not senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        if len(senha) < 3:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 3 caracteres!")
            return

        from models.usuario import Administrador

        # Cria e salva o Administrador inicial
        novo_admin = Administrador(username, senha, nome)
        self.usuarios = [novo_admin]
        salvar_usuario(self.usuarios)

        messagebox.showinfo("Sucesso", f"Administrador '{nome}' cadastrado com sucesso!")
        
        # Fecha a tela de login e inicia logado
        self.destroy()
        main_app = App(self.service, self.cardapio, novo_admin)
        main_app.mainloop()

    def toggle_senha(self):
        if self.entry_pass.cget("show") == "*":
            self.entry_pass.configure(show="")
            self.btn_show_pass.configure(text="🔒")
        else:
            self.entry_pass.configure(show="*")
            self.btn_show_pass.configure(text="👁")
