---
name: remote-management
description: "Manage remote Windows servers via WinRM, PowerShell remoting, and SSH. Use when user needs to execute commands on remote hosts or establish remote sessions."
license: MIT
compatibility:
  - copilot-cli
  - vscode-copilot
  - claude
allowed-tools:
  - windows-command-line
  - console-automation
---

# Remote Server Management Skill

## When to Activate
- User mentions: remote, WinRM, PSRemoting, Enter-PSSession, Invoke-Command, SSH
- User wants to run commands on another server
- User needs to manage multiple servers at once

## Prerequisites

### Enable WinRM on Target
```powershell
# On target server (run as admin)
Enable-PSRemoting -Force
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "*" -Force  # Or specific hosts
```

### Verify Connectivity
```powershell
Test-WSMan -ComputerName $remoteHost
Test-NetConnection -ComputerName $remoteHost -Port 5985  # HTTP
Test-NetConnection -ComputerName $remoteHost -Port 5986  # HTTPS
```

## Remote Execution Patterns

### Single Command to Single Host
```powershell
Invoke-Command -ComputerName $remoteHost -ScriptBlock {
    Get-Process | Sort-Object CPU -Descending | Select-Object -First 5
}
```

### Single Command to Multiple Hosts
```powershell
$servers = @('Server01', 'Server02', 'Server03')
Invoke-Command -ComputerName $servers -ScriptBlock {
    [PSCustomObject]@{
        Host = $env:COMPUTERNAME
        Uptime = (Get-Date) - (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
        FreeMemGB = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 2)
    }
} | Select-Object Host, Uptime, FreeMemGB
```

### Interactive Session
```powershell
# Enter interactive session
Enter-PSSession -ComputerName $remoteHost

# Exit when done
Exit-PSSession
```

### With Credentials
```powershell
$cred = Get-Credential
Invoke-Command -ComputerName $remoteHost -Credential $cred -ScriptBlock { whoami }

# Or use stored credential
$cred = New-Object PSCredential("DOMAIN\User", (ConvertTo-SecureString "password" -AsPlainText -Force))
```

### Pass Variables to Remote
```powershell
$serviceName = "Spooler"
Invoke-Command -ComputerName $remoteHost -ScriptBlock {
    param($svc)
    Get-Service -Name $svc
} -ArgumentList $serviceName

# Or using $using: scope (PS 3.0+)
Invoke-Command -ComputerName $remoteHost -ScriptBlock {
    Get-Service -Name $using:serviceName
}
```

### Copy Files to Remote
```powershell
# Using PS remoting session
$session = New-PSSession -ComputerName $remoteHost
Copy-Item -Path "C:\local\file.txt" -Destination "C:\remote\" -ToSession $session
Remove-PSSession $session
```

## SSH Alternative (OpenSSH)

### Connect via SSH
```powershell
ssh user@$remoteHost

# Run single command
ssh user@$remoteHost "Get-Process | Select -First 5"
```

### PowerShell over SSH
```powershell
# Requires OpenSSH and PowerShell subsystem configured
Enter-PSSession -HostName $remoteHost -UserName $username -SSHTransport
```

## Parallel Execution (PS 7+)

```powershell
$servers = @('Server01', 'Server02', 'Server03', 'Server04', 'Server05')

$servers | ForEach-Object -Parallel {
    Invoke-Command -ComputerName $_ -ScriptBlock {
        [PSCustomObject]@{
            Server = $env:COMPUTERNAME
            CPU = (Get-CimInstance Win32_Processor).LoadPercentage
        }
    }
} -ThrottleLimit 5
```

## Troubleshooting WinRM

| Error | Solution |
|-------|----------|
| "WinRM cannot complete the operation" | Enable WinRM: `Enable-PSRemoting -Force` |
| "Access denied" | Check credentials, group membership |
| "The WinRM client cannot process the request" | Add to TrustedHosts or use HTTPS |
| Connection timeout | Check firewall (5985/5986), network path |

```powershell
# Diagnose WinRM issues
winrm quickconfig
winrm get winrm/config/client
```
