# sentinel-net

SentinelNet is a modern network auditing solution designed to simplify asset mapping and attack surface evaluation. By leveraging the power of Scapy for packet manipulation and CustomTkinter for a high-end UI, this tool makes cybersecurity accessible to network administrators of all levels.

## 🚀 Key Features

* **Intelligent Surface Scan**: Automatic detection of active network interfaces (WiFi or Ethernet) and IP configuration using `Psutil`.
* **Packet-Level Analysis**: High-precision discovery engine powered by `Scapy` to identify active hosts and open services.
* **Risk Assessment**: Automatic identification of vulnerable ports with a classification system (SAFE, WARNING, CRITICAL).
* **Dynamic Dashboard**: Instant visualization of total devices, critical risks, and exposed services.
* **Modern UX/UI**: Sleek "Dark Mode" interface with a "Typewriter" animation to follow real-time scan progress.
* **Data Persistence**: Automatic logging of every scan into an `SQLite3` database for historical tracking.

---

## 🛠️ Tech Stack

* **Language**: Python 3.x
* **Interface**: `CustomTkinter` (Modern & Responsive UI)
* **Network Engine**: `Scapy` (Advanced packet crafting and scanning)
* **System Discovery**: `Psutil` & `Socket` (Interface detection and hostname resolution)
* **Database**: `SQLite3` (Lightweight local data storage)

---

## 📦 Installation

### 1. Prerequisites (Linux/Ubuntu)
Since Scapy interacts with network layers, you may need to install certain dependencies:

```
sudo apt update && sudo apt install python3-pip

2. Clone the Project
Bash

git clone https://github.com/Wilondja243/sentinel-net.git
cd SentinelNet

3. Setup Virtual Environment

python3 -m venv gen_env
source gen_env/bin/activate

4. Install Dependencies

pip install scapy customtkinter psutil

```

🖥️ Usage

To launch the application, run the main script (Note: Scapy requires root privileges to send raw packets on Linux):
Bash

sudo ./gen_env/bin/python main.py

    Check the Network Badge at the top right to confirm your active interface (WIFI or CABLE).

    Click the Central Button "Launch Audit" to start the sequence.

    Monitor the Progress via the typewriter logs while the engine scans the subnet.

    Review the Stats in the dashboard once the scan status shows "COMPLETED".

📂 Project Structure
Plaintext

SentinelNet/
├── assets/
├── core/
├── database/
├── interfaces/
├── models/
├── utils/
└── main.py

🛡️ Security & Responsibility

This tool is intended for educational purposes and authorized security testing only. Scanning networks without prior authorization is illegal. The authors are not responsible for any misuse of this software.
👥 Presentation Note

Developed for a university project, SentinelNet focuses on bridging the gap between complex low-level networking and intuitive visual design. It demonstrates how raw packet data can be transformed into actionable security insights.