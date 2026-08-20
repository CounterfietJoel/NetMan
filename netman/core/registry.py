"""
NetMan Registry Engine
Manages Windows network throttling index, multimedia network responsiveness, and Delivery Optimization.
"""
from typing import Dict, Any
from netman.core.utils import run_command

class RegistryTweaks:
    @staticmethod
    def apply_network_throttling_removal() -> bool:
        """Disables Windows network throttling for non-multimedia traffic (default throttles to 10 pkts/ms)."""
        cmd1 = r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v NetworkThrottlingIndex /t REG_DWORD /d 0xFFFFFFFF /f'
        cmd2 = r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v SystemResponsiveness /t REG_DWORD /d 10 /f'
        c1, _, _ = run_command(cmd1)
        c2, _, _ = run_command(cmd2)
        return c1 == 0 and c2 == 0

    @staticmethod
    def optimize_dns_cache_ttl() -> bool:
        """Increases positive DNS cache TTL and decreases negative cache TTL for lightning-fast lookups."""
        cmd1 = r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters" /v MaxCacheTtl /t REG_DWORD /d 7200 /f'
        cmd2 = r'reg add "HKLM\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters" /v MaxNegativeCacheTtl /t REG_DWORD /d 5 /f'
        c1, _, _ = run_command(cmd1)
        c2, _, _ = run_command(cmd2)
        return c1 == 0 and c2 == 0

    @staticmethod
    def disable_delivery_optimization_p2p() -> bool:
        """Stops background Windows Update Delivery Optimization from uploading data to internet peers."""
        cmd = r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization" /v DODownloadMode /t REG_DWORD /d 0 /f'
        c, _, _ = run_command(cmd)
        return c == 0

    @staticmethod
    def restore_registry_defaults() -> bool:
        """Restores default Windows values for multimedia profile and Delivery Optimization."""
        cmd1 = r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v NetworkThrottlingIndex /t REG_DWORD /d 10 /f'
        cmd2 = r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v SystemResponsiveness /t REG_DWORD /d 20 /f'
        cmd3 = r'reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization" /v DODownloadMode /f'
        run_command(cmd1)
        run_command(cmd2)
        run_command(cmd3)
        return True
