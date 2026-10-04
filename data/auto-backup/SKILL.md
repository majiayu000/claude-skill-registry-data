---
name: auto-backup
description: "Automated backup solution for databases, files, and cloud storage. Supports multiple destinations and incremental backups."
triggers:
  - "auto backup"
  - "自动备份"
  - "backup database"
  - "schedule backup"
---

# Auto Backup

Automated backup solution for databases, files, and cloud storage.

## Features

- 💾 **Multi-source** — Files, databases, Docker volumes
- ☁️ **Multi-dest** — S3, GCS, FTP, Local
- 📦 **Incremental** — Only backup changes
- 📅 **Schedule** — Cron-based scheduling
- 🔐 **Encrypted** — AES-256 encryption

## Supported Sources

| Source | Type | Status |
|--------|------|--------|
| PostgreSQL | Database | ✅ |
| MySQL | Database | ✅ |
| MongoDB | Database | ✅ |
| Files | Directory | ✅ |
| Docker Volumes | Container | ✅ |
| Redis | Cache | ✅ |

## Supported Destinations

| Destination | Type | Status |
|-------------|------|--------|
| AWS S3 | Cloud | ✅ |
| Google Cloud Storage | Cloud | ✅ |
| FTP/SFTP | Server | ✅ |
| Local | Disk | ✅ |
| Backblaze B2 | Cloud | ✅ |

## Usage

### Backup Database

```bash
# Backup PostgreSQL
hermes backup postgres \
  --host localhost \
  --database mydb \
  --output s3://my-bucket/backups/

# With encryption
hermes backup postgres --encrypt --password secret123
```

### Backup Files

```bash
# Backup directory
hermes backup files /var/www/html \
  --dest s3://my-bucket/files/ \
  --exclude "node_modules,*.log"
```

### Schedule Backup

```bash
# Daily at 2am
hermes backup schedule --cron "0 2 * * *" --task db-backup

# Hourly
hermes backup schedule --cron "0 * * * *" --task log-archive
```

## Configuration

```yaml
# backup-config.yml
backup:
  compress: gzip
  encryption: aes-256
  
sources:
  postgres:
    host: ${DB_HOST}
    port: 5432
    database: mydb
    
destinations:
  s3:
    bucket: my-backup-bucket
    region: us-east-1
    prefix: backups/
```

## Restore

```bash
# Restore from backup
hermes backup restore s3://my-bucket/backups/postgres-2026-05-30.sql.gz

# List available backups
hermes backup list --source postgres
```

## Pitfalls

1. **Storage Cost** — Monitor cloud storage usage
2. **Retention** — Set retention policies to save cost
3. **Test Restore** — Regularly test backup restoration