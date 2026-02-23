
import customtkinter as ctk
from utils.color import get_color

class AssetPage(ctk.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(master=parent, fg_color="transparent", **kwargs)

        self.controller = controller
        self.colors = self.controller.colors if hasattr(
            self.controller, 'colors') else get_color()
        
        # Liste pour stockés les widgets sur chaques lignes du table
        self.rows = []

        # carte de statistiques
        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.pack(fill="x", pady=(0, 20))
        
        # On configure 4 colonnes de carte
        self.stats_container.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.update_stats_display()

        # Titre au dessus de tableau
        self.table_label = ctk.CTkLabel(
            self, text="● HÔTES DETECTÉS",
            font=("Inter", 16, "bold"),
            text_color="#3498db"
        )
        self.table_label.pack(anchor="w", pady=(10, 15), padx=(20, 0))

        # Tableau d'affichage de machines trouvées sur le réseau
        self.table_container = ctk.CTkFrame(
            self, fg_color=self.colors.get("bs_card"),
            corner_radius=20, border_width=1,
            border_color=self.colors.get("bs_card_border")
        )
        self.table_container.pack(fill="both", expand=True, pady=20, padx=20)

        # En-tête du tableau
        self.setup_table_headers()

        self.content_frame = ctk.CTkFrame(
            self.table_container,
            fg_color="transparent",
            corner_radius=20
        )
        self.content_frame.pack(fill="both", expand=True)

        self.show_empty_state()

        self.refresh_from_db()

    # Affichage de card avec les informations provenant de la base de données
    def update_stats_display(self):
        # Récupération des données réelles
        stats = self.controller.db.get_dashboard_stats()
        
        # Mise à jour des cartes avec les vraies valeurs
        self.create_stat_card(
            0, "APPAREILS TOTAUX", stats["total_devices"],
            "Actifs sur le sous-réseau local", "blue"
        )
        self.create_stat_card(
            1, "RISQUES CRITIQUES", stats["critical_level"],
            "Intervention immédiate requise", "red"
        )
        self.create_stat_card(
            2, "PORTS OUVERTS", stats["total_ports"],
            f"Détectés : {stats['port_list']}...", "orange"
        )
        self.create_stat_card(
            3, "ÉTAT DU SCAN", "TERMINÉ",
            "Dernier scan : À l'instant", "green"
        )

    # Style au cas où le tableau est vide
    def show_empty_state(self):
        
        # Cette boucle néttoie le content_frame au cas où aucune line
        # n'est disponible dans le tableau
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Création d'un style d'affichage si le tableau est vide
        self.empty_view = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.empty_view.pack(expand=True, pady=50)

        self.empty_icon = ctk.CTkLabel(
            self.empty_view, text="🔍", font=("Inter", 50)
        )
        
        self.empty_icon.pack()

        self.empty_text = ctk.CTkLabel(
            self.empty_view, 
            text="AUCUNE INFORMATION DISPONIBLE", 
            font=("Inter", 14, "bold"),
            text_color="#4b5563"
        )
        self.empty_text.pack(pady=10)

        self.empty_subtext = ctk.CTkLabel(
            self.empty_view, 
            text="Lancez un scan pour détecter les hôtes sur le réseau.", 
            font=("Inter", 12),
            text_color=self.colors.get("bs_muted")
        )
        self.empty_subtext.pack()

    # Méthode pour créer une carte
    def create_stat_card(self, col, title, value, subtitle, color_type):

        # Couleurs qui seront utilisées pour les cartes
        bg_color = "#111827" 
        accent = {
            "blue": "#3498db",
            "red": "#e74c3c",
            "orange": "#f39c12",
            "green": "#2ecc71"}[color_type]
        
        # Le conteneur parent de toutes les cartes
        card = ctk.CTkFrame(
            self.stats_container,
            fg_color=bg_color, height=120,
            corner_radius=10, border_width=1,
            border_color="#1f2937"
        )
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        card.grid_propagate(False)

        # Contenu de la carte
        title_lbl = ctk.CTkLabel(
            card, text=title, 
            font=("Inter", 11, "bold"),
            text_color="#94a3b8"
        )
        title_lbl.pack(anchor="w", padx=15, pady=(15, 0))

        val_lbl = ctk.CTkLabel(
            card, text=value,
            font=("Inter", 28, "bold"),
            text_color=accent
        )
        val_lbl.pack(anchor="w", padx=15)

        sub_lbl = ctk.CTkLabel(
            card, text=subtitle,
            font=("Inter", 11),
            text_color="#64748b"
        )
        sub_lbl.pack(anchor="w", padx=15, pady=(0, 10))

    # L'en tête du tableau
    def setup_table_headers(self):
        headers = [
            "TYPE",
            "ADDRESS IP",
            "ADDRESS MAC",
            "PORTS",
            "VENDEUR",
            "OS",
            "NOM DE L'HÔTE",
        ]
        header_frame = ctk.CTkFrame(
            self.table_container,
            corner_radius=20,
            fg_color="#1B2430",
            height=40,
        )
        header_frame.pack(fill="x", padx=10, pady=15)

        # On parcours la liste "headers" pour afficher ses élement un par un dans le CTKLabel
        for i, text in enumerate(headers):

            # On ajuste les poids des colonnes pour que l'IP et le Hostname aient plus de place
            header_frame.grid_columnconfigure(i, weight=1 if i not in [1, 3] else 2)
            lbl = ctk.CTkLabel(
                header_frame, text=text,
                font=("Inter", 11, "bold"),
                text_color="#b8bcc2"
            )
            lbl.grid(row=0, column=i, sticky="w", padx=10)
            
        # Ligne de séparation
        sep = ctk.CTkFrame(self.table_container, fg_color=self.colors.get("bs_bg"), height=1)
        sep.pack(fill="x", padx=10)

    # Méthode pour ajouter les machines trouvées sur le tableau d'affichage
    def add_device_row(self, device):
        # Nettoyage de l'état vide au premier ajout
        if not self.rows:
            for widget in self.content_frame.winfo_children():
                widget.destroy()

        # Création du conteneur de la ligne (Frame avec effet de surbrillance au besoin)
        row_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=45)
        row_frame.pack(fill="x", padx=10, pady=1)
        
        # On réplique la même structure de grille que le header
        for i in range(7):
            row_frame.grid_columnconfigure(i, weight=1 if i not in [1, 3] else 2)

        # Ajout des données dans les colonnes
        ctk.CTkLabel(
            row_frame,
            text="💻",
            font=("Inter", 14)).grid(
                row=0, column=0, sticky="w", padx=10)
        
        # Colonne 1 pour l'address IP 
        ip_address = device.get("ip") or device.get("ip_address") or 'N/A'
        ctk.CTkLabel(
            row_frame,
            text=ip_address,
            font=("Inter", 12, "bold"),
            text_color="#ffffff").grid(
                row=0, column=1, sticky="w", padx=10)
        
        # Colonne 2 pour MAC Address
        mac_address = device.get("mac") or device.get("mac_address") or "N/A"
        ctk.CTkLabel(
            row_frame,
            text=mac_address.upper(),
            font=("Inter", 11), 
            text_color="#94a3b8").grid(
                row=0, column=2, sticky="w", padx=10)
        
        # Colonne 3 pour l'hôte de la machine
        ctk.CTkLabel(
            row_frame,
            text=device.get('hostname', 'Unknown'),
            font=("Inter", 12),
            text_color="#3498db").grid(
                row=0, column=3, sticky="w", padx=10)
        
        # Colonne 4 pour le vendeur de la machine
        ctk.CTkLabel(
            row_frame, 
            text=device.get('vendor', 'Unknown'), 
            font=("Inter", 11),
            text_color="#b8bcc2").grid(
                row=0, column=4, sticky="w", padx=10)
        
        # Colonne 5 pour famille d'os
        ctk.CTkLabel(
            row_frame,
            text=device.get('os_family', '-').upper(),
            font=("Inter", 11),
            text_color="#b8bcc2").grid(
                row=0, column=5, sticky="w", padx=10)

        # Colonne 6 pour le port
        risk_level = device.get('open_ports', 'SAFE')
        badge = self.create_risk_badge(row_frame, risk_level)
        badge.grid(row=0, column=6, sticky="w", padx=10)

        # Ligne de séparation fine
        sep = ctk.CTkFrame(self.content_frame, fg_color="#1f2937", height=1)
        sep.pack(fill="x", padx=20)

        self.rows.append(row_frame)
    

    def create_risk_badge(self, parent, level):

        if isinstance(level, list):
            level = level[0] if level else "UNKNOWN"
        level = str(level).upper().strip() 

        colors = {
            "SAFE": ("#064e3b", "#10b981"),
            "WARNING": ("#451a03", "#f59e0b"),
            "HIGH": ("#450a0a", "#ef4444")
        }
        
        bg, fg = colors.get(level, ("#1f2937", "#94a3b8"))

        badge_frame = ctk.CTkFrame(parent, fg_color=bg, corner_radius=6, height=24)
        # On utilise pack_propagate(False) pour forcer une taille si besoin, 
        # mais ici on laisse le texte donner la taille avec du padding
        
        lbl = ctk.CTkLabel(
            badge_frame, text=f" {level} ", 
            font=("Inter", 10, "bold"), 
            text_color=fg
        )
        lbl.pack(padx=8, pady=2)

        return badge_frame

    # Récuperer les dernieres machines trouvées dans la base de données
    def refresh_from_db(self):
        devices = self.controller.db.get_all_devices()

        if devices:
            for device in devices:
                self.add_device_row(device)
        else:
            self.show_empty_state()