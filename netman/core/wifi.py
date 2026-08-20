"""
NetMan Wi-Fi Engine
Manages Wi-Fi adapter properties, BSSID scanning, band preference, and throughput booster.
"""
import re
from typing import Dict, List, Any, Optional
from netman.core.utils import run_powershell, run_command

class WifiManager:
    @staticmethod
    def get_current_connection() -> Dict[str, Any]:
        """Gets active Wi-Fi interface details (SSID, BSSID, Band, Channel, Signal, Link Speed)."""
        info = {
            "connected": False,
            "name": "Wi-Fi",
            "adapter": "Unknown",
            "ssid": "Not Connected",
            "bssid": "",
            "band": "Unknown",
            "channel": "",
            "signal": 0,
            "rx_rate": 0,
            "tx_rate": 0,
            "radio_type": ""
        }
        
        code, out, _ = run_command("netsh wlan show interfaces")
        if code != 0 or "State" not in out:
            return info
            
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("Description"):
                info["adapter"] = line.split(":", 1)[1].strip()
            elif line.startswith("State"):
                state = line.split(":", 1)[1].strip()
                info["connected"] = (state.lower() == "connected")
            elif line.startswith("SSID") and not line.startswith("SSID "):
                info["ssid"] = line.split(":", 1)[1].strip()
            elif line.startswith("AP BSSID") or line.startswith("BSSID"):
                info["bssid"] = line.split(":", 1)[1].strip()
            elif line.startswith("Band"):
                info["band"] = line.split(":", 1)[1].strip()
            elif line.startswith("Channel"):
                info["channel"] = line.split(":", 1)[1].strip()
            elif line.startswith("Signal"):
                sig_match = re.search(r"(\d+)%", line)
                if sig_match:
                    info["signal"] = int(sig_match.group(1))
            elif line.startswith("Receive rate"):
                r_match = re.search(r"(\d+)", line)
                if r_match:
                    info["rx_rate"] = int(r_match.group(1))
            elif line.startswith("Transmit rate"):
                t_match = re.search(r"(\d+)", line)
                if t_match:
                    info["tx_rate"] = int(t_match.group(1))
            elif line.startswith("Radio type"):
                info["radio_type"] = line.split(":", 1)[1].strip()
                
        return info

    @staticmethod
    def get_adapter_advanced_properties(adapter_name: str = "Wi-Fi") -> Dict[str, Dict[str, Any]]:
        """Gets configurable driver properties for the Wi-Fi card."""
        cmd = f"""
        Get-NetAdapterAdvancedProperty -Name '{adapter_name}' -ErrorAction SilentlyContinue | 
        Select-Object DisplayName, DisplayValue, ValidDisplayValues | 
        ConvertTo-Json -Compress
        """
        code, out, _ = run_powershell(cmd)
        result = {}
        if code == 0 and out:
            import json
            try:
                data = json.loads(out)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    name = item.get("DisplayName")
                    if name:
                        result[name] = {
                            "value": item.get("DisplayValue"),
                            "valid_values": item.get("ValidDisplayValues", [])
                        }
            except Exception:
                pass
        return result

    @staticmethod
    def set_adapter_property(display_name: str, display_value: str, adapter_name: str = "Wi-Fi") -> bool:
        """Sets an advanced hardware property on the adapter."""
        cmd = f"Set-NetAdapterAdvancedProperty -Name '{adapter_name}' -DisplayName '{display_name}' -DisplayValue '{display_value}' -ErrorAction Stop"
        code, _, _ = run_powershell(cmd)
        return code == 0

    @staticmethod
    def optimize_wifi_for_performance(adapter_name: str = "Wi-Fi") -> Dict[str, bool]:
        """Applies high-speed 5GHz preference, Throughput Booster, and full MIMO."""
        results = {}
        props = WifiManager.get_adapter_advanced_properties(adapter_name)
        
        # 1. Preferred Band
        if "Preferred Band" in props:
            valid = props["Preferred Band"]["valid_values"]
            target = "5. Prefer 5GHz + 6GHz band" if "5. Prefer 5GHz + 6GHz band" in valid else (
                "3. Prefer 5GHz band" if "3. Prefer 5GHz band" in valid else "Prefer 5GHz"
            )
            results["Preferred Band"] = WifiManager.set_adapter_property("Preferred Band", target, adapter_name)

        # 2. Throughput Booster
        if "Throughput Booster" in props:
            results["Throughput Booster"] = WifiManager.set_adapter_property("Throughput Booster", "Enabled", adapter_name)

        # 3. MIMO Power Save Mode (No SMPS keeps both RX/TX antenna chains active)
        if "MIMO Power Save Mode" in props:
            results["MIMO Power Save Mode"] = WifiManager.set_adapter_property("MIMO Power Save Mode", "No SMPS", adapter_name)

        # 4. Roaming Aggressiveness (Medium is optimal for campus/office networks)
        if "Roaming Aggressiveness" in props:
            results["Roaming Aggressiveness"] = WifiManager.set_adapter_property("Roaming Aggressiveness", "3. Medium", adapter_name)

        return results
