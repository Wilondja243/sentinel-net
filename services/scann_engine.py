import ipaddress
import socket
import psutil
from scapy.all import (
    Ether, ARP,
    IP, TCP, srp,
    sr1, conf,
)
from services.ports import target_ports

class ScannerEngine:
    
    def __init__(self):
        self.is_running = False

    def get_hostname(self, ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return "Inconnu"

    def scan_ports(self, ip):
        open_ports = []

        for port in target_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            result = s.connect_ex((ip, port))

            if result == 0:
                open_ports.append(port)
            s.close()
            
        return open_ports
    
    def estimate_os(self, ip, open_ports):
        if 445 in open_ports or 135 in open_ports:
            return "Windows"
        if 22 in open_ports or 548 in open_ports:
            return "Linux/macOS"
        
        try:
            ans = sr1(IP(dst=ip)/TCP(dport=80, flags="S"), timeout=0.5, verbose=False)
            if ans:
                if ans.ttl <= 64: return "Linux/Android"
                if ans.ttl <= 128: return "Windows"
        except:
            pass
            
        return "Indéterminé"
    
    def evaluate_risk(self):
        
        if any(p in target_ports for p in target_ports):
            return "CRITICAL"
        elif len(target_ports) > 3:
            return "WARNING"
        else:
            return "SAFE"
    
    # C'est la méthode principale du programme
    # Cette méthode est utilisée pour scanner un réseau local tel que le wifi, un réseau filaire, ...
    def scan_local_network(self, target, callback=None):

        self.is_running = True

        conf.L2listen = True
        conf.checkIPaddr = False

        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target)

        answered, unanswered = srp(
            packet, timeout=2, verbose=False,
            iface=conf.iface, inter=0.01, retry=2
        )

        if not answered:
            print("Aucune machine n'a répondu")

        devices = []
        
        for sent, received in answered:

            if not self.is_running:
                print("[!]: ScanneEngine: Arrêt détecté.")
                break

            target_ip = received.psrc
            
            device_info = {
                'ip': target_ip,
                'mac': received.hwsrc,
                'hostname': self.get_hostname(target_ip),
                'os_family': self.estimate_os(target_ip, self.scan_ports(target_ip)),
                'open_ports': self.scan_ports(target_ip),
                'vendor': "Recherche via API ou préfixe MAC..." 
            }

            if callback:
                callback(device_info)

            devices.append(device_info)

        print(devices)

        self.is_running = False
        
        return devices
    
    # Récuperer l'address ip du réseau au quel on est connecté
    def get_active_interface_info(self):

        # Trouver l'interface qui a la route par défaut (Internet)
        # On crée une socket UDP temporaire pour voir quelle IP locale est utilisée pour sortir
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            active_ip = s.getsockname()[0]
            s.close()
        except Exception:
            active_ip = None

        for interface, addresses in psutil.net_if_addrs().items():
            # Sous Windows, on peut aussi vérifier si "Wi-Fi" est dans le nom
            # mais le test de l'IP active est le plus fiable.

            for addr in addresses:

                if addr.family == socket.AF_INET and addr.address != "127.0.0.1":
                    
                    # Si cette interface possède l'IP qui sort sur internet

                    if addr.address == active_ip:
                        ip = addr.address
                        netmask = addr.netmask
                        network = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)

                        print("interface: ", interface)
                        print("ip: ", ip)
                        print('network', str(network))
                        
                        return {
                            "interface": interface,
                            "ip": ip,
                            "network": str(network)
                        }
        return None
    
