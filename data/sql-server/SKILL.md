---
name: "sql-server"
description: 'Develop SQL Server databases with T-SQL, stored procedures, indexing, and performance optimization. Use when writing T-SQL queries, creating stored procedures/functions, designing index strategies, optimizing query execution plans, or troubleshooting SQL Server performance.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
compatibility:
 languages: ["sql", "tsql"]
 platforms: ["windows", "linux"]
---

# SQL Server Database Development

> **Purpose**: Production-ready SQL Server development for enterprise applications. 
> **Audience**: Backend engineers and database administrators working with Microsoft SQL Server. 
> **Standard**: Follows [github/awesome-copilot](https://github.com/github/awesome-copilot) SQL Server patterns.

---

## When to Use This Skill

- Writing T-SQL queries and stored procedures
- Designing SQL Server index strategies
- Optimizing query execution plans
- Using window functions and CTEs
- Troubleshooting SQL Server performance issues

## Prerequisites

- SQL Server 2019+ or Azure SQL Database
- SSMS, Azure Data Studio, or DBeaver client

## Quick Reference

| Need | Solution | Pattern |
|------|----------|---------|
| **Stored procedure** | CREATE PROCEDURE | `CREATE PROCEDURE GetUser @UserId INT AS BEGIN ... END` |
| **Transaction** | BEGIN/COMMIT/ROLLBACK | `BEGIN TRANSACTION; ... COMMIT;` |
| **Error handling** | TRY...CATCH | `BEGIN TRY ... END TRY BEGIN CATCH ... END CATCH` |
| **Indexing** | CREATE INDEX | `CREATE NONCLUSTERED INDEX ON Users(Email)` |
| **Query optimization** | Execution plan | `SET STATISTICS IO ON; SET STATISTICS TIME ON;` |
| **Upsert** | MERGE statement | `MERGE INTO target USING source ON ...` |

---

## SQL Server Version

**Current**: SQL Server 2022 
**Minimum**: SQL Server 2019

---

## Common Pitfalls

| Issue | Problem | Solution |
|-------|---------|----------|
| **SELECT *** | Unnecessary data transfer | Select only needed columns |
| **Missing indexes** | Table scans | Add indexes on WHERE/JOIN columns |
| **Functions on columns** | Prevents index usage | Rewrite without functions |
| **Implicit conversions** | Performance hit | Match data types |
| **CURSOR usage** | Slow row-by-row processing | Use set-based operations |
| **No error handling** | Silent failures | Use TRY...CATCH blocks |

---

## Resources

- **SQL Server Docs**: [learn.microsoft.com/sql/sql-server](https://learn.microsoft.com/sql/sql-server/)
- **Execution Plan Reference**: [use-the-index-luke.com](https://use-the-index-luke.com)
- **SQL Server Management Studio (SSMS)**: Official GUI tool
- **Azure Data Studio**: Cross-platform database tool
- **Awesome Copilot**: [github.com/github/awesome-copilot](https://github.com/github/awesome-copilot)

---

**See Also**: [Skills.md](../../../../Skills.md) - [AGENTS.md](../../../../AGENTS.md) - [Database Skill](../../architecture/database/SKILL.md)

**Last Updated**: January 27, 2026

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Query timeout | Check execution plan for table scans, add missing indexes, update statistics |
| Deadlock victim errors | Access tables in consistent order, keep transactions short, use NOLOCK for read-only queries |
| Stored procedure parameter sniffing | Use OPTION (RECOMPILE) or local variables for parameter values |

## References

- [Tsql Basics](references/tsql-basics.md)
- [Indexing Optimization Transactions](references/indexing-optimization-transactions.md)
- [Advanced Tsql](references/advanced-tsql.md)