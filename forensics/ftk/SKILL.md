---
name: ftk
description: "Automate authorized FTK evidence workflows with FTK Imager, distributed processing, and known-file hash filtering."
category: digital-forensics
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["ftk", "ftk-imager", "forensic-toolkit", "dpe", "kff-filter", "digital-forensics", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Exterro FTK (Forensic Toolkit) AI Skill Guide (Claude)

## Overview & Engine Architecture
Exterro FTK (Forensic Toolkit) is an enterprise-grade digital forensics platform known for its **Distributed Processing Engine (DPE)**, centralized PostgreSQL database backend, and **FTK Imager** forensic acquisition suite. FTK processes multi-terabyte evidence sets simultaneously across worker clusters, integrating the **Known File Filter (KFF)**, Cerberus malware triage, and automated OCR. Claude operates as a Senior Forensic Systems Engineer and DFIR Architect, specializing in **FTK Imager CLI automation**, **DPE cluster troubleshooting**, **volatile memory acquisition (RAM)**, and **case database optimization**.

### FTK Distributed Processing & Database Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 FTK Enterprise Architecture                 │
│                                                             │
│  Central Core & Database Layer                              │
│  ├── PostgreSQL Database Cluster (Case Meta & Artifact DB)  │
│  ├── KFF (Known File Filter - NSRL Hash Set Library)        │
│  └── Cerberus Malware Analysis & Scoring Engine             │
│                                                             │
│  Distributed Processing & Acquisition Layer                 │
│  ├── Distributed Processing Engine (DPE Worker Nodes - 5000)│
│  ├── FTK Imager CLI (`ftkimager.exe` E01/RAW Bitstream Acq)│
│  └── Optical Character Recognition (OCR Engine Subsystem)   │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **FTK Imager CLI Automation**: Script automated forensic acquisitions of physical disks (`\\.\PhysicalDrive0`) and volatile physical memory into E01 containers with embedded cryptographic verification (MD5/SHA-1).
2. **Distributed Processing Engine (DPE) Optimization**: Configure and troubleshoot DPE worker node communication over TCP port 5000, adjusting thread worker allocations and PostgreSQL connection pools.
3. **KFF & Hash Library Management**: Maintain Known File Filter (KFF) hash libraries, importing NIST NSRL databases to automatically eliminate benign operating system binaries from investigator review.
4. **Live RAM & Volatile Triage**: Safely acquire live RAM dumps from Windows workstations, diagnosing kernel driver blocking caused by Windows Virtualization-Based Security (VBS/HVCI).

---

## Production PowerShell Automation: Automated FTK Imager Live Acquisition

Save this script as `Run-FTKAcquisition.ps1` to automate physical drive imaging and volatile RAM acquisition via FTK Imager CLI:

```powershell
<#
.SYNOPSIS
    Automated Forensic Live Acquisition using FTK Imager CLI (ftkimager.exe)
.DESCRIPTION
    Dumps volatile physical RAM and acquires PhysicalDrive0 into E01 container with verification.
#>
param (
    [Parameter(Mandatory=$true)]
    [string]$CaseName,

    [Parameter(Mandatory=$true)]
    [string]$DestinationDir
)

$FTK_CLI = "C:\Program Files\AccessData\FTK Imager\ftkimager.exe"

if (-not (Test-Path $FTK_CLI)) {
    Write-Error "FTK Imager CLI not found at '$FTK_CLI'."
    exit 1
}

New-Item -ItemType Directory -Force -Path $DestinationDir | Out-Null
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

# 1. Acquire Volatile Physical Memory (RAM)
$RamOut = Join-Path $DestinationDir "${CaseName}_${Timestamp}_RAM.raw"
Write-Host "[1/2] Acquiring Physical Memory (RAM) to: $RamOut..." -ForegroundColor Cyan
& $FTK_CLI --print-physical-memory $RamOut

# 2. Acquire Physical Drive 0 to E01 Container
$DiskOut = Join-Path $DestinationDir "${CaseName}_${Timestamp}_Disk"
Write-Host "[2/2] Acquiring PhysicalDrive0 to E01 format: $DiskOut.E01..." -ForegroundColor Cyan
& $FTK_CLI "\\.\PhysicalDrive0" $DiskOut `
    --e01 `
    --compress 6 `
    --frag 2048M `
    --case-number "$CaseName" `
    --evidence-number "001" `
    --examiner "DFIR Lead" `
    --description "Automated Live Triage Disk Image" `
    --verify

if ($LASTEXITCODE -eq 0) {
    Write-Host "Forensic acquisition completed and cryptographically verified!" -ForegroundColor Green
} else {
    Write-Error "Acquisition failed with exit code $LASTEXITCODE"
}
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **DPE Worker Node Disconnects / Fails Registration** | Windows Firewall blocked TCP port 5000 or the worker service lost PostgreSQL database credentials. | 1. In `services.msc`, verify **AccessData Distributed Processing Engine** service is Running.<br>2. Open inbound TCP port **5000** and **5432** on FTK server and workers.<br>3. Check `DPE.log` in `%PROGRAMDATA%\AccessData\Logs\`. |
| **RAM Acquisition Produces Blank or Incomplete File** | Windows 11 Virtualization-Based Security (VBS) or Hypervisor-Protected Code Integrity (HVCI) blocked raw `\\Device\PhysicalMemory`. | 1. Check if HVCI is active in Windows Security $\rightarrow$ *Core Isolation*.<br>2. Use kernel-level acquisition tools (e.g. WinPmem / DumpIt driver) or suspend virtualization security during live triage.<br>3. Execute `ftkimager.exe` strictly as elevated Administrator. |
| **PostgreSQL Database Case Deadlock on Large Ingest** | Default PostgreSQL `shared_buffers` and `max_connections` parameters too low for high-core DPE clusters. | 1. In `postgresql.conf`, increase `shared_buffers = 8GB` (or 25% of RAM) and `work_mem = 64MB`.<br>2. Increase `max_connections = 300`.<br>3. Restart PostgreSQL service. |
| **OCR Processing Freezes Ingestion Pipeline** | Corrupted multi-thousand-page scanned PDF file locking OCR worker process. | 1. In Processing Profile, set OCR file size limit to $\le 50\text{MB}$.<br>2. Exclude non-document binary formats from OCR queue.<br>3. Set OCR timeout to 60 seconds per item. |

---

## Command Line Syntax & Operational Recipes

```bash
# 1. Acquire Logical Directory to AD1 Custom Content Container
ftkimager.exe "C:\Users\TargetUser\AppData" "C:\Evidence\User_AppData" --ad1 --verify

# 2. Extract Registry Hives from Live Windows System
ftkimager.exe --extract-protected-files C:\Windows\System32\config\SYSTEM C:\Evidence\SYSTEM

# 3. Mount E01 Image as Virtual Drive via FTK Imager CLI
ftkimager.exe --mount "C:\Evidence\Disk.E01" /drive=Z: /mode=read-only
```

### Essential File Locations
- **FTK Configuration**: `C:\Program Files\Exterro\FTK\FTK.cfg`
- **DPE Worker Logs**: `%PROGRAMDATA%\AccessData\Logs\DPE`
- **PostgreSQL Data Directory**: `C:\Program Files\PostgreSQL\<VER>\data`

---

## Agent Operational Directive
> **MANDATORY**: When executing FTK Imager CLI acquisitions, always include the `--verify` flag to compute and log acquisition vs verification checksums (MD5/SHA-1). Tune PostgreSQL `shared_buffers` before running high-throughput DPE ingest clusters.
