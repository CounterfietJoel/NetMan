"""
NetMan Backup & Factory Restore View
Safe rollback and snapshot manager.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from netman.ui.theme import THEME
from netman.core.backup import BackupManager

class BackupView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=THEME["bg_dark"])
        self.setup_ui()
        self.check_snapshot()

    def setup_ui(self):
        header = tk.Frame(self, bg=THEME["bg_dark"])
        header.pack(fill="x", padx=25, pady=(20, 10))

        title = tk.Label(header, text="Backup & Factory Restore Point", font=THEME["font_title"], fg=THEME["text_primary"], bg=THEME["bg_dark"])
        title.pack(anchor="w")

        subtitle = tk.Label(header, text="NetMan creates automatic backups before applying changes. You can restore default Windows settings anytime in 1 click.", font=THEME["font_small"], fg=THEME["text_secondary"], bg=THEME["bg_dark"])
        subtitle.pack(anchor="w", pady=(2, 0))

        card = tk.Frame(self, bg=THEME["bg_card"], padx=20, pady=20, highlightbackground=THEME["border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=25, pady=15)

        self.lbl_snap = tk.Label(card, text="Snapshot Status: Checking...", font=THEME["font_bold"], fg=THEME["text_primary"], bg=THEME["bg_card"])
        self.lbl_snap.pack(anchor="w")

        desc = tk.Label(card, text="If you experience unexpected behavior or move to a network where default settings are preferred, click below to restore all Wi-Fi adapter properties, DHCP DNS, and Windows TCP settings back to factory state.", font=THEME["font_body"], fg=THEME["text_secondary"], bg=THEME["bg_card"], wraplength=650, justify="left")
        desc.pack(anchor="w", pady=(10, 20))

        btn_row = tk.Frame(card, bg=THEME["bg_card"])
        btn_row.pack(fill="x")

        btn_create = tk.Button(btn_row, text="📸 Create New Snapshot Now", font=THEME["font_body"], bg=THEME["bg_card_hover"], fg=THEME["text_primary"], relief="flat", padx=15, pady=10, cursor="hand2", command=self.create_snap)
        btn_create.pack(side="left", padx=(0, 10))

        btn_restore = tk.Button(btn_row, text="🔄 Restore All Windows Factory Defaults", font=THEME["font_bold"], bg=THEME["accent_warning"], fg="#FFFFFF", relief="flat", padx=20, pady=10, cursor="hand2", command=self.restore_defaults)
        btn_restore.pack(side="left")

    def check_snapshot(self):
        info = BackupManager.get_snapshot_info()
        if info:
            self.lbl_snap.config(text=f"📸 Last Saved Snapshot: {info.get('timestamp', 'Unknown')}", fg=THEME["accent_success"])
        else:
            self.lbl_snap.config(text="ℹ No saved snapshot yet. (Automatic snapshots are created when boosting).", fg=THEME["text_secondary"])

    def create_snap(self):
        res = BackupManager.create_snapshot("Wi-Fi")
        messagebox.showinfo("NetMan Snapshot", res)
        self.check_snapshot()

    def restore_defaults(self):
        if messagebox.askyesno("Confirm Factory Restore", "Are you sure you want to revert all Wi-Fi, DNS, TCP, and registry optimizations back to Windows default values?"):
            log = BackupManager.restore_defaults("Wi-Fi")
            messagebox.showinfo("NetMan Factory Restore", "All settings reverted to Windows factory defaults successfully!")
            self.check_snapshot()
