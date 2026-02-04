---
name: media-stack-full-refresh
description: Complete workflow to refresh the entire media stack after changes - cleanup Real-Debrid, restart Zurg/Rclone mounts, clear caches, verify mount health, and trigger Jellyfin library scan. Use this after deleting torrents, when mount shows stale data, after configuration changes, or when content doesn't sync between RD and Jellyfin.
allowed-tools:
  - bash
  - read
  - grep
---

# Media Stack Full Refresh

Complete end-to-end refresh workflow for the entire media infrastructure.

## What This Does

Orchestrates the full refresh chain:
1. **Restart Zurg** - Rebuild torrent database from Real-Debrid
2. **Restart Rclone** - Clear mount cache
3. **Verify mount** - Ensure files accessible
4. **(Optional) Restart Jellyfin** - Clear metadata cache
5. **Trigger scan** - Index new content
6. **Verify results** - Confirm content detected

## When To Use This

### Primary Use Cases
- **After RD cleanup**: Deleted torrents still show in mount
- **Content not syncing**: Added torrents don't appear in Jellyfin
- **Stale mount data**: Files deleted but directories persist
- **Configuration changes**: Modified Zurg config.yml
- **Cache corruption**: Rclone showing incorrect file sizes

### Symptoms That Need This
```
❌ Deleted 9-1-1 from RD but 42 folders still in /mnt/rd/shows/
❌ Added Naruto to RD but doesn't appear in Jellyfin
❌ Zurg logs show "404" for files that should exist
❌ Rclone mount frozen or stale
❌ Jellyfin shows "0 items" after adding content
```

## Quick Start

### Option 1: Automated Script (Recommended)

```bash
ssh automation@srv759970.hstgr.cloud

# Download script
cd /home/automation/scripts
wget https://raw.githubusercontent.com/YOUR_REPO/main/.claude/skills/media-stack-refresh/scripts/full_refresh.sh
chmod +x full_refresh.sh

# Run full refresh
./full_refresh.sh

# Or skip Jellyfin restart (faster, doesn't interrupt streams)
./full_refresh.sh --skip-jellyfin
```

**Duration**: 3-5 minutes (5-30 minutes with scan)

### Option 2: Manual Step-by-Step

```bash
ssh automation@srv759970.hstgr.cloud

# 1. Restart Zurg
docker restart zurg && sleep 10

# 2. Restart Rclone
docker restart rclone && sleep 15

# 3. Verify mount
ls /mnt/rd/shows/ | wc -l

# 4. (Optional) Restart Jellyfin
docker restart jellyfin && sleep 30

# 5. Trigger scan
curl -X POST 'http://localhost:8096/Library/Refresh' \
  -H 'X-Emby-Token: 9af5f56a66e44ee68ddeec7bd07c9db8'

# 6. Wait and verify (2-30 min depending on library size)
```

## Expected Output

### Automated Script Output
```
[INFO] Step 1/7: Restarting Zurg...
[INFO] ✓ Zurg is healthy
[INFO]   Compiled 489 torrents

[INFO] Step 2/7: Restarting Rclone...
[INFO] ✓ Rclone is running

[INFO] Step 3/7: Verifying mount health...
[INFO] ✓ Mount accessible (282 shows found)

[INFO] Step 4/7: Restarting Jellyfin...
[WARN]   This will interrupt active streams!
[INFO] ✓ Jellyfin is healthy

[INFO] Step 5/7: Triggering Jellyfin library scan...
[INFO] ✓ Library scan triggered

[INFO] Step 6/7: Waiting for scan to complete...
[WARN]   This may take 2-30 minutes depending on library size

[INFO] Step 7/7: Verifying results...
[INFO] ✓ Library statistics retrieved
[INFO]   Series: 245
[INFO]   Episodes: 8,432
[INFO]   Movies: 1,234

=========================================
  MEDIA STACK REFRESH COMPLETED
=========================================
```

## Verification Steps

### 1. Verify Zurg Updated

```bash
# Check Zurg compiled new torrent count
docker logs zurg 2>&1 | grep "Compiled" | tail -1
```

**Expected**: New torrent count matching Real-Debrid

### 2. Verify Mount Reflects Changes

```bash
# If you deleted 9-1-1, this should return 0
ls /mnt/rd/shows/ | grep -i "9-1-1" | wc -l

# If you added Naruto, this should find it
ls /mnt/rd/shows/ | grep -i "naruto"
```

### 3. Verify Jellyfin Updated

```bash
# Check library stats
curl -s 'http://localhost:8096/Items/Counts' \
  -H 'X-Emby-Token: 9af5f56a66e44ee68ddeec7bd07c9db8' | \
  grep -oP '"SeriesCount":\K\d+'

# Search for specific content
curl -s 'http://localhost:8096/Items?SearchTerm=Naruto&Recursive=true' \
  -H 'X-Emby-Token: 9af5f56a66e44ee68ddeec7bd07c9db8' | \
  grep -oP '"Name":.*?Naruto'
```

## Cache Behavior Explained

### Why Deleted Torrents Still Show

**The cache chain**:
```
Real-Debrid API
    ↓ (cached 5min)
Zurg Database
    ↓ (cached until restart)
Rclone VFS Cache
    ↓ (cached 1h default)
Filesystem Mount
    ↓ (cached 30s kernel)
Jellyfin Library
    ↓ (cached until scan)
```

**Each layer must be refreshed** - that's why simple `docker restart` often isn't enough!

## Integration with Other Skills

### Typical Workflow

```
Step 1: realdebrid-cleanup
  └─ Delete dead torrents from Real-Debrid

Step 2: media-stack-refresh ← YOU ARE HERE
  ├─ Restart Zurg (rebuild database)
  ├─ Restart Rclone (clear cache)
  └─ Trigger Jellyfin scan

Step 3: jellyfin-scan
  └─ Monitor scan progress

Step 4: health-check
  └─ Verify all services healthy
```

## Performance Optimization

### For Large Libraries (500+ items)

**1. Skip Jellyfin restart** (faster, doesn't interrupt streams):
```bash
./full_refresh.sh --skip-jellyfin
```

**2. Scan specific library only**:
```bash
# Get library ID
curl -s 'http://localhost:8096/Library/VirtualFolders' \
  -H 'X-Emby-Token: YOUR_TOKEN' | jq '.[] | {Name, ItemId}'

# Scan just TV library
curl -X POST 'http://localhost:8096/Items/{LibraryId}/Refresh?Recursive=true' \
  -H 'X-Emby-Token: YOUR_TOKEN'
```

**3. Increase Rclone cache** (fewer API calls):
```yaml
# In docker-compose.yml for rclone
command:
  - --vfs-cache-max-size=20G  # Increase from 10G
```

## Typical Timings

| Step | Duration | Can Skip? |
|------|----------|-----------|
| Restart Zurg | 10-15s | No |
| Restart Rclone | 15-20s | No |
| Verify Mount | 5s | No (critical) |
| Restart Jellyfin | 30-45s | Yes |
| Trigger Scan | 1s | No |
| Wait for Scan | 2-30min | No (async) |
| Verify Results | 30s | No (critical) |

**Total minimum**: ~2 minutes (no Jellyfin restart, small library)
**Total typical**: ~10 minutes (with restart, medium library)
**Total maximum**: ~35 minutes (full refresh, large library)

## Troubleshooting Quick Reference

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Mount not accessible | Rclone crashed | `docker restart rclone` |
| Zurg not healthy | Config error | Check `docker logs zurg` |
| Deleted content still shows | Cache not cleared | Force: `docker exec rclone rclone rc vfs/forget` |
| Jellyfin scan finds nothing | Mount not accessible | `docker exec jellyfin ls /media/shows/` |
| Scan takes >30min | Too many files | Scan specific library only |

## Automation Setup

### Scheduled Refresh (Daily at 4am)

```bash
# Add to automation crontab
crontab -e

# Daily refresh (skip Jellyfin to avoid interrupting streams)
0 4 * * * /home/automation/scripts/full_refresh.sh --skip-jellyfin >> /home/automation/logs/media-refresh.log 2>&1
```

### Post-Cleanup Hook

Auto-refresh after Real-Debrid cleanup:
```bash
#!/bin/bash
# /home/automation/scripts/cleanup_and_refresh.sh

# Run RD cleanup
python3 /home/automation/scripts/cleanup_realdebrid.py "$@"

# If cleanup succeeded, refresh stack
if [ $? -eq 0 ]; then
    echo "Cleanup completed, refreshing media stack..."
    /home/automation/scripts/full_refresh.sh --skip-jellyfin
fi
```

## For More Details

See [reference.md](./reference.md) for:
- Detailed troubleshooting guide for each step
- Advanced configuration options
- Cache clearing techniques
- Service recovery procedures

See [scripts/full_refresh.sh](./scripts/full_refresh.sh) for:
- Complete bash source code
- Customization options
- Error handling details
