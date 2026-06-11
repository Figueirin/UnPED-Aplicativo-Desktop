import customtkinter as ctk

# Importa os frames secundários
from views.dashboard import DashboardFrame
from views.detalhe_pedido import DetalhePedidoFrame
from views.cardapio import CardapioFrame
from views.usuarios import UsuariosFrame

class App(ctk.CTk):
    """
    Janela Principal do Sistema UnPED.
    Gerencia a navegação lateral e a exibição das abas de acordo com o cargo do usuário.
    """
    def __init__(self, service, cardapio, usuario):
        super().__init__()
        self.service = service
        self.cardapio = cardapio
        self.usuario = usuario  # Guarda o objeto do usuário logado (Garcom ou Gerente)
        
        # Configuração da janela
        self.title("UnPED - Seu PDV")
        self.geometry("1100x650")

        # Layout do grid principal (1 linha, 2 colunas)
        self.grid_rowconfigure(0, weight=1) # Eixo vertical se expande
        self.grid_columnconfigure(1, weight=1) # Conteúdo principal se expande

        # Criação do Frame da Sidebar (Barra Lateral)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0) 
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        # Adiciona o título UnPED ao topo da sidebar
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="UnPED",
            font=ctk.CTkFont(family="Outfit", size=26, weight="bold"),
            text_color="#1f6aa5"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Exibe o Nome e o Cargo do Colaborador Logado
        self.lbl_usuario = ctk.CTkLabel(
            self.sidebar_frame, 
            text=f"Olá, {self.usuario.nome}\n({self.usuario.cargo})",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="gray"
        )
        self.lbl_usuario.grid(row=1, column=0, padx=20, pady=(0, 20))

        # Botão: Dashboard
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame, text="Dashboard", fg_color="transparent",
            text_color=("gray10", "gray90"), anchor="w",
            command=lambda: self.selecionar_aba("dashboard")
        )
        self.btn_dashboard.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        # Botão: Cardápio (Apenas Gerente poderá interagir)
        self.btn_cardapio = ctk.CTkButton(
            self.sidebar_frame, text="Cardápio", fg_color="transparent",
            text_color=("gray10", "gray90"), anchor="w",
            command=lambda: self.selecionar_aba("cardapio")
        )
        self.btn_cardapio.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        # Botão: Usuários (Apenas Administrador poderá interagir)
        self.btn_usuarios = ctk.CTkButton(
            self.sidebar_frame, text="Usuários", fg_color="transparent",
            text_color=("gray10", "gray90"), anchor="w",
            command=lambda: self.selecionar_aba("usuarios")
        )
        self.btn_usuarios.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        # Restrição de Acesso Baseada em Cargo
        if self.usuario.cargo != "Gerente":
            self.btn_cardapio.configure(state="disabled")
        if self.usuario.cargo != "Administrador":
            self.btn_usuarios.configure(state="disabled")

        # Configura a "mola" da sidebar na linha 5 para empurrar o rodapé de temas para baixo
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # Rótulo de Tema
        self.appearance_label = ctk.CTkLabel(
            self.sidebar_frame, text="Tema Visual",
            anchor="w", font=ctk.CTkFont(size=10)
        )
        self.appearance_label.grid(row=6, column=0, padx=20, pady=(10, 2), sticky="w")

        # Dropdown para alternar o tema do sistema (Light/Dark)
        self.appearence_optionmenu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=["Dark", "Light", "System"],
            command=self.mudar_aparencia
        )
        self.appearence_optionmenu.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Instanciar os frames de conteúdo
        self.frame_dashboard = DashboardFrame(self, self)
        self.frame_detalhes = DetalhePedidoFrame(self, self)
        self.frame_cardapio = CardapioFrame(self, self)
        self.frame_usuarios = UsuariosFrame(self, self)

        # Mostrar tela inicial (Dashboard)
        self.frame_dashboard.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.btn_dashboard.configure(fg_color="#1f6aa5", text_color="white")

    def ir_para_detalhes(self, comanda_numero):
        # Esconder todas as telas
        self.frame_dashboard.grid_forget()
        self.frame_cardapio.grid_forget()
        self.frame_usuarios.grid_forget()

        # Carregar e exibir detalhes da comanda
        self.frame_detalhes.carregar_comanda(comanda_numero)
        self.frame_detalhes.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Atualizar cores do menu (nenhuma aba lateral está ativa)
        self.btn_dashboard.configure(fg_color="transparent", text_color=("gray10", "gray90"))
        self.btn_cardapio.configure(fg_color="transparent", text_color=("gray10", "gray90"))
        self.btn_usuarios.configure(fg_color="transparent", text_color=("gray10", "gray90"))

    def selecionar_aba(self, nome_aba):
        # Esconder todas as telas
        self.frame_dashboard.grid_forget()
        self.frame_detalhes.grid_forget()
        self.frame_cardapio.grid_forget()
        self.frame_usuarios.grid_forget()

        # Resetar estilos de botões da sidebar
        self.btn_dashboard.configure(fg_color="transparent", text_color=("gray10", "gray90"))
        self.btn_cardapio.configure(fg_color="transparent", text_color=("gray10", "gray90"))
        self.btn_usuarios.configure(fg_color="transparent", text_color=("gray10", "gray90"))

        if nome_aba == "dashboard":
            self.frame_dashboard.atualizar()
            self.frame_dashboard.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.btn_dashboard.configure(fg_color="#1f6aa5", text_color="white")
            
        elif nome_aba == "cardapio" and self.usuario.cargo == "Gerente":
            self.frame_cardapio.atualizar_lista()
            self.frame_cardapio.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.btn_cardapio.configure(fg_color="#1f6aa5", text_color="white")
            
        elif nome_aba == "usuarios" and self.usuario.cargo == "Administrador":
            self.frame_usuarios.atualizar_lista()
            self.frame_usuarios.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            self.btn_usuarios.configure(fg_color="#1f6aa5", text_color="white")

    def mudar_aparencia(self, novo_modo_aparencia):
        ctk.set_appearance_mode(novo_modo_aparencia)

if __name__ == "__main__":
    from services.comanda_service import ComandaService
    from models.cardapio import Cardapio
    from services.persistencia import carregar_cardapio, carregar_comandas
    from views.login import LoginWindow

    # 1. Instancia os controladores
    service = ComandaService()
    cardapio = Cardapio()
    
    # 2. Carrega os dados JSON persistidos
    carregar_cardapio(cardapio)
    carregar_comandas(service, cardapio)

    # 3. Abre primeiro a tela de Login
    login = LoginWindow(service, cardapio)
    login.mainloop()

