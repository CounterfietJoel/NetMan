"""
NetMan DNS Engine
Manages DNS benchmarking, switching public Anycast providers, and cache flushing.
"""
import time
import socket
from typing import Dict, List, Tuple
from netman.core.utils import run_powershell, run_command

DNS_PRESETS = {
    "Cloudflare (Fastest & Privacy)": ["1.1.1.1", "1.0.0.1"],
    "Google Public DNS (Reliable)": ["8.8.8.8", "8.8.4.4"],
    "Quad9 (Malware Blocking)": ["9.9.9.9", "149.112.112.112"],
    "OpenDNS Home (Family Safe)": ["208.67.222.222", "208.67.220.220"],
    "Control D (Uncensored)": ["76.76.2.0", "76.76.10.0"],
    "AdGuard DNS (Ad Blocking)": ["94.140.14.14", "94.140.15.15"]
}

class DnsManager:
    @staticmethod
    def get_current_dns(adapter_name: str = "Wi-Fi") -> List[str]:
        """Gets current IPv4 DNS servers for adapter."""
        cmd = f"(Get-DnsClientServerAddress -InterfaceAlias '{adapter_name}' -AddressFamily IPv4 -ErrorAction SilentlyContinue).ServerAddresses"
        code, out, _ = run_powershell(cmd)
        if code == 0 and out:
            return [line.strip() for line in out.splitlines() if line.strip()]
        return []

    @staticmethod
    def benchmark_resolver(ip: str, test_domains: List[str] = None) -> float:
        """Benchmarks a DNS server IP by resolving domains and returns average latency in ms."""
        if test_domains is None:
            test_domains = ["google.com", "github.com", "cloudflare.com", "microsoft.com"]
            
        cmd = f"""
        $domains = @({','.join([f"'{d}'" for d in test_domains])})
        $ip = '{ip}'
        $times = @()
        foreach ($d in $domains) {{
            try {{
                $sw = [System.Diagnostics.Stopwatch]::StartNew()
                $null = Resolve-DnsName -Name $d -Server $ip -Type A -QuickTimeout -ErrorAction Stop
                $sw.Stop()
                $times += $sw.ElapsedMilliseconds
            }} catch {{}}
        }}
        if ($times.Count -gt 0) {{ ($times | Measure-Object -Average).Average }} else {{ -1 }}
        """
        code, out, _ = run_powershell(cmd)
        if code == 0 and out:
            try:
                val = float(out.strip())
                return round(val, 1)
            except ValueError:
                pass
        return -1.0

    @staticmethod
    def set_dns(servers: List[str], adapter_name: str = "Wi-Fi") -> bool:
        """Sets custom DNS servers on the adapter and flushes DNS cache."""
        if not servers:
            return DnsManager.reset_to_dhcp(adapter_name)
            
        server_args = "@(" + ",".join([f"'{s}'" for s in servers]) + ")"
        cmd = f"Set-DnsClientServerAddress -InterfaceAlias '{adapter_name}' -ServerAddresses {server_args} -ErrorAction Stop"
        code, _, _ = run_powershell(cmd)
        if code != 0:
            # Fallback to netsh
            first = servers[0]
            c1, _, _ = run_command(f'netsh interface ip set dns name="{adapter_name}" static {first}')
            for s in servers[1:]:
                run_command(f'netsh interface ip add dns name="{adapter_name}" {s} index=2')
        DnsManager.flush_cache()
        return True

    @staticmethod
    def reset_to_dhcp(adapter_name: str = "Wi-Fi") -> bool:
        """Resets DNS back to DHCP (automatic router assigned)."""
        cmd = f"Set-DnsClientServerAddress -InterfaceAlias '{adapter_name}' -ResetServerAddresses -ErrorAction SilentlyContinue"
        code, _, _ = run_powershell(cmd)
        if code != 0:
            run_command(f'netsh interface ip set dns name="{adapter_name}" dhcp')
        DnsManager.flush_cache()
        return True

    @staticmethod
    def flush_cache() -> bool:
        """Flushes the Windows local DNS resolver cache."""
        code, _, _ = run_command("ipconfig /flushdns")
        return code == 0
