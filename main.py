"""
NetMan Entry Point
Launches GUI application or CLI turbo optimizer.
"""
import sys
from netman.ui.app import NetManApp
from netman.core.wifi import WifiManager
from netman.core.dns import DnsManager
from netman.core.tcp import TcpManager
from netman.core.registry import RegistryTweaks
from netman.core.backup import BackupManager

def cli_boost():
    print("=" * 60)
    print("⚡ NetMan CLI Turbo Optimizer")
    print("=" * 60)
    print("[1/5] Creating safety snapshot...")
    BackupManager.create_snapshot("Wi-Fi")
    
    print("[2/5] Optimizing Intel/Realtek Wi-Fi Adapter (5GHz Preference, Booster, MIMO)...")
    WifiManager.optimize_wifi_for_performance("Wi-Fi")
    
    print("[3/5] Setting Cloudflare Low-Latency DNS (1.1.1.1 / 1.0.0.1)...")
    DnsManager.set_dns(["1.1.1.1", "1.0.0.1", "8.8.8.8"], "Wi-Fi")
    
    print("[4/5] Tuning TCP/IP Stack Global Parameters (CUBIC, AutoTuning, FastOpen)...")
    TcpManager.optimize_tcp_stack()
    
    print("[5/5] Disabling Windows Network Throttling & P2P Delivery Optimization...")
    RegistryTweaks.apply_network_throttling_removal()
    RegistryTweaks.optimize_dns_cache_ttl()
    RegistryTweaks.disable_delivery_optimization_p2p()
    
    print("\n[✔] All optimizations completed successfully!")

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("--boost", "-b", "--cli"):
        cli_boost()
    else:
        app = NetManApp()
        app.mainloop()

if __name__ == "__main__":
    main()
