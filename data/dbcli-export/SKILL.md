---
name: dbcli-export
description: Export table data as SQL INSERT statements from 30+ databases using DbCli. Essential for creating backups before dangerous modifications (UPDATE/DELETE/DROP). Use when user needs to backup data, migrate tables, or create portable SQL dumps.
license: MIT
compatibility: Requires DbCli CLI tool (based on .NET 10 and SqlSugar). Supports Windows, Linux, macOS.
metadata:
  tool: dbcli
  version: "1.0.0"
  category: database
  operation-type: backup-export
  supported-databases: "30+"
allowed-tools: dbcli
---


## Command Style (Use PATH)

All examples use the plain command name `dbcli` (no directory prefix).
Ensure `dbcli` is on PATH instead of hardcoding paths like `.\.claude\skills\dbcli\dbcli.exe`.


# DbCli Export Skill

Export table data as SQL INSERT statements - essential for backup before dangerous operations.

## When to Use This Skill

- **MANDATORY before UPDATE/DELETE/DROP operations** - Create backups first
- User wants to backup table data
- User needs to migrate data between databases
- User wants portable SQL dump for version control
- User needs to copy table data to another environment
- Creating disaster recovery backups

## ⚠️ Safety-Critical Use Cases

This skill is **REQUIRED** before:
1. **UPDATE operations** - Backup data before modifying
2. **DELETE operations** - Backup data before removing
3. **DROP TABLE** - Backup before destroying table
4. **ALTER TABLE** - Backup before structure changes
5. **Bulk modifications** - Backup before mass updates

## Command Syntax

```bash
dbcli -c "CONNECTION_STRING" [-t DATABASE_TYPE] export TABLE_NAME > output.sql
```

## Global Options

- `-c, --connection`: Database connection string (required)
- `-t, --db-type`: Database type (default: sqlite)

## Basic Export

### Single Table Export

```bash
# SQLite - Export Users table
dbcli -c "Data Source=app.db" export Users > Users_backup.sql

# Output file contains:
# INSERT INTO Users (Id, Name, Email) VALUES (1, 'Alice', 'alice@example.com');
# INSERT INTO Users (Id, Name, Email) VALUES (2, 'Bob', 'bob@example.com');
```

### With Timestamp

```bash
# Create timestamped backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" export Users > Users_backup_${TIMESTAMP}.sql

echo "Backup created: Users_backup_${TIMESTAMP}.sql"
```

### Different Databases

```bash
# SQL Server
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Server=localhost;Database=mydb;Trusted_Connection=True" -t sqlserver export Users > Users_backup_${TIMESTAMP}.sql

# MySQL
dbcli -c "Server=localhost;Database=mydb;Uid=root;Pwd=xxxxxxxxxx" -t mysql export Customers > Customers_backup_${TIMESTAMP}.sql

# PostgreSQL
dbcli -c "Host=localhost;Database=mydb;Username=postgres;Password=xxxxxxxxxx" -t postgresql export Orders > Orders_backup_${TIMESTAMP}.sql
```

## Mandatory Backup Before Dangerous Operations

### Before UPDATE - Export Backup Workflow

```bash
#!/bin/bash
# Safe UPDATE workflow with mandatory backup

TABLE="Users"
CONNECTION="Data Source=app.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${TABLE}_backup_${TIMESTAMP}.sql"

# STEP 1: MANDATORY BACKUP
echo "Creating mandatory backup before UPDATE..."
dbcli -c "$CONNECTION" export $TABLE > $BACKUP_FILE

# Verify backup created
if [ ! -f "$BACKUP_FILE" ]; then
    echo "ERROR: Backup failed! Aborting UPDATE."
    exit 1
fi

BACKUP_SIZE=$(wc -l < "$BACKUP_FILE")
echo "Backup created: $BACKUP_FILE ($BACKUP_SIZE lines)"

# STEP 2: Confirm with user
read -p "Backup complete. Proceed with UPDATE? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "UPDATE cancelled by user"
    exit 0
fi

# STEP 3: Execute UPDATE
echo "Executing UPDATE..."
dbcli -c "$CONNECTION" exec "UPDATE Users SET status = 'verified' WHERE email_confirmed = 1"

echo "UPDATE complete. Backup saved: $BACKUP_FILE"
```

### Before DELETE - Export Affected Records

```bash
#!/bin/bash
# Safe DELETE workflow with selective backup

TABLE="Users"
CONNECTION="Data Source=app.db"
WHERE_CLAUSE="last_login < date('now', '-365 days')"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# STEP 1: Preview what will be deleted
echo "Records to be deleted:"
dbcli -c "$CONNECTION" -f table query "SELECT * FROM $TABLE WHERE $WHERE_CLAUSE"

# Count affected records
COUNT=$(dbcli -c "$CONNECTION" query "SELECT COUNT(*) as count FROM $TABLE WHERE $WHERE_CLAUSE" | jq -r '.[0].count')
echo "Total records to delete: $COUNT"

# STEP 2: MANDATORY BACKUP of affected records
if [ "$COUNT" -gt 0 ]; then
    BACKUP_FILE="${TABLE}_deleted_${TIMESTAMP}.sql"
    echo "Creating backup of records to be deleted..."

    # Export full table (safest approach)
    dbcli -c "$CONNECTION" export $TABLE > $BACKUP_FILE

    echo "Backup created: $BACKUP_FILE"
fi

# STEP 3: Confirm deletion
read -p "Delete $COUNT records? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "DELETE cancelled"
    exit 0
fi

# STEP 4: Execute DELETE
dbcli -c "$CONNECTION" exec "DELETE FROM $TABLE WHERE $WHERE_CLAUSE"
echo "Deleted $COUNT records. Backup: $BACKUP_FILE"
```

### Before DROP TABLE - Full Export

```bash
#!/bin/bash
# Safe DROP TABLE workflow with complete backup

TABLE="OldTable"
CONNECTION="Data Source=app.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"

mkdir -p $BACKUP_DIR

# STEP 1: Export table schema
echo "Exporting table schema..."
dbcli -c "$CONNECTION" -f table columns $TABLE > "${BACKUP_DIR}/${TABLE}_schema_${TIMESTAMP}.txt"

# STEP 2: MANDATORY data export
echo "Exporting table data..."
dbcli -c "$CONNECTION" export $TABLE > "${BACKUP_DIR}/${TABLE}_data_${TIMESTAMP}.sql"

# STEP 3: Create table copy (fastest recovery option)
echo "Creating table copy..."
dbcli -c "$CONNECTION" query "CREATE TABLE ${TABLE}_copy_${TIMESTAMP} AS SELECT * FROM $TABLE"

# Verify backups
DATA_LINES=$(wc -l < "${BACKUP_DIR}/${TABLE}_data_${TIMESTAMP}.sql")
COPY_COUNT=$(dbcli -c "$CONNECTION" query "SELECT COUNT(*) as count FROM ${TABLE}_copy_${TIMESTAMP}" | jq -r '.[0].count')

echo "Backups created:"
echo "  - Schema: ${BACKUP_DIR}/${TABLE}_schema_${TIMESTAMP}.txt"
echo "  - Data: ${BACKUP_DIR}/${TABLE}_data_${TIMESTAMP}.sql ($DATA_LINES lines)"
echo "  - Table copy: ${TABLE}_copy_${TIMESTAMP} ($COPY_COUNT rows)"

# STEP 4: Confirm DROP
read -p "All backups created. DROP TABLE $TABLE? (type 'DROP' to confirm): " confirm
if [ "$confirm" != "DROP" ]; then
    echo "DROP TABLE cancelled"
    exit 0
fi

# STEP 5: Execute DROP
echo "Dropping table..."
dbcli -c "$CONNECTION" ddl "DROP TABLE $TABLE"
echo "Table dropped. Recovery files available in $BACKUP_DIR/"
```

## Export All Tables (Database Backup)

```bash
#!/bin/bash
# Export all tables in database

CONNECTION="Data Source=app.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backup_${TIMESTAMP}"

mkdir -p $BACKUP_DIR

echo "Exporting all tables..."

# Get list of tables
dbcli -c "$CONNECTION" tables | jq -r '.[].TableName' | while read table; do
    echo "  Exporting $table..."
    dbcli -c "$CONNECTION" export $table > "${BACKUP_DIR}/${table}.sql"
done

# Create archive
tar -czf "backup_${TIMESTAMP}.tar.gz" $BACKUP_DIR

echo "Backup complete: backup_${TIMESTAMP}.tar.gz"
```

## Restore from Export

### Restore Single Table

```bash
# Drop and recreate table, then import backup
dbcli -c "Data Source=app.db" ddl "DROP TABLE IF EXISTS Users"
dbcli -c "Data Source=app.db" ddl -F Users_schema.sql  # Create table structure
dbcli -c "Data Source=app.db" exec -F Users_backup_20250127_143022.sql

echo "Table restored from backup"
```

### Restore Specific Records

```bash
# Restore only specific records from backup
grep "WHERE Id IN (1, 2, 3)" Users_backup_20250127_143022.sql | \
    dbcli -c "Data Source=app.db" exec -F -

# Or manually edit SQL file to restore selective records
```

### Cross-Database Migration

```bash
# Export from MySQL
dbcli -c "Server=source;Database=mydb;Uid=root;Pwd=xxxxxxxxxx" -t mysql export Users > Users_export.sql

# Import to PostgreSQL (may need SQL syntax adjustments)
dbcli -c "Host=target;Database=mydb;Username=postgres;Password=xxxxxxxxxx" -t postgresql exec -F Users_export.sql
```

## Chinese Domestic Databases

### DaMeng (达梦)

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Export table
dbcli -c "Server=localhost;User Id=SYSDBA;PWD=xxxxxxxxxx;DATABASE=mydb" -t dm export dm_test > dm_test_backup_${TIMESTAMP}.sql

# Before UPDATE
echo "Creating backup before UPDATE..."
dbcli -c "Server=localhost;User Id=SYSDBA;PWD=xxxxxxxxxx;DATABASE=mydb" -t dm export dm_test > dm_test_backup_${TIMESTAMP}.sql
read -p "Backup complete. Continue with UPDATE? (yes/no): " confirm
if [ "$confirm" = "yes" ]; then
    dbcli -c "Server=localhost;User Id=SYSDBA;PWD=xxxxxxxxxx;DATABASE=mydb" -t dm exec "UPDATE dm_test SET status = 1"
fi
```

### GaussDB

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CONNECTION="Host=localhost;Port=8000;Database=mydb;Username=gaussdb;Password=xxxxxxxxxx"

# Export with timestamp
dbcli -c "$CONNECTION" -t gaussdb export gauss_test > gauss_test_backup_${TIMESTAMP}.sql

# Safe DELETE workflow
echo "Creating backup before DELETE..."
dbcli -c "$CONNECTION" -t gaussdb export gauss_test > gauss_test_backup_${TIMESTAMP}.sql
echo "Backup: gauss_test_backup_${TIMESTAMP}.sql"
read -p "Proceed with DELETE? (yes/no): " confirm
[ "$confirm" = "yes" ] && dbcli -c "$CONNECTION" -t gaussdb exec "DELETE FROM gauss_test WHERE inactive = 1"
```

## Programmatic Export with Safety

### Python - Safe Modification Function

```python
import subprocess
import json
from datetime import datetime
import os

def safe_modify_table(connection, table, modify_sql, db_type='sqlite'):
    """Execute modification with automatic backup"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = 'backups'
    os.makedirs(backup_dir, exist_ok=True)

    backup_file = f"{backup_dir}/{table}_backup_{timestamp}.sql"

    # STEP 1: MANDATORY BACKUP
    print(f"Creating backup: {backup_file}")
    export_cmd = ['dbcli', '-c', connection, '-t', db_type, 'export', table]

    with open(backup_file, 'w', encoding='utf-8') as f:
        result = subprocess.run(export_cmd, stdout=f, text=True)

    if result.returncode != 0:
        raise Exception("Backup failed! Aborting modification.")

    # Verify backup file created
    if not os.path.exists(backup_file):
        raise Exception("Backup file not created!")

    backup_size = os.path.getsize(backup_file)
    print(f"Backup created: {backup_size} bytes")

    # STEP 2: Prompt user
    confirm = input(f"Backup complete. Execute modification? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Modification cancelled by user")
        return None

    # STEP 3: Execute modification
    print("Executing modification...")
    exec_cmd = ['dbcli', '-c', connection, '-t', db_type, 'exec', modify_sql]
    result = subprocess.run(exec_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Modification failed: {result.stderr}")
        print(f"Backup available: {backup_file}")
        return None

    data = json.loads(result.stdout)
    print(f"Modified {data['AffectedRows']} rows")
    print(f"Backup saved: {backup_file}")

    return backup_file

# Usage
backup = safe_modify_table(
    connection='Data Source=app.db',
    table='Users',
    modify_sql="UPDATE Users SET verified = 1 WHERE email_confirmed = 1"
)
```

### PowerShell - Backup Before Delete

```powershell
function Remove-TableDataSafely {
    param(
        [string]$Connection,
        [string]$Table,
        [string]$WhereClause,
        [string]$DbType = 'sqlite'
    )

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupFile = "${Table}_backup_${timestamp}.sql"

    # Preview deletion
    $previewSql = "SELECT * FROM $Table WHERE $WhereClause"
    Write-Host "Records to be deleted:"
    dbcli -c $Connection -t $DbType -f table query $previewSql

    $countSql = "SELECT COUNT(*) as count FROM $Table WHERE $WhereClause"
    $count = (dbcli -c $Connection -t $DbType query $countSql | ConvertFrom-Json)[0].count
    Write-Host "Total records to delete: $count"

    # MANDATORY BACKUP
    Write-Host "Creating backup..."
    dbcli -c $Connection -t $DbType export $Table > $backupFile

    if (-not (Test-Path $backupFile)) {
        Write-Error "Backup failed! Aborting deletion."
        return
    }

    Write-Host "Backup created: $backupFile"

    # Confirm deletion
    $confirm = Read-Host "Delete $count records? (yes/no)"
    if ($confirm -ne 'yes') {
        Write-Host "Deletion cancelled"
        return
    }

    # Execute DELETE
    $deleteSql = "DELETE FROM $Table WHERE $WhereClause"
    $result = dbcli -c $Connection -t $DbType exec $deleteSql | ConvertFrom-Json

    Write-Host "Deleted $($result.AffectedRows) rows"
    Write-Host "Backup: $backupFile"
}

# Usage
Remove-TableDataSafely -Connection "Data Source=app.db" `
                        -Table "Users" `
                        -WhereClause "active = 0"
```

## Backup Verification

```bash
# Verify backup completeness
TABLE="Users"
BACKUP="Users_backup_20250127_143022.sql"

# Count records in original table
ORIGINAL_COUNT=$(dbcli -c "Data Source=app.db" query "SELECT COUNT(*) as count FROM $TABLE" | jq -r '.[0].count')

# Count INSERT statements in backup
BACKUP_COUNT=$(grep -c "^INSERT INTO" $BACKUP)

echo "Original table: $ORIGINAL_COUNT records"
echo "Backup file: $BACKUP_COUNT INSERT statements"

if [ "$ORIGINAL_COUNT" -eq "$BACKUP_COUNT" ]; then
    echo "Backup verified - counts match"
else
    echo "WARNING: Backup incomplete! Counts don't match!"
fi
```

## Automated Backup Schedule

```bash
#!/bin/bash
# daily_backup.sh - Schedule with cron

CONNECTION="Data Source=production.db"
BACKUP_DIR="/backups/database"
RETENTION_DAYS=30
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Export all tables
dbcli -c "$CONNECTION" tables | jq -r '.[].TableName' | while read table; do
    dbcli -c "$CONNECTION" export $table > "${BACKUP_DIR}/${table}_${TIMESTAMP}.sql"
done

# Compress backups
tar -czf "${BACKUP_DIR}/full_backup_${TIMESTAMP}.tar.gz" ${BACKUP_DIR}/*_${TIMESTAMP}.sql
rm ${BACKUP_DIR}/*_${TIMESTAMP}.sql

# Delete old backups
find $BACKUP_DIR -name "full_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup complete: full_backup_${TIMESTAMP}.tar.gz"
```

## Best Practices

1. **ALWAYS export before dangerous operations** - UPDATE, DELETE, DROP
2. **Use timestamps** in backup filenames for version control
3. **Verify backups** immediately after creation
4. **Compress large backups** to save disk space
5. **Store backups off-server** for disaster recovery
6. **Test restore procedures** regularly
7. **Document backup locations** for team members
8. **Automate regular backups** with cron/scheduled tasks

## Common Patterns

### Pre-Modification Checklist

```bash
#!/bin/bash
# pre_modify_checklist.sh

TABLE="$1"
CONNECTION="Data Source=app.db"

echo "=== Pre-Modification Safety Checklist ==="
echo

# 1. Export current data
echo "[1/4] Creating backup..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "$CONNECTION" export $TABLE > "${TABLE}_backup_${TIMESTAMP}.sql"
echo "    Backup: ${TABLE}_backup_${TIMESTAMP}.sql"

# 2. Count records
COUNT=$(dbcli -c "$CONNECTION" query "SELECT COUNT(*) FROM $TABLE" | jq -r '.[0].count')
echo "[2/4] Record count: $COUNT"

# 3. Check table structure
echo "[3/4] Table structure:"
dbcli -c "$CONNECTION" -f table columns $TABLE

# 4. Create table copy
COPY_TABLE="${TABLE}_copy_${TIMESTAMP}"
dbcli -c "$CONNECTION" query "CREATE TABLE $COPY_TABLE AS SELECT * FROM $TABLE"
echo "[4/4] Table copy created: $COPY_TABLE"

echo
echo "=== Checklist Complete ==="
echo "Safe to proceed with modifications"
```
