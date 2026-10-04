---
name: rclone
description: "Plan and run Rclone cloud transfers, synchronization, encrypted remotes, and mounts while checking source and destination behavior."
category: cross-platform
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["rclone", "cloud-storage", "fuse-mount", "s3", "google-drive", "vfs-cache", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Rclone Cloud Storage Engine AI Skill Guide (Claude)

## Overview & Engine Architecture
Rclone ("rsync for cloud storage") is a high-performance Go-based command-line program to synchronize, copy, cryptographically encrypt, and mount files across 70+ cloud storage providers (AWS S3, Google Cloud Storage, Azure Blob, Google Drive, OneDrive, Backblaze B2, SFTP, WebDAV). Claude operates as a Senior Cloud Infrastructure Engineer and Data Migration Specialist, specializing in **high-throughput transfer tuning (`--transfers`, `--checkers`)**, **FUSE virtual filesystem mounting (`rclone mount` + VFS full cache)**, **client-side zero-knowledge encryption (`rclone crypt`)**, and **automated disaster recovery backup pipelines**.

### Rclone Core Architecture & VFS Mount Subsystem

```
┌─────────────────────────────────────────────────────────────┐
│                 Rclone Storage Architecture                 │
│                                                             │
│  Storage Abstraction Layer (70+ Cloud Backends)             │
│  ├── Object Storage (S3, GCS, B2, Azure Blob)               │
│  ├── Document Cloud (Google Drive, OneDrive, Dropbox)       │
│  └── Protocols & Local (SFTP, WebDAV, FTP, Local Disk)      │
│                                                             │
│  Virtual Filesystem & Crypto Engine                         │
│  ├── `rclone crypt` (Client-Side AES-256-GCM / Poly1305)   │
│  ├── FUSE Kernel Module & WinFsp (Windows File System Proxy)│
│  └── VFS Caching Engine (Sparse Read/Write Cache Layer)     │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **High-Throughput Sync Optimization**: Configure optimal transfer concurrency parameters (`--transfers=8 --checkers=16 --fast-list --buffer-size=64M`) tailored to network bandwidth and API request quotas.
2. **Production FUSE Mount Configuration**: Author robust `rclone mount` background services with `--vfs-cache-mode full` to enable compatibility with databases, media servers (Plex/Jellyfin), and non-sequential writes.
3. **Zero-Knowledge Encryption Setup**: Configure layered `crypt` remotes with obfuscated filenames and encrypted file headers before uploading sensitive backups to third-party clouds.
4. **Disaster Recovery & Bi-Directional Sync**: Implement `rclone bisync` and differential snapshots with strict dry-run verification (`--dry-run`) to prevent accidental data loss.

---

## Production Bash Automation: Automated S3/Drive Differential Backup Pipeline

Save this script as `cloud_backup.sh` to run reliable automated nightly cloud backups with bandwidth management and health alerting:

```bash
#!/usr/bin/env bash
# Automated High-Reliability Rclone Backup Pipeline
set -euo pipefail

SOURCE_DIR="/data/production_app"
REMOTE_DEST="s3_secure_backup:enterprise-backups/daily"
LOG_FILE="/var/log/rclone_backup.log"
BW_LIMIT="50M" # Limit upload to 50 MB/s to prevent saturation

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Differential Backup..." | tee -a "$LOG_FILE"

# Execute High-Throughput Sync with VFS checks
rclone sync "$SOURCE_DIR" "$REMOTE_DEST" \
    --config="$HOME/.config/rclone/rclone.conf" \
    --transfers=8 \
    --checkers=16 \
    --fast-list \
    --buffer-size=64M \
    --bwlimit="$BW_LIMIT" \
    --use-mtime \
    --stats=30s \
    --stats-one-line \
    --log-file="$LOG_FILE" \
    --log-level=INFO \
    --retries=5 \
    --low-level-retries=10 \
    --exclude=".git/**" \
    --exclude="node_modules/**" \
    --exclude="*.tmp"

EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup Completed Successfully!" | tee -a "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Backup Failed with Exit Code $EXIT_CODE" | tee -a "$LOG_FILE"
    exit $EXIT_CODE
fi
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Google Drive `403 User Rate Limit Exceeded`** | Rclone's default shared OAuth2 client ID reached Google API quota limits. | 1. Open Google Cloud Console $\rightarrow$ Enable Google Drive API.<br>2. Create custom OAuth2 Client ID and Client Secret.<br>3. In `rclone config`, edit remote and paste custom `client_id` and `client_secret`. |
| **FUSE Mount Fails: `Cannot open file for read/write`** | Mount started with default `--vfs-cache-mode off`, which disallows random-access in-place file modifications. | 1. Always specify `--vfs-cache-mode full` for general desktop/server mounting.<br>2. Configure cache size limit: `--vfs-cache-max-size 50G`.<br>3. On Windows, ensure **WinFsp** driver is installed. |
| **S3 Multipart Upload Fails: `RequestTimeout`** | Network jitter caused multipart chunk upload timeout on large files ($>5\text{GB}$). | 1. Increase S3 chunk size: `--s3-chunk-size 64M`.<br>2. Increase timeout: `--timeout 10m`.<br>3. Increase retry count: `--low-level-retries 20`. |
| **`rclone sync` Deleted Files Unexpectedly on Remote** | `sync` forces destination to match source identically (unlike `copy`, which only adds/updates). | 1. Always run with `--dry-run` first to preview deletions.<br>2. Use `rclone copy` if remote historical files must be retained.<br>3. Set `--backup-dir remote:trash` to move deleted files to a safety archive. |

---

## Command Line Syntax & Production Recipes

```bash
# 1. Mount Remote as Local Drive with Full VFS Cache (Linux/macOS FUSE & Windows WinFsp)
rclone mount remote_s3:mybucket /mnt/s3_drive --vfs-cache-mode full --vfs-cache-max-size 40G --allow-other --daemon

# 2. Check Cryptographic Hash Integrity of Cloud Files against Local Disk
rclone check /local/data encrypted_remote:secure_data --one-way

# 3. High-Speed Interactive Terminal Copy with Real-Time Transfer Stats
rclone copy /var/www/uploads b2_remote:media-archive --progress --transfers 12 --fast-list

# 4. Clean Up Partial Failed Multipart Uploads on AWS S3
rclone cleanup s3_remote:mybucket
```

### Essential File Locations
- **Master Configuration File**: `~/.config/rclone/rclone.conf` (Linux/macOS) or `%APPDATA%\rclone\rclone.conf` (Windows)
- **VFS Cache Directory**: `~/.cache/rclone/vfs/`
- **Windows WinFsp Driver**: `C:\Program Files (x86)\WinFsp\`

---

## Agent Operational Directive
> **MANDATORY**: When mounting remotes as local filesystem paths, always specify `--vfs-cache-mode full`. When using `rclone sync`, execute with `--dry-run` first or configure `--backup-dir` to prevent irreversible remote file deletion.
