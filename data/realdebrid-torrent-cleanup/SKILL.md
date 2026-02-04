---
name: realdebrid-torrent-cleanup
description: Identifies and removes dead, unavailable, or error torrents from Real-Debrid account using the API. Shows torrent status, filters by health, and safely deletes torrents with missing files. Use this when Jellyfin scans are slow, when troubleshooting 404 errors, to clean account storage, or before major library refreshes.
allowed-tools:
  - bash
  - grep
  - read
---

# Real-Debrid Torrent Cleanup

Automatically detect and remove dead torrents from your Real-Debrid account.

## What This Does

1. **Lists all torrents** with status breakdown
2. **Identifies dead torrents**: magnet_error, dead, virus, 404
3. **Shows statistics**: Total size, reclaimable space
4. **Safe deletion**: Whitelist support, dry-run mode, confirmation required
5. **Post-cleanup**: Displays before/after comparison

## When To Use This

- Jellyfin scans taking >10 minutes (dead files slow scanning)
- Zurg logs showing "404 file not found" errors
- Account storage approaching limit (cleanup frees 50-200GB typically)
- After bulk torrent adding (some may fail to download)
- Monthly maintenance to keep account healthy

## Quick Start

### 1. Install Script on Server

```bash
ssh automation@srv759970.hstgr.cloud
cd /home/automation/scripts

# Download script (from repo or copy manually)
wget https://raw.githubusercontent.com/YOUR_REPO/main/.claude/skills/realdebrid-cleanup/scripts/cleanup_realdebrid.py

# Or copy from local repo
cat > cleanup_realdebrid.py << 'EOF'
[paste script from scripts/cleanup_realdebrid.py]
EOF

chmod +x cleanup_realdebrid.py
```

### 2. Dry-Run (See What Would Be Deleted)

```bash
python3 /home/automation/scripts/cleanup_realdebrid.py --dry-run
```

**Expected output**:
```
📊 Fetching Real-Debrid torrents...
Total torrents: 537
Total size: 2.30 TB

--- Status Breakdown ---
🟢 downloaded: 480
🔴 magnet_error: 23
🔴 dead: 18
🔴 virus: 4
🟡 downloading: 12

🔴 Found 45 dead torrents
Reclaimable: 156 GB

--- Dead Torrents ---
1. [MAGNET_ERROR] Movie.XYZ.2024.mkv
2. [DEAD] Old.Show.S01.Complete
...

🔍 DRY-RUN MODE - No torrents will be deleted
```

### 3. Execute Cleanup

```bash
python3 /home/automation/scripts/cleanup_realdebrid.py
# Type 'DELETE' when prompted
```

### 4. Post-Cleanup Workflow

After cleanup, refresh the media stack:

```bash
# See media-stack-refresh skill for complete workflow
docker restart zurg rclone
sleep 15
curl -X POST 'http://localhost:8096/Library/Refresh' \
  -H 'X-Emby-Token: 9af5f56a66e44ee68ddeec7bd07c9db8'
```

## Safety Features

### Automatic Protections
- ✅ Never deletes active torrents (downloading, uploading, queued)
- ✅ Whitelist support (preserve specific content)
- ✅ Dry-run mode available
- ✅ Confirmation required ("Type DELETE")
- ✅ Respects API rate limits (0.5s between requests)

### Whitelist Configuration

Edit script to protect specific torrents:

```python
# In cleanup_realdebrid.py
WHITELIST = [
    "Naruto",            # By filename (partial match)
    "Breaking Bad",
    "4QMHWXG66PW64"     # By torrent ID (exact match)
]
```

## Torrent Status Reference

| Status | Meaning | Action |
|--------|---------|--------|
| `downloaded` | Fully available | ✅ Keep |
| `downloading` | In progress | ✅ Keep |
| `queued` | Waiting to start | ✅ Keep |
| `magnet_error` | Failed to resolve | 🔴 Delete |
| `dead` | Files unavailable | 🔴 Delete |
| `virus` | Flagged by RD | 🔴 Delete |
| `error` | Generic error | 🔴 Delete |
| `timeout` | Download timeout | 🔴 Delete |

## Typical Results

| Scenario | Torrents Deleted | Space Freed | Time Saved |
|----------|------------------|-------------|------------|
| First cleanup | 30-50% | 100-200 GB | Scans 5-10x faster |
| Monthly | 5-10% | 20-50 GB | Minor improvement |
| After bulk add | 10-20% | 50-100 GB | Moderate improvement |

## Integration with Other Skills

```
Before cleanup:
  ├─ server-diagnostics (check disk space)
  └─ backup-status (ensure configs backed up)

Run cleanup:
  └─ realdebrid-torrent-cleanup ← YOU ARE HERE

After cleanup:
  ├─ media-stack-refresh (restart Zurg/Rclone)
  └─ jellyfin-scan (monitor library update)
```

## API Configuration

### API Key Location
- Stored in: `SECRETS.md` (not committed to Git)
- Environment variable: `RD_API_KEY` (optional)

### Rate Limits
- **500 requests/hour** per IP
- Script adds **0.5s delay** between requests
- Safe for accounts with 1000+ torrents

## Troubleshooting

### Issue: Script returns 401 Unauthorized
**Cause**: Invalid or expired API key

**Solution**:
```bash
# Update API key in script or set environment variable
export RD_API_KEY="your_new_key_here"
python3 cleanup_realdebrid.py
```

### Issue: Can't delete torrent (403 Forbidden)
**Cause**: Torrent is active or locked

**Solution**: Wait for torrent to finish or cancel it manually in Real-Debrid web UI

### Issue: Deleted torrents reappear
**Cause**: Sonarr/Radarr re-added the torrent

**Solution**: Remove from *arr apps first, then cleanup

## For More Details

See [reference.md](./reference.md) for:
- Complete API endpoint documentation
- Advanced configuration options
- Detailed troubleshooting guide
- Automation setup (cron job)

See [scripts/cleanup_realdebrid.py](./scripts/cleanup_realdebrid.py) for:
- Complete Python source code
- Customization options
- Function documentation
