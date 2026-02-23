
import customtkinter as ctk
from interfaces.components.button import Button

class ConfirmModal(ctk.CTkToplevel):
    def __init__(
            self,
            master,
            title="Confirmation",
            message="Annuler le scan ?",
            on_confirm=None
        ):

        super().__init__(master)
        
        # Configuration de la fenêtre popup
        self.title(title)
        self.geometry("350x200")
        self.configure(fg_color="#111821")
        self.resizable(False, False)
        
        # Rendre le modal prioritaire
        self.transient(master)
        self.lift()

        # Texte d'avertissement
        self.icon = ctk.CTkLabel(self, text="⚠️", font=("Inter", 40))
        self.icon.pack(pady=(20, 5))
        
        self.msg_label = ctk.CTkLabel(self, text=message, font=("Inter", 14), text_color="white")
        self.msg_label.pack(pady=10)

        # Conteneur pour les DEUX boutons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20, fill="x", padx=20)

        # 1. Bouton pour Annuler le popup
        self.btn_cancel = Button(
            self.btn_frame, "Non, rester",
            fg_color=self.master.colors.get("bs_border"),
            hover_color="#334155",
            width=150, height=65,
            command=self.destroy
        )
        self.btn_cancel.pack(side="left", padx=10, expand=True)

        # 2. Bouton pour confirmer l'annulation du scan
        self.btn_confirm = Button(
            self.btn_frame, 
            text="Oui, arrêter",
            fg_color=self.master.colors.get("bs_danger"), 
            hover_color="#dc2626",
            width=150, height=65,
            command=lambda: self.confirm_action(on_confirm) 
        )
        self.btn_confirm.pack(side="right", padx=10, expand=True)

    def confirm_action(self, callback):

        if callback:
            # Appelle de la méthode stop_can()
            callback()

        self.destroy()