"""
NetMan Backup & Snapshot Engine
Provides snapshot creation from live state, dynamic restoration from JSON snapshot,
and 1-click factory restore.
"""
import os
import json
import time
from typing import Dict, Any, Optional
from netman.core.wifi import WifiManager
from netman.core.dns import DnsManager
from netman.core.tcp import TcpManager
from netman.core.registry import RegistryTweaks

BACKUP_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "backup_state.json")

class BackupManager:
    @staticmethod
    def create_snapshot(adapter_name: str = "Wi-Fi") -> str:
        """Takes a full snapshot of Wi-Fi properties, DNS, and TCP settings and saves to JSON."""
        snapshot = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "adapter_name": adapter_name,
            "wifi_properties": WifiManager.get_adapter_advanced_properties(adapter_name),
            "dns_servers": DnsManager.get_current_dns(adapter_name),
            "tcp_settings": TcpManager.get_tcp_global_settings()
        }
        try:
            with open(BACKUP_FILE, "w", encoding="utf-8") as f:
                json.dump(snapshot, f, indent=2)
            return f"Snapshot saved successfully at {snapshot['timestamp']}."
        except Exception as e:
            return f"Failed to save snapshot: {e}"

    @staticmethod
    def get_snapshot_info() -> Optional[Dict[str, Any]]:
        """Returns loaded snapshot information if available."""
        if os.path.exists(BACKUP_FILE):
            try:
                with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    @staticmethod
    def restore_from_snapshot() -> Dict[str, str]:
        """Restores the exact previous configuration saved in backup_state.json."""
        snap = BackupManager.get_snapshot_info()
        if not snap:
            return BackupManager.restore_defaults("Wi-Fi")

        log = {}
        adapter_name = snap.get("adapter_name", "Wi-Fi")

        # 1. Restore Wi-Fi Adapter Properties
        wifi_props = snap.get("wifi_properties", {})
        for prop_name, prop_data in wifi_props.items():
            val = prop_data.get("value")
            if val:
                WifiManager.set_adapter_property(prop_name, val, adapter_name)
        log["Wi-Fi Adapter"] = f"Restored {len(wifi_props)} adapter properties from snapshot."

        # 2. Restore DNS
        dns_servers = snap.get("dns_servers", [])
        if dns_servers:
            DnsManager.set_dns(dns_servers, adapter_name)
            log["DNS"] = f"Restored DNS servers: {', '.join(dns_servers)}"
        else:
            DnsManager.reset_to_dhcp(adapter_name)
            log["DNS"] = "Restored DNS to automatic DHCP."

        # 3. Restore TCP defaults
        TcpManager.reset_tcp_stack_defaults()
        log["TCP Stack"] = "Restored TCP global settings."

        # 4. Restore Registry
        RegistryTweaks.restore_registry_defaults()
        log["Registry Tweaks"] = "Restored Windows default network throttling."

        return log

    @staticmethod
    def restore_defaults(adapter_name: str = "Wi-Fi") -> Dict[str, str]:
        """Restores Wi-Fi adapter properties, DNS, TCP stack, and registry tweaks to default Windows settings."""
        log = {}
        # 1. Reset Wi-Fi adapter properties
        WifiManager.set_adapter_property("Preferred Band", "1. No Preference", adapter_name)
        WifiManager.set_adapter_property("Throughput Booster", "Disabled", adapter_name)
        WifiManager.set_adapter_property("MIMO Power Save Mode", "Auto SMPS", adapter_name)
        log["Wi-Fi Adapter"] = "Reset to No Band Preference & default power savings."

        # 2. Reset DNS to DHCP
        DnsManager.reset_to_dhcp(adapter_name)
        log["DNS"] = "Reset to DHCP (Automatic ISP/Router assigned)."

        # 3. Reset TCP Stack
        TcpManager.reset_tcp_stack_defaults()
        log["TCP Stack"] = "Reset to Windows global defaults."

        # 4. Reset Registry Tweaks
        RegistryTweaks.restore_registry_defaults()
        log["Registry Tweaks"] = "Restored Windows default network throttling."

        return log
