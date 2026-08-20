"""
NetMan Main Window Application
Sidebar navigation, sleek dark theme, view switcher.
"""
import tkinter as tk
from tkinter import ttk
from netman.ui.theme import THEME
from netman.ui.views.dashboard import DashboardView
from netman.ui.views.wifi_view import WifiView
from netman.ui.views.dns_view import DnsView
from netman.ui.views.tcp_view import TcpView
from netman.ui.views.diagnostics_view import DiagnosticsView
from netman.ui.views.backup_view import BackupView

class NetManApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NetMan - Windows Network & Wi-Fi Optimizer")
        self.geometry("1000x680")
        self.minsize(900, 600)
        self.configure(bg=THEME["bg_dark"])

        self.setup_layout()
        self.switch_view("dashboard")

    def setup_layout(self):
        # Sidebar Frame
        self.sidebar = tk.Frame(self, bg=THEME["bg_sidebar"], width=220, highlightbackground=THEME["border"], highlightthickness=1)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand / Logo Header
        brand_frame = tk.Frame(self.sidebar, bg=THEME["bg_sidebar"], padx=15, pady=20)
        brand_frame.pack(fill="x")

        logo = tk.Label(brand_frame, text="⚡ NetMan", font=("Segoe UI", 16, "bold"), fg=THEME["text_primary"], bg=THEME["bg_sidebar"])
        logo.pack(anchor="w")

        sub = tk.Label(brand_frame, text="v1.0.0 Open Source", font=THEME["font_small"], fg=THEME["text_muted"], bg=THEME["bg_sidebar"])
        sub.pack(anchor="w")

        # Nav Buttons Container
        self.nav_frame = tk.Frame(self.sidebar, bg=THEME["bg_sidebar"], padx=10, pady=10)
        self.nav_frame.pack(fill="x")

        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "📊 Dashboard"),
            ("wifi", "📶 Wi-Fi Optimizer"),
            ("dns", "🌐 DNS Benchmark"),
            ("tcp", "⚙ TCP Stack & QoS"),
            ("diagnostics", "📡 Live Diagnostics"),
            ("backup", "🔄 Backup & Restore")
        ]

        for view_key, label in nav_items:
            btn = tk.Button(
                self.nav_frame,
                text=label,
                font=THEME["font_bold"],
                fg=THEME["text_secondary"],
                bg=THEME["bg_sidebar"],
                activebackground=THEME["bg_card"],
                activeforeground=THEME["text_primary"],
                relief="flat",
                anchor="w",
                padx=15,
                pady=10,
                cursor="hand2",
                command=lambda k=view_key: self.switch_view(k)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[view_key] = btn

        # Main Content Container
        self.content_area = tk.Frame(self, bg=THEME["bg_dark"])
        self.content_area.pack(side="right", fill="both", expand=True)

        # Pre-instantiate views
        self.views = {
            "dashboard": DashboardView(self.content_area),
            "wifi": WifiView(self.content_area),
            "dns": DnsView(self.content_area),
            "tcp": TcpView(self.content_area),
            "diagnostics": DiagnosticsView(self.content_area),
            "backup": BackupView(self.content_area)
        }

    def switch_view(self, view_name):
        for k, v in self.views.items():
            v.pack_forget()

        for k, btn in self.nav_buttons.items():
            if k == view_name:
                btn.config(bg=THEME["accent_primary"], fg="#FFFFFF")
            else:
                btn.config(bg=THEME["bg_sidebar"], fg=THEME["text_secondary"])

        target = self.views.get(view_name)
        if target:
            target.pack(fill="both", expand=True)
