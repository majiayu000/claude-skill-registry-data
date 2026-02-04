---
name: sql-server-admin
description: SQL Server administration and maintenance. Use for database backups, security, user management, maintenance tasks, monitoring, and troubleshooting.
allowed-tools: Bash, Read, Grep
---

# SQL Server Administration Skill

Expert knowledge for SQL Server database administration, maintenance, security, and operational tasks.

## Database Management

### Create Database

```sql
CREATE DATABASE MyDatabase
ON PRIMARY (
    NAME = 'MyDatabase_Data',
    FILENAME = '/var/opt/mssql/data/MyDatabase.mdf',
    SIZE = 100MB,
    MAXSIZE = 1GB,
    FILEGROWTH = 10MB
)
LOG ON (
    NAME = 'MyDatabase_Log',
    FILENAME = '/var/opt/mssql/data/MyDatabase_log.ldf',
    SIZE = 50MB,
    MAXSIZE = 500MB,
    FILEGROWTH = 5MB
);
```

### Alter Database

```sql
-- Change database name
ALTER DATABASE OldName MODIFY NAME = NewName;

-- Set recovery model
ALTER DATABASE MyDatabase SET RECOVERY FULL;
-- Options: SIMPLE, FULL, BULK_LOGGED

-- Set to single-user mode
ALTER DATABASE MyDatabase SET SINGLE_USER WITH ROLLBACK IMMEDIATE;

-- Set back to multi-user
ALTER DATABASE MyDatabase SET MULTI_USER;

-- Enable snapshot isolation
ALTER DATABASE MyDatabase SET ALLOW_SNAPSHOT_ISOLATION ON;
```

### Drop Database

```sql
-- Drop database (must not be in use)
DROP DATABASE MyDatabase;

-- Force drop (disconnect users first)
ALTER DATABASE MyDatabase SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
DROP DATABASE MyDatabase;
```

### Database Information

```sql
-- List all databases
SELECT
    name,
    database_id,
    create_date,
    state_desc,
    recovery_model_desc
FROM sys.databases
ORDER BY name;

-- Database size
EXEC sp_spaceused;

-- Database file information
SELECT
    name,
    physical_name,
    size * 8 / 1024 AS SizeMB,
    max_size
FROM sys.database_files;
```

## Backup and Restore

### Full Backup

```sql
-- Full database backup
BACKUP DATABASE MyDatabase
TO DISK = '/var/opt/mssql/backup/MyDatabase_Full.bak'
WITH FORMAT, COMPRESSION, STATS = 10;

-- Full backup with name and description
BACKUP DATABASE MyDatabase
TO DISK = '/var/opt/mssql/backup/MyDatabase_Full_20241220.bak'
WITH
    FORMAT,
    COMPRESSION,
    NAME = 'MyDatabase Full Backup',
    DESCRIPTION = 'Full backup performed on 2024-12-20',
    STATS = 10;
```

### Differential Backup

```sql
-- Differential backup (changes since last full backup)
BACKUP DATABASE MyDatabase
TO DISK = '/var/opt/mssql/backup/MyDatabase_Diff.bak'
WITH DIFFERENTIAL, FORMAT, COMPRESSION;
```

### Transaction Log Backup

```sql
-- Transaction log backup (requires FULL recovery model)
BACKUP LOG MyDatabase
TO DISK = '/var/opt/mssql/backup/MyDatabase_Log.trn'
WITH FORMAT, COMPRESSION;
```

### Restore Database

```sql
-- View backup file contents
RESTORE FILELISTONLY
FROM DISK = '/var/opt/mssql/backup/MyDatabase_Full.bak';

-- Restore with replace
RESTORE DATABASE MyDatabase
FROM DISK = '/var/opt/mssql/backup/MyDatabase_Full.bak'
WITH REPLACE,
    MOVE 'MyDatabase_Data' TO '/var/opt/mssql/data/MyDatabase.mdf',
    MOVE 'MyDatabase_Log' TO '/var/opt/mssql/data/MyDatabase_log.ldf';

-- Restore to different database name
RESTORE DATABASE MyDatabase_Copy
FROM DISK = '/var/opt/mssql/backup/MyDatabase_Full.bak'
WITH
    MOVE 'MyDatabase_Data' TO '/var/opt/mssql/data/MyDatabase_Copy.mdf',
    MOVE 'MyDatabase_Log' TO '/var/opt/mssql/data/MyDatabase_Copy_log.ldf';

-- Restore with recovery/norecovery
RESTORE DATABASE MyDatabase
FROM DISK = '/var/opt/mssql/backup/MyDatabase_Full.bak'
WITH NORECOVERY;  -- To apply more backups (diff/log)

-- Apply differential backup
RESTORE DATABASE MyDatabase
FROM DISK = '/var/opt/mssql/backup/MyDatabase_Diff.bak'
WITH NORECOVERY;

-- Apply log backup and bring online
RESTORE LOG MyDatabase
FROM DISK = '/var/opt/mssql/backup/MyDatabase_Log.trn'
WITH RECOVERY;  -- Brings database online
```

### Point-in-Time Restore

```sql
-- Restore to specific point in time
RESTORE DATABASE MyDatabase
FROM DISK = '/var/opt/mssql/backup/MyDatabase_Full.bak'
WITH NORECOVERY;

RESTORE LOG MyDatabase
FROM DISK = '/var/opt/mssql/backup/MyDatabase_Log.trn'
WITH STOPAT = '2024-12-20 14:30:00', RECOVERY;
```

## User and Security Management

### Create Login

```sql
-- SQL Server authentication
CREATE LOGIN john_doe
WITH PASSWORD = 'StrongP@ssw0rd!';

-- Windows authentication
CREATE LOGIN [DOMAIN\username]
FROM WINDOWS;
```

### Create User

```sql
-- Create database user from login
USE MyDatabase;
CREATE USER john_doe FOR LOGIN john_doe;

-- Create user without login (for contained databases)
CREATE USER app_user WITH PASSWORD = 'StrongP@ssw0rd!';
```

### Grant Permissions

```sql
-- Grant database role membership
ALTER ROLE db_datareader ADD MEMBER john_doe;
ALTER ROLE db_datawriter ADD MEMBER john_doe;

-- Grant specific permissions
GRANT SELECT, INSERT, UPDATE ON dbo.Orders TO john_doe;
GRANT EXECUTE ON dbo.GetCustomerOrders TO john_doe;

-- Grant schema permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::Sales TO john_doe;

-- Grant database-level permissions
GRANT CREATE TABLE TO john_doe;
GRANT VIEW DATABASE STATE TO monitoring_user;
```

### Revoke Permissions

```sql
REVOKE SELECT ON dbo.Orders FROM john_doe;
REVOKE EXECUTE ON dbo.GetCustomerOrders FROM john_doe;
```

### Deny Permissions

```sql
-- Explicitly deny (overrides grants)
DENY DELETE ON dbo.Customers TO john_doe;
```

### Database Roles

```sql
-- Create custom role
CREATE ROLE SalesTeam;

-- Grant permissions to role
GRANT SELECT, INSERT, UPDATE ON SCHEMA::Sales TO SalesTeam;

-- Add users to role
ALTER ROLE SalesTeam ADD MEMBER john_doe;

-- Built-in database roles:
-- db_owner       - Full control
-- db_datareader  - SELECT on all tables
-- db_datawriter  - INSERT, UPDATE, DELETE on all tables
-- db_ddladmin    - CREATE, ALTER, DROP objects
-- db_backupoperator - Backup operations
```

### View Permissions

```sql
-- User's permissions
SELECT * FROM fn_my_permissions(NULL, 'DATABASE');

-- Specific user's permissions
EXECUTE AS USER = 'john_doe';
SELECT * FROM fn_my_permissions(NULL, 'DATABASE');
REVERT;

-- User's role memberships
SELECT
    USER_NAME(rm.member_principal_id) AS UserName,
    USER_NAME(rm.role_principal_id) AS RoleName
FROM sys.database_role_members rm;
```

## Index Maintenance

### Check Index Fragmentation

```sql
SELECT
    OBJECT_NAME(ips.object_id) AS TableName,
    i.name AS IndexName,
    ips.index_type_desc,
    ips.avg_fragmentation_in_percent,
    ips.page_count,
    CASE
        WHEN ips.avg_fragmentation_in_percent < 10 THEN 'No action needed'
        WHEN ips.avg_fragmentation_in_percent < 30 THEN 'Reorganize'
        ELSE 'Rebuild'
    END AS Recommendation
FROM sys.dm_db_index_physical_stats(
    DB_ID(), NULL, NULL, NULL, 'LIMITED'
) ips
INNER JOIN sys.indexes i
    ON ips.object_id = i.object_id
    AND ips.index_id = i.index_id
WHERE ips.page_count > 1000  -- Only indexes with significant pages
ORDER BY ips.avg_fragmentation_in_percent DESC;
```

### Rebuild Indexes

```sql
-- Rebuild single index
ALTER INDEX IX_Orders_CustomerId ON Orders REBUILD;

-- Rebuild all indexes on table
ALTER INDEX ALL ON Orders REBUILD;

-- Rebuild with options
ALTER INDEX IX_Orders_CustomerId ON Orders
REBUILD WITH (
    ONLINE = ON,          -- Enterprise Edition only
    MAXDOP = 4,           -- Parallel processing
    SORT_IN_TEMPDB = ON   -- Use tempdb for sorting
);
```

### Reorganize Indexes

```sql
-- Reorganize index (online operation)
ALTER INDEX IX_Orders_CustomerId ON Orders REORGANIZE;

-- Reorganize with LOB compaction
ALTER INDEX IX_Orders_CustomerId ON Orders
REORGANIZE WITH (LOB_COMPACTION = ON);
```

### Update Statistics

```sql
-- Update statistics for table
UPDATE STATISTICS Orders;

-- Update with full scan
UPDATE STATISTICS Orders WITH FULLSCAN;

-- Update specific index statistics
UPDATE STATISTICS Orders IX_Orders_CustomerId WITH FULLSCAN;

-- Update all statistics in database
EXEC sp_updatestats;
```

### Maintenance Plan Script

```sql
-- Comprehensive maintenance script
DECLARE @SQL NVARCHAR(MAX);

-- Rebuild fragmented indexes (>30%)
DECLARE index_cursor CURSOR FOR
SELECT
    'ALTER INDEX ' + QUOTENAME(i.name) +
    ' ON ' + QUOTENAME(OBJECT_SCHEMA_NAME(i.object_id)) + '.' + QUOTENAME(OBJECT_NAME(i.object_id)) +
    ' REBUILD;'
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ips
INNER JOIN sys.indexes i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
WHERE ips.avg_fragmentation_in_percent > 30
    AND ips.page_count > 1000
    AND i.name IS NOT NULL;

OPEN index_cursor;
FETCH NEXT FROM index_cursor INTO @SQL;

WHILE @@FETCH_STATUS = 0
BEGIN
    PRINT @SQL;
    EXEC sp_executesql @SQL;
    FETCH NEXT FROM index_cursor INTO @SQL;
END;

CLOSE index_cursor;
DEALLOCATE index_cursor;

-- Update statistics
EXEC sp_updatestats;
```

## Monitoring and Performance

### Active Sessions

```sql
SELECT
    session_id,
    login_name,
    host_name,
    program_name,
    status,
    cpu_time,
    total_elapsed_time / 1000 AS elapsed_seconds,
    reads,
    writes,
    last_request_start_time
FROM sys.dm_exec_sessions
WHERE is_user_process = 1
ORDER BY cpu_time DESC;
```

### Currently Running Queries

```sql
SELECT
    r.session_id,
    r.status,
    r.command,
    r.cpu_time,
    r.total_elapsed_time / 1000 AS elapsed_seconds,
    r.reads,
    r.writes,
    r.blocking_session_id,
    SUBSTRING(qt.text, (r.statement_start_offset/2)+1,
        ((CASE r.statement_end_offset
            WHEN -1 THEN DATALENGTH(qt.text)
            ELSE r.statement_end_offset
        END - r.statement_start_offset)/2) + 1) AS query_text
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) qt
WHERE r.session_id <> @@SPID  -- Exclude current session
ORDER BY r.total_elapsed_time DESC;
```

### Blocking

```sql
-- Find blocking chains
SELECT
    blocked.session_id AS blocked_session_id,
    blocked_sql.text AS blocked_query,
    blocker.session_id AS blocker_session_id,
    blocker_sql.text AS blocker_query,
    waits.wait_type,
    waits.wait_time_ms
FROM sys.dm_exec_requests blocked
INNER JOIN sys.dm_exec_requests blocker
    ON blocked.blocking_session_id = blocker.session_id
CROSS APPLY sys.dm_exec_sql_text(blocked.sql_handle) blocked_sql
CROSS APPLY sys.dm_exec_sql_text(blocker.sql_handle) blocker_sql
LEFT JOIN sys.dm_os_waiting_tasks waits
    ON blocked.session_id = waits.session_id;
```

### Kill Session

```sql
-- Kill blocking session
KILL 53;  -- session_id

-- Kill with rollback status
KILL 53 WITH STATUSONLY;
```

### Wait Statistics

```sql
SELECT TOP 20
    wait_type,
    wait_time_ms / 1000 AS wait_time_seconds,
    (wait_time_ms * 100.0) / SUM(wait_time_ms) OVER() AS percentage,
    waiting_tasks_count
FROM sys.dm_os_wait_stats
WHERE wait_type NOT IN (
    -- Filter out benign waits
    'CLR_SEMAPHORE', 'LAZYWRITER_SLEEP', 'RESOURCE_QUEUE',
    'SLEEP_TASK', 'SLEEP_SYSTEMTASK', 'SQLTRACE_BUFFER_FLUSH',
    'WAITFOR', 'LOGMGR_QUEUE', 'CHECKPOINT_QUEUE',
    'REQUEST_FOR_DEADLOCK_SEARCH', 'XE_TIMER_EVENT', 'BROKER_TO_FLUSH',
    'BROKER_TASK_STOP', 'CLR_MANUAL_EVENT', 'CLR_AUTO_EVENT',
    'DISPATCHER_QUEUE_SEMAPHORE', 'FT_IFTS_SCHEDULER_IDLE_WAIT',
    'XE_DISPATCHER_WAIT', 'XE_DISPATCHER_JOIN', 'SQLTRACE_INCREMENTAL_FLUSH_SLEEP'
)
ORDER BY wait_time_ms DESC;
```

### Database Size Growth

```sql
SELECT
    DB_NAME() AS database_name,
    name AS file_name,
    type_desc,
    physical_name,
    size * 8 / 1024 AS size_mb,
    (size * 8 / 1024) - (FILEPROPERTY(name, 'SpaceUsed') * 8 / 1024) AS free_space_mb,
    CAST((FILEPROPERTY(name, 'SpaceUsed') * 100.0 / size) AS DECIMAL(5,2)) AS percent_used
FROM sys.database_files;
```

## Troubleshooting

### Check Error Log

```sql
-- Read SQL Server error log
EXEC sp_readerrorlog;

-- Read specific error log
EXEC sp_readerrorlog 0;  -- Current log
EXEC sp_readerrorlog 1;  -- Previous log

-- Search for specific text
EXEC sp_readerrorlog 0, 1, N'error';
```

### Deadlocks

```sql
-- Enable trace flag for deadlock capture
DBCC TRACEON(1222, -1);  -- Global

-- Read captured deadlocks from error log
EXEC sp_readerrorlog 0, 1, N'deadlock';

-- Turn off trace flag
DBCC TRACEOFF(1222, -1);
```

### DBCC Commands

```sql
-- Check database integrity
DBCC CHECKDB('MyDatabase') WITH NO_INFOMSGS;

-- Check specific table
DBCC CHECKTABLE('Orders') WITH NO_INFOMSGS;

-- Update usage stats
DBCC UPDATEUSAGE('MyDatabase');

-- Free procedure cache
DBCC FREEPROCCACHE;

-- Clear wait stats (useful after solving issues)
DBCC SQLPERF('sys.dm_os_wait_stats', CLEAR);

-- Shrink database (avoid in production!)
DBCC SHRINKDATABASE('MyDatabase', 10);  -- 10% free space

-- Shrink file
DBCC SHRINKFILE('MyDatabase_Log', 50);  -- MB
```

## sqlcmd Usage

### Connect to SQL Server

```bash
# Connect with SQL authentication
sqlcmd -S localhost -U sa -P 'YourPassword'

# Connect with Windows authentication (if supported)
sqlcmd -S localhost -E

# Connect to specific database
sqlcmd -S localhost -U sa -P 'YourPassword' -d MyDatabase

# Execute query from command line
sqlcmd -S localhost -U sa -P 'YourPassword' -Q "SELECT @@VERSION"

# Execute script file
sqlcmd -S localhost -U sa -P 'YourPassword' -i script.sql

# Output to file
sqlcmd -S localhost -U sa -P 'YourPassword' -Q "SELECT * FROM Users" -o output.txt

# Use variable
sqlcmd -S localhost -U sa -P 'YourPassword' -v MyVar=Value -i script.sql
```

### sqlcmd Commands

Within sqlcmd session:
```sql
-- List databases
SELECT name FROM sys.databases;
GO

-- Change database
USE MyDatabase;
GO

-- Execute script
:r script.sql

-- Set variable
:setvar MyVar "MyValue"
SELECT '$(MyVar)';
GO

-- Quit
EXIT
-- or
QUIT
```

## Useful Queries

### Table Sizes

```sql
SELECT
    OBJECT_SCHEMA_NAME(p.object_id) AS SchemaName,
    OBJECT_NAME(p.object_id) AS TableName,
    SUM(a.total_pages) * 8 / 1024 AS TotalSpaceMB,
    SUM(a.used_pages) * 8 / 1024 AS UsedSpaceMB,
    (SUM(a.total_pages) - SUM(a.used_pages)) * 8 / 1024 AS UnusedSpaceMB,
    SUM(p.rows) AS RowCount
FROM sys.partitions p
INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
WHERE OBJECT_SCHEMA_NAME(p.object_id) <> 'sys'
GROUP BY p.object_id
ORDER BY TotalSpaceMB DESC;
```

### Index Usage

```sql
SELECT
    OBJECT_NAME(s.object_id) AS TableName,
    i.name AS IndexName,
    s.user_seeks,
    s.user_scans,
    s.user_lookups,
    s.user_updates,
    s.last_user_seek,
    s.last_user_scan
FROM sys.dm_db_index_usage_stats s
INNER JOIN sys.indexes i ON s.object_id = i.object_id AND s.index_id = i.index_id
WHERE database_id = DB_ID()
    AND OBJECTPROPERTY(s.object_id, 'IsUserTable') = 1
ORDER BY s.user_seeks + s.user_scans + s.user_lookups DESC;
```

## When to Use This Skill

Use this skill when:
- Managing databases (create, backup, restore)
- Setting up security and users
- Performing maintenance tasks
- Troubleshooting performance issues
- Monitoring database health
- Using sqlcmd for database operations
- Managing indexes and statistics

Simply mention database administration, maintenance, backups, users, or monitoring, and this knowledge will be applied.
