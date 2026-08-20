"""
NetMan Wi-Fi View
Fine-grained controls for Intel Wi-Fi 6/6E/7 and standard wireless adapter properties.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from netman.ui.theme import THEME
from netman.core.wifi import WifiManager

class WifiView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=THEME["bg_dark"])
        self.setup_ui()
        self.load_adapter_properties()

    def setup_ui(self):
        header = tk.Frame(self, bg=THEME["bg_dark"])
        header.pack(fill="x", padx=25, pady=(20, 10))

        title = tk.Label(header, text="Wi-Fi Hardware & Driver Tuning", font=THEME["font_title"], fg=THEME["text_primary"], bg=THEME["bg_dark"])
        title.pack(anchor="w")

        subtitle = tk.Label(header, text="Configure Intel / Realtek adapter advanced properties to prevent 2.4GHz sticky roaming and maximize throughput.", font=THEME["font_small"], fg=THEME["text_secondary"], bg=THEME["bg_dark"])
        subtitle.pack(anchor="w", pady=(2, 0))

        # Main Properties Card
        card = tk.Frame(self, bg=THEME["bg_card"], padx=20, pady=20, highlightbackground=THEME["border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=25, pady=15)

        # Property Rows
        self.combos = {}

        self.add_prop_row(card, 0, "Preferred Band", "Controls whether the adapter prefers 5GHz/6GHz over crowded 2.4GHz bands.", 
                          ["5. Prefer 5GHz + 6GHz band", "3. Prefer 5GHz band", "2. Prefer 2.4GHz band", "1. No Preference"])

        self.add_prop_row(card, 1, "Throughput Booster", "Enables packet burst aggregation on transmission for higher upload/download rates.", 
                          ["Enabled", "Disabled"])

        self.add_prop_row(card, 2, "MIMO Power Save Mode", "Controls antenna sleep. 'No SMPS' keeps both RX/TX antenna chains active at all times.", 
                          ["No SMPS", "Auto SMPS", "Dynamic SMPS", "Static SMPS"])

        self.add_prop_row(card, 3, "Roaming Aggressiveness", "How actively the laptop scans and switches to a stronger access point as you move.", 
                          ["3. Medium", "4. Medium-High", "5. Highest", "2. Medium-low", "1. Lowest"])

        # Buttons
        btn_frame = tk.Frame(card, bg=THEME["bg_card"])
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(25, 0), sticky="w")

        self.btn_apply = tk.Button(btn_frame, text="Save & Apply Wi-Fi Settings", font=THEME["font_bold"], bg=THEME["accent_primary"], fg="#FFFFFF", relief="flat", padx=20, pady=8, cursor="hand2", command=self.apply_settings)
        self.btn_apply.pack(side="left", padx=(0, 10))

        self.btn_reload = tk.Button(btn_frame, text="Reload Current Driver Values", font=THEME["font_body"], bg=THEME["bg_card_hover"], fg=THEME["text_primary"], relief="flat", padx=15, pady=8, cursor="hand2", command=self.load_adapter_properties)
        self.btn_reload.pack(side="left")

        card.columnconfigure(0, weight=1)
        card.columnconfigure(1, weight=1)

    def add_prop_row(self, parent, row, title, desc, default_options):
        f = tk.Frame(parent, bg=THEME["bg_card"])
        f.grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)

        left = tk.Frame(f, bg=THEME["bg_card"])
        left.pack(side="left", fill="x", expand=True)

        t_lbl = tk.Label(left, text=title, font=THEME["font_header"], fg=THEME["text_primary"], bg=THEME["bg_card"])
        t_lbl.pack(anchor="w")
        d_lbl = tk.Label(left, text=desc, font=THEME["font_small"], fg=THEME["text_secondary"], bg=THEME["bg_card"], wraplength=450, justify="left")
        d_lbl.pack(anchor="w", pady=(2, 0))

        combo = ttk.Combobox(f, values=default_options, state="readonly", width=25, font=THEME["font_body"])
        combo.pack(side="right", padx=10)
        if default_options:
            combo.current(0)
        self.combos[title] = combo

    def load_adapter_properties(self):
        def _task():
            props = WifiManager.get_adapter_advanced_properties("Wi-Fi")
            self.after(0, lambda: self._update_props_ui(props))
        threading.Thread(target=_task, daemon=True).start()

    def _update_props_ui(self, props):
        for name, combo in self.combos.items():
            if name in props:
                val = props[name]["value"]
                valid = props[name]["valid_values"]
                if valid:
                    combo["values"] = valid
                if val:
                    combo.set(val)

    def apply_settings(self):
        def _apply():
            for name, combo in self.combos.items():
                val = combo.get()
                if val:
                    WifiManager.set_adapter_property(name, val, "Wi-Fi")
            self.after(0, lambda: messagebox.showinfo("NetMan", "Wi-Fi Adapter settings updated successfully!"))
        threading.Thread(target=_apply, daemon=True).start()
