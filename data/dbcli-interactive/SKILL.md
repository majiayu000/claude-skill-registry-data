---
name: dbcli-interactive
description: Interactive SQL mode for 30+ databases using DbCli. Provides REPL environment for exploratory queries, rapid prototyping, and database administration. Includes safety prompts before dangerous operations (UPDATE/DELETE/DROP). Use when user wants interactive database session.
license: MIT
compatibility: Requires DbCli CLI tool (based on .NET 10 and SqlSugar). Supports Windows, Linux, macOS.
metadata:
  tool: dbcli
  version: "1.0.0"
  category: database
  mode: interactive-repl
  safety-prompts: enabled
  supported-databases: "30+"
allowed-tools: dbcli
---


## Command Style (Use PATH)

All examples use the plain command name `dbcli` (no directory prefix).
Ensure `dbcli` is on PATH instead of hardcoding paths like `.\.claude\skills\dbcli\dbcli.exe`.


# DbCli Interactive Skill

Interactive SQL mode (REPL) for database exploration and administration with built-in safety prompts.

## When to Use This Skill

- User wants to explore database interactively
- User needs to run multiple ad-hoc queries
- User prefers REPL environment over one-off commands
- User wants to prototype SQL statements
- User needs database administration session
- Learning/teaching SQL on real databases

## ⚠️ Safety Features

Interactive mode includes:
- **Safety prompts** before UPDATE/DELETE/DROP operations
- **Automatic backup suggestions** for dangerous operations
- **Query preview** before execution
- **Confirmation dialogs** for destructive commands
- **Transaction rollback** support (where available)

## Command Syntax

```bash
dbcli -c "CONNECTION_STRING" [-t DATABASE_TYPE] interactive
```

### Aliases

```bash
dbcli -c "CONNECTION_STRING" i          # Short form
dbcli -c "CONNECTION_STRING" -i         # Alternative
```

## Global Options

- `-c, --connection`: Database connection string (required)
- `-t, --db-type`: Database type (default: sqlite)

## Starting Interactive Mode

### Basic Usage

```bash
# SQLite
dbcli -c "Data Source=app.db" interactive

# Welcome to DbCli Interactive Mode
# Type .help for commands, .exit to quit
# dbcli>
```

### Different Databases

```bash
# SQL Server
dbcli -c "Server=localhost;Database=mydb;Trusted_Connection=True" -t sqlserver interactive

# MySQL
dbcli -c "Server=localhost;Database=mydb;Uid=root;Pwd=xxxxxxxxxx" -t mysql interactive

# PostgreSQL
dbcli -c "Host=localhost;Database=mydb;Username=postgres;Password=xxxxxxxxxx" -t postgresql interactive

# DaMeng (达梦)
dbcli -c "Server=localhost;User Id=SYSDBA;PWD=xxxxxxxxxx;DATABASE=mydb" -t dm interactive

# GaussDB
dbcli -c "Host=localhost;Port=8000;Database=mydb;Username=gaussdb;Password=xxxxxxxxxx" -t gaussdb interactive
```

## Interactive Commands

### Meta Commands (Dot Commands)

```
.help                 - Show help message
.tables               - List all tables
.columns <table>      - Show table structure
.format <type>        - Change output format (json/table/csv)
.exit / .quit         - Exit interactive mode
.clear                - Clear screen
.history              - Show command history
```

### SQL Execution

```sql
dbcli> SELECT * FROM Users LIMIT 5;
-- Results displayed immediately

dbcli> SELECT COUNT(*) as user_count FROM Users;
-- Returns: { "user_count": 42 }
```

## Interactive Session Examples

### Exploration Session

```bash
$ dbcli -c "Data Source=app.db" interactive

dbcli> .tables
Users
Orders
Products

dbcli> .columns Users
ColumnName | DataType | IsNullable | IsPrimaryKey
-------------------------------------------------------
Id         | INTEGER  | False      | True
Name       | TEXT     | False      | False
Email      | TEXT     | True       | False
CreatedAt  | TIMESTAMP| True       | False

dbcli> SELECT * FROM Users LIMIT 3;
+----+-------+-------------------+
| Id | Name  | Email             |
+----+-------+-------------------+
| 1  | Alice | alice@example.com |
| 2  | Bob   | bob@example.com   |
| 3  | Carol | carol@example.com |
+----+-------+-------------------+

dbcli> .format json
Output format changed to: json

dbcli> SELECT Name, Email FROM Users WHERE Id = 1;
[{"Name":"Alice","Email":"alice@example.com"}]

dbcli> .exit
Goodbye!
```

### Data Analysis Session

```bash
dbcli> -- Check total records
dbcli> SELECT COUNT(*) as total FROM Orders;
{"total": 1547}

dbcli> -- Find top customers
dbcli> SELECT CustomerId, COUNT(*) as order_count, SUM(Total) as total_spent
       FROM Orders
       GROUP BY CustomerId
       ORDER BY total_spent DESC
       LIMIT 5;

+------------+-------------+-------------+
| CustomerId | order_count | total_spent |
+------------+-------------+-------------+
| 42         | 23          | 15420.50    |
| 17         | 19          | 12350.00    |
...

dbcli> -- Analyze by month
dbcli> SELECT strftime('%Y-%m', OrderDate) as month,
       COUNT(*) as orders,
       SUM(Total) as revenue
       FROM Orders
       GROUP BY month
       ORDER BY month DESC
       LIMIT 6;
```

## Safety Prompts for Dangerous Operations

### UPDATE with Safety Prompt

```bash
dbcli> UPDATE Users SET status = 'verified' WHERE email_confirmed = 1;

⚠️  WARNING: UPDATE operation detected
This will modify records in table: Users

Preview affected records? (yes/no): yes

Records to be updated:
+----+--------+----------------------+
| Id | Name   | Email                |
+----+--------+----------------------+
| 5  | John   | john@example.com     |
| 8  | Sarah  | sarah@example.com    |
+----+--------+----------------------+

Estimated affected records: 2

Recommended actions:
  1. Create backup: .export Users Users_backup_20250127_143022.sql
  2. Create table copy: CREATE TABLE Users_copy_20250127_143022 AS SELECT * FROM Users

Create automatic backup before UPDATE? (yes/no): yes

Creating backup: Users_backup_20250127_143022.sql... Done.

Proceed with UPDATE? (yes/no): yes

Executing UPDATE...
Updated 2 rows.
Backup saved: Users_backup_20250127_143022.sql
```

### DELETE with Safety Prompt

```bash
dbcli> DELETE FROM Orders WHERE status = 'cancelled' AND created_at < date('now', '-365 days');

⚠️  DANGER: DELETE operation detected
This will permanently remove records from table: Orders

Preview records to be deleted? (yes/no): yes

Records to be deleted:
+----+-----------+------------+
| Id | Status    | CreatedAt  |
+----+-----------+------------+
| 23 | cancelled | 2023-05-10 |
| 45 | cancelled | 2023-08-22 |
...
+----+-----------+------------+

Estimated affected records: 37

⚠️  This operation CANNOT BE UNDONE without backup!

Create automatic backup before DELETE? (yes/no): yes

Creating backup: Orders_backup_20250127_143022.sql... Done.

Type 'DELETE' to confirm deletion: DELETE

Executing DELETE...
Deleted 37 rows.
Backup saved: Orders_backup_20250127_143022.sql
```

### DROP TABLE with Critical Warning

```bash
dbcli> DROP TABLE TempData;

🛑 CRITICAL WARNING: DROP TABLE operation detected
This will PERMANENTLY DESTROY table: TempData

Table information:
  - Records: 1,245
  - Columns: 7
  - Indexes: 2
  - Size: ~450 KB

This operation is IRREVERSIBLE!

Recommended actions:
  1. Export data: .export TempData TempData_backup.sql
  2. Export schema: .columns TempData > TempData_schema.txt
  3. Create table copy: CREATE TABLE TempData_copy AS SELECT * FROM TempData

Create complete backup (data + schema)? (yes/no): yes

Creating backups...
  ✓ Data exported: TempData_backup_20250127_143022.sql
  ✓ Schema saved: TempData_schema_20250127_143022.txt
  ✓ Table copy created: TempData_copy_20250127_143022

Type 'DROP TABLE TempData' exactly to confirm: DROP TABLE TempData

Executing DROP TABLE...
Table 'TempData' has been dropped.
Recovery files available in: backups/
```

## Special Interactive Features

### Auto-Completion (Planned)

```bash
dbcli> SELECT * FROM Us<TAB>
-- Auto-completes to: SELECT * FROM Users

dbcli> SELECT Na<TAB>, Em<TAB> FROM Users
-- Auto-completes column names
```

### Command History

```bash
dbcli> .history
1. SELECT * FROM Users LIMIT 5
2. .tables
3. .columns Orders
4. SELECT COUNT(*) FROM Orders
5. UPDATE Users SET status = 'active'

dbcli> !3
-- Re-executes: .columns Orders
```

### Multi-Line Queries

```sql
dbcli> SELECT u.Name,
...>        o.OrderDate,
...>        o.Total
...>  FROM Users u
...>  JOIN Orders o ON u.Id = o.UserId
...>  WHERE o.Total > 100
...>  ORDER BY o.OrderDate DESC;
-- (Press Enter on empty line or end with ';' to execute)
```

### Transaction Support

```bash
dbcli> BEGIN TRANSACTION;
Transaction started.

dbcli> UPDATE Users SET balance = balance - 100 WHERE Id = 5;
Updated 1 row.

dbcli> UPDATE Users SET balance = balance + 100 WHERE Id = 8;
Updated 1 row.

dbcli> -- Check balances
dbcli> SELECT Id, Name, balance FROM Users WHERE Id IN (5, 8);
+----+-------+---------+
| Id | Name  | balance |
+----+-------+---------+
| 5  | Alice | 400     |
| 8  | Bob   | 600     |
+----+-------+---------+

dbcli> COMMIT;
Transaction committed.

-- Or rollback if something wrong:
dbcli> ROLLBACK;
Transaction rolled back.
```

## Configuration in Interactive Mode

### Set Output Format

```bash
dbcli> .format table
Output format: table

dbcli> SELECT * FROM Users LIMIT 2;
+----+-------+-------------------+
| Id | Name  | Email             |
+----+-------+-------------------+
...

dbcli> .format json
Output format: json

dbcli> SELECT * FROM Users LIMIT 2;
[{"Id":1,"Name":"Alice","Email":"alice@example.com"}...]

dbcli> .format csv
Output format: csv

dbcli> SELECT * FROM Users LIMIT 2;
Id,Name,Email
1,Alice,alice@example.com
```

### Session Variables (Future Feature)

```bash
dbcli> .set safety_prompts on
Safety prompts enabled

dbcli> .set auto_backup on
Auto-backup before dangerous operations: enabled

dbcli> .set
Current settings:
  safety_prompts: on
  auto_backup: on
  output_format: table
  max_rows: 100
```

## Use Cases

### 1. Database Development

```bash
# Test query iterations
dbcli> SELECT * FROM Products WHERE price > 100;
-- Review results

dbcli> SELECT * FROM Products WHERE price > 100 AND stock > 0;
-- Refine query

dbcli> SELECT name, price, stock FROM Products WHERE price > 100 AND stock > 0 ORDER BY price;
-- Final query for application
```

### 2. Data Cleanup

```bash
# Find duplicates
dbcli> SELECT email, COUNT(*) as count
       FROM Users
       GROUP BY email
       HAVING count > 1;

# Review duplicate records
dbcli> SELECT * FROM Users WHERE email = 'duplicate@example.com';

# Remove duplicates (with safety prompt)
dbcli> DELETE FROM Users WHERE Id IN (SELECT MAX(Id) FROM Users GROUP BY email HAVING COUNT(*) > 1);
⚠️  Safety prompt triggered...
```

### 3. Database Migration Testing

```bash
# Test migration script step by step
dbcli> BEGIN TRANSACTION;

dbcli> ALTER TABLE Users ADD COLUMN age INTEGER;

dbcli> .columns Users
-- Verify new column added

dbcli> UPDATE Users SET age = 25 WHERE Id = 1;
-- Test update

dbcli> SELECT * FROM Users WHERE Id = 1;
-- Verify data

dbcli> COMMIT;
-- Or ROLLBACK if issues found
```

### 4. Quick Data Inspection

```bash
# Explore unfamiliar database
dbcli> .tables
-- See what tables exist

dbcli> .columns Users
-- Check structure

dbcli> SELECT * FROM Users LIMIT 3;
-- Sample data

dbcli> SELECT COUNT(*) FROM Users;
-- Record count
```

## Scripting with Interactive Mode

### Pipe SQL from File

```bash
# Execute script in interactive mode
cat migration.sql | dbcli -c "Data Source=app.db" interactive
```

### Heredoc Script

```bash
dbcli -c "Data Source=app.db" interactive <<EOF
.format table
.tables
SELECT COUNT(*) FROM Users;
SELECT * FROM Users LIMIT 5;
.exit
EOF
```

## Best Practices

1. **Enable safety prompts** - Never disable for production databases
2. **Use transactions** - Wrap multiple updates in BEGIN/COMMIT
3. **Test on backup first** - Clone database for dangerous operations
4. **Keep command history** - Reference previous successful queries
5. **Use .format table** for review, json for programmatic use
6. **Create backups** before DELETE/UPDATE/DROP
7. **Exit cleanly** with .exit (ensures connection cleanup)

## Keyboard Shortcuts (Future)

```
Ctrl+C        - Cancel current query
Ctrl+D        - Exit interactive mode
Ctrl+L        - Clear screen
Up/Down       - Navigate command history
Tab           - Auto-complete table/column names
Ctrl+R        - Reverse search history
```

## Integration with Other Skills

Interactive mode can call other skills internally:

```bash
dbcli> .export Users
-- Internally calls: dbcli export Users

dbcli> .import backup.sql
-- Internally calls: dbcli exec -F backup.sql
```

## Exit Codes

```
0  - Normal exit
1  - Connection error
2  - Syntax error in SQL
3  - User cancelled dangerous operation
```

## Comparison with Other Skills

| Feature | Interactive | One-Off Commands |
|---------|-------------|------------------|
| Speed for single query | Slower (startup overhead) | Faster |
| Multiple queries | Much faster | Slower (reconnect each time) |
| Exploration | Excellent | Poor |
| Safety prompts | Built-in | Manual |
| Automation | Limited | Excellent |
| Learning curve | Low | Medium |

**Use interactive mode when**: Exploring, testing, multiple queries
**Use one-off commands when**: Automation, scripts, single operations
