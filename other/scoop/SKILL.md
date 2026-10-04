---
name: scoop
description: "Manage Windows tools with Scoop manifests, buckets, and shims; troubleshoot package installation and download behavior."
category: windows
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["scoop", "powershell-package-manager", "scoop-buckets", "shims-path", "aria2-acceleration", "windows-cli", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Scoop Windows Package Manager AI Skill Guide (Claude)

## Overview & Engine Architecture
Scoop is a user-mode command-line package manager for Microsoft Windows built entirely on **PowerShell**. Engineered specifically for developers, Scoop installs applications into isolated user-space directories (**`$env:USERPROFILE\scoop\apps\`**), eliminating system file pollution, registry corruption, and UAC elevation requirements. The architecture relies on **Git-backed Bucket Repositories** containing declarative JSON manifests, an automated **Shim Generator (`$env:USERPROFILE\scoop\shims\`)** for instant `PATH` accessibility, a **`persist` directory** preserving user configuration across upgrades, and **Aria2 multi-connection download acceleration**. Claude operates as a Principal Windows Systems Automation Architect and DevOps Package Management Specialist, specializing in **declarative Scoop provisioning scripts**, **custom bucket manifest authoring**, **shim conflict resolution**, and **unattended workstation bootstrapping**.

### Scoop Package Management Architecture & Shims Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                 Scoop Architecture & Pipeline               │
│                                                             │
│  CLI Engine & Bucket Subsystem                              │
│  ├── PowerShell CLI Engine (`scoop.ps1` Execution Core)     │
│  ├── Git Buckets (`main`, `extras`, `versions`, `nerd-fonts`)│
│  └── JSON App Manifests (`version`, `url`, `bin`, `persist`)│
│                                                             │
│  Storage, Shims & Isolation Hierarchy                       │
│  ├── User-Space Apps: `~/scoop/apps/<app>/<version>/`       │
│  ├── Shims Engine: `~/scoop/shims/` (Batch / Shim Binaries) │
│  └── State Persistence: `~/scoop/persist/<app>/`            │
│                                                             │
│  Download & Acceleration Engine                             │
│  ├── Multi-Connection Accelerator (`aria2c.exe` Engine)     │
│  ├── SHA256 Integrity Verification & Checksum Engine        │
│  └── Global Config Store (`~/.config/scoop/config.json`)    │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Automated Workstation Provisioning**: Author idempotent PowerShell bootstrapping scripts that configure execution policies, initialize Scoop, subscribe to buckets (`extras`, `versions`, `sysinternals`), and install developer toolchains.
2. **Aria2 Download Acceleration Tuning**: Configure Aria2 integration (`scoop config aria2-enabled true`, `aria2-max-connection-per-server 16`) to drastically accelerate large SDK and runtime downloads.
3. **Custom Bucket JSON Manifest Authoring**: Write and validate Scoop application JSON manifests declaring portable URLs, 64-bit architecture binaries, shim aliases, and persistent data links.
4. **Shim Conflict & Version Switching Triage**: Resolve `PATH` precedence collisions and execute seamless version switching (`scoop reset python@3.11`).

---

## Production PowerShell Automation: Idempotent Developer Toolchain Bootstrapper

Save this script as `Bootstrap-ScoopEnvironment.ps1`:

```powershell
<#
.SYNOPSIS
    Idempotent Scoop Developer Environment Provisioning Script
    Configures execution policy, installs Scoop, enables Aria2 acceleration, and deploys toolchains.
#>

$ErrorActionPreference = "Stop"

Write-Host "--- [STARTING SCOOP DEVELOPER PROVISIONING] ---" -ForegroundColor Cyan

# 1. Ensure PowerShell Execution Policy Permits CurrentUser Scripts
$currentPolicy = Get-ExecutionPolicy -Scope CurrentUser
if ($currentPolicy -ne "RemoteSigned" -and $currentPolicy -ne "Unrestricted") {
    Write-Host "Configuring CurrentUser ExecutionPolicy to RemoteSigned..."
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
}

# 2. Install Scoop if Not Present
if (-not (Get-Command "scoop" -ErrorAction SilentlyContinue)) {
    Write-Host "Scoop not detected. Installing Scoop in user directory..."
    Invoke-RestMethod -Uri "https://get.scoop.sh" | Invoke-Expression
} else {
    Write-Host "✅ Scoop is already installed." -ForegroundColor Green
}

# 3. Add Core Developer Buckets
$bucketsToAdd = @("extras", "versions", "sysinternals", "nerd-fonts")
$installedBuckets = scoop bucket list | Select-Object -ExpandProperty Name

foreach ($bucket in $bucketsToAdd) {
    if ($installedBuckets -notcontains $bucket) {
        Write-Host "Adding Scoop bucket: $bucket..."
        scoop bucket add $bucket
    }
}

# 4. Install Aria2 and Configure Multi-Connection Download Acceleration
if (-not (Get-Command "aria2c" -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Aria2 download accelerator..."
    scoop install aria2
}
scoop config aria2-enabled true
scoop config aria2-max-connection-per-server 16
scoop config aria2-split 16
scoop config aria2-min-split-size 1M
Write-Host "✅ Aria2 acceleration enabled (16 connections/server)." -ForegroundColor Green

# 5. Deploy Standard Core Developer Package Suite
$packages = @(
    "git",
    "7zip",
    "neovim",
    "ripgrep",
    "fzf",
    "jq",
    "curl",
    "windows-terminal"
)

Write-Host "Installing Core Developer Tools..." -ForegroundColor Cyan
foreach ($pkg in $packages) {
    Write-Host "• Verifying: $pkg..."
    scoop install $pkg
}

# 6. Cleanup Download Cache and Old Versions
Write-Host "Purging download cache and outdated version shims..."
scoop cleanup *
scoop cache rm *

Write-Host "✅ Scoop provisioning complete! Your developer environment is ready." -ForegroundColor Green
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`File cannot be loaded because running scripts is disabled`** | Windows PowerShell restricted execution policy active. | Run in PowerShell: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force`. |
| **`Hash check failed for <package>`** | Upstream vendor released a new minor patch or download was corrupted in transit. | 1. Purge cache: `scoop cache rm <package>`.<br>2. Update bucket definitions: `scoop update`.<br>3. Bypass temporarily if verified safe: `scoop install -s <package>`. |
| **`Bucket clone failed / Git network timeout`** | Network firewall or ISP blocking GitHub HTTPS endpoint. | Configure Scoop proxy: `scoop config proxy 127.0.0.1:7890` or retry with `git config --global http.postBuffer 524288000`. |
| **Installed Binary Not Found in Command Prompt** | New `~/scoop/shims` directory not loaded into active shell `PATH`. | Restart terminal session or run: `$env:Path = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")`. |

---

## Command Line Syntax & Management Recipes

```powershell
# 1. Update Scoop Engine and All Bucket Manifests
scoop update

# 2. Upgrade All Installed Applications
scoop update *

# 3. Check for Outdated Packages and Health Issues
scoop status
scoop checkup

# 4. Switch Active Version of Multi-Version Tool
scoop reset nodejs-lts
```

### Essential File Locations
- **Installed Applications**: `%USERPROFILE%\scoop\apps\`
- **Executable Shims**: `%USERPROFILE%\scoop\shims\`
- **Buckets Repository**: `%USERPROFILE%\scoop\buckets\`
- **Configuration**: `%USERPROFILE%\.config\scoop\config.json`

---

## Agent Operational Directive
> **MANDATORY**: Always configure `aria2-enabled true` when provisioning Scoop on Windows to ensure resilient, multi-threaded parallel package downloads.
