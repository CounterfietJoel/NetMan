"""
NetMan Advanced Network Engine
Implements MTU Discovery & Optimizer, IPv6 Latency Fixes, and Adapter Power Management.
"""
import re
from typing import Tuple, Dict, Any
from netman.core.utils import run_powershell, run_command

class AdvancedNetworkManager:
    @staticmethod
    def find_optimal_mtu(target_host: str = "1.1.1.1") -> int:
        """
        Sweeps ICMP packet sizes with Don't Fragment (DF) flag set to find 
        the maximum unfragmented MTU for the current network link.
        """
        best_payload = 1472  # 1472 payload + 28 bytes header = 1500 MTU
        for payload in range(1472, 1300, -10):
            # ping -f -n 1 -l <payload> <host>
            code, out, _ = run_command(f"ping -f -n 1 -l {payload} {target_host}")
            if "Packet needs to be fragmented" not in out and "0% loss" in out or "Reply from" in out:
                best_payload = payload
                break
        optimal_mtu = best_payload + 28
        return optimal_mtu

    @staticmethod
    def get_current_mtu(adapter_name: str = "Wi-Fi") -> int:
        """Gets current configured MTU for the interface."""
        code, out, _ = run_powershell(f'(Get-NetIPInterface -InterfaceAlias "{adapter_name}" -AddressFamily IPv4 -ErrorAction SilentlyContinue).NlMtu')
        if code == 0 and out.strip().isdigit():
            return int(out.strip())
        return 1500

    @staticmethod
    def set_mtu(mtu_val: int, adapter_name: str = "Wi-Fi") -> bool:
        """Sets persistent MTU on the network interface."""
        cmd = f'netsh interface ipv4 set subinterface "{adapter_name}" mtu={mtu_val} store=persistent'
        code, _, _ = run_command(cmd)
        return code == 0

    @staticmethod
    def optimize_ipv6_prefix_policy() -> bool:
        """
        Configures Windows IPv6 prefix policy to prefer IPv4 over broken IPv6.
        Prevents the classic 1-3 second connection timeout delay on campus/ISP networks
        where IPv6 is half-configured with no external gateway route.
        """
        cmd = "netsh interface ipv6 set prefixpolicy ::ffff:0:0/96 46 4"
        code, _, _ = run_command(cmd)
        return code == 0

    @staticmethod
    def reset_ipv6_prefix_policy() -> bool:
        """Resets IPv6 prefix policies to Windows default."""
        cmd = "netsh interface ipv6 reset"
        code, _, _ = run_command(cmd)
        return code == 0
