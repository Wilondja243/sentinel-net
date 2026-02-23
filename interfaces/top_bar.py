
import customtkinter as ctk
from interfaces.components.button import Button
from utils.color import get_color
from PIL import Image


class TopBar(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(
            master=master,
            fg_color=get_color().get("bs_card"),
            corner_radius=80,
            border_width=1,
            border_color=get_color().get("bs_card_border"),
            **kwargs
        )

        self.colors = get_color()

        # Left topbar content
        self.left_content = ctk.CTkFrame(
            self, width=300, fg_color=self.colors.get("bs_card")
        )
        self.left_content.pack(side="left", pady=10, padx=25)

        self.sentinel_icon = ctk.CTkImage(
            dark_image=Image.open("assets/icons/audit.png"),
            size=(60, 60)
        )
        self.sentinel_icon_label = ctk.CTkLabel(
            self.left_content, image=self.sentinel_icon,
            text="",
        )
        self.sentinel_icon_label.pack(side="left", padx=15)
        self.text_content = ctk.CTkFrame(
            self.left_content, fg_color=self.colors.get("bs_card")
        )
        self.text_content.pack(side="left")

        self.label = ctk.CTkLabel(
            self.text_content, text="Audit Réseau",
            text_color="white", font=("Arial", 16, "bold")
        )
        self.label.pack(anchor="w")
        self.text_muted = ctk.CTkLabel(
            self.text_content, text="Audit de sécurité réseau",
            text_color=self.colors.get("bs_muted")
        )
        self.text_muted.pack(anchor="w")

        # Right topbar content
        self.right_content = ctk.CTkFrame(self, fg_color=self.colors.get("bs_card"))
        self.right_content.pack(side="right", pady=10, padx=25)

        self.btn1 = Button(
            self.right_content,
            "Aperçu",
            fg_color=self.colors.get("bs_card"),
            width=130, height=50,
            image=self.get_icon()["icon_overview"],
            command=lambda: self.master.show_frame("AuditPage")
        )
        self.btn1.pack(side="left", padx=5)

        self.btn2 = Button(
            self.right_content,
            "Assets",
            fg_color=self.colors.get("bs_card"),
            text_color="white",
            width=130, height=50,
            image=self.get_icon()["icon_asset"],
            command=lambda: self.master.show_frame("AssetPage")
        )
        self.btn2.pack(side="left", padx=5)

        self.btn3 = Button(
            self.right_content,
            "Rapport",
            fg_color=self.colors.get("bs_card"),
            text_color="white",
            width=130, height=50,
            image=self.get_icon()["icon_report"],
            # command=self.master.show_frame("Repport")
        )
        self.btn3.pack(side="left", padx=5)

        self.show_interface_and_ip()

    # On récupère toutes les images dans assets/icons/
    def get_icon(self):

        return {
            "icon_overview": ctk.CTkImage(
                dark_image=Image.open("assets/icons/globe.png"),
                size=(20, 20),
                
            ),

            "icon_asset": ctk.CTkImage(
                dark_image=Image.open("assets/icons/wifi.png"),
                size=(20, 20)
            ),

            "icon_connect": ctk.CTkImage(
                dark_image=Image.open("assets/icons/connect.png"),
                size=(30, 30)
            ),

            "icon_report": ctk.CTkImage(
                dark_image=Image.open("assets/icons/chart.png"),
                size=(20, 20)
            ),
        }
    
    # Affichage d'interface réseau et l'address ip
    def show_interface_and_ip(self):
        active_infos = self.master.engine.get_active_interface_info()
        raw_iface = active_infos.get('interface', '').lower()

        if any(pre in raw_iface for pre in ["wlp", "wlan", "wifi", "wi-fi"]):
            display_name = "WIFI"
            accent_color = "#3b82f6"
        elif any(pre in raw_iface for pre in ["enp", "eth", "eno", "eth"]):
            display_name = "CÂBLE"
            accent_color = "#10b981"
        elif "lo" in raw_iface:
            display_name = "LOCAL"
            accent_color = "#94a3b8"
        else:
            display_name = "RÉSEAU"
            accent_color = "#f59e0b"
        
        # Le Conteneur Principal
        self.net_badge = ctk.CTkFrame(
            self.right_content, 
            fg_color="#111827", 
            height=45,
            corner_radius=12,
            border_width=1,
            border_color="#1f2937"
        )
        self.net_badge.pack(side="right", padx=20, pady=5)

        # Section Interface
        # On utilise un Frame interne pour créer un badge dans le badge
        self.iface_container = ctk.CTkFrame(
            self.net_badge,
            fg_color="#1f2937",
            corner_radius=8,
            width=60, height=28
        )
        self.iface_container.pack(side="left", padx=(8, 5), pady=8)
        self.iface_container.pack_propagate(False)

        self.iface_label = ctk.CTkLabel(
            self.iface_container, 
            text=display_name.upper(),
            font=("Inter", 10, "bold"),
            text_color=accent_color
        )
        self.iface_label.pack(expand=True)

        # séparateur 
        self.sep = ctk.CTkFrame(self.net_badge, width=1, height=20, fg_color="#374151")
        self.sep.pack(side="left", padx=10)

        # 4. Section Data (IP et Icône)
        self.data_container = ctk.CTkFrame(self.net_badge, fg_color="transparent")
        self.data_container.pack(side="left", padx=(0, 15))

        # Petit point lumineux
        self.dot = ctk.CTkLabel(
            self.data_container, 
            text="●", 
            font=("Inter", 8),
            text_color="#10b981"
        )
        self.dot.pack(side="left", padx=(0, 5))

        self.ip_val_label = ctk.CTkLabel(
            self.data_container,
            text=active_infos.get('ip', '0.0.0.0'),
            font=("JetBrains Mono", 12, "bold"),
            text_color="#f8fafc"
        )
        self.ip_val_label.pack(side="left")