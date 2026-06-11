import customtkinter as ctk

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, app_instance):
        #master = container pricipal
        #app_instace = ref para acessar os services e os dados
        super().__init__(master, fg_color="transparent")
        self.app = app_instance

        self.header_label = ctk.CTkLabel(
            self, text="Painel de Comandas abertas",
            font=ctk.CTkFont(family="Outfit", size=14, weight="bold")
        )
        self.header_label.pack(anchor="w", padx=20, pady=20)

    def atualizar(self):
        pass