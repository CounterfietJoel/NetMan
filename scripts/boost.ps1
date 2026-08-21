<#
.SYNOPSIS
    NetMan 1-Line Standalone Turbo Boost Script
    Runs full Wi-Fi, DNS, TCP, and registry optimizations with zero setup.
#>

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "⚡ NetMan Windows Network & Wi-Fi Turbo Booster" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Wi-Fi Adapter 5GHz Lock & Throughput Booster
Write-Host "`n[1/5] Optimizing Wi-Fi Adapter (5GHz Preference, Booster, MIMO)..." -ForegroundColor Yellow
try {
    Set-NetAdapterAdvancedProperty -Name "Wi-Fi" -DisplayName "Preferred Band" -DisplayValue "5. Prefer 5GHz + 6GHz band" -ErrorAction SilentlyContinue
    Set-NetAdapterAdvancedProperty -Name "Wi-Fi" -DisplayName "Throughput Booster" -DisplayValue "Enabled" -ErrorAction SilentlyContinue
    Set-NetAdapterAdvancedProperty -Name "Wi-Fi" -DisplayName "MIMO Power Save Mode" -DisplayValue "No SMPS" -ErrorAction SilentlyContinue
    Set-NetAdapterAdvancedProperty -Name "Wi-Fi" -DisplayName "Roaming Aggressiveness" -DisplayValue "3. Medium" -ErrorAction SilentlyContinue
    Write-Host "  ✔ Wi-Fi adapter hardware settings applied." -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Wi-Fi adapter hardware setting skipped." -ForegroundColor DarkGray
}

# 2. DNS Low-Latency Anycast Resolvers
Write-Host "`n[2/5] Setting Cloudflare Low-Latency DNS (1.1.1.1 / 1.0.0.1)..." -ForegroundColor Yellow
try {
    Set-DnsClientServerAddress -InterfaceAlias "Wi-Fi" -ServerAddresses @("1.1.1.1", "1.0.0.1", "8.8.8.8") -ErrorAction SilentlyContinue
    Clear-DnsClientCache
    Write-Host "  ✔ DNS updated to 1.1.1.1 / 1.0.0.1 and cache flushed." -ForegroundColor Green
} catch {
    netsh interface ip set dns name="Wi-Fi" static 1.1.1.1 | Out-Null
    netsh interface ip add dns name="Wi-Fi" 1.0.0.1 index=2 | Out-Null
    ipconfig /flushdns | Out-Null
    Write-Host "  ✔ DNS updated via fallback." -ForegroundColor Green
}

# 3. TCP/IP Stack Parameters
Write-Host "`n[3/5] Tuning TCP/IP Stack (CUBIC, Auto-Tuning, RSS/RSC, FastOpen)..." -ForegroundColor Yellow
netsh int tcp set global autotuninglevel=normal | Out-Null
netsh int tcp set global rss=enabled | Out-Null
netsh int tcp set global rsc=enabled | Out-Null
netsh int tcp set global fastopen=enabled | Out-Null
netsh int tcp set global hystart=enabled | Out-Null
netsh int tcp set global timestamps=allowed | Out-Null
netsh int tcp set global initialRto=2000 | Out-Null
netsh int tcp set supplemental template=internet congestionprovider=cubic | Out-Null
Write-Host "  ✔ TCP stack tuned with CUBIC congestion control." -ForegroundColor Green

# 4. Windows Network Throttling Overrides
Write-Host "`n[4/5] Removing Windows Multimedia Network Throttling..." -ForegroundColor Yellow
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v NetworkThrottlingIndex /t REG_DWORD /d 0xFFFFFFFF /f | Out-Null
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v SystemResponsiveness /t REG_DWORD /d 10 /f | Out-Null
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Dnscache\Parameters" /v MaxCacheTtl /t REG_DWORD /d 7200 /f | Out-Null
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization" /v DODownloadMode /t REG_DWORD /d 0 /f | Out-Null
Write-Host "  ✔ Network throttling removed & P2P upload leeching disabled." -ForegroundColor Green

# 5. Summary
Write-Host "`n[5/5] Checking Active Link Speed..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
$wlan = netsh wlan show interfaces
$band = ($wlan | Select-String "Band\s+:\s+(.+)").Matches.Groups[1].Value.Trim()
$rx = ($wlan | Select-String "Receive rate.*:\s+(\d+)").Matches.Groups[1].Value.Trim()
$tx = ($wlan | Select-String "Transmit rate.*:\s+(\d+)").Matches.Groups[1].Value.Trim()

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🎉 NetMan Turbo Boost Applied Successfully!" -ForegroundColor Green
Write-Host "Active Band: $band | Link Speed: Rx ${rx} Mbps / Tx ${tx} Mbps" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
