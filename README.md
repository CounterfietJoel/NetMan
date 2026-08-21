# ⚡ NetMan — Windows Network & Wi-Fi Performance Manager

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D4.svg?logo=windows)](https://github.com/CounterfietJoel/NetMan)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg?logo=python)](https://www.python.org/)
[![GitHub Stars](https://img.shields.io/github/stars/CounterfietJoel/NetMan?style=social)](https://github.com/CounterfietJoel/NetMan/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/CounterfietJoel/NetMan/pulls)

**The all-in-one, open-source utility to boost Wi-Fi speeds, eliminate lag, tune the TCP/IP stack, benchmark DNS resolvers, and optimize Windows 10/11 network performance.**  
*Inspired by tools like [Wu10Man](https://github.com/WereDev/wu10man), NetMan gives power users, gamers, students, and sysadmins 1-click control over their network adapter hardware, DNS settings, and kernel network stack.*

[Quick Start](#-quick-start) • [Key Features](#-key-features) • [Why NetMan Works](#-why-netman-works-the-engineering) • [How to Use](#-how-to-use) • [FAQ](#-frequently-asked-questions) • [Contributing](#-contributing)

</div>

---

## 🔍 Overview: Why Windows Network Throttles Your Connection

Out of the box, Windows 10 and 11 prioritize battery preservation and legacy compatibility over maximum network throughput:
1. **Sticky 2.4 GHz Band**: Laptops frequently stay trapped on slow, congested 2.4 GHz Wi-Fi channels (18–30 Mbps) even when clean 5 GHz Wi-Fi 6 (400–1000+ Mbps) is broadcast from the exact same access point.
2. **Antenna Sleep Modes (Auto SMPS)**: Wireless cards constantly put spatial antennas to sleep to save milliwatts of power, causing packet micro-stutters and jitter.
3. **Slow ISP DNS Lookups**: Default router/ISP DNS servers often take **200–1200 ms** per domain resolution, causing web pages and applications to feel sluggish.
4. **Windows Network Throttling Index**: Windows limits non-multimedia network processing to 10 packets per millisecond by default.
5. **Background P2P Upload Leeching**: Windows Delivery Optimization uploads update packages to external internet peers, saturating upload bandwidth.

**NetMan solves all of these issues in one lightweight, transparent, open-source tool.**

---

## 🚀 Key Features

| Category | Optimization | Description |
| :--- | :--- | :--- |
| **📶 Wi-Fi Hardware Acceleration** | **5 GHz / 6 GHz Band Lock** | Prevents laptops from getting stuck on congested 2.4 GHz campus & office access points. |
| | **Throughput Booster** | Enables packet burst aggregation for maximum transmission throughput. |
| | **Full 2x2 MIMO (No SMPS)** | Prevents antennas from entering low-power sleep states, eliminating packet drop spikes. |
| | **Enterprise Roaming Tuning** | Configures optimal access point handoff sensitivity for campus and enterprise networks. |
| **🌐 Anycast DNS Benchmark** | **Real-Time DNS Latency Meter** | Benchmarks live lookup times for Cloudflare (1.1.1.1), Google (8.8.8.8), Quad9 (9.9.9.9), OpenDNS, Control D, and AdGuard. |
| | **1-Click Resolver Switcher** | Instantly activates the fastest DNS provider with automatic cache flushing. |
| **⚙ TCP/IP Kernel Tuning** | **CUBIC Congestion Provider** | Switches to modern CUBIC congestion control optimized for lossy and high-bandwidth wireless links. |
| | **Dynamic Window Auto-Tuning** | Uncaps the TCP receive window to utilize 100% of available bandwidth. |
| | **RSS & RSC Hardware Offloading** | Distributes network packet processing across multiple CPU cores. |
| | **TCP Fast Open & HyStart** | Accelerates connection handshakes and reduces round-trip delays. |
| **🛠 Windows Registry Tweaks** | **Disable Network Throttling** | Sets `NetworkThrottlingIndex = 0xFFFFFFFF` to remove artificial network packet caps. |
| | **Disable P2P Delivery Optimization** | Stops background Windows Update services from uploading to internet peers. |
| | **Optimized DNS Cache TTL** | Caches verified lookups for 2 hours for instant page loads. |
| **🔬 Advanced Diagnostics** | **MTU Discovery & Optimizer** | Sweeps ICMP packet sizes with DF-bit to calculate and apply unfragmented MTU. |
| | **IPv6 Latency / Routing Fix** | Configures prefix policy to prefer IPv4 over broken/unrouted campus IPv6 networks. |
| | **Live Ping & Jitter Monitor** | Real-time gateway router and internet ping latency graph. |
| **🔄 100% Safe & Reversible** | **State Snapshot Engine** | Saves your original network state to JSON before making changes. |
| | **1-Click Factory Restore** | Restores all adapter properties, DNS, TCP stack, and registry keys to Windows factory defaults. |

---

## 📊 Why NetMan Works: The Engineering Behind the Speedup

When testing NetMan on an Intel Wi-Fi 6E AX211 card connected to an enterprise campus network (`KPR Institutions`):

```
BEFORE OPTIMIZATION:
- Band: 2.4 GHz (Channel 11) | Channel Load: 55%
- Physical Link Speed: 18 – 26 Mbps
- DNS Resolution Latency: 1,173 ms
- Ping Latency: 227 ms

AFTER NETMAN TURBO BOOST:
- Band: 5 GHz Wi-Fi 6 (Channel 120) | Channel Load: 10%
- Physical Link Speed: 516 Mbps (20x Faster!)
- DNS Resolution Latency: 17.8 ms (65x Faster!)
- Ping Latency: 12 – 15 ms (15x Lower Latency!)
```

---

## 📦 Quick Start & Installation

### Option 1: Run from Source (Python 3.9+)

```bash
# 1. Clone the repository
git clone https://github.com/CounterfietJoel/NetMan.git
cd NetMan

# 2. Launch the Modern GUI
python main.py
```

### Option 2: 1-Click CLI Turbo Boost Mode

```bash
# Run turbo optimization directly from terminal
python main.py --boost
```

### Option 3: Compile Standalone Executable (`NetMan.exe`)

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name "NetMan" main.py
```
*The compiled single-file `NetMan.exe` will be generated inside the `dist/` directory with zero runtime dependencies.*

---

## 🖥 User Interface & Navigation

NetMan features a modern dark-mode interface built with native Windows styling:

1. **📊 Dashboard**: Status cards displaying active SSID, BSSID, Band, Link Speed, RSSI signal, and 1-Click Turbo Boost.
2. **📶 Wi-Fi Optimizer**: Fine-grained controls for band preference (5GHz/6GHz), Throughput Booster, MIMO power management, and roaming sensitivity.
3. **🌐 DNS Benchmark**: Live multi-threaded latency test against global Anycast providers.
4. **⚙ TCP Stack & QoS**: Kernel TCP/IP stack toggles and network throttling removal.
5. **📡 Live Diagnostics**: Continuous gateway and internet ping monitor with packet jitter detection.
6. **🔄 Backup & Restore**: Automatic state snapshot manager with 1-click factory restore.

---

## ❓ Frequently Asked Questions (FAQ)

<details>
<summary><b>Does NetMan affect the internet speed of people around me?</b></summary>
No. In fact, it helps them! By moving your high-bandwidth laptop from the congested 2.4 GHz band to the spacious 5 GHz band, you free up airtime and wireless spectrum for other nearby devices.
</details>

<details>
<summary><b>Is NetMan safe and reversible?</b></summary>
Yes. NetMan creates a complete JSON snapshot of your original adapter properties and network configuration before applying changes. You can revert everything back to Windows defaults with 1 click in the "Backup & Restore" tab.
</details>

<details>
<summary><b>Do I need to run NetMan every time I boot my PC?</b></summary>
No. The Wi-Fi adapter hardware properties and TCP/IP stack configurations are saved in the Windows hardware registry and persist across reboots, sleep cycles, and network reconnects.
</details>

<details>
<summary><b>Does NetMan work on all Wi-Fi cards?</b></summary>
Yes. Wi-Fi band locking, Throughput Booster, and MIMO controls work across Intel (Wi-Fi 5, 6, 6E, 7), Realtek, MediaTek, and Qualcomm wireless adapters. DNS benchmarking and TCP stack tuning work on all Windows 10 and 11 network adapters (both Wi-Fi and Ethernet).
</details>

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

<div align="center">
Made with ⚡ by <a href="https://github.com/CounterfietJoel">CounterfietJoel</a>
</div>
