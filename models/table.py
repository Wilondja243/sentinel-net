import os
import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_name="sentinel_net.db"):
        self.db_name = db_name
        self.root_dir = os.path.dirname(__file__)
        self.db_dir = os.path.join(os.path.dirname(self.root_dir), 'db')

        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        self.db_path = os.path.join(self.db_dir, self.db_name)
        self.setup_tables()

    # connexion à la base de données
    def get_connexion(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        return conn
    
    # création de tables (Devices et AuditHistory)
    def setup_tables(self):
        conn = self.get_connexion()
        cursor = conn.cursor()

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS Devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mac_address TEXT UNIQUE,
                    ip_address  TEXT,
                    first_seen TEXT,
                    last_seen TEXT,
                    vendor TEXT,
                    open_ports TEXT,
                    hostname TEXT,
                    os_family TEXT,
                    risk_level TEXT DEFAULT 'SAFE'
                )
            """
        )

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS AuditHistory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    device_found INTEGER,
                    critical_ports_found INTEGER
                )
            """
        )

        conn.commit()
        conn.close()

    # Enregistrement de données dans la table Devices
    def save_device(self, device):

        conn = self.get_connexion()
        cursor = conn.cursor()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        open_ports = device.get("open_ports", [])

        if isinstance(open_ports, list):
            open_ports_str = ", ".join(map(str, open_ports))
        else:
            open_ports_str = str(open_ports)

        cursor.execute("""
            INSERT INTO Devices (
                    mac_address,ip_address, first_seen,
                    last_seen, vendor, open_ports, hostname, os_family)

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(mac_address) DO UPDATE SET

                ip_address=excluded.ip_address,
                last_seen=excluded.last_seen,
                vendor=excluded.vendor,
                open_ports=excluded.open_ports,
                hostname=excluded.hostname,
                os_family=excluded.os_family
        """,(
                device.get("mac"),
                device.get("ip"),
                now, now,
                device.get("vendor"),
                device.get("hostname"),
                open_ports_str,
                device.get("os_family"),
            )
        )

        conn.commit()
        conn.close() 

    # Obtenir toutes les équipements connectés
    def get_all_devices(self):
        
        conn = self.get_connexion()
        cursor = conn.cursor()

        cursor.execute(" SELECT * FROM Devices ")
        rows = cursor.fetchall()

        conn.close()
        
        return [dict(row) for row in rows]
    
    # Récuperer l'address mac
    def get_device_by_mac(self, mac):

        conn = self.get_connexion()
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Devices WHERE mac_address = ?", (mac,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    # Récupère les statistiques globales pour le tableau de bord.
    def get_dashboard_stats(self):
        conn = self.get_connexion()
        cursor = conn.cursor()
        
        # Nombre total de machines
        cursor.execute("SELECT COUNT(*) FROM Devices")
        total_devices = cursor.fetchone()[0]

        # On récupere les ports critiques
        cursor.execute("SELECT COUNT(*) FROM Devices WHERE risk_level = 'CRITICAL'")
        criticals = cursor.fetchone()[0]
        
        # Nombre de ports ouverts
        cursor.execute("SELECT open_ports FROM Devices")
        rows = cursor.fetchall()
        
        total_ports = 0
        unique_ports = set()
        
        for row in rows:
            port_str = row[0]
            if port_str and port_str != "None":

                # On sépare par virgule et on nettoie
                ports = [p.strip() for p in port_str.split(',') if p.strip()]
                total_ports += len(ports)

                for p in ports:
                    unique_ports.add(p)
        
        conn.close()
        
        return {
            "total_devices": str(total_devices),
            "total_ports": str(total_ports),
            "critical_level": criticals,
            "port_list": ", ".join(list(unique_ports)[:3])
        }