"""
NetMan Dashboard View
Quick Overview card, live connection status, and 1-Click Turbo Boost.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from netman.ui.theme import THEME
from netman.core.wifi import WifiManager
from netman.core.dns import DnsManager
from netman.core.tcp import TcpManager
from netman.core.registry import RegistryTweaks
from netman.core.backup import BackupManager
from netman.core.utils import is_admin

class DashboardView(tk.Frame):
    def __init__(self, parent, notify_status=None):
        super().__init__(parent, bg=THEME["bg_dark"])
        self.notify_status = notify_status
        self.setup_ui()
        self.refresh_status()

    def setup_ui(self):
        # Header Banner
        header = tk.Frame(self, bg=THEME["bg_dark"])
        header.pack(fill="x", padx=25, pady=(20, 10))

        title = tk.Label(header, text="Network Performance Dashboard", font=THEME["font_title"], fg=THEME["text_primary"], bg=THEME["bg_dark"])
        title.pack(anchor="w")

        subtitle = tk.Label(header, text="Monitor your active Wi-Fi link parameters and boost performance with 1-click.", font=THEME["font_small"], fg=THEME["text_secondary"], bg=THEME["bg_dark"])
        subtitle.pack(anchor="w", pady=(2, 0))

        # Admin Badge
        admin_text = "🛡 Administrator Mode Active" if is_admin() else "⚠ Standard User (Some OS tweaks require Admin)"
        admin_color = THEME["accent_success"] if is_admin() else THEME["accent_warning"]
        admin_badge = tk.Label(header, text=admin_text, font=THEME["font_small"], fg=admin_color, bg=THEME["bg_dark"])
        admin_badge.pack(anchor="w", pady=(4, 0))

        # Metric Cards Container
        cards_frame = tk.Frame(self, bg=THEME["bg_dark"])
        cards_frame.pack(fill="x", padx=25, pady=15)

        # 4 Status Cards
        self.card_ssid = self.create_card(cards_frame, "CONNECTED NETWORK", "Scanning...", "SSID / AP")
        self.card_band = self.create_card(cards_frame, "FREQUENCY BAND", "--", "Channel & Radio")
        self.card_speed = self.create_card(cards_frame, "PHY LINK SPEED", "-- Mbps", "Rx / Tx Rate")
        self.card_signal = self.create_card(cards_frame, "SIGNAL STRENGTH", "--%", "RSSI Quality")

        self.card_ssid.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        self.card_band.grid(row=0, column=1, padx=10, sticky="nsew")
        self.card_speed.grid(row=0, column=2, padx=10, sticky="nsew")
        self.card_signal.grid(row=0, column=3, padx=(10, 0), sticky="nsew")
        
        cards_frame.columnconfigure((0, 1, 2, 3), weight=1)

        # 1-Click Action Frame
        action_card = tk.Frame(self, bg=THEME["bg_card"], padx=20, pady=20, highlightbackground=THEME["border"], highlightthickness=1)
        action_card.pack(fill="x", padx=25, pady=10)

        boost_title = tk.Label(action_card, text="⚡ 1-Click Quick Turbo Boost", font=THEME["font_header"], fg=THEME["text_primary"], bg=THEME["bg_card"])
        boost_title.pack(anchor="w")

        boost_desc = tk.Label(action_card, text="Automatically locks Intel Wi-Fi to 5GHz/6GHz, enables Throughput Booster & MIMO, sets Cloudflare low-latency Anycast DNS, enables TCP CUBIC stack, and removes Windows network throttling.", font=THEME["font_body"], fg=THEME["text_secondary"], bg=THEME["bg_card"], wraplength=700, justify="left")
        boost_desc.pack(anchor="w", pady=(5, 15))

        btn_row = tk.Frame(action_card, bg=THEME["bg_card"])
        btn_row.pack(fill="x")

        self.btn_boost = tk.Button(btn_row, text="⚡ Apply 1-Click Boost", font=THEME["font_bold"], bg=THEME["accent_primary"], fg="#FFFFFF", activebackground=THEME["accent_hover"], activeforeground="#FFFFFF", relief="flat", padx=20, pady=10, cursor="hand2", command=self.run_turbo_boost)
        self.btn_boost.pack(side="left", padx=(0, 10))

        self.btn_refresh = tk.Button(btn_row, text="🔄 Refresh Stats", font=THEME["font_body"], bg=THEME["bg_card_hover"], fg=THEME["text_primary"], activebackground=THEME["border"], activeforeground="#FFFFFF", relief="flat", padx=15, pady=10, cursor="hand2", command=self.refresh_status)
        self.btn_refresh.pack(side="left")

    def create_card(self, parent, title, val, sub):
        card = tk.Frame(parent, bg=THEME["bg_card"], padx=15, pady=15, highlightbackground=THEME["border"], highlightthickness=1)
        lbl_t = tk.Label(card, text=title, font=THEME["font_small"], fg=THEME["text_muted"], bg=THEME["bg_card"])
        lbl_t.pack(anchor="w")
        lbl_v = tk.Label(card, text=val, font=("Segoe UI", 16, "bold"), fg=THEME["text_primary"], bg=THEME["bg_card"])
        lbl_v.pack(anchor="w", pady=(5, 2))
        lbl_s = tk.Label(card, text=sub, font=THEME["font_small"], fg=THEME["text_secondary"], bg=THEME["bg_card"])
        lbl_s.pack(anchor="w")
        card.val_label = lbl_v
        card.sub_label = lbl_s
        return card

    def refresh_status(self):
        def _task():
            info = WifiManager.get_current_connection()
            self.after(0, lambda: self._update_cards(info))
        threading.Thread(target=_task, daemon=True).start()

    def _update_cards(self, info):
        if info["connected"]:
            self.card_ssid.val_label.config(text=info["ssid"][:16])
            self.card_ssid.sub_label.config(text=f"BSSID: {info['bssid']}")
            self.card_band.val_label.config(text=info["band"])
            self.card_band.sub_label.config(text=f"Ch {info['channel']} ({info['radio_type']})")
            self.card_speed.val_label.config(text=f"↓{info['rx_rate']} ↑{info['tx_rate']} M")
            self.card_speed.sub_label.config(text=f"Rx: {info['rx_rate']} Mbps / Tx: {info['tx_rate']} Mbps")
            self.card_signal.val_label.config(text=f"{info['signal']}%")
            self.card_signal.sub_label.config(text="Excellent" if info['signal'] > 70 else "Good" if info['signal'] > 50 else "Fair")
        else:
            self.card_ssid.val_label.config(text="Disconnected")
            self.card_band.val_label.config(text="--")
            self.card_speed.val_label.config(text="--")
            self.card_signal.val_label.config(text="--")

    def run_turbo_boost(self):
        self.btn_boost.config(state="disabled", text="⚡ Optimizing...")
        def _boost_thread():
            BackupManager.create_snapshot("Wi-Fi")
            WifiManager.optimize_wifi_for_performance("Wi-Fi")
            DnsManager.set_dns(["1.1.1.1", "1.0.0.1", "8.8.8.8"], "Wi-Fi")
            TcpManager.optimize_tcp_stack()
            RegistryTweaks.apply_network_throttling_removal()
            RegistryTweaks.optimize_dns_cache_ttl()
            RegistryTweaks.disable_delivery_optimization_p2p()
            
            import time
            time.sleep(3)
            info = WifiManager.get_current_connection()
            
            self.after(0, lambda: self._on_boost_complete(info))
        threading.Thread(target=_boost_thread, daemon=True).start()

    def _on_boost_complete(self, info):
        self.btn_boost.config(state="normal", text="⚡ Apply 1-Click Boost")
        self._update_cards(info)
        messagebox.showinfo("NetMan Turbo Boost", "All network & Wi-Fi optimizations applied successfully!\n\n- Locked to 5GHz/6GHz Wi-Fi 6\n- Low-latency Cloudflare DNS configured\n- TCP stack tuned with CUBIC\n- Network throttling removed")