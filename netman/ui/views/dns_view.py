"""
NetMan DNS View
DNS benchmark engine & 1-Click Anycast DNS Switcher.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from netman.ui.theme import THEME
from netman.core.dns import DnsManager, DNS_PRESETS

class DnsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=THEME["bg_dark"])
        self.benchmark_results = {}
        self.setup_ui()
        self.load_current_dns()

    def setup_ui(self):
        header = tk.Frame(self, bg=THEME["bg_dark"])
        header.pack(fill="x", padx=25, pady=(20, 10))

        title = tk.Label(header, text="DNS Benchmark & Switcher", font=THEME["font_title"], fg=THEME["text_primary"], bg=THEME["bg_dark"])
        title.pack(anchor="w")

        subtitle = tk.Label(header, text="Benchmark response times to public Anycast resolvers and switch to the lowest-latency DNS in 1 click.", font=THEME["font_small"], fg=THEME["text_secondary"], bg=THEME["bg_dark"])
        subtitle.pack(anchor="w", pady=(2, 0))

        # Current DNS card
        top_card = tk.Frame(self, bg=THEME["bg_card"], padx=15, pady=12, highlightbackground=THEME["border"], highlightthickness=1)
        top_card.pack(fill="x", padx=25, pady=10)

        self.lbl_current = tk.Label(top_card, text="Active DNS Servers: Scanning...", font=THEME["font_bold"], fg=THEME["text_primary"], bg=THEME["bg_card"])
        self.lbl_current.pack(side="left")

        btn_flush = tk.Button(top_card, text="🧹 Flush DNS Cache", font=THEME["font_small"], bg=THEME["bg_card_hover"], fg=THEME["text_primary"], relief="flat", padx=10, pady=5, cursor="hand2", command=self.flush_cache)
        btn_flush.pack(side="right")

        # Benchmark List Card
        card = tk.Frame(self, bg=THEME["bg_card"], padx=20, pady=15, highlightbackground=THEME["border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=25, pady=10)

        # Benchmark actions
        action_row = tk.Frame(card, bg=THEME["bg_card"])
        action_row.pack(fill="x", pady=(0, 10))

        self.btn_bench = tk.Button(action_row, text="⚡ Run Speed Benchmark (All Providers)", font=THEME["font_bold"], bg=THEME["accent_primary"], fg="#FFFFFF", relief="flat", padx=15, pady=8, cursor="hand2", command=self.run_benchmark)
        self.btn_bench.pack(side="left")

        # Table for Providers
        self.table_frame = tk.Frame(card, bg=THEME["bg_card"])
        self.table_frame.pack(fill="both", expand=True)

        self.render_preset_list()

    def render_preset_list(self):
        for w in self.table_frame.winfo_children():
            w.destroy()

        r = 0
        for name, ips in DNS_PRESETS.items():
            f = tk.Frame(self.table_frame, bg=THEME["bg_card_hover"], padx=12, pady=8, highlightbackground=THEME["border"], highlightthickness=1)
            f.pack(fill="x", pady=4)

            left = tk.Frame(f, bg=THEME["bg_card_hover"])
            left.pack(side="left", fill="x", expand=True)

            t = tk.Label(left, text=name, font=THEME["font_bold"], fg=THEME["text_primary"], bg=THEME["bg_card_hover"])
            t.pack(anchor="w")

            ip_text = f"Primary: {ips[0]} | Secondary: {ips[1]}"
            sub = tk.Label(left, text=ip_text, font=THEME["font_small"], fg=THEME["text_secondary"], bg=THEME["bg_card_hover"])
            sub.pack(anchor="w")

            # Benchmark Result Label
            ms_val = self.benchmark_results.get(name, "-- ms")
            ms_color = THEME["accent_success"] if "ms" in str(ms_val) and ms_val != "-- ms" else THEME["text_secondary"]
            ms_lbl = tk.Label(f, text=str(ms_val), font=("Segoe UI", 12, "bold"), fg=ms_color, bg=THEME["bg_card_hover"], width=10)
            ms_lbl.pack(side="left", padx=15)

            # Apply Button
            btn_set = tk.Button(f, text="Set as Active", font=THEME["font_small"], bg=THEME["accent_primary"], fg="#FFFFFF", relief="flat", padx=12, pady=4, cursor="hand2", command=lambda s=ips, n=name: self.set_dns_preset(s, n))
            btn_set.pack(side="right")

    def load_current_dns(self):
        def _task():
            dns = DnsManager.get_current_dns("Wi-Fi")
            text = "Active DNS: " + (", ".join(dns) if dns else "Automatic (DHCP Router)")
            self.after(0, lambda: self.lbl_current.config(text=text))
        threading.Thread(target=_task, daemon=True).start()

    def run_benchmark(self):
        self.btn_bench.config(state="disabled", text="Testing Latency...")
        def _task():
            for name, ips in DNS_PRESETS.items():
                latency = DnsManager.benchmark_resolver(ips[0])
                self.benchmark_results[name] = f"{latency} ms" if latency > 0 else "Timed Out"
                self.after(0, self.render_preset_list)
            self.after(0, lambda: self.btn_bench.config(state="normal", text="⚡ Run Speed Benchmark (All Providers)"))
        threading.Thread(target=_task, daemon=True).start()

    def set_dns_preset(self, servers, name):
        def _task():
            DnsManager.set_dns(servers, "Wi-Fi")
            self.after(0, lambda: messagebox.showinfo("NetMan DNS", f"Successfully activated {name} ({', '.join(servers)})!"))
            self.load_current_dns()
        threading.Thread(target=_task, daemon=True).start()

    def flush_cache(self):
        DnsManager.flush_cache()
        messagebox.showinfo("NetMan DNS", "Local Windows DNS Cache flushed successfully!")
