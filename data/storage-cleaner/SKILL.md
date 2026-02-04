---
name: storage-cleaner
description: Manage computer storage and clean up disk space. Use this skill when the user needs to find large files, detect duplicate files, remove unused applications, clear caches, or clean up Docker resources. Supports macOS, Windows, and Linux with platform-specific commands for storage analysis and cleanup operations.
---

# Storage Cleaner

## Overview

Comprehensive disk space management skill for finding and removing unnecessary files across macOS, Windows, and Linux. Helps identify large files, duplicates, unused applications, system caches, and Docker waste. All operations include safety confirmations before deletion.

## When to Use This Skill

Use this skill when:
- User needs to free up disk space
- User wants to find large files consuming storage
- User needs to identify and remove duplicate files
- User wants to clean system caches and temporary files
- User needs to remove unused applications
- User wants to clean up Docker resources (images, containers, volumes)
- User asks for storage analysis or disk cleanup

## Critical Safety Protocol

**ALWAYS follow this workflow:**

1. **Analyze First**: Run analysis commands to gather information about storage usage
2. **Report to User**: Present findings with sizes, paths, and potential space savings
3. **Wait for Confirmation**: Never execute deletion commands without explicit user approval
4. **Verify Before Delete**: Show exactly what will be deleted and ask for final confirmation
5. **Execute Safely**: Run approved operations with appropriate safeguards

**NEVER auto-execute deletion operations.** File deletion is irreversible and potentially critical.

## Prerequisites

**macOS:**
- Built-in: `find`, `du`, `md5`
- Optional: `brew install fdupes` (for duplicate detection)
- Docker Desktop (if using Docker cleanup)

**Windows:**
- Built-in: PowerShell 5.1+
- Optional: Windows Subsystem for Linux (WSL)
- Docker Desktop (if using Docker cleanup)

**Linux:**
- Built-in: `find`, `du`, `md5sum`
- Optional: `fdupes` (install via `apt install fdupes` or `yum install fdupes`)
- Docker (if using Docker cleanup)

## Core Operations

### 1. Large Files Detection

Find files larger than specified size threshold.

**macOS / Linux:**
```bash
# Find files larger than 1GB in home directory
find ~ -type f -size +1G -exec ls -lh {} \; 2>/dev/null | awk '{print $5, $9}'

# Find top 20 largest files
find ~ -type f -exec du -h {} \; 2>/dev/null | sort -rh | head -20

# Find large files in specific directory
find /path/to/dir -type f -size +500M -exec ls -lh {} \; 2>/dev/null
```

**Windows (PowerShell):**
```powershell
# Find files larger than 1GB
Get-ChildItem -Path $env:USERPROFILE -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object {$_.Length -gt 1GB} |
  Select-Object FullName, @{Name="Size(GB)";Expression={[math]::Round($_.Length/1GB, 2)}} |
  Sort-Object "Size(GB)" -Descending

# Find top 20 largest files
Get-ChildItem -Path $env:USERPROFILE -Recurse -File -ErrorAction SilentlyContinue |
  Sort-Object Length -Descending |
  Select-Object -First 20 FullName, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB, 2)}}
```

### 2. Duplicate Files Detection

Identify duplicate files by content hash.

**macOS:**
```bash
# Find duplicates in directory using md5
find /path/to/dir -type f -exec md5 -r {} \; | sort | uniq -d -w 32

# With fdupes (recommended)
fdupes -r /path/to/dir
```

**Linux:**
```bash
# Find duplicates using md5sum
find /path/to/dir -type f -exec md5sum {} \; | sort | uniq -d -w 32

# With fdupes
fdupes -r /path/to/dir
```

**Windows (PowerShell):**
```powershell
# Find duplicates by hash
Get-ChildItem -Path "C:\Path\To\Dir" -Recurse -File -ErrorAction SilentlyContinue |
  Get-FileHash -Algorithm MD5 |
  Group-Object -Property Hash |
  Where-Object {$_.Count -gt 1} |
  ForEach-Object {$_.Group | Select-Object Path, Hash}
```

### 3. Unused Applications

Find and manage unused applications.

**macOS:**
```bash
# List all applications with sizes
du -sh /Applications/*.app | sort -rh

# Find apps not used in last 180 days
find /Applications -name "*.app" -type d -atime +180 -exec ls -ld {} \;

# Check app last access time
mdls -name kMDItemLastUsedDate /Applications/YourApp.app
```

**Windows (PowerShell):**
```powershell
# List installed programs
Get-WmiObject -Class Win32_Product |
  Select-Object Name, InstallDate, Version |
  Sort-Object InstallDate -Descending

# List programs with install location
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* |
  Select-Object DisplayName, InstallLocation, InstallDate
```

**Linux:**
```bash
# Debian/Ubuntu - List installed packages by size
dpkg-query -W -f='${Installed-Size}\t${Package}\n' | sort -rn | head -20

# Red Hat/CentOS - List packages by size
rpm -qa --queryformat '%{SIZE} %{NAME}\n' | sort -rn | head -20
```

### 4. Cache Cleanup

Clear system and application caches.

**macOS:**
```bash
# User cache size
du -sh ~/Library/Caches

# System log size
du -sh /var/log

# Clear user caches (with confirmation)
# WARNING: May log out of some applications
rm -rf ~/Library/Caches/*

# Clear Homebrew cache
brew cleanup -s

# Clear npm cache
npm cache clean --force

# Clear pip cache
pip cache purge
```

**Windows (PowerShell - Run as Administrator):**
```powershell
# Show temp folder sizes
Get-ChildItem $env:TEMP | Measure-Object -Property Length -Sum
Get-ChildItem "C:\Windows\Temp" | Measure-Object -Property Length -Sum

# Clear temp folders
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue

# Clear Windows Update cache
Stop-Service wuauserv
Remove-Item -Path "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force
Start-Service wuauserv

# Run Disk Cleanup utility
cleanmgr /sagerun:1
```

**Linux:**
```bash
# Clear package manager cache
# Debian/Ubuntu
sudo apt-get clean
sudo apt-get autoclean

# Red Hat/CentOS
sudo yum clean all

# User cache size
du -sh ~/.cache

# Clear user cache
rm -rf ~/.cache/*

# Clear systemd journal logs (keep last 7 days)
sudo journalctl --vacuum-time=7d
```

### 5. Docker Cleanup

Remove unused Docker resources.

**All Platforms (requires Docker):**
```bash
# Show Docker disk usage
docker system df

# Remove unused containers, networks, images, and build cache
docker system prune -a

# Remove only stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes (WARNING: may delete data)
docker volume prune

# Remove everything (containers, images, volumes, networks)
docker system prune -a --volumes

# Show specific resource usage
docker ps -a --format "table {{.Names}}\t{{.Size}}"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

## Safety Guidelines

**Always confirm before deletion:**
- Show list of files/resources to be deleted
- Ask user for explicit confirmation
- Provide size estimates before cleanup
- Never use `sudo` without explicit user permission

**Preserve important data:**
- Do not delete files in `/System` (macOS) or `C:\Windows\System32` (Windows)
- Avoid deleting configuration files without confirmation
- Warn about Docker volume deletion (may contain databases)
- Skip active/locked files automatically

**Platform detection:**
```bash
# Detect OS in bash scripts
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS commands
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux commands
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows commands (Git Bash)
fi
```

## Example Workflows

**Storage analysis (Safe - Read-only):**
1. Detect OS
2. Find top 20 largest files
3. Show disk usage summary
4. Present findings to user
5. Suggest cleanup options
6. **Wait for user decision**

**Free up space (Requires Approval):**
1. **Analysis Phase**: Check cache sizes → Find large files (>1GB) → Check Docker usage
2. **Report Phase**: Present all findings with sizes and locations
3. **Approval Phase**: Ask user which items to remove
4. **Confirmation Phase**: Show exactly what will be deleted and final size
5. **Execution Phase**: Execute approved deletions only
6. **Verification Phase**: Report actual space freed

**Docker cleanup (Requires Approval):**
1. **Analysis**: Run `docker system df` to show current usage
2. **Report**: Show breakdown of containers, images, volumes with sizes
3. **Explain**: Clarify what will be removed and potential impacts
4. **Approval**: Get explicit user confirmation
5. **Execute**: Run `docker system prune` with approved options
6. **Report**: Show space saved

**Find duplicates (Requires Approval):**
1. **Analysis**: Detect OS → Check tool availability → Run duplicate detection
2. **Report**: Group duplicates by hash with file paths and sizes
3. **Review**: Present duplicate groups to user
4. **Approval**: Ask user which copies to keep/delete for EACH group
5. **Execute**: Delete only user-approved files
6. **Verify**: Confirm deletions and report space freed

## Best Practices

**Safety first (CRITICAL):**
- **Analysis before action**: Always run read-only analysis commands first
- **Report before delete**: Present complete findings to user before any deletion
- **Explicit approval required**: Never execute `rm`, `docker prune`, or cleanup commands without user confirmation
- **Double-check critical operations**: Verify paths and show file list before deletion
- **Preserve user data**: When in doubt, do NOT delete
- **Warn about irreversibility**: Clearly state that deletions cannot be undone

**Approval workflow:**
1. Show what will be deleted (file paths, sizes, count)
2. Ask: "Do you want to proceed with deleting these items? (yes/no)"
3. Wait for explicit "yes" response
4. Execute only if confirmed
5. Report results after execution

**Platform detection:** Automatically detect OS and use appropriate commands. Handle path differences (/ vs \). Account for permission models (sudo vs admin).

**Error handling:** Skip protected directories on permission denied. Offer installation for missing tools. Report partial success if operations fail.

**Output formatting:** Use human-readable sizes (GB/MB/KB). Sort by size (largest first). Provide clear next steps and space estimates.
