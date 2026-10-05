---
name: jarvis-secure
description: >
  One-command laptop security sweep + speed/hardening pass for Windows (Jarvis core).
  Read-only audit first (Defender status, threat history, live connections, listening ports,
  firewall, autoruns, scheduled tasks, network neighbors), then OPTIONAL hardening
  (Public firewall inbound block, disable SMB1, remove Lenovo SoftLanding bloat) and
  OPTIONAL cleanup (measure %TEMP%/caches/Recycle Bin, then clean safe targets).
  Ends with a hardware verdict (RAM / SSD vs HDD / CPU / free disk / power plan).
  Use when user says "run jarvis", "antivirus scan", "scan my laptop", "scan my network",
  "is my laptop safe", "clean temp files", "make my laptop faster", "security check",
  "/jarvis-secure", "harden my pc", or asks to check the machine/network for threats.
---

# Jarvis Secure — Windows laptop security + speed sweep

Windows-only (PowerShell). Three phases: **AUDIT (read-only)** → **HARDEN (opt-in)** → **CLEANUP + speed verdict (opt-in)**. Never run destructive/irreversible steps without explicit user yes. Caveman-mode safe (general terse, security/multi-step normal).

## HARD RULES (learned, do not violate)

- **Measure before delete.** Always size temp/cache/Recycle Bin and show the table BEFORE removing anything.
- **Recycle Bin = irreversible.** Never `Clear-RecycleBin` without explicit confirm — it can hold GBs the user wants back.
- **SSD = NEVER defrag.** Check `MediaType`. If SSD, do not suggest/run defrag (TRIM auto-handles; defrag wears it).
- **Elevation: don't fight quote-escaping.** `Start-Process -Verb RunAs` with inline `-Command "...\"...\""` reliably fails to parse. Instead WRITE a `.ps1` file and run it elevated via `-File`. Have it log result to a text file you can Read back (the non-elevated session can't read elevated stdout).
- **Cleaning %TEMP% deletes Claude's own task-output file.** Expect one "output file could not be read" error after a temp clean — harmless; re-measure to confirm.
- **Public Wi-Fi with one MAC for all IPs = client isolation (proxy-ARP).** Peers unreachable BY DESIGN — can't scan them, don't claim you can. Advise VPN + no plaintext logins.

## PHASE 1 — AUDIT (read-only, run in parallel)

```powershell
# Defender status + threat history
Get-MpComputerStatus | Select AMServiceEnabled,RealTimeProtectionEnabled,AntivirusSignatureLastUpdated,QuickScanAge,FullScanAge,NISEnabled | Format-List
Get-MpThreat -ErrorAction SilentlyContinue | Select ThreatName,SeverityID,IsActive   # empty = clean

# Network config + neighbors (one MAC for all = isolation)
Get-NetIPConfiguration | Select InterfaceAlias,IPv4Address,IPv4DefaultGateway
Get-NetNeighbor -AddressFamily IPv4 -State Reachable,Stale | ? {$_.IPAddress -notlike "224.*" -and $_.IPAddress -notlike "239.*"} | Select IPAddress,LinkLayerAddress,State

# Live outbound connections w/ process (spot rogue phone-home)
Get-NetTCPConnection -State Established | ? {$_.RemoteAddress -notlike "127.*" -and $_.RemoteAddress -ne "::1"} | % { $p=Get-Process -Id $_.OwningProcess -EA SilentlyContinue; [PSCustomObject]@{Remote="$($_.RemoteAddress):$($_.RemotePort)";Proc=$p.ProcessName;PID=$_.OwningProcess} } | Sort Proc | Format-Table -Auto

# Listening ports (flag 445/139 on public net), firewall, autoruns, non-MS scheduled tasks
Get-NetTCPConnection -State Listen | ? {$_.LocalAddress -notlike "127.*" -and $_.LocalAddress -ne "::1"} | % { $p=Get-Process -Id $_.OwningProcess -EA SilentlyContinue; [PSCustomObject]@{Local="$($_.LocalAddress):$($_.LocalPort)";Proc=$p.ProcessName} } | Sort Proc | Format-Table -Auto
Get-NetFirewallProfile | Select Name,Enabled,DefaultInboundAction
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -EA SilentlyContinue | Select * -Exclude PS*
Get-ItemProperty "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" -EA SilentlyContinue | Select * -Exclude PS*
Get-ScheduledTask | ? {$_.State -in "Ready","Running" -and $_.TaskPath -notlike "\Microsoft\*"} | Select TaskName,TaskPath,State | Format-Table -Auto
```

Optional full disk scan (long — run in background, notify on done):

```powershell
& "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -SignatureUpdate   # update sigs first
& "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -Scan -ScanType 2   # ScanType 2 = full ; run_in_background
```

Read verdict from output file: `hr=0` + `Get-MpThreat` empty = clean.

Inspect any unknown non-MS scheduled task before judging:

```powershell
Get-ScheduledTask -TaskPath "\NAME\*" | % { $_.TaskName; $_.Actions | Select Execute,Arguments }
```

Known bloat: **`\SoftLanding\*` = Lenovo promo/ad content-delivery engine** (empty Execute = COM handler, runs ~every 15 min). Not malware. Offer removal.

## PHASE 2 — HARDEN (opt-in; firewall + SMB1 need admin via .ps1)

Remove Lenovo SoftLanding bloat (per-user, usually no elevation):

```powershell
Get-ScheduledTask -TaskPath "\SoftLanding\*" | Unregister-ScheduledTask -Confirm:$false
```

Firewall + SMB1 — write a script, run elevated, log result (the reliable path):

```powershell
# 1) write harden.ps1
@'
Set-NetFirewallProfile -Profile Public -DefaultInboundAction Block
Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force
Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart
"Public inbound: " + (Get-NetFirewallProfile -Profile Public).DefaultInboundAction | Out-File C:\Users\<USER>\jarvis_harden_result.txt
'@ | Set-Content C:\Users\<USER>\harden.ps1 -Encoding utf8
```

User runs elevated (UAC):

```
Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File C:\Users\<USER>\harden.ps1'
```

Then Read `jarvis_harden_result.txt` to verify `Public inbound: Block`. Clean up both temp files after.

- SMB2/3 stay on → normal file sharing unaffected. SMB1 = WannaCry/EternalBlue vector. No speed impact, no reboot.
- `! ` prefix is a Claude Code PROMPT feature — never tell user to paste `!` into a real PowerShell window (it errors `Missing expression after unary operator`).

## PHASE 3 — CLEANUP + speed verdict (opt-in)

Measure first (show table), then clean safe targets only:

```powershell
function Sz($p){ try{$b=(Get-ChildItem $p -Recurse -Force -EA SilentlyContinue|Measure Length -Sum).Sum; if($b){[math]::Round($b/1MB,1)}else{0}}catch{0} }
# size: $env:TEMP, $env:WINDIR\Temp, Prefetch, SoftwareDistribution\Download, browser caches, thumbcache, CrashDumps, C:\$Recycle.Bin
```

Safe to delete: `$env:TEMP\*`, `$env:WINDIR\Temp\*`, `$env:LOCALAPPDATA\CrashDumps\*`, `thumbcache_*.db`, browser `Cache`. Locked/in-use files skip automatically with `-EA SilentlyContinue`.
Win Update cache (needs admin): `Stop-Service wuauserv,bits -Force; Remove-Item "$env:WINDIR\SoftwareDistribution\Download\*" -Recurse -Force; Start-Service wuauserv,bits`
Recycle Bin (**CONFIRM FIRST**): `Clear-RecycleBin -Force`
Storage Sense (auto-clean forever): set `HKCU:\...\StorageSense\Parameters\StoragePolicy` value `01` = 1.

Hardware verdict (the real speed story):

```powershell
"RAM GB: " + [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB,1)
Get-PhysicalDisk | Select FriendlyName,MediaType,@{n="SizeGB";e={[math]::Round($_.Size/1GB)}}
(Get-CimInstance Win32_Processor).Name
"Free C: GB: " + [math]::Round((Get-PSDrive C).Free/1GB,1)
powercfg /getactivescheme
```

High-perf power plan: `powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c`
If machine feels slow but specs are strong (SSD + ≥16GB + recent i7) → bottleneck is **software** (browser tabs, background apps), not hardware. Advise close-tabs + weekly reboot, not defrag.

## OUTPUT FORMAT

End with a scorecard table (Defender / threats / connections / ports / firewall / autoruns / tasks), a hardware verdict table, total GB reclaimed, and a one-line ship verdict. Flag anything UNVERIFIED — never claim a threat is gone without `hr=0` + empty `Get-MpThreat`.
