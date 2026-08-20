# ⚡ NetMan (Windows Network & Wi-Fi Optimizer)

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D4.svg)
![Python](https://img.shields.io/badge/python-3.9+-yellow.svg)
![GitHub stars](https://img.shields.io/github/stars/CounterfietJoel/NetMan?style=social)

**An open-source, modern Windows 10/11 network performance manager and Wi-Fi optimizer.**  
*Inspired by utilities like [Wu10Man](https://github.com/WereDev/wu10man), NetMan gives you complete control over your wireless adapter, DNS resolvers, TCP stack, and system network throttling.*

[Features](#-key-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [How It Works](#-how-it-works) • [License](#-license)

</div>

---

## 🚀 Key Features

### 📶 1. Wi-Fi Hardware & Band Acceleration
- **5 GHz / 6 GHz Band Lock**: Prevents laptops from getting stuck on congested 2.4 GHz campus/office access points.
- **Throughput Booster**: Activates packet burst aggregation for maximum transmission speeds.
- **Full 2x2 MIMO (No SMPS)**: Prevents wireless cards from powering down spatial antennas, eliminating micro-stutters and packet drops.
- **Optimized Roaming**: Smooth enterprise access point handoff across multi-AP environments (campuses, universities, corporate offices).

### 🌐 2. Live DNS Benchmark & 1-Click Switcher
- Real-time latency benchmark against top global Anycast resolvers (**Cloudflare, Google, Quad9, OpenDNS, Control D, AdGuard**).
- 1-click instant activation with automatic DNS cache flushing.

### ⚙ 3. TCP/IP Stack Kernel Tuning
- **CUBIC Congestion Provider**: Modern congestion control algorithm designed for high-throughput wireless networks.
- **Dynamic Window Auto-Tuning**: Eliminates artificial TCP buffer bottlenecks.
- **Receive-Side Scaling (RSS) & RSC**: Offloads packet processing across all CPU threads.
- **TCP Fast Open & HyStart**: Reduces connection handshake times.

### 🛠 4. Windows Network Throttling Overrides
- **Remove Multimedia Throttling**: Eliminates Windows default 10 packet/ms cap on non-multimedia traffic (`NetworkThrottlingIndex = 0xFFFFFFFF`).
- **Disable P2P Delivery Optimization**: Stops Windows Update from leeching upload bandwidth to internet peers.
- **Extended DNS Cache TTL**: Keeps resolved DNS lookups cached for instant page loads.

### 🔄 5. 100% Safety & 1-Click Factory Restore
- Takes a snapshot of all adapter and system network configurations before making any modifications.
- Revert everything back to Windows factory defaults with a single click at any time.

---

## 📦 Installation

### Option 1: Run from Source (Python 3.9+)
```bash
git clone https://github.com/CounterfietCounterfietJoel/NetMan.git
cd NetMan
python main.py
```

### Option 2: CLI 1-Click Turbo Boost Mode
```bash
python main.py --boost
```

### Option 3: Build Standalone EXE
Run `build.bat` or compile with PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name "NetMan" main.py
```
Your compiled standalone application will be generated in `dist/NetMan.exe`.

---

## 🖥 Architecture & Project Structure

```
NetMan/
├── netman/
│   ├── core/
│   │   ├── wifi.py       # Wi-Fi driver tuning & BSSID scanner
│   │   ├── dns.py        # DNS benchmarking & Anycast switcher
│   │   ├── tcp.py        # TCP stack & CUBIC congestion optimizer
│   │   ├── registry.py   # Multimedia throttling & QoS tweaks
│   │   ├── backup.py     # Snapshot engine & factory restore
│   │   └── utils.py      # PowerShell execution & Admin elevation
│   └── ui/
│       ├── theme.py      # Modern Windows Dark Palette
│       ├── app.py        # Main Window & View Navigation
│       └── views/        # Dashboard, Wi-Fi, DNS, TCP, Diagnostics, Backup
├── main.py               # Main Entrypoint (GUI & CLI)
├── build.bat             # 1-Click PyInstaller compiler
└── README.md
```

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
