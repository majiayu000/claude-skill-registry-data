---
name: backup
description: Back up the ChefFlow database. Runs pg_dump via the backup script.
user-invocable: true
---

# Database Backup

Run the database backup script.

```bash
bash scripts/backup-db.sh
```

Report: backup file path, size, timestamp. If it fails, show the exact error.

**IMPORTANT:** This is a read-only export (pg_dump). Safe to run anytime. Does not modify the database.
