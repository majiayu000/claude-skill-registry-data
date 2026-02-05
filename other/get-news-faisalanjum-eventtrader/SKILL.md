---
name: get-news
description: Fetch news for a ticker up to a cutoff date, optionally for a specific month window
context: fork
allowed-tools:
  - mcp__neo4j-cypher__read_neo4j_cypher
---

## Arguments

`$ARGUMENTS` = `TICKER CUTOFF_DATETIME [MONTH_OFFSET]`

Examples:
- `AAPL 2025-04-01T00:00:00` → all news up to April 1st
- `AAPL 2025-04-01T00:00:00 1m` → March only
- `AAPL 2025-04-01T00:00:00 2m` → February only
- `AAPL 2025-04-01T00:00:00 3m` → January only

## Logic

Parse arguments:
1. TICKER = first argument
2. CUTOFF = second argument (datetime)
3. MONTH_OFFSET = optional third argument (1m, 2m, 3m, etc.)

Calculate date range:
- If no offset: `start = '1900-01-01'`, `end = CUTOFF`
- If offset Nm:
  - `end` = first day of month that is (N-1) months before CUTOFF
  - `start` = first day of month that is N months before CUTOFF

Example with CUTOFF = 2025-04-01T00:00:00:
- 1m → start: 2025-03-01, end: 2025-04-01 (March)
- 2m → start: 2025-02-01, end: 2025-03-01 (February)
- 3m → start: 2025-01-01, end: 2025-02-01 (January)

## Query

```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company {ticker: $ticker})
WHERE n.created >= $start AND n.created < $end
RETURN n.created, n.title, r.daily_stock
ORDER BY n.created ASC
```

## Output

Return pipe-delimited, one per line:
```
datetime|title|return
```

If no results: `NO_NEWS_FOUND`
