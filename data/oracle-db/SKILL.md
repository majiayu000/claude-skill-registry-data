---
name: Oracle DB
description: Write Oracle SQL and PL/SQL with proper syntax, hints, and performance patterns.
metadata: {"clawdbot":{"emoji":"🔴","requires":{"anyBins":["sqlplus","sql"]},"os":["linux","darwin","win32"]}}
---

## Syntax Differences

- `ROWNUM` for limiting rows—`WHERE ROWNUM <= 10`; 12c+ supports `FETCH FIRST 10 ROWS ONLY`
- `DUAL` table for expressions—`SELECT sysdate FROM dual`
- `VARCHAR2` not `VARCHAR`—VARCHAR is reserved, VARCHAR2 is the standard
- String concatenation with `||`—not CONCAT for multiple values
- Empty string equals NULL—`'' IS NULL` is true; breaks logic from other databases

## Pagination

- ROWNUM assigned before ORDER BY—wrap in subquery: `SELECT * FROM (SELECT ... ORDER BY x) WHERE ROWNUM <= 10`
- Offset requires nested subquery: `SELECT * FROM (SELECT a.*, ROWNUM rn FROM (...) a WHERE ROWNUM <= 20) WHERE rn > 10`
- 12c+: `OFFSET 10 ROWS FETCH NEXT 10 ROWS ONLY`—cleaner, use when available

## NULL Handling

- `NVL(col, default)` for null replacement—faster than COALESCE for two args
- `NVL2(col, if_not_null, if_null)` for conditional—common Oracle pattern
- Empty string is NULL—`LENGTH('')` returns NULL, not 0
- `NULLIF(a, b)` returns NULL if equal—useful for avoiding division by zero

## Dates

- `SYSDATE` for current datetime—no parentheses
- `TO_DATE('2024-01-15', 'YYYY-MM-DD')` for string to date—format required
- `TO_CHAR(date, 'YYYY-MM-DD HH24:MI:SS')` for date to string
- Date arithmetic in days—`SYSDATE + 1` is tomorrow, `SYSDATE + 1/24` is one hour

## Sequences

- Create: `CREATE SEQUENCE seq_name START WITH 1 INCREMENT BY 1`
- Get next: `seq_name.NEXTVAL`—`SELECT seq_name.NEXTVAL FROM dual`
- Current value: `seq_name.CURRVAL`—only after NEXTVAL in same session
- 12c+: identity columns—`GENERATED ALWAYS AS IDENTITY`

## Hierarchical Queries

- `CONNECT BY PRIOR child = parent` for tree traversal
- `START WITH parent IS NULL` for root nodes
- `LEVEL` pseudo-column shows depth—`WHERE LEVEL <= 3` limits depth
- `SYS_CONNECT_BY_PATH(col, '/')` builds path string

## Bind Variables

- Always use bind variables—literals cause hard parse every time
- PL/SQL: `:variable_name` syntax
- Performance critical—literal values fill shared pool, cause contention
- `CURSOR_SHARING=FORCE` as workaround but not recommended long-term

## Hints

- `/*+ INDEX(table idx_name) */` forces index use
- `/*+ FULL(table) */` forces full table scan
- `/*+ PARALLEL(table, 4) */` enables parallel query
- Hints inside `SELECT /*+ hint */`—common placement after SELECT keyword

## PL/SQL Blocks

- Anonymous block: `BEGIN ... END;` with `/` on new line to execute
- `DBMS_OUTPUT.PUT_LINE()` for debug output—`SET SERVEROUTPUT ON` first
- Exception handling: `EXCEPTION WHEN OTHERS THEN`—always handle or log
- `EXECUTE IMMEDIATE 'sql string'` for dynamic SQL—beware injection

## Transactions

- No auto-commit by default—must `COMMIT` explicitly
- `SAVEPOINT name` then `ROLLBACK TO name` for partial rollback
- DDL auto-commits—`CREATE TABLE` commits any pending transaction
- `SELECT FOR UPDATE WAIT 5` waits 5 seconds for lock—avoids indefinite hang

## Performance

- `EXPLAIN PLAN FOR sql; SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY)`—shows plan
- `V$SQL` and `V$SESSION` for monitoring—requires privileges
- Avoid `SELECT *`—fetches all columns including LOBs
- Index hint when optimizer chooses wrong—`/*+ INDEX(t idx) */`

## Common Traps

- `MINUS` instead of `EXCEPT`—Oracle uses MINUS for set difference
- `DECODE` is Oracle-specific—use CASE for portability
- Implicit type conversion—`WHERE num_col = '123'` works but prevents index use
- `ROWID` is physical—don't store or rely on across transactions
