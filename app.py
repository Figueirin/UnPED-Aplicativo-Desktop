import customtkinter as ctk

from views.dashboard import DashboardFrame
#from views.detalhe_pedido import DetalhePedidoFrame
#from views.cardapio import CardapioFrame


class App(ctk.CTk):
    def __init__(self, service, cardapio):
        super().__init__()
        self.service = service
        self.cardapio = cardapio
        
        #Configuração da janela
        self.title("UnPED - Seu PDV")
        self.geometry("1050x600")

        #Layout do grid
        self.grid_rowconfigure(0, weight=1) # Menu lateral
        self.grid_columnconfigure(1, weight=1) # Conteudo Principal

        self.sidebar_frame = ctk.CTkFrame(self,width=200, corner_radius=0) 

        #Posiciona o sidebar no grid principal
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        #Adiciona o titulo UnPED ao sidebar
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="UnPED",
            font = ctk.CTkFont(family="Outfit", size=26, weight="bold"),
            text_color = "white"
        )

        self.logo_label.grid(row=0, column=0, padx=20, pady=(20,20))

        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        #botao dashboard
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame, text="Dashboard", fg_color="transparent",
            text_color=("gray10", "gray90"), anchor="w",
            command=lambda: self.selecionar_aba("dashboard")
        )
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        #botao cardapio
        self.btn_cardapio = ctk.CTkButton(
            self.sidebar_frame, text="Cardapio", fg_color="transparent",
            text_color=("gray10", "gray90"), anchor="w",
            command=lambda: self.selecionar_aba("Cardapio")
        )

        self.btn_cardapio.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.appearance_label = ctk.CTkLabel(
            self.sidebar_frame, text="Tema",
            anchor="w", font=ctk.CTkFont(size = 10)
        )
        self.appearance_label.grid(row=4, column=0, padx=0, pady=(10,2), sticky="w")

        self.appearence_optionmenu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=["Dark", "Light", "System"],
            command=self.mudar_aparencia
        )
        self.appearence_optionmenu.grid(row=5, column=0, padx=20, pady=(0,20), sticky="ew")

    def selecionar_aba(self, nome_aba):
        print(f"Aba selecionada: {nome_aba}")

    def mudar_aparencia(self, novo_modo_aparencia):
        ctk.set_appearance_mode(novo_modo_aparencia)


if __name__ == "__main__":
    app = App(None, None)
    app.mainloop()




