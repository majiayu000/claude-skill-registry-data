---
name: network-diagnostics
description: "Diagnose network connectivity issues: DNS, routing, firewall, port checks, traceroutes. Use for troubleshooting server-to-server communication or client access problems."
license: MIT
compatibility:
  - copilot-cli
  - vscode-copilot
  - claude
allowed-tools:
  - windows-command-line
  - console-automation
---

# Network Diagnostics Skill

## When to Activate
- User mentions: connectivity, DNS, ping, traceroute, port, firewall, routing, network unreachable
- User asks why a server can't reach another server
- User reports "connection refused" or "timeout" errors

## Diagnostic Workflow

### Step 1: Identify the Target
```powershell
# Extract hostname/IP and port from user's description
$target = "hostname-or-ip"
$port = 443  # or whatever port is relevant
```

### Step 2: Basic Connectivity
```powershell
# Quick ping test
Test-Connection -ComputerName $target -Count 4

# DNS resolution
Resolve-DnsName $target -Type A
Resolve-DnsName $target -Type AAAA
```

### Step 3: Port Accessibility
```powershell
# TCP port test
Test-NetConnection -ComputerName $target -Port $port -InformationLevel Detailed

# Multiple ports at once
@(22, 80, 443, 3389, 5985) | ForEach-Object {
    Test-NetConnection -ComputerName $target -Port $_ -WarningAction SilentlyContinue |
    Select-Object ComputerName, RemotePort, TcpTestSucceeded
}
```

### Step 4: Route Analysis
```powershell
# Trace the path
Test-NetConnection -ComputerName $target -TraceRoute

# Or classic tracert for more detail
tracert -d $target
```

### Step 5: Local Firewall Check
```powershell
# Check if Windows Firewall might block
Get-NetFirewallRule | Where-Object {
    $_.Enabled -eq 'True' -and $_.Direction -eq 'Outbound'
} | Select-Object DisplayName, Action -First 20
```

## Common Issues & Solutions

| Symptom | Likely Cause | Check |
|---------|--------------|-------|
| DNS timeout | DNS server unreachable | `nslookup $target 8.8.8.8` |
| Connection refused | Service not running | `Test-NetConnection -Port` |
| Request timeout | Firewall blocking | Check both local and remote FW |
| TTL exceeded | Routing loop | `tracert` to find the loop |
| No route to host | Missing route | `Get-NetRoute -DestinationPrefix 0.0.0.0/0` |

## Output Format
Always report:
1. What was tested
2. What succeeded ✅
3. What failed ❌
4. Recommended next step
