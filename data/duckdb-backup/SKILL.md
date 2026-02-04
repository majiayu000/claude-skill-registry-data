---
name: DuckDB Backup
description: Comprehensive DuckDB database backup toolkit supporting both file-based (cp) and native (ATTACH+COPY) backup approaches. Use when you need to backup DuckDB databases locally or to remote storage, create daily scheduled backups, verify backup integrity, or manage backup retention policies.
---

# DuckDB Backup Skill

## Quick Start

Two backup methods, choose based on your needs:

### File-Based Backup (cp method) - Fast for local backups

```bash
python3 scripts/backup_duckdb.py \
  --db data/awsntp.duckdb \
  --backup data/backup-20251223.duckdb \
  --method cp
```

### Native DuckDB Backup (attach method) - For remote/cloud backups

```bash
python3 scripts/backup_duckdb.py \
  --db data/awsntp.duckdb \
  --backup data/backup-20251223.duckdb \
  --method attach
```

### With Automatic Timestamp Naming

```bash
python3 scripts/backup_duckdb.py \
  --db data/awsntp.duckdb \
  --backup data/backups/ \
  --method cp \
  --timestamp
# Creates: data/backups/backup-20251223-153045.duckdb
```

## Features

- **Two backup methods**: cp (fast, local) and attach (flexible, cloud-ready)
- **Timestamped backups**: Automatic unique naming with YYYYMMDD-HHMMSS format
- **Error handling**: Comprehensive logging and error reporting
- **Scheduled backups**: cron/Task Scheduler integration for daily backups
- **Verification**: Tools to verify backup integrity and table counts
- **Retention policies**: Scripts to manage backup history and cleanup

## When to Use

### File-Based (cp method):
- Daily local backups (fastest approach)
- Pre-materialization safety snapshots
- Development/testing environments
- When speed is critical
- Local machine backups

### Native DuckDB (attach method):
- Cloud/remote storage backups
- Cross-environment transfers
- Database in active use scenarios
- When you need portable backups
- Complex backup scenarios

## Command Reference

```bash
python3 scripts/backup_duckdb.py --db <source> --backup <target> [options]
```

**Arguments:**
- `--db` (required): Path to source DuckDB database
- `--backup` (required): Backup target (file path for cp, directory for attach with --timestamp)
- `--method` (optional): Backup method - `cp` (default) or `attach`
- `--timestamp` (optional): Add YYYYMMDD-HHMMSS timestamp to filename

**Exit codes:**
- `0`: Backup successful
- `1`: Backup failed (check logs)

## Examples

### Example 1: One-time Local Backup

```bash
python3 scripts/backup_duckdb.py \
  --db ~/LocalRepos/awsntpdagster/data/awsntp.duckdb \
  --backup ~/LocalRepos/awsntpdagster/data/backup-20251223.duckdb \
  --method cp
```

### Example 2: Daily Timestamped Backups to Folder

```bash
python3 scripts/backup_duckdb.py \
  --db ~/LocalRepos/awsntpdagster/data/awsntp.duckdb \
  --backup ~/LocalRepos/awsntpdagster/data/backups \
  --method cp \
  --timestamp
```

### Example 3: Scheduled Daily Backup (cron)

Add to crontab:
```cron
0 2 * * * python3 /path/to/backup_duckdb.py --db /path/to/awsntp.duckdb --backup /path/to/backups/ --method cp --timestamp >> /var/log/duckdb_backup.log 2>&1
```

### Example 4: Backup with Retention Cleanup

```bash
#!/bin/bash
# Backup and keep only 7 most recent
BACKUP_DIR="/path/to/backups"

python3 scripts/backup_duckdb.py \
  --db data/awsntp.duckdb \
  --backup "$BACKUP_DIR" \
  --method cp \
  --timestamp

# Keep only 7 most recent backups
ls -t "$BACKUP_DIR"/backup-*.duckdb | tail -n +8 | xargs rm -f
```

## Backup Strategy Selection

**For 975 MB DuckDB database (awsntp.duckdb):**

| Scenario | Method | Speed | Best For |
|----------|--------|-------|----------|
| Daily backup before asset materialization | cp | ~1-2s | Production safety |
| Weekly archive to external drive | cp | ~1-2s | Local storage |
| Cloud backup to S3 | attach | ~30-60s | Remote storage |
| Backup during active queries | attach | N/A | Concurrent access |

## Advanced Usage

### Verify Backup Integrity

```bash
# Check backup exists and is readable
duckdb data/backup-20251223-153045.duckdb \
  "SELECT COUNT(*) as table_count FROM information_schema.tables;"
```

### Compare Original and Backup Sizes

```bash
ls -lh data/awsntp.duckdb data/backup-*.duckdb | awk '{print $5, $9}'
```

### List All Backups Chronologically

```bash
ls -lt data/backups/backup-*.duckdb | head -10
```

## Troubleshooting

**Issue: "duckdb: command not found"**
- Install DuckDB CLI or update PATH
- Use full path to duckdb binary if attach method needed

**Issue: "database is locked"**
- Ensure no active connections to source database
- attach method can work around this (doesn't lock database)

**Issue: "out of disk space"**
- Check available disk space: `df -h`
- Use attach method for cloud storage
- Implement retention cleanup scripts

**Issue: Slow backup**
- For large databases, cp method is fastest
- Schedule backups during off-peak hours
- Consider incremental backup strategies

## Integration with Your Pipeline

### Pre-materialization Backup

```bash
# Backup before running expensive assets
python3 scripts/backup_duckdb.py \
  --db data/awsntp.duckdb \
  --backup data/pre-materialization-backup.duckdb \
  --method cp

# Then run your asset materialization
dagster asset materialize -m awsntpdagster.definitions --select awsntp_features_merged_v6
```

### Scheduled Daily Backup

For your awsntpdagster project:

**macOS/Linux crontab:**
```cron
0 2 * * * cd /Users/zhaoliang/LocalRepos/awsntpdagster && python3 src/awsntpdagster/scripts/backup_duckdb.py --db data/awsntp.duckdb --backup data/backups/ --method cp --timestamp
```

## Reference

For detailed backup strategy guide, scheduling patterns, and retention policies, see:
- **[backup_strategies.md](references/backup_strategies.md)** - When to use each method, cron setup, verification, troubleshooting

## Performance Notes

- **cp method**: ~1-2 seconds for 975 MB database (your awsntp.duckdb)
- **attach method**: ~30-60 seconds for 975 MB database
- Both methods: Minimal CPU usage
- Disk space required: 1x original database size
