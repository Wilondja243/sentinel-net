
import threading
import customtkinter as ctk
from utils.writer import writer
from models.table import DatabaseManager
from core.scann_engine import ScannerEngine
from utils.color import get_color

from interfaces.top_bar import TopBar
from interfaces.audit_page import AuditPage
from interfaces.asset_page import AssetPage

# La classe qui démarre le programme
class SentinelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = DatabaseManager()
        self.engine = ScannerEngine()
        self.inter = self.engine.get_active_interface_info()

        colors = get_color()

        # 2. Dictionnaire pour stocker nos différentes sections de navigation
        self.frames = {}

        # windows config
        self.title("SENTINEL-NET v1.0.0")
        self.geometry("900x700")

        # theme config
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=colors.get("bs_bg"))

        self.topbar = TopBar(self)
        self.topbar.pack(fill="x", padx=20, pady=20)

        # le conteneur principal de toutes les menus de navigation
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        for PageClass in [AuditPage, AssetPage]:
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # On ne les pack pas encore, on les superpose
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("AuditPage")

    # Pour afficher une frame (page de menu) spécifique
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def run_scanner(self):
        thread = threading.Thread(target=self.run_engine_process, daemon=True)
        thread.start()

    def run_engine_process(self):
        devices = self.engine.scan_local_network(
            self.inter["network"], callback=self.send_to_interface)

        for device in devices:
            self.db.save_device(device)

            clean_device = self.db.get_device_by_mac(device.get("mac_address"))

            if  clean_device:
                self.after(0, lambda d=device: self.frames["AssetPage"].add_device_row(d))

    def send_to_interface(self, device):
        self.after(0, lambda: self.add_line_in_the_table(device))

    def add_line_in_the_table(self, device):
        writer(f"Ajout visuel de : {device['ip']}")

        msg = f"[+] {device['ip']:15} | {device['mac']} | {device['os_family']:12} | {device['hostname']:15}\n"
        
        # On envoie le message à la log_area de la section Audit
        if "AuditPage" in self.frames:
            audit_page = self.frames["AuditPage"]
            audit_page.update_log(msg)
        
        # On met à jour le tableau
        # if "AssetPage" in self.frames:
        #     self.frames["AssetPage"].add_device_row(device)


if __name__ == "__main__":
    sentinelApp = SentinelApp()
    sentinelApp.mainloop()
