import customtkinter as ctk
from tkinter import messagebox
from services.persistencia import carregar_usuario
from app import App

class LoginWindow(ctk.CTk):
    def __init__(self, service, cardapio):
        super().__init__()
        
        self.service = service
        self.cardapio = cardapio
        
        # Carrega os usuários a partir do JSON usando a função que você escreveu!
        self.usuarios = carregar_usuario()

        # Configurações da Janela de Login
        self.title("UnPED - Acesso do Colaborador")
        self.geometry("400x450")
        self.resizable(False, False)

        # Container Principal
        self.main_frame = ctk.CTkFrame(self, width=350, height=400)
        self.main_frame.pack(expand=True, padx=20, pady=20)
        self.main_frame.pack_propagate(False)

        # Título da Tela
        self.title_label = ctk.CTkLabel(
            self.main_frame, text="UnPED Login", 
            font=ctk.CTkFont(family="Outfit", size=26, weight="bold"),
            text_color="#1f6aa5"
        )
        self.title_label.pack(pady=(40, 30))

        # Campo Usuário
        self.lbl_user = ctk.CTkLabel(self.main_frame, text="Nome de Usuário", font=ctk.CTkFont(size=12))
        self.lbl_user.pack(anchor="w", padx=30, pady=(10, 2))
        self.entry_user = ctk.CTkEntry(self.main_frame, placeholder_text="Ex: garcom1", width=290)
        self.entry_user.pack(padx=30, pady=(0, 15))

        # Campo Senha (usamos show="*" para esconder os caracteres)
        self.lbl_pass = ctk.CTkLabel(self.main_frame, text="Senha", font=ctk.CTkFont(size=12))
        self.lbl_pass.pack(anchor="w", padx=30, pady=(10, 2))
        self.entry_pass = ctk.CTkEntry(self.main_frame, placeholder_text="Senha", show="*", width=290)
        self.entry_pass.pack(padx=30, pady=(0, 30))

        # Botão Entrar
        self.btn_login = ctk.CTkButton(
            self.main_frame, text="Autenticar", height=40, width=290,
            command=self.tentar_login
        )
        self.btn_login.pack(padx=30)

    def tentar_login(self):
        username = self.entry_user.get().strip()
        senha = self.entry_pass.get().strip()

        # Procura se existe algum usuário com esse username e senha correspondentes
        usuario_encontrado = None
        for u in self.usuarios:
            if u.username == username and u.senha == senha:
                usuario_encontrado = u
                break

        if usuario_encontrado:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario_encontrado.nome} ({usuario_encontrado.cargo})!")
            
            # 1. Fecha a janela de login física da tela
            self.destroy()
            
            # 2. Inicializa a janela principal do sistema passando o usuário autenticado!
            from app import App
            main_app = App(self.service, self.cardapio, usuario_encontrado)
            main_app.mainloop()
        else:
            messagebox.showerror("Acesso Negado", "Nome de usuário ou senha inválidos!")
