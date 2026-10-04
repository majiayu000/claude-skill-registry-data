---
name: mssql-expert
description: 'MS SQL Server expert for writing optimized queries, selecting appropriate data types, and leveraging core SQL Server features. Use for: query optimization, performance tuning, T-SQL development, schema design, index strategy, stored procedures, functions, and advanced SQL Server features.'
argument-hint: 'Describe the SQL Server task (e.g., optimize query, design schema, write stored procedure)'
---

# MS SQL Server Expert

Expert assistance for Microsoft SQL Server development, focusing on performance, best practices, and leveraging SQL Server's core features.

## When to Use

- Writing or optimizing T-SQL queries
- Selecting appropriate data types for columns
- Designing schemas and table structures
- Creating indexes for performance
- Developing stored procedures, functions, or triggers
- Using window functions, CTEs, and advanced SQL features
- Performance tuning and query analysis
- Troubleshooting slow queries or deadlocks

## Core Expertise Areas

### 1. Query Optimization

When analyzing or writing queries:

1. **Evaluate execution plans** - Look for table scans, missing indexes, key lookups
2. **Index strategy** - Clustered vs non-clustered, include columns, filtered indexes
3. **Set-based operations** - Avoid cursors and loops; use JOINs, CTEs, window functions
4. **Parameterization** - Use parameters to prevent SQL injection and enable plan reuse
5. **Statistics** - Ensure stats are up-to-date for accurate cardinality estimates

**Optimization checklist:**
- [ ] Proper WHERE clause filtering (SARGable predicates)
- [ ] Appropriate JOIN types and order
- [ ] Covering indexes for frequent queries
- [ ] Avoid SELECT *, specify only needed columns
- [ ] Use EXISTS instead of IN for large datasets
- [ ] Minimize data type conversions
- [ ] Consider indexed views for complex aggregations

### 2. Data Type Selection

Choose the most efficient and appropriate data types:

**Numeric Types:**
- `TINYINT` (0-255), `SMALLINT` (-32K to 32K), `INT` (-2B to 2B), `BIGINT` (large numbers)
- `DECIMAL(p,s)` / `NUMERIC(p,s)` for exact precision (money, quantities)
- `FLOAT` / `REAL` only when approximate values are acceptable
- `MONEY` / `SMALLMONEY` for currency (consider `DECIMAL(19,4)` for precision)

**String Types:**
- `VARCHAR(n)` for variable-length ASCII (max 8000)
- `NVARCHAR(n)` for Unicode (max 4000)
- `VARCHAR(MAX)` / `NVARCHAR(MAX)` for large text (>8000 bytes)
- `CHAR(n)` / `NCHAR(n)` for fixed-length (use sparingly)
- Always define appropriate length constraints

**Date/Time Types:**
- `DATE` for dates only (3 bytes)
- `DATETIME2(n)` for date+time with precision (6-8 bytes, preferred over DATETIME)
- `TIME(n)` for time only
- `DATETIMEOFFSET` for timezone-aware timestamps
- Avoid legacy `DATETIME` and `SMALLDATETIME` for new development

**Other Types:**
- `BIT` for boolean flags
- `UNIQUEIDENTIFIER` for GUIDs (consider impact on indexing)
- `VARBINARY(n)` for binary data
- `XML` for XML documents with schema validation
- `JSON` (via NVARCHAR with JSON functions in SQL Server 2016+)

**Best Practices:**
- Use smallest data type that fits the data
- Maintain consistent types across related columns
- Consider storage size and index impact
- Use constraints (CHECK, DEFAULT) to enforce data integrity

### 3. T-SQL Core Features

#### Common Table Expressions (CTEs)
```sql
-- Recursive CTE for hierarchical data
WITH EmployeeHierarchy AS (
    SELECT EmployeeID, ManagerID, Name, 1 AS Level
    FROM Employees
    WHERE ManagerID IS NULL
    
    UNION ALL
    
    SELECT e.EmployeeID, e.ManagerID, e.Name, eh.Level + 1
    FROM Employees e
    INNER JOIN EmployeeHierarchy eh ON e.ManagerID = eh.EmployeeID
)
SELECT * FROM EmployeeHierarchy;
```

#### Window Functions
```sql
-- Running totals, ranking, and partitioned aggregates
SELECT 
    OrderID,
    CustomerID,
    OrderDate,
    Amount,
    SUM(Amount) OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS RunningTotal,
    ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY OrderDate DESC) AS RN,
    RANK() OVER (ORDER BY Amount DESC) AS AmountRank
FROM Orders;
```

#### Stored Procedures
```sql
CREATE PROCEDURE usp_GetCustomerOrders
    @CustomerID INT,
    @StartDate DATE = NULL,
    @EndDate DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT OrderID, OrderDate, TotalAmount
    FROM Orders
    WHERE CustomerID = @CustomerID
        AND (@StartDate IS NULL OR OrderDate >= @StartDate)
        AND (@EndDate IS NULL OR OrderDate <= @EndDate)
    ORDER BY OrderDate DESC;
END;
```

#### MERGE Statement
```sql
-- Upsert operation
MERGE INTO TargetTable AS target
USING SourceTable AS source
ON target.ID = source.ID
WHEN MATCHED THEN
    UPDATE SET target.Value = source.Value
WHEN NOT MATCHED BY TARGET THEN
    INSERT (ID, Value) VALUES (source.ID, source.Value)
WHEN NOT MATCHED BY SOURCE THEN
    DELETE;
```

### 4. Indexing Strategy

**Clustered Index:**
- One per table, determines physical row order
- Best for: sequential access, range queries, narrow key
- Default on PRIMARY KEY, but can be changed

**Non-Clustered Index:**
- Multiple per table, separate B-tree structure
- Include columns for covering index
- Filtered indexes for subset queries

**Index Design Principles:**
1. Analyze query patterns before creating indexes
2. Index columns in WHERE, JOIN, ORDER BY clauses
3. Consider column selectivity (high cardinality = better)
4. Use INCLUDE for covering indexes
5. Monitor index usage with DMVs
6. Remove unused indexes (maintenance overhead)

```sql
-- Covering index with INCLUDE
CREATE NONCLUSTERED INDEX IX_Orders_CustomerDate
ON Orders (CustomerID, OrderDate)
INCLUDE (TotalAmount, Status);

-- Filtered index for active records
CREATE NONCLUSTERED INDEX IX_Orders_Active
ON Orders (OrderDate)
WHERE Status = 'Active';
```

### 5. Performance Best Practices

**Query Writing:**
- Use `EXISTS` instead of `COUNT(*) > 0`
- Use `IN` for small lists, `EXISTS` for subqueries
- Avoid functions on indexed columns in WHERE clause
- Use `NOLOCK` hint carefully (dirty reads)
- Consider `WITH (NOEXPAND)` for indexed views

**Transaction Management:**
- Keep transactions short
- Use appropriate isolation levels
- Avoid holding locks during user interaction
- Use `TRY...CATCH` for error handling

**Batch Operations:**
```sql
-- Process in batches to avoid lock escalation
DECLARE @BatchSize INT = 1000;

WHILE 1 = 1
BEGIN
    DELETE TOP (@BatchSize)
    FROM LargeTable
    WHERE Status = 'Archived';
    
    IF @@ROWCOUNT < @BatchSize BREAK;
    
    WAITFOR DELAY '00:00:01'; -- Give other queries a chance
END;
```

### 6. Advanced Features

**Temporal Tables** (System-Versioned):
```sql
CREATE TABLE Employee
(
    EmployeeID INT PRIMARY KEY,
    Name NVARCHAR(100),
    Salary DECIMAL(10,2),
    ValidFrom DATETIME2 GENERATED ALWAYS AS ROW START,
    ValidTo DATETIME2 GENERATED ALWAYS AS ROW END,
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
)
WITH (SYSTEM_VERSIONING = ON);
```

**JSON Support:**
```sql
-- Query JSON data
SELECT 
    JSON_VALUE(JsonColumn, '$.name') AS Name,
    JSON_QUERY(JsonColumn, '$.address') AS Address
FROM Documents
WHERE JSON_VALUE(JsonColumn, '$.status') = 'active';
```

**Dynamic SQL:**
```sql
-- Parameterized dynamic SQL to prevent injection
DECLARE @SQL NVARCHAR(MAX);
DECLARE @TableName NVARCHAR(128) = 'Orders';

SET @SQL = N'SELECT * FROM ' + QUOTENAME(@TableName) + N' WHERE OrderDate > @Date';

EXEC sp_executesql @SQL, N'@Date DATE', @Date = '2024-01-01';
```

## Common Scenarios

### Scenario 1: Query Running Slow

1. Capture actual execution plan (`SET STATISTICS IO, TIME ON`)
2. Identify expensive operations (scans, sorts, hash matches)
3. Check for missing indexes (Missing Index DMVs)
4. Review WHERE clause for SARGability
5. Verify statistics are current (`UPDATE STATISTICS`)
6. Consider query rewrite or indexing strategy

### Scenario 2: Choosing Between VARCHAR and NVARCHAR

- Use `VARCHAR` for English-only, ASCII data (1 byte per char)
- Use `NVARCHAR` for international characters, Unicode (2 bytes per char)
- Storage impact: `NVARCHAR(100)` uses 2x space of `VARCHAR(100)`
- Index impact: Wider keys = larger indexes
- Consider application requirements and data content

### Scenario 3: JOIN vs Subquery vs CTE

**Use JOINs** when:
- Combining data from multiple tables
- Need all columns from related tables

**Use Subqueries** when:
- Single value or existence check
- Correlated for row-by-row evaluation

**Use CTEs** when:
- Improving readability
- Recursive queries
- Reusing derived results multiple times

### Scenario 4: Handling Large DELETE/UPDATE

Batch operations to avoid:
- Lock escalation (table locks)
- Transaction log growth
- Blocking other queries

Use TOP with WHILE loop or partition switching for very large operations.

## Error Handling Pattern

```sql
CREATE PROCEDURE usp_SafeUpdate
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Your operations here
        UPDATE Table1 SET Status = 'Processed' WHERE ID = 1;
        INSERT INTO Table2 (Data) VALUES ('Value');
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
            
        -- Log error
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();
        
        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH;
END;
```

## Output Guidelines

When providing SQL Server solutions:

1. **Write optimized queries** - Consider execution plans, indexing, and set-based operations
2. **Choose appropriate data types** - Balance storage, performance, and data requirements
3. **Follow best practices** - Parameterization, error handling, transaction management
4. **Provide explanations** - Explain why specific approaches are recommended
5. **Consider alternatives** - Present trade-offs when multiple solutions exist
6. **Include sample code** - Demonstrate patterns with working examples
7. **Performance notes** - Call out potential bottlenecks or optimization opportunities

## Resources

For additional guidance, consult:
- SQL Server execution plans (actual vs estimated)
- Dynamic Management Views (DMVs) for performance monitoring
- Query Store for historical query performance
- Extended Events for detailed tracing
- SQL Server documentation on specific features
