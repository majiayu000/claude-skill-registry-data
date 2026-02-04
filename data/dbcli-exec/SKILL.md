---
name: dbcli-exec
description: Execute INSERT, UPDATE, DELETE statements on 30+ databases using DbCli. Includes mandatory backup procedures before destructive operations. Use when user needs to modify data, insert records, update fields, or delete rows. Always create backups first.
license: MIT
compatibility: Requires DbCli CLI tool (based on .NET 10 and SqlSugar). Supports Windows, Linux, macOS.
metadata:
  tool: dbcli
  version: "1.0.0"
  category: database
  safety-level: requires-backup
  supported-databases: "30+"
allowed-tools: dbcli
---


## Command Style (Use PATH)

All examples use the plain command name `dbcli` (no directory prefix).
Ensure `dbcli` is on PATH instead of hardcoding paths like `.\.claude\skills\dbcli\dbcli.exe`.


# DbCli Exec Skill

Execute INSERT, UPDATE, DELETE (DML) operations on databases with mandatory backup procedures.

## Supported Databases (DML)

`exec` is intended for **SQL / relational databases** supported by DbCli (SqlSugar providers). Examples include:

- SQL Server
- MySQL-family (MySQL, MariaDB, TiDB, OceanBase, etc.)
- PostgreSQL-family (PostgreSQL, GaussDB, Kingbase, etc.)
- SQLite
- Oracle
- IBM DB2
- Chinese domestic databases like DM (DaMeng)

For connection string examples and the full list, see `skills/CONNECTION_STRINGS.md`.

## ⚠️ CRITICAL SAFETY REQUIREMENT

**ALWAYS CREATE BACKUPS BEFORE EXECUTING UPDATE/DELETE OPERATIONS**

Backup naming convention:
- Table copy: `tablename_copy_YYYYMMDD_HHMMSS`
- SQL export: `tablename_backup_YYYYMMDD_HHMMSS.sql`

## When to Use This Skill

- User wants to insert new records into a table
- User needs to update existing data
- User wants to delete records
- User mentions INSERT, UPDATE, DELETE, modify, change, or remove data
- **Never use without creating backups first for UPDATE/DELETE**

## Command Syntax

```bash
dbcli -c "CONNECTION_STRING" [-t DATABASE_TYPE] exec "DML_STATEMENT" [-p JSON] [-P params.json]
```

### Global Options

- `-c, --connection`: Database connection string (required)
- `-t, --db-type`: Database type (default: sqlite)

### Subcommand Options

- `-F, --file`: Execute SQL from file instead of command line
- `-p, --params`: JSON parameters object (use `@Param` placeholders)
- `-P, --params-file`: Read JSON parameters from file

## Safe Operation Workflow

### INSERT Operations (No Backup Required)

```bash
# Direct INSERT - safe operation
dbcli -c "Data Source=app.db" exec "INSERT INTO Users (Name, Email) VALUES ('Alice', 'alice@example.com')"
```

### Parameterized Execute (RDB)

```bash
dbcli -c "Data Source=app.db" exec "INSERT INTO Users (Id, Name) VALUES (@Id, @Name)" -p '{"Id":1,"Name":"Alice"}'
```

Notes:

- SQL Server supports `GO` batch separators for `exec` when not using `-p/-P` (use `-F` for scripts).
- SQLite providers may require `DisableClearParameters: true` in config (maps to SqlSugar `IsClearParameters=false`).

### UPDATE Operations (Backup Required)

```bash
# STEP 1: Create backup (table copy - fastest)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" query "CREATE TABLE Users_copy_${TIMESTAMP} AS SELECT * FROM Users"

# STEP 2: Execute UPDATE
dbcli -c "Data Source=app.db" exec "UPDATE Users SET Email = 'newemail@example.com' WHERE Id = 1"

# STEP 3: Verify changes
dbcli -c "Data Source=app.db" -f table query "SELECT * FROM Users WHERE Id = 1"

# STEP 4 (if needed): Rollback from backup
dbcli -c "Data Source=app.db" exec "DELETE FROM Users"
dbcli -c "Data Source=app.db" exec "INSERT INTO Users SELECT * FROM Users_copy_${TIMESTAMP}"
```

### DELETE Operations (Backup Required)

```bash
# STEP 1: Create backup (SQL export - portable)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" export Users > Users_backup_${TIMESTAMP}.sql

# STEP 2: Execute DELETE
dbcli -c "Data Source=app.db" exec "DELETE FROM Users WHERE inactive = 1"

# STEP 3: Verify deletion
dbcli -c "Data Source=app.db" query "SELECT COUNT(*) as remaining FROM Users"

# STEP 4 (if needed): Restore from backup
dbcli -c "Data Source=app.db" exec -F Users_backup_${TIMESTAMP}.sql
```

## INSERT Operations

### Single Row Insert

```bash
# SQLite
dbcli -c "Data Source=app.db" exec "INSERT INTO Users (Name, Email) VALUES ('John', 'john@example.com')"

# SQL Server
dbcli -c "Server=localhost;Database=mydb;Trusted_Connection=True" -t sqlserver exec "INSERT INTO Users (Name, Email) VALUES ('John', 'john@example.com')"

# MySQL
dbcli -c "Server=localhost;Database=mydb;Uid=root;Pwd=xxxxxxxxxx" -t mysql exec "INSERT INTO Users (Name, Email) VALUES ('John', 'john@example.com')"

# PostgreSQL
dbcli -c "Host=localhost;Database=mydb;Username=postgres;Password=xxxxxxxxxx" -t postgresql exec "INSERT INTO Users (Name, Email) VALUES ('John', 'john@example.com')"

# Oracle
dbcli -c "Data Source=localhost:1521/XEPDB1;User Id=system;Password=xxxxxxxxxx" -t oracle exec "INSERT INTO Users (Name, Email) VALUES ('John', 'john@example.com')"

# DB2
dbcli -c "Server=localhost:50000;Database=MYDB;UID=db2inst1;PWD=xxxxxxxxxx" -t db2 exec "INSERT INTO Users (Name, Email) VALUES ('John', 'john@example.com')"

# DM (DaMeng)
dbcli -c "Server=localhost;Database=MYDB;User Id=SYSDBA;Password=xxxxxxxxxx" -t dm exec "INSERT INTO Users (Name, Email) VALUES ('John', 'john@example.com')"
```

### Multiple Row Insert

```bash
dbcli -c "Data Source=app.db" exec "INSERT INTO Users (Name, Email) VALUES ('Alice', 'alice@example.com'), ('Bob', 'bob@example.com'), ('Charlie', 'charlie@example.com')"
```

### Insert with Auto-Generated ID

```bash
# SQLite - Returns affected rows
dbcli -c "Data Source=app.db" exec "INSERT INTO Users (Name, Email) VALUES ('David', 'david@example.com')"

# Output: {"AffectedRows": 1}
```

### Insert from File

```bash
# Create insert file
cat > bulk_insert.sql <<EOF
INSERT INTO Products (Name, Price) VALUES ('Laptop', 5999.00);
INSERT INTO Products (Name, Price) VALUES ('Mouse', 99.00);
INSERT INTO Products (Name, Price) VALUES ('Keyboard', 299.00);
EOF

# Execute from file
dbcli -c "Data Source=app.db" exec -F bulk_insert.sql
```

## UPDATE Operations

### Simple UPDATE with Backup

```bash
# Backup first
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" query "CREATE TABLE Users_copy_${TIMESTAMP} AS SELECT * FROM Users WHERE Id = 1"

# Execute UPDATE
dbcli -c "Data Source=app.db" exec "UPDATE Users SET Email = 'updated@example.com' WHERE Id = 1"
```

### Bulk UPDATE with Verification

```bash
# 1. Count records to be updated
dbcli -c "Data Source=app.db" query "SELECT COUNT(*) as count FROM Users WHERE status = 'inactive'"

# 2. Create backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" query "CREATE TABLE Users_copy_${TIMESTAMP} AS SELECT * FROM Users WHERE status = 'inactive'"

# 3. Execute UPDATE
dbcli -c "Data Source=app.db" exec "UPDATE Users SET status = 'archived' WHERE status = 'inactive'"

# 4. Verify changes
dbcli -c "Data Source=app.db" query "SELECT COUNT(*) as count FROM Users WHERE status = 'archived'"
```

### UPDATE Multiple Columns

```bash
# Backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" export Users > Users_backup_${TIMESTAMP}.sql

# Update multiple fields
dbcli -c "Data Source=app.db" exec "UPDATE Users SET Name = 'Jane Doe', Email = 'jane@example.com', UpdatedAt = datetime('now') WHERE Id = 5"
```

### Conditional UPDATE

```bash
# Backup affected records
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" query "CREATE TABLE Orders_copy_${TIMESTAMP} AS SELECT * FROM Orders WHERE status = 'pending' AND created_at < date('now', '-30 days')"

# Update old pending orders
dbcli -c "Data Source=app.db" exec "UPDATE Orders SET status = 'expired' WHERE status = 'pending' AND created_at < date('now', '-30 days')"
```

## DELETE Operations

### DELETE with WHERE Clause

```bash
# 1. Preview what will be deleted
dbcli -c "Data Source=app.db" -f table query "SELECT * FROM Users WHERE last_login < date('now', '-365 days')"

# 2. Create backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" export Users > Users_backup_${TIMESTAMP}.sql

# 3. Execute DELETE
dbcli -c "Data Source=app.db" exec "DELETE FROM Users WHERE last_login < date('now', '-365 days')"

# 4. Verify deletion
dbcli -c "Data Source=app.db" query "SELECT COUNT(*) as remaining FROM Users"
```

### DELETE All Records (DANGEROUS)

```bash
# FULL TABLE BACKUP REQUIRED
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create TWO backups (safety)
dbcli -c "Data Source=app.db" query "CREATE TABLE Users_copy_${TIMESTAMP} AS SELECT * FROM Users"
dbcli -c "Data Source=app.db" export Users > Users_backup_${TIMESTAMP}.sql

# Confirm with user before proceeding
read -p "Delete ALL records from Users table? (yes/no): " confirm
if [ "$confirm" = "yes" ]; then
    dbcli -c "Data Source=app.db" exec "DELETE FROM Users"
    echo "All records deleted. Backups: Users_copy_${TIMESTAMP} and Users_backup_${TIMESTAMP}.sql"
fi
```

### DELETE with JOIN (Advanced)

```bash
# Backup first
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" export OrderItems > OrderItems_backup_${TIMESTAMP}.sql

# Delete orphaned order items
dbcli -c "Data Source=app.db" exec "DELETE FROM OrderItems WHERE order_id NOT IN (SELECT id FROM Orders)"
```

## Chinese Domestic Databases

### DaMeng (达梦)

```bash
# INSERT
dbcli -c "Server=localhost;User Id=SYSDBA;PWD=xxxxxxxxxx;DATABASE=mydb" -t dm exec "INSERT INTO dm_test (id, name) VALUES (1, '测试')"

# UPDATE with backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Server=localhost;User Id=SYSDBA;PWD=xxxxxxxxxx;DATABASE=mydb" -t dm query "CREATE TABLE dm_test_copy_${TIMESTAMP} AS SELECT * FROM dm_test WHERE id = 1"
dbcli -c "Server=localhost;User Id=SYSDBA;PWD=xxxxxxxxxx;DATABASE=mydb" -t dm exec "UPDATE dm_test SET name = '更新' WHERE id = 1"
```

### GaussDB

```bash
# INSERT
dbcli -c "Host=localhost;Port=8000;Database=mydb;Username=gaussdb;Password=xxxxxxxxxx" -t gaussdb exec "INSERT INTO gauss_test (name, amount) VALUES ('产品A', 99.99)"

# Bulk UPDATE with backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Host=localhost;Port=8000;Database=mydb;Username=gaussdb;Password=xxxxxxxxxx" -t gaussdb export gauss_test > gauss_backup_${TIMESTAMP}.sql
dbcli -c "Host=localhost;Port=8000;Database=mydb;Username=gaussdb;Password=xxxxxxxxxx" -t gaussdb exec "UPDATE gauss_test SET amount = amount * 1.1 WHERE category = 'premium'"
```

## Programmatic Usage

### Python with Backup

```python
import subprocess
import json
from datetime import datetime

def safe_update(connection, table, update_sql):
    """Execute UPDATE with automatic backup"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_table = f"{table}_copy_{timestamp}"

    # Create backup
    backup_cmd = [
        'dbcli', '-c', connection,
        'query', f'CREATE TABLE {backup_table} AS SELECT * FROM {table}'
    ]
    subprocess.run(backup_cmd, check=True)
    print(f"Backup created: {backup_table}")

    # Execute UPDATE
    update_cmd = ['dbcli', '-c', connection, 'exec', update_sql]
    result = subprocess.run(update_cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    print(f"Updated {data['AffectedRows']} rows")

    return backup_table

# Usage
backup = safe_update(
    'Data Source=app.db',
    'Users',
    "UPDATE Users SET status = 'active' WHERE verified = 1"
)
```

### PowerShell with Verification

```powershell
function Safe-DbUpdate {
    param(
        [string]$Connection,
        [string]$Table,
        [string]$UpdateSql
    )

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backup = "${Table}_backup_${timestamp}.sql"

    # Export backup
    dbcli -c $Connection export $Table > $backup
    Write-Host "Backup created: $backup"

    # Execute UPDATE
    $result = dbcli -c $Connection exec $UpdateSql | ConvertFrom-Json
    Write-Host "Updated $($result.AffectedRows) rows"

    return $backup
}

# Usage
$backup = Safe-DbUpdate -Connection "Data Source=app.db" `
                        -Table "Users" `
                        -UpdateSql "UPDATE Users SET Email = LOWER(Email)"
```

## Response Format

All exec operations return JSON with affected row count:

```json
{
  "AffectedRows": 5
}
```

## Error Handling

```bash
# Check if operation succeeded
dbcli -c "Data Source=app.db" exec "DELETE FROM temp_data"
if [ $? -eq 0 ]; then
    echo "Delete succeeded"
else
    echo "Delete failed - check error message"
    exit 1
fi
```

## Common Patterns

### Upsert Pattern (INSERT or UPDATE)

```bash
# SQLite - INSERT OR REPLACE
dbcli -c "Data Source=app.db" exec "INSERT OR REPLACE INTO Settings (key, value) VALUES ('theme', 'dark')"

# MySQL - INSERT ON DUPLICATE KEY UPDATE
dbcli -c "Server=localhost;Database=mydb;Uid=root;Pwd=xxxxxxxxxx" -t mysql exec "INSERT INTO Settings (key, value) VALUES ('theme', 'dark') ON DUPLICATE KEY UPDATE value = 'dark'"
```

### Batch Insert from CSV

```bash
# Generate INSERT statements from CSV
awk -F',' 'NR>1 {print "INSERT INTO products (name, price) VALUES (\""$1"\", "$2");"}' products.csv > insert_products.sql

# Execute batch
dbcli -c "Data Source=app.db" exec -F insert_products.sql
```

### Increment Counter

```bash
dbcli -c "Data Source=app.db" exec "UPDATE counters SET value = value + 1 WHERE name = 'page_views'"
```

## Security Best Practices

1. **Always create backups** before UPDATE/DELETE
2. **Use WHERE clauses** to avoid accidental full-table updates
3. **Verify affected rows** match expectations
4. **Test on backup database** first for complex operations
5. **Use transactions** for multi-step operations when possible
6. **Avoid dynamic SQL** - validate all user input
7. **Use read-only users** when possible (query-only access)

## Backup Recovery

### Restore from Table Copy

```bash
# Restore entire table
dbcli -c "Data Source=app.db" exec "DELETE FROM Users"
dbcli -c "Data Source=app.db" exec "INSERT INTO Users SELECT * FROM Users_copy_20250127_143022"
```

### Restore from SQL Export

```bash
# Restore from SQL file
dbcli -c "Data Source=app.db" exec "DELETE FROM Users"
dbcli -c "Data Source=app.db" exec -F Users_backup_20250127_143022.sql
```

### Selective Restore

```bash
# Restore only specific records
dbcli -c "Data Source=app.db" exec "INSERT INTO Users SELECT * FROM Users_copy_20250127_143022 WHERE Id IN (1, 2, 3)"
```
