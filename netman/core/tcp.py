"""
NetMan TCP/IP Engine
Manages TCP window auto-tuning, CUBIC congestion control, RSS, RSC, and ECN.
"""
from typing import Dict, Any
from netman.core.utils import run_command

class TcpManager:
    @staticmethod
    def get_tcp_global_settings() -> Dict[str, str]:
        """Gets current TCP global stack settings."""
        settings = {}
        code, out, _ = run_command("netsh int tcp show global")
        if code == 0:
            for line in out.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    settings[k.strip()] = v.strip()
        return settings

    @staticmethod
    def optimize_tcp_stack() -> Dict[str, bool]:
        """Applies CUBIC congestion provider, Normal Auto-Tuning, RSS, RSC, and HyStart."""
        commands = [
            ("Auto-Tuning Level", "netsh int tcp set global autotuninglevel=normal"),
            ("RSS (Receive Side Scaling)", "netsh int tcp set global rss=enabled"),
            ("RSC (Receive Segment Coalescing)", "netsh int tcp set global rsc=enabled"),
            ("TCP Fast Open", "netsh int tcp set global fastopen=enabled"),
            ("Fast Open Fallback", "netsh int tcp set global fastopenfallback=enabled"),
            ("HyStart", "netsh int tcp set global hystart=enabled"),
            ("PRR (Proportional Rate Reduction)", "netsh int tcp set global prr=enabled"),
            ("RFC 1323 Timestamps", "netsh int tcp set global timestamps=allowed"),
            ("Initial RTO (1000ms)", "netsh int tcp set global initialRto=1000"),
            ("CUBIC Congestion Provider", "netsh int tcp set supplemental template=internet congestionprovider=cubic")
        ]
        results = {}
        for name, cmd in commands:
            code, _, _ = run_command(cmd)
            results[name] = (code == 0)
        return results

    @staticmethod
    def reset_tcp_stack_defaults() -> bool:
        """Resets TCP stack to default Windows settings."""
        commands = [
            "netsh int tcp set global autotuninglevel=normal",
            "netsh int tcp set global rss=enabled",
            "netsh int tcp set global ecncapability=disabled",
            "netsh int tcp set global timestamps=allowed",
            "netsh int tcp set supplemental template=internet congestionprovider=default"
        ]
        for cmd in commands:
            run_command(cmd)
        return True
