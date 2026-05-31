import customtkinter as ctk

#from views.dashboard import DashboardFrame
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

        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame, text="Dashboard", fg_color="transparent",
            text_color=("gray10", "gray90"), anchor="w",
            command=lambda: self.selecionar_aba("dashboard")
        )
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

if __name__ == "__main__":
    app = App(None, None)
    app.mainloop()




