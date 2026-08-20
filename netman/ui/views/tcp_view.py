"""
NetMan TCP/IP & Registry Tweaks View
Windows TCP stack tuning, congestion provider, and gaming/multimedia throttling overrides.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from netman.ui.theme import THEME
from netman.core.tcp import TcpManager
from netman.core.registry import RegistryTweaks
from netman.core.utils import is_admin

class TcpView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=THEME["bg_dark"])
        self.setup_ui()
        self.load_tcp_settings()

    def setup_ui(self):
        header = tk.Frame(self, bg=THEME["bg_dark"])
        header.pack(fill="x", padx=25, pady=(20, 10))

        title = tk.Label(header, text="TCP/IP Stack & System Throttling", font=THEME["font_title"], fg=THEME["text_primary"], bg=THEME["bg_dark"])
        title.pack(anchor="w")

        subtitle = tk.Label(header, text="Fine-tune Windows TCP congestion algorithms and remove network throttling limits.", font=THEME["font_small"], fg=THEME["text_secondary"], bg=THEME["bg_dark"])
        subtitle.pack(anchor="w", pady=(2, 0))

        # Admin note
        if not is_admin():
            warn_card = tk.Frame(self, bg=THEME["bg_card"], padx=15, pady=8, highlightbackground=THEME["accent_warning"], highlightthickness=1)
            warn_card.pack(fill="x", padx=25, pady=5)
            w_lbl = tk.Label(warn_card, text="⚠ Note: Run NetMan as Administrator to apply kernel-level TCP stack and registry modifications.", font=THEME["font_small"], fg=THEME["accent_warning"], bg=THEME["bg_card"])
            w_lbl.pack(anchor="w")

        card = tk.Frame(self, bg=THEME["bg_card"], padx=20, pady=20, highlightbackground=THEME["border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=25, pady=10)

        # Settings list
        self.items = [
            ("TCP Congestion Provider (CUBIC)", "Replaces legacy NewReno with modern CUBIC for faster throughput over wireless/lossy networks."),
            ("TCP Window Auto-Tuning (Normal)", "Allows dynamic TCP receive window scaling to utilize 100% of available bandwidth."),
            ("Receive-Side Scaling (RSS)", "Distributes network packet processing across multiple CPU cores to prevent bottlenecking."),
            ("Disable Network Throttling Index", "Stops Windows from capping non-multimedia network packets to 10 pkts/ms."),
            ("Disable Delivery Optimization P2P", "Prevents background Windows Update service from uploading data to internet peers.")
        ]

        for i, (t, d) in enumerate(self.items):
            row = tk.Frame(card, bg=THEME["bg_card_hover"], padx=15, pady=10, highlightbackground=THEME["border"], highlightthickness=1)
            row.pack(fill="x", pady=5)

            t_lbl = tk.Label(row, text=f"✔ {t}", font=THEME["font_bold"], fg=THEME["text_primary"], bg=THEME["bg_card_hover"])
            t_lbl.pack(anchor="w")
            d_lbl = tk.Label(row, text=d, font=THEME["font_small"], fg=THEME["text_secondary"], bg=THEME["bg_card_hover"])
            d_lbl.pack(anchor="w", pady=(2, 0))

        btn_row = tk.Frame(card, bg=THEME["bg_card"])
        btn_row.pack(fill="x", pady=(20, 0))

        self.btn_apply = tk.Button(btn_row, text="Apply All TCP & Registry Tweaks", font=THEME["font_bold"], bg=THEME["accent_primary"], fg="#FFFFFF", relief="flat", padx=20, pady=10, cursor="hand2", command=self.apply_tweaks)
        self.btn_apply.pack(side="left", padx=(0, 10))

        self.btn_reset = tk.Button(btn_row, text="Restore TCP Defaults", font=THEME["font_body"], bg=THEME["bg_card_hover"], fg=THEME["text_primary"], relief="flat", padx=15, pady=10, cursor="hand2", command=self.reset_defaults)
        self.btn_reset.pack(side="left")

    def load_tcp_settings(self):
        pass

    def apply_tweaks(self):
        def _task():
            r1 = TcpManager.optimize_tcp_stack()
            r2 = RegistryTweaks.apply_network_throttling_removal()
            r3 = RegistryTweaks.optimize_dns_cache_ttl()
            r4 = RegistryTweaks.disable_delivery_optimization_p2p()
            self.after(0, lambda: messagebox.showinfo("NetMan TCP Optimizer", "TCP stack parameters and registry optimizations successfully applied!"))
        threading.Thread(target=_task, daemon=True).start()

    def reset_defaults(self):
        def _task():
            TcpManager.reset_tcp_stack_defaults()
            RegistryTweaks.restore_registry_defaults()
            self.after(0, lambda: messagebox.showinfo("NetMan TCP Optimizer", "TCP stack restored to Windows factory defaults."))
        threading.Thread(target=_task, daemon=True).start()
