
import tkinter as tk
import customtkinter as ctk
from utils.color import get_color
from interfaces.components.button import Button
from interfaces.components.confirm_modal import ConfirmModal

class AuditPage(ctk.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(
            master=parent,
            fg_color=get_color().get("bs_card"),
            corner_radius=20,
            border_width=1,
            border_color=get_color().get("bs_card_border"),
            **kwargs
        )

        self.controller = controller
        self.colors = self.controller.colors if hasattr(self.controller, 'colors') else get_color()

        # --- Conteneur d'En-tête Style "Dashboard" ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=30, pady=(30, 20))

        # 1. Barre d'accentuation verticale (donne un look pro instantané)
        self.accent_bar = ctk.CTkFrame(
            self.header_frame, 
            width=4, height=50, 
            fg_color="#3b82f6", # Le bleu de ton bouton
            corner_radius=2
        )
        self.accent_bar.pack(side="left", padx=(0, 15))

        # 2. Conteneur de textes
        self.text_stack = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.text_stack.pack(side="left", fill="y")

        # Titre avec un espacement de caractères plus moderne
        self.title_label = ctk.CTkLabel(
            self.text_stack, 
            text="Analyse du Périmètre et de la Surface Interne".upper(), 
            font=("Inter", 22, "bold"), 
            text_color="white",
            anchor="w"
        )
        self.title_label.pack(fill="x")
        
        # Sous-titre avec une couleur "slate" pour le contraste
        self.desc_label = ctk.CTkLabel(
            self.text_stack, 
            text="Analyse contrôlée des actifs et détection des vulnérabilités réseaux.", 
            font=("Inter", 13), 
            text_color="#64748b",
            anchor="w"
        )
        self.desc_label.pack(fill="x")

        # Bouton Stop (Caché au début)
        self.stop_btn = Button(
            self.header_frame, "Stoper le scan",
            fg_color=self.colors.get("bs_danger"),
            hover_color= "#dc2626",
            width=150, height=40,
            font=("Inter", 12, "bold"),
            command=self.trigger_modal
        )

        # Badge "Live" à droite
        self.live_badge = ctk.CTkLabel(
            self.header_frame,
            text=" READY ",
            font=("Inter", 10, "bold"),
            text_color="#e2f5ef",
            fg_color="#10b981",
            corner_radius=6
        )

        # Zone Centrale 
        self.center_container = ctk.CTkFrame(self, fg_color="transparent")
        self.center_container.pack(expand=True, fill="both")

        self.network_infos()

        # Canvas pour le Bouton Circulaire
        self.canvas = tk.Canvas(
            self.center_container, width=250, height=250, 
            bg=self.colors.get("bs_card"), highlightthickness=0, cursor="hand2"
        )
        self.canvas.pack()
        
        self.draw_button("#3b82f6") 

        # Événements du bouton
        self.canvas.bind("<Enter>", lambda e: self.draw_button("#60a5fa"))
        self.canvas.bind("<Leave>", lambda e: self.draw_button("#3b82f6"))
        self.canvas.bind("<Button-1>", lambda e: self.start_scan())

        self.log_area = ctk.CTkTextbox(
            self, fg_color=self.colors.get("bs_bg"), text_color="#4ade80", 
            font=("Consolas", 13), border_width=1, border_color="#1e293b"
        )

    # Information du réseau au dessus du bouton
    def network_infos(self):
        active_infos = self.controller.engine.get_active_interface_info()

        self.net_info = ctk.CTkButton(
            self.center_container,
            text=active_infos.get("network", '8.8.8.8'), 
            fg_color="#1e293b",
            hover_color="#334155",
            text_color="#3b82f6",
            width=200, height=35,
            corner_radius=20, font=("Inter", 12, "bold")
        )
        self.net_info.pack(pady=20)

    def draw_button(self, color):
        self.canvas.delete("all")
        # Bordures extérieures
        self.canvas.create_oval(10, 10, 210, 210, outline="#1e293b", width=2)
        # Cercle principal
        self.canvas.create_oval(30, 30, 190, 190, outline=color, width=3)
        
        # Textes
        self.canvas.create_text(
            110, 85, text="INITIATE",
            fill="#64748b", font=("Inter", 10, "bold"))
        self.canvas.create_text(
            110, 115, text="Scan Now",
            fill="white", font=("Inter", 18, "bold"))
        self.canvas.create_text(
            110, 145, text="Click to start",
            fill="#64748b", font=("Inter", 9))

    # Méthode pour démarrer le scan
    def start_scan(self):

        # 1. On cache TOUT le conteneur central d'un coup
        # Cela inclut le bouton reseau et le canvas du cercle
        self.center_container.pack_forget()

        self.stop_btn.pack(side="right", anchor="n", pady=5)

        self.live_badge.pack_forget()

        self.log_area.pack(padx=30, pady=(10, 20), fill="both", expand=True)
        
        self.log_area.insert("0.0", "> Initializing Network Audit...\n")

        self.controller.run_scanner()

        self.after(2000, self.run_init_sequence)

    # Méthode pour arrêter de scanner
    def stop_scan(self):

        self.controller.engine.is_running = False

        self.log_area.insert("end", "\n[!] SCAN STOPPED BY USER\n")
        self.stop_btn.pack_forget()
        self.log_area.pack_forget()

        # On nettoi le champ textarea qui affiche les logs
        self.log_area.delete('0.0', 'end')

        # 4. Réafficher les éléments du menu principal
        self.live_badge.pack(side="right", anchor="n", pady=5)
        self.title_label.pack(anchor="w", padx=30, pady=(30, 0))
        self.desc_label.pack(anchor="w", padx=30, pady=(5, 20))
        self.center_container.pack(expand=True, fill="both")

    # Affiche le texte lettre par lettre sans créer de nouvelle ligne.
    def typewriter_log(self, text, index=0, callback=None):
        if index == 0:
            # Au début d'une nouvelle phrase, on efface l'ancienne ligne
            self.log_area.configure(state="normal")
            self.log_area.delete("1.0", "end") 
            self.log_area.insert("1.0", "> ")

        if index < len(text):
            self.log_area.configure(state="normal")
            self.log_area.insert("end", text[index])
            self.log_area.configure(state="disabled")
            self.log_area.see("end")
            self.after(
                60,
                lambda: self.typewriter_log(text, index + 1, callback)
            )
        elif callback:
            # On laisse la phrase affichée un court instant avant de passer à la suite
            self.after(600, callback)

    def run_init_sequence(self, steps=None):
        if steps is None:
            steps = [
                "Establishing secure connection...",
                "Loading scanning modules...",
                "Identifying active subnets...",
                "Bypassing firewall restrictions...",
                "SentinelNet Engine warming up..."
            ]

        if steps:
            phrase = steps.pop(0)
            self.typewriter_log(phrase, callback=lambda: self.run_init_sequence(steps))
        else:
            # On affiche le message final et on lance le scan
            self.log_area.configure(state="normal")
            self.log_area.delete("1.0", "end")
            self.log_area.insert("1.0", "[!] ENGINE READY - STARTING SCAN... \n")
            self.log_area.configure(state="disabled")
            
            # On laisse le message final 1 seconde avant que les vrais logs arrivent
            self.after(1000, self.controller.run_scanner)

    # Mettre à jour le log dans le log_area(le champ qui affiche le résultat en direct)
    def update_log(self, msg):

        # On déverrouille le champ pour écrire
        self.log_area.configure(state="normal")

        # On insère à la fin
        self.log_area.insert("end", msg)

        # On scroll automatiquement vers le bas
        self.log_area.see("end")

        # On verrouille à nouveau
        self.log_area.configure("desabled")

        self.update_idletasks()
    
    # Afficher le modal de
    def trigger_modal(self):
        ConfirmModal(
            self,
            message="Voulez-vous vraiment stopper?",
            on_confirm=self.stop_scan,
        )
