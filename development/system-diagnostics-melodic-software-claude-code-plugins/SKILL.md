---
name: system-diagnostics
description: Comprehensive Windows 11 system diagnostics via PowerShell. Diagnoses crashes, freezes, reboots, BSOD, disk health, memory issues, hardware errors, and performance problems. Use when troubleshooting Windows stability issues, analyzing Event Viewer logs, checking disk/memory health, investigating hardware errors, or diagnosing system performance problems.
allowed-tools: Bash, Read, Glob, Grep
---

# Windows System Diagnostics

Comprehensive Windows 11 system diagnostics using PowerShell. This skill helps diagnose crashes, freezes, unexpected reboots, disk problems, memory issues, hardware errors, and performance bottlenecks.

## Table of Contents

- [Quick Start](#quick-start) - Immediate diagnostic commands
- [Platform Requirements](#platform-requirements) - Windows 11, PowerShell 7+
- [Diagnostic Categories](#diagnostic-categories) - What this skill covers
- [Quick Health Check](#quick-health-check) - Fast system overview
- [Reference Loading](#reference-loading-guide) - Progressive disclosure
- [Safety Model](#safety-model) - Read-only vs suggested repairs
- [Common Issues](#common-diagnostic-scenarios) - Troubleshooting patterns

## Overview

This skill provides read-only diagnostic capabilities to gather system health information. It does NOT execute repair commands - those are provided as suggestions for the user to run manually.

**Capabilities:**

- Event log analysis (crashes, errors, warnings)
- Disk health monitoring (SMART data, filesystem errors)
- Memory diagnostics (usage, leaks, hardware issues)
- Hardware error detection (device failures, drivers, WHEA)
- Performance analysis (CPU, memory, disk bottlenecks)
- System stability metrics (uptime, restart reasons)

## When to Use This Skill

Use this skill when:

- Computer is crashing, freezing, or rebooting unexpectedly
- Blue Screen of Death (BSOD) errors occur
- Disk health concerns (slow performance, errors)
- Memory issues suspected (high usage, crashes under load)
- Hardware errors or driver problems
- Need to analyze Windows Event Viewer logs
- System performance degradation
- Investigating application crashes

## Platform Requirements

**Required:**

- Windows 11 (this skill is optimized for Windows 11 Pro)
- PowerShell 7+ (`pwsh`) for best compatibility

**Verify PowerShell version:**

```powershell
$PSVersionTable.PSVersion
```

**Note:** Most commands also work with Windows PowerShell 5.1, but PowerShell 7+ is recommended for consistent behavior.

## Quick Start

### Immediate System Health Check

Run these commands to get a quick overview of system health:

```powershell
# System info and uptime
Get-Uptime
Get-ComputerInfo | Select-Object OsName, OsVersion, OsBuildNumber, CsProcessors, CsTotalPhysicalMemory

# Recent critical/error events (last 7 days)
Get-WinEvent -FilterHashtable @{LogName='System';Level=1,2;StartTime=(Get-Date).AddDays(-7)} -MaxEvents 20 |
    Select-Object TimeCreated, Id, ProviderName, Message | Format-Table -Wrap

# Disk health
Get-PhysicalDisk | Select-Object FriendlyName, MediaType, Size, HealthStatus, OperationalStatus

# Top memory consumers
Get-Process | Sort-Object WorkingSet64 -Descending |
    Select-Object -First 10 ProcessName, Id, @{N='MB';E={[math]::Round($_.WorkingSet64/1MB,0)}}

# Device errors
Get-PnpDevice -PresentOnly | Where-Object { $_.Status -in 'Error','Degraded','Unknown' } |
    Select-Object Class, FriendlyName, Status
```

## Diagnostic Categories

| Category | Description | Reference |
| --- | --- | --- |
| Event Logs | Windows Event Viewer analysis | [event-logs.md](references/event-logs.md) |
| Disk Health | SMART data, filesystem, storage | [disk-health.md](references/disk-health.md) |
| Memory | RAM usage, leaks, hardware | [memory-diagnostics.md](references/memory-diagnostics.md) |
| Stability | Uptime, restarts, BSOD | [system-stability.md](references/system-stability.md) |
| Hardware | Device errors, WHEA, drivers | [hardware-errors.md](references/hardware-errors.md) |
| Performance | CPU, memory, disk bottlenecks | [performance-analysis.md](references/performance-analysis.md) |
| Crashes | Minidumps, WER, BSOD analysis | [crash-analysis.md](references/crash-analysis.md) |
| Elevation | Admin requirements, graceful degradation | [admin-elevation.md](references/admin-elevation.md) |

## Quick Health Check

### System Information

```powershell
# Basic system info
Get-ComputerInfo | Select-Object `
    OsName, OsVersion, OsBuildNumber, `
    CsName, CsDomain, `
    CsProcessors, CsNumberOfLogicalProcessors, `
    @{N='RAM_GB';E={[math]::Round($_.CsTotalPhysicalMemory/1GB,1)}}

# System uptime
Get-Uptime
Get-Uptime -Since  # Last boot time
```

### Recent System Errors

```powershell
# Critical and Error events from System log (last 7 days)
Get-WinEvent -FilterHashtable @{
    LogName = 'System'
    Level = 1,2  # 1=Critical, 2=Error
    StartTime = (Get-Date).AddDays(-7)
} -MaxEvents 50 | Select-Object TimeCreated, Id, ProviderName, LevelDisplayName, Message
```

### Disk Quick Check

```powershell
# Physical disk health
Get-PhysicalDisk | Select-Object FriendlyName, MediaType, Size, HealthStatus, OperationalStatus

# SMART-like reliability data
Get-PhysicalDisk | ForEach-Object {
    $disk = $_
    $counters = $_ | Get-StorageReliabilityCounter
    [PSCustomObject]@{
        Disk = $disk.FriendlyName
        Health = $disk.HealthStatus
        Temperature = $counters.Temperature
        ReadErrors = $counters.ReadErrorsTotal
        WriteErrors = $counters.WriteErrorsTotal
        PowerOnHours = $counters.PowerOnHours
    }
}
```

### Memory Quick Check

```powershell
# System memory overview
Get-CimInstance Win32_OperatingSystem | Select-Object `
    @{N='Total_GB';E={[math]::Round($_.TotalVisibleMemorySize/1MB,2)}},
    @{N='Free_GB';E={[math]::Round($_.FreePhysicalMemory/1MB,2)}},
    @{N='Used_Pct';E={[math]::Round((1 - $_.FreePhysicalMemory/$_.TotalVisibleMemorySize)*100,1)}}

# Top 10 memory-consuming processes
Get-Process | Sort-Object WorkingSet64 -Descending |
    Select-Object -First 10 ProcessName, Id,
        @{N='WS_MB';E={[math]::Round($_.WorkingSet64/1MB,0)}},
        @{N='PM_MB';E={[math]::Round($_.PrivateMemorySize64/1MB,0)}}
```

### Hardware Quick Check

```powershell
# Devices with errors
Get-PnpDevice -PresentOnly | Where-Object { $_.Status -in 'Error','Degraded','Unknown' } |
    Select-Object Class, FriendlyName, InstanceId, Status

# WHEA hardware errors (last 30 days)
Get-WinEvent -FilterHashtable @{
    LogName = 'System'
    ProviderName = 'Microsoft-Windows-WHEA-Logger'
    StartTime = (Get-Date).AddDays(-30)
} -MaxEvents 20 -ErrorAction SilentlyContinue | Select-Object TimeCreated, Id, Message
```

## Reference Loading Guide

References are loaded on-demand based on the diagnostic category being investigated. This progressive disclosure keeps token usage efficient.

### Always Load (Core)

The main SKILL.md provides quick commands for initial triage (~4k tokens).

### Conditional Load

Load specific references based on what you're investigating:

| Trigger | Reference to Load |
| --- | --- |
| Event logs, errors, warnings | [event-logs.md](references/event-logs.md) |
| Disk, storage, SMART, chkdsk | [disk-health.md](references/disk-health.md) |
| Memory, RAM, paging, leaks | [memory-diagnostics.md](references/memory-diagnostics.md) |
| Uptime, restarts, reliability | [system-stability.md](references/system-stability.md) |
| Hardware, drivers, WHEA, devices | [hardware-errors.md](references/hardware-errors.md) |
| CPU, performance, bottlenecks | [performance-analysis.md](references/performance-analysis.md) |
| BSOD, minidump, crashes, WER | [crash-analysis.md](references/crash-analysis.md) |
| Admin, elevation, permissions | [admin-elevation.md](references/admin-elevation.md) |

### Token Estimates

- Quick health check: ~4k tokens (SKILL.md only)
- Single category deep dive: ~7k tokens (SKILL.md + 1 reference)
- Full diagnostic: ~25k tokens (SKILL.md + all references)

## Safety Model

This skill follows a **read-only diagnostics** model. All commands executed by the skill only gather information - they do not modify the system.

### Read-Only (Skill Can Execute)

These commands are safe to run:

| Category | Commands |
| --- | --- |
| Event Logs | `Get-WinEvent` |
| Disk Health | `Get-PhysicalDisk`, `Get-StorageReliabilityCounter`, `Get-Volume` |
| Memory | `Get-Process`, `Get-CimInstance Win32_OperatingSystem` |
| Devices | `Get-PnpDevice` |
| Performance | `Get-Counter` |
| System Info | `Get-Uptime`, `Get-ComputerInfo` |

### Suggested Only (User Runs Manually)

These repair/diagnostic commands modify the system or require reboot. The skill will provide instructions but NOT execute them:

| Command | Purpose | Notes |
| --- | --- | --- |
| `chkdsk /f /r` | Disk repair | Requires reboot for system drive |
| `sfc /scannow` | System file repair | Requires admin |
| `DISM /Online /Cleanup-Image /RestoreHealth` | System image repair | Requires admin, internet |
| `mdsched.exe` | Memory diagnostic | Requires reboot |
| `Repair-Volume -SpotFix` | Quick disk repair | Requires admin |
| Driver reinstall | Fix driver issues | Manual process |

### Elevation Notes

Some read-only operations require administrator privileges:

- `Get-WinEvent -LogName Security` (Security log)
- `Repair-Volume -Scan` (even read-only scan)
- Some WMI queries

The skill will note when elevation is needed and provide graceful degradation for non-admin scenarios.

## Common Diagnostic Scenarios

### Scenario: Computer Keeps Crashing/Rebooting

1. Check uptime and recent restart events
2. Look for Kernel-Power Event ID 41 (unexpected shutdown)
3. Check for BSOD minidumps
4. Review hardware errors (WHEA)
5. Check disk and memory health

**Key commands:**

```powershell
# Recent restart events
Get-WinEvent -FilterHashtable @{LogName='System';Id=41,1074,6008} -MaxEvents 20

# BSOD events
Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-WER-SystemErrorReporting'} -MaxEvents 10

# Check for minidumps
Get-ChildItem C:\Windows\Minidump -ErrorAction SilentlyContinue
```

### Scenario: Slow Performance

1. Check CPU/memory/disk utilization
2. Identify resource-hungry processes
3. Check for disk health issues
4. Look for hardware throttling

**Key commands:**

```powershell
# Current resource usage
Get-Counter -Counter '\Processor(_Total)\% Processor Time','\Memory\% Committed Bytes In Use','\PhysicalDisk(_Total)\% Disk Time'

# Top CPU consumers
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 ProcessName, CPU, @{N='MB';E={[math]::Round($_.WorkingSet64/1MB)}}
```

### Scenario: Disk Errors Suspected

1. Check physical disk health status
2. Review SMART reliability counters
3. Look for disk-related events
4. Check filesystem dirty bit

**Key commands:**

```powershell
# Disk health
Get-PhysicalDisk | Select-Object FriendlyName, HealthStatus, OperationalStatus

# Reliability counters
Get-PhysicalDisk | Get-StorageReliabilityCounter | Select-Object DeviceId, Temperature, ReadErrorsTotal, WriteErrorsTotal

# Recent disk events
Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='disk','ntfs'} -MaxEvents 20
```

### Scenario: Memory Issues

1. Check current memory usage
2. Identify memory-hungry processes
3. Look for memory-related events
4. Check for previous memory diagnostic results

**Key commands:**

```powershell
# Memory usage
Get-CimInstance Win32_OperatingSystem | Select-Object @{N='Used%';E={[math]::Round((1-$_.FreePhysicalMemory/$_.TotalVisibleMemorySize)*100,1)}}

# Top memory processes
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 ProcessName, @{N='MB';E={[math]::Round($_.WorkingSet64/1MB)}}

# Memory diagnostic results
Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-MemoryDiagnostics-Results'} -ErrorAction SilentlyContinue
```

## Anti-Patterns

**Do NOT:**

- Execute repair commands (chkdsk /f, sfc /scannow, etc.) - only suggest them
- Run commands that require reboot (mdsched.exe) without explicit user consent
- Assume admin privileges are available
- Ignore elevation errors - report them and suggest running as admin
- Make hardware recommendations without diagnostic evidence

**Do:**

- Start with quick health checks before deep dives
- Load references progressively based on investigation needs
- Report findings with severity (Critical, Warning, Info)
- Provide actionable next steps for the user
- Explain what each suggested repair command does

## Version History

- v1.0.0 (2025-12-03): Initial release with Windows 11 diagnostics

## Last Updated

**Date:** 2025-12-03
**Model:** claude-opus-4-5-20251101
