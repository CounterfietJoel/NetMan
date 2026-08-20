"""
NetMan Diagnostics & Ping Monitor View
Live ping latency graph and packet jitter analyzer.
"""
import tkinter as tk
from tkinter import ttk
import threading
import time
from netman.ui.theme import THEME
from netman.core.utils import run_powershell

class DiagnosticsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=THEME["bg_dark"])
        self.is_monitoring = False
        self.history = []
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg=THEME["bg_dark"])
        header.pack(fill="x", padx=25, pady=(20, 10))

        title = tk.Label(header, text="Network Diagnostics & Latency Monitor", font=THEME["font_title"], fg=THEME["text_primary"], bg=THEME["bg_dark"])
        title.pack(anchor="w")

        subtitle = tk.Label(header, text="Live ping tests to gateway router and internet endpoints to detect jitter and packet loss.", font=THEME["font_small"], fg=THEME["text_secondary"], bg=THEME["bg_dark"])
        subtitle.pack(anchor="w", pady=(2, 0))

        # Controls & Live Stats Card
        top_card = tk.Frame(self, bg=THEME["bg_card"], padx=20, pady=15, highlightbackground=THEME["border"], highlightthickness=1)
        top_card.pack(fill="x", padx=25, pady=10)

        self.btn_toggle = tk.Button(top_card, text="▶ Start Live Ping Monitor", font=THEME["font_bold"], bg=THEME["accent_primary"], fg="#FFFFFF", relief="flat", padx=15, pady=8, cursor="hand2", command=self.toggle_monitoring)
        self.btn_toggle.pack(side="left")

        self.lbl_gw = tk.Label(top_card, text="Gateway Ping: -- ms", font=THEME["font_body"], fg=THEME["text_primary"], bg=THEME["bg_card"])
        self.lbl_gw.pack(side="left", padx=20)

        self.lbl_inet = tk.Label(top_card, text="Internet Ping (1.1.1.1): -- ms", font=THEME["font_body"], fg=THEME["text_primary"], bg=THEME["bg_card"])
        self.lbl_inet.pack(side="left", padx=20)

        # Log Output Card
        log_card = tk.Frame(self, bg=THEME["bg_card"], padx=15, pady=15, highlightbackground=THEME["border"], highlightthickness=1)
        log_card.pack(fill="both", expand=True, padx=25, pady=10)

        self.txt_log = tk.Text(log_card, bg="#0e1013", fg="#D1D5DB", font=("Consolas", 10), relief="flat", padx=10, pady=10)
        self.txt_log.pack(fill="both", expand=True)

    def toggle_monitoring(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.btn_toggle.config(text="⏹ Stop Monitoring", bg=THEME["accent_warning"])
            threading.Thread(target=self._monitor_loop, daemon=True).start()
        else:
            self.is_monitoring = False
            self.btn_toggle.config(text="▶ Start Live Ping Monitor", bg=THEME["accent_primary"])

    def _monitor_loop(self):
        while self.is_monitoring:
            cmd = """
            $gw = (Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue | Select-Object -First 1).NextHop
            $resGw = if ($gw) { (Test-Connection -ComputerName $gw -Count 1 -ErrorAction SilentlyContinue).ResponseTime } else { -1 }
            $resInet = (Test-Connection -ComputerName '1.1.1.1' -Count 1 -ErrorAction SilentlyContinue).ResponseTime
            Write-Output "$resGw,$resInet"
            """
            code, out, _ = run_powershell(cmd)
            if code == 0 and "," in out:
                parts = out.strip().split(",")
                gw_ms = parts[0] if len(parts) > 0 else "--"
                inet_ms = parts[1] if len(parts) > 1 else "--"
                self.after(0, lambda g=gw_ms, i=inet_ms: self._append_log(g, i))
            time.sleep(1.5)

    def _append_log(self, gw_ms, inet_ms):
        ts = time.strftime("%H:%M:%S")
        self.lbl_gw.config(text=f"Gateway Ping: {gw_ms} ms")
        self.lbl_inet.config(text=f"Internet Ping (1.1.1.1): {inet_ms} ms")
        line = f"[{ts}] Gateway: {gw_ms} ms  |  Internet (Cloudflare): {inet_ms} ms\n"
        self.txt_log.insert("end", line)
        self.txt_log.see("end")
