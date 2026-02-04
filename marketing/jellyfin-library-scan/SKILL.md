---
name: jellyfin-library-scan
description: Triggers and monitors Jellyfin library scans, shows scan progress, displays newly added content, and verifies library statistics. Use this after adding new media, when content doesn't appear in Jellyfin, or when investigating indexing issues.
allowed-tools:
  - bash
  - read
---

# Jellyfin Library Scan

Force library scan and monitor indexing progress.

## What This Does

1. **Triggers library scan**: Forces immediate refresh of all libraries
2. **Monitors progress**: Shows scan status in real-time
3. **Displays new content**: Lists recently added movies/shows
4. **Shows statistics**: Total items per library
5. **Verifies indexing**: Confirms specific content detected

## When To Use This

- **New content added** but doesn't appear in Jellyfin
- **After Zurg configuration** changes
- **After mount point** changes or restart
- **Library showing "0 items"** incorrectly
- **Testing content detection**
- **After media-stack-refresh** workflow
- **Investigating missing media**

## Quick Start

### Option 1: Automated Monitoring (Recommended)

```bash
ssh automation@srv759970.hstgr.cloud

# Install monitor script
cd /home/automation/scripts
wget https://raw.githubusercontent.com/YOUR_REPO/main/.claude/skills/jellyfin-scan/scripts/monitor_scan.py
chmod +x monitor_scan.py

# Trigger scan and monitor progress
python3 monitor_scan.py --trigger
```

**Output**:
```
🔄 Triggering library scan...
✓ Library scan triggered

📊 Monitoring scan progress...
[13:45:23] 🔄 Scan running... (0%) - 5s elapsed
[13:46:10] 🔄 Scan running... (45%) - 52s elapsed
[13:47:30] ✓ Scan completed! - Total time: 127s

--- Library Statistics ---
  Series: 287
  Episodes: 12,456
  Movies: 1,234
```

### Option 2: Manual Trigger

```bash
ssh automation@srv759970.hstgr.cloud

# Trigger full library refresh
curl -X POST 'http://localhost:8096/Library/Refresh' \
  -H 'X-Emby-Token: 9af5f56a66e44ee68ddeec7bd07c9db8'

# Monitor logs manually
docker logs jellyfin --follow | grep -i "scan\|library\|validat"
```

## Scan Types

### 1. Full Library Refresh (All Content)
```bash
curl -X POST 'http://localhost:8096/Library/Refresh' \
  -H 'X-Emby-Token: YOUR_TOKEN'
```
- **Duration**: 5-30 minutes (depends on library size)
- **Use**: After major changes (new mount, config change)

### 2. Specific Library Only
```bash
# Get library IDs first
curl -s 'http://localhost:8096/Library/VirtualFolders' \
  -H 'X-Emby-Token: YOUR_TOKEN' | jq '.[] | {Name, ItemId}'

# Scan just TV library
curl -X POST 'http://localhost:8096/Items/{LibraryId}/Refresh?Recursive=true' \
  -H 'X-Emby-Token: YOUR_TOKEN'
```
- **Duration**: 1-5 minutes
- **Use**: After adding content to one library only

### 3. Single Item Refresh
```bash
# Get item ID
curl -s 'http://localhost:8096/Items?SearchTerm=Naruto' \
  -H 'X-Emby-Token: YOUR_TOKEN' | jq '.Items[0].Id'

# Refresh single show
curl -X POST 'http://localhost:8096/Items/{ItemId}/Refresh' \
  -H 'X-Emby-Token: YOUR_TOKEN'
```
- **Duration**: 5-30 seconds
- **Use**: Fixing metadata for one item

## Verifying Scan Results

### Check Library Statistics
```bash
curl -s 'http://localhost:8096/Items/Counts' \
  -H 'X-Emby-Token: 9af5f56a66e44ee68ddeec7bd07c9db8' | jq
```

**Expected output**:
```json
{
  "MovieCount": 1234,
  "SeriesCount": 287,
  "EpisodeCount": 12456,
  "ArtistCount": 0,
  "ProgramCount": 0,
  "TrailerCount": 0,
  "SongCount": 0,
  "AlbumCount": 0,
  "MusicVideoCount": 0,
  "BoxSetCount": 0,
  "BookCount": 0,
  "ItemCount": 14977
}
```

### Search for Specific Content
```bash
# Check if Naruto was detected
curl -s 'http://localhost:8096/Items?SearchTerm=Naruto&Recursive=true' \
  -H 'X-Emby-Token: 9af5f56a66e44ee68ddeec7bd07c9db8' | \
  jq '.Items[] | {Name, Type, Id}'
```

### List Recently Added
```bash
# Last 20 items added
curl -s 'http://localhost:8096/Items?SortBy=DateCreated&SortOrder=Descending&Limit=20' \
  -H 'X-Emby-Token: 9af5f56a66e44ee68ddeec7bd07c9db8' | \
  jq '.Items[] | {Name, Type, DateCreated}'
```

## Troubleshooting Quick Reference

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Scan doesn't start | Invalid API token | Check token in SECRETS.md |
| Scan takes >30min | Too many files or dead links | Scan specific library only |
| Items = 0 after scan | Mount not accessible | `docker exec jellyfin ls /media/shows/` |
| Content not detected | File naming wrong | Check naming conventions (see reference.md) |
| Scan stuck at X% | Network/disk issues | Restart Jellyfin, try again |

## File Naming Requirements

Jellyfin requires specific naming patterns:

### TV Shows ✅
```
Good:
/media/shows/Naruto (2002)/Season 01/Naruto S01E01.mkv
/media/shows/Breaking Bad/Season 05/Breaking.Bad.S05E01.mkv

Bad:
/media/shows/Naruto/01.mkv
/media/shows/[Anime] Naruto - Episode 01.mkv
```

### Movies ✅
```
Good:
/media/movies/Avatar (2009)/Avatar (2009).mkv
/media/movies/Inception (2010).mkv

Bad:
/media/movies/movie1.mkv
/media/movies/Avatar.mkv  (missing year)
```

## Integration with Other Skills

```
Typical workflow:
  media-stack-refresh
    └─ Restart Zurg/Rclone, trigger scan

  jellyfin-scan ← YOU ARE HERE
    └─ Monitor scan progress

  health-check
    └─ Verify all services healthy
```

## Performance Tips

### For Large Libraries (1000+ items)

1. **Disable real-time monitoring** (reduces I/O):
   - Dashboard → Libraries → Edit → Disable "Real-time monitoring"

2. **Scan during off-hours** (less resource contention)

3. **Disable thumbnail extraction during scan**:
   - Dashboard → Scheduled Tasks → "Extract chapter images" → Disable

4. **Use specific library scans** instead of full refresh

## For More Details

See [reference.md](./reference.md) for:
- Complete API endpoint documentation
- Advanced scan configuration
- File naming patterns for all media types
- Detailed troubleshooting guide

See [scripts/monitor_scan.py](./scripts/monitor_scan.py) for:
- Python source code
- Customization options
- Real-time monitoring implementation
