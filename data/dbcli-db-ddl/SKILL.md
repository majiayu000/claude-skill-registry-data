---
name: dbcli-db-ddl
description: Execute DDL (Data Definition Language) statements - CREATE, ALTER, DROP tables, indexes, views on 30+ databases using DbCli. CRITICAL - requires mandatory backup before DROP/ALTER operations. Use when user needs to create schema, modify structure, or drop database objects.
license: MIT
compatibility: Requires DbCli CLI tool (based on .NET 10 and SqlSugar). Supports Windows, Linux, macOS.
metadata:
  tool: dbcli
  version: "1.0.0"
  category: database
  safety-level: critical-requires-backup
  supported-databases: "30+"
allowed-tools: dbcli
---


## Command Style (Use PATH)

All examples use the plain command name `dbcli` (no directory prefix).
Ensure `dbcli` is on PATH instead of hardcoding paths like `.\.claude\skills\dbcli\dbcli.exe`.


# DbCli Database DDL Skill

Execute Data Definition Language (DDL) operations - CREATE, ALTER, DROP tables, indexes, and views.

## ⚠️ CRITICAL SAFETY REQUIREMENT

**MANDATORY BACKUPS BEFORE DROP/ALTER OPERATIONS**

- DROP TABLE: Export table data + create table copy
- ALTER TABLE: Export table schema + data
- DROP INDEX/VIEW: Document structure before dropping

## When to Use This Skill

- User wants to create tables, indexes, or views
- User needs to modify table structure (add/drop columns, change types)
- User wants to drop tables, indexes, or views
- User mentions CREATE, ALTER, DROP, schema, structure, or database design
- **Never DROP/ALTER without backups**

## Command Syntax

```bash
dbcli -c "CONNECTION_STRING" [-t DATABASE_TYPE] ddl "DDL_STATEMENT"
```

### Global Options

- `-c, --connection`: Database connection string (required)
- `-t, --db-type`: Database type (default: sqlite)

### Subcommand Options

- `-F, --file`: Execute DDL from file

Notes:

- SQL Server supports `GO` batch separators in DDL scripts (use `-F` and keep `GO` on its own line).

## CREATE Operations (Safe - No Backup Required)

### Create Table

```bash
# SQLite - Basic table
dbcli -c "Data Source=app.db" ddl "CREATE TABLE Users (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Email TEXT UNIQUE, CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"

# SQL Server
dbcli -c "Server=localhost;Database=mydb;Trusted_Connection=True" -t sqlserver ddl "CREATE TABLE Users (Id INT PRIMARY KEY IDENTITY(1,1), Name NVARCHAR(100) NOT NULL, Email NVARCHAR(255) UNIQUE, CreatedAt DATETIME DEFAULT GETDATE())"

# MySQL
dbcli -c "Server=localhost;Database=mydb;Uid=root;Pwd=xxxxxxxxxx" -t mysql ddl "CREATE TABLE Users (Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(100) NOT NULL, Email VARCHAR(255) UNIQUE, CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"

# PostgreSQL
dbcli -c "Host=localhost;Database=mydb;Username=postgres;Password=xxxxxxxxxx" -t postgresql ddl "CREATE TABLE Users (Id SERIAL PRIMARY KEY, Name VARCHAR(100) NOT NULL, Email VARCHAR(255) UNIQUE, CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
```

### Create Table with Foreign Key

```bash
dbcli -c "Data Source=app.db" ddl "CREATE TABLE Orders (Id INTEGER PRIMARY KEY AUTOINCREMENT, UserId INTEGER NOT NULL, Total REAL NOT NULL, OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (UserId) REFERENCES Users(Id))"
```

### Create Table from Query (Backup/Copy)

```bash
# Create backup table
dbcli -c "Data Source=app.db" ddl "CREATE TABLE Users_backup AS SELECT * FROM Users"

# Create filtered copy
dbcli -c "Data Source=app.db" ddl "CREATE TABLE ActiveUsers AS SELECT * FROM Users WHERE active = 1"
```

### Create Table if Not Exists

```bash
dbcli -c "Data Source=app.db" ddl "CREATE TABLE IF NOT EXISTS Settings (Key TEXT PRIMARY KEY, Value TEXT)"
```

### Create Index

```bash
# Single column index
dbcli -c "Data Source=app.db" ddl "CREATE INDEX idx_users_email ON Users(Email)"

# Multi-column index
dbcli -c "Data Source=app.db" ddl "CREATE INDEX idx_orders_user_date ON Orders(UserId, OrderDate)"

# Unique index
dbcli -c "Data Source=app.db" ddl "CREATE UNIQUE INDEX idx_users_username ON Users(Username)"
```

### Create View

```bash
# Simple view
dbcli -c "Data Source=app.db" ddl "CREATE VIEW ActiveUsers AS SELECT Id, Name, Email FROM Users WHERE active = 1"

# Complex view with JOIN
dbcli -c "Data Source=app.db" ddl "CREATE VIEW UserOrders AS SELECT u.Name, o.Id as OrderId, o.Total, o.OrderDate FROM Users u JOIN Orders o ON u.Id = o.UserId"
```

## DROP Operations (DANGEROUS - Requires Backup)

### Safe DROP TABLE Workflow

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# STEP 1: Export table schema (for reference)
dbcli -c "Data Source=app.db" -f table columns OldTable > OldTable_schema_${TIMESTAMP}.txt

# STEP 2: Export table data (SQL format)
dbcli -c "Data Source=app.db" export OldTable > OldTable_backup_${TIMESTAMP}.sql

# STEP 3: Create table copy (fastest recovery)
dbcli -c "Data Source=app.db" query "CREATE TABLE OldTable_copy_${TIMESTAMP} AS SELECT * FROM OldTable"

# STEP 4: Verify backup
dbcli -c "Data Source=app.db" query "SELECT COUNT(*) FROM OldTable"
dbcli -c "Data Source=app.db" query "SELECT COUNT(*) FROM OldTable_copy_${TIMESTAMP}"

# STEP 5: Drop table
dbcli -c "Data Source=app.db" ddl "DROP TABLE IF EXISTS OldTable"

echo "Table dropped. Backups: OldTable_backup_${TIMESTAMP}.sql, OldTable_copy_${TIMESTAMP}"
```

### Safe DROP INDEX

```bash
# Document index before dropping
dbcli -c "Data Source=app.db" query "SELECT sql FROM sqlite_master WHERE type='index' AND name='idx_old_index'" > idx_old_index_definition.sql

# Drop index
dbcli -c "Data Source=app.db" ddl "DROP INDEX IF EXISTS idx_old_index"
```

### Safe DROP VIEW

```bash
# Export view definition
dbcli -c "Data Source=app.db" query "SELECT sql FROM sqlite_master WHERE type='view' AND name='OldView'" > OldView_definition.sql

# Drop view
dbcli -c "Data Source=app.db" ddl "DROP VIEW IF EXISTS OldView"
```

## ALTER Operations (CRITICAL - Requires Backup)

### Safe ALTER TABLE Workflow

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# STEP 1: Full table backup (data + schema)
dbcli -c "Data Source=app.db" export Users > Users_backup_${TIMESTAMP}.sql
dbcli -c "Data Source=app.db" query "CREATE TABLE Users_copy_${TIMESTAMP} AS SELECT * FROM Users"

# STEP 2: Verify backup
dbcli -c "Data Source=app.db" query "SELECT COUNT(*) FROM Users"
dbcli -c "Data Source=app.db" query "SELECT COUNT(*) FROM Users_copy_${TIMESTAMP}"

# STEP 3: Execute ALTER
dbcli -c "Data Source=app.db" ddl "ALTER TABLE Users ADD COLUMN PhoneNumber TEXT"

# STEP 4: Verify structure
dbcli -c "Data Source=app.db" -f table columns Users
```

### ALTER TABLE - Add Column

```bash
# Backup first
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" export Users > Users_backup_${TIMESTAMP}.sql

# Add column
dbcli -c "Data Source=app.db" ddl "ALTER TABLE Users ADD COLUMN Age INTEGER"

# Add column with default
dbcli -c "Data Source=app.db" ddl "ALTER TABLE Users ADD COLUMN Status TEXT DEFAULT 'active'"
```

### ALTER TABLE - Drop Column

```bash
# CRITICAL: Full backup required
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" export Users > Users_backup_${TIMESTAMP}.sql
dbcli -c "Data Source=app.db" query "CREATE TABLE Users_copy_${TIMESTAMP} AS SELECT * FROM Users"

# Drop column (SQL Server syntax)
dbcli -c "Server=localhost;Database=mydb;Trusted_Connection=True" -t sqlserver ddl "ALTER TABLE Users DROP COLUMN TempColumn"
```

### ALTER TABLE - Rename Table

```bash
# Backup first
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" export OldName > OldName_backup_${TIMESTAMP}.sql

# Rename (SQLite syntax)
dbcli -c "Data Source=app.db" ddl "ALTER TABLE OldName RENAME TO NewName"

# Rename (SQL Server syntax)
dbcli -c "Server=localhost;Database=mydb;Trusted_Connection=True" -t sqlserver ddl "EXEC sp_rename 'OldName', 'NewName'"
```

### ALTER TABLE - Rename Column

```bash
# Backup first
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
dbcli -c "Data Source=app.db" export Users > Users_backup_${TIMESTAMP}.sql

# Rename column (SQLite 3.25+)
dbcli -c "Data Source=app.db" ddl "ALTER TABLE Users RENAME COLUMN OldColumnName TO NewColumnName"

# SQL Server
dbcli -c "Server=localhost;Database=mydb;Trusted_Connection=True" -t sqlserver ddl "EXEC sp_rename 'Users.OldColumnName', 'NewColumnName', 'COLUMN'"
```

## DDL from File

### Execute Schema File

```bash
# Create schema.sql
cat > schema.sql <<EOF
CREATE TABLE Users (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT UNIQUE,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Orders (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    UserId INTEGER NOT NULL,
    Total REAL NOT NULL,
    OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserId) REFERENCES Users(Id)
);

CREATE INDEX idx_users_email ON Users(Email);
CREATE INDEX idx_orders_user ON Orders(UserId);
EOF

# Execute schema
dbcli -c "Data Source=app.db" ddl -F schema.sql
```

### Migration Scripts

```bash
# migrations/001_create_users.sql
dbcli -c "Data Source=app.db" ddl -F migrations/001_create_users.sql

# migrations/002_add_orders.sql
dbcli -c "Data Source=app.db" ddl -F migrations/002_add_orders.sql

# migrations/003_add_indexes.sql
dbcli -c "Data Source=app.db" ddl -F migrations/003_add_indexes.sql
```

## Chinese Domestic Databases

### DaMeng (达梦)

```bash
# Create table
dbcli -c "Server=localhost;User Id=SYSDBA;PWD=xxxxxxxxxx;DATABASE=mydb" -t dm ddl "CREATE TABLE dm_test (id INT PRIMARY KEY, name VARCHAR(100), create_time TIMESTAMP)"

# Create index
dbcli -c "Server=localhost;User Id=SYSDBA;PWD=xxxxxxxxxx;DATABASE=mydb" -t dm ddl "CREATE INDEX idx_dm_test_name ON dm_test(name)"

# Create view
dbcli -c "Server=localhost;User Id=SYSDBA;PWD=xxxxxxxxxx;DATABASE=mydb" -t dm ddl "CREATE VIEW v_dm_test AS SELECT id, name FROM dm_test WHERE id > 0"
```

### GaussDB

```bash
# Create table with sequence
dbcli -c "Host=localhost;Port=8000;Database=mydb;Username=gaussdb;Password=xxxxxxxxxx" -t gaussdb ddl "CREATE TABLE gauss_test (id SERIAL PRIMARY KEY, name VARCHAR(100), amount DECIMAL(10,2))"

# Create index
dbcli -c "Host=localhost;Port=8000;Database=mydb;Username=gaussdb;Password=xxxxxxxxxx" -t gaussdb ddl "CREATE INDEX idx_gauss_test_name ON gauss_test(name)"

# Create function (PL/pgSQL)
dbcli -c "Host=localhost;Port=8000;Database=mydb;Username=gaussdb;Password=xxxxxxxxxx" -t gaussdb ddl "CREATE OR REPLACE FUNCTION get_total() RETURNS DECIMAL AS \$\$ BEGIN RETURN (SELECT SUM(amount) FROM gauss_test); END; \$\$ LANGUAGE plpgsql"
```

### KingbaseES (人大金仓)

```bash
# Create table
dbcli -c "Server=localhost;Port=54321;UID=system;PWD=xxxxxxxxxx;database=mydb" -t kdbndp ddl "CREATE TABLE kingbase_test (id SERIAL PRIMARY KEY, name VARCHAR(100), price NUMERIC(10,2))"

# Create view
dbcli -c "Server=localhost;Port=54321;UID=system;PWD=xxxxxxxxxx;database=mydb" -t kdbndp ddl "CREATE VIEW v_kingbase_active AS SELECT * FROM kingbase_test WHERE status = 1"
```

## Advanced DDL

### Composite Primary Key

```bash
dbcli -c "Data Source=app.db" ddl "CREATE TABLE UserRoles (UserId INTEGER NOT NULL, RoleId INTEGER NOT NULL, AssignedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (UserId, RoleId))"
```

### Check Constraints

```bash
dbcli -c "Data Source=app.db" ddl "CREATE TABLE Products (Id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Price REAL CHECK(Price > 0), Stock INTEGER CHECK(Stock >= 0))"
```

### Triggers (SQLite)

```bash
dbcli -c "Data Source=app.db" ddl "CREATE TRIGGER update_timestamp AFTER UPDATE ON Users BEGIN UPDATE Users SET UpdatedAt = datetime('now') WHERE Id = NEW.Id; END"
```

### Partial Index

```bash
dbcli -c "Data Source=app.db" ddl "CREATE INDEX idx_active_users ON Users(Email) WHERE active = 1"
```

## Backup Recovery for DDL

### Recover Dropped Table

```bash
# From table copy
dbcli -c "Data Source=app.db" ddl "CREATE TABLE Users AS SELECT * FROM Users_copy_20250127_143022"

# From SQL export
dbcli -c "Data Source=app.db" exec -F Users_backup_20250127_143022.sql
```

### Recover Dropped Index

```bash
# Re-create from saved definition
dbcli -c "Data Source=app.db" ddl -F idx_users_email_definition.sql
```

### Rollback ALTER TABLE

```bash
# Drop altered table
dbcli -c "Data Source=app.db" ddl "DROP TABLE Users"

# Restore from backup
dbcli -c "Data Source=app.db" ddl "CREATE TABLE Users AS SELECT * FROM Users_copy_20250127_143022"
```

## Schema Verification

### Check Table Exists

```bash
# SQLite
dbcli -c "Data Source=app.db" query "SELECT name FROM sqlite_master WHERE type='table' AND name='Users'"

# SQL Server
dbcli -c "Server=localhost;Database=mydb;Trusted_Connection=True" -t sqlserver query "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Users'"
```

### Check Column Exists

```bash
# SQLite
dbcli -c "Data Source=app.db" query "PRAGMA table_info(Users)"

# SQL Server
dbcli -c "Server=localhost;Database=mydb;Trusted_Connection=True" -t sqlserver query "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Users' AND COLUMN_NAME = 'Email'"
```

### Check Index Exists

```bash
# SQLite
dbcli -c "Data Source=app.db" query "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='Users' AND name='idx_users_email'"
```

## Common Patterns

### Idempotent DDL (Safe Re-run)

```bash
# Drop if exists, then create
dbcli -c "Data Source=app.db" ddl "DROP TABLE IF EXISTS TempTable"
dbcli -c "Data Source=app.db" ddl "CREATE TABLE TempTable (Id INTEGER PRIMARY KEY, Data TEXT)"

# Create if not exists
dbcli -c "Data Source=app.db" ddl "CREATE TABLE IF NOT EXISTS Settings (Key TEXT PRIMARY KEY, Value TEXT)"
```

### Database Initialization

```bash
#!/bin/bash
# init_db.sh

CONNECTION="Data Source=app.db"

# Create tables
dbcli -c "$CONNECTION" ddl -F schema/001_users.sql
dbcli -c "$CONNECTION" ddl -F schema/002_orders.sql
dbcli -c "$CONNECTION" ddl -F schema/003_products.sql

# Create indexes
dbcli -c "$CONNECTION" ddl -F schema/004_indexes.sql

# Create views
dbcli -c "$CONNECTION" ddl -F schema/005_views.sql

echo "Database initialized"
```

### Schema Migration

```bash
#!/bin/bash
# migrate.sh

CONNECTION="Data Source=app.db"
BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup entire database
cp app.db "${BACKUP_DIR}/app_${TIMESTAMP}.db"

# Run migrations
for migration in migrations/*.sql; do
    echo "Running $migration..."
    dbcli -c "$CONNECTION" ddl -F "$migration"
    if [ $? -ne 0 ]; then
        echo "Migration failed: $migration"
        echo "Restoring from backup..."
        cp "${BACKUP_DIR}/app_${TIMESTAMP}.db" app.db
        exit 1
    fi
done

echo "All migrations completed successfully"
```

## Security Best Practices

1. **Always backup before DROP/ALTER** - Cannot emphasize enough
2. **Test DDL on backup database** first
3. **Use transactions** for multiple DDL operations when supported
4. **Document schema changes** with timestamps and reasons
5. **Version control** all DDL scripts
6. **Limit DDL permissions** to admin users only
7. **Review constraints** before adding (can block future inserts)
