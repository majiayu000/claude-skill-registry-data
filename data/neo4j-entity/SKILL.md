---
name: neo4j-entity
description: Query companies, sectors, industries, price series, dividends, and splits from Neo4j. Use when fetching entity data or market information.
---

# Neo4j Entity Queries

Queries for Company, Sector, Industry, MarketIndex, and related market data (prices, dividends, splits).

## Company Queries

### Company by ticker
```cypher
MATCH (c:Company {ticker: $ticker})
RETURN c
```

### Company with classification
```cypher
MATCH (c:Company {ticker: $ticker})-[:BELONGS_TO]->(ind:Industry)-[:BELONGS_TO]->(sec:Sector)-[:BELONGS_TO]->(idx:MarketIndex)
RETURN c.ticker, c.name, ind.name AS industry, sec.name AS sector, idx.name AS market_index
```

### All companies in a sector
```cypher
MATCH (c:Company)-[:BELONGS_TO]->(ind:Industry)-[:BELONGS_TO]->(sec:Sector {name: $sector_name})
RETURN c.ticker, c.name, ind.name AS industry
ORDER BY c.ticker
```

### Related companies
```cypher
MATCH (c:Company {ticker: $ticker})-[r:RELATED_TO]-(other:Company)
RETURN other.ticker, other.name, r.relationship_type
```

## Market Index (SPY)

### Market index info
```cypher
MATCH (m:MarketIndex)
RETURN m.ticker, m.name, m.etf
```

### News impact on market
```cypher
MATCH (n:News)-[r:INFLUENCES]->(m:MarketIndex {ticker: 'SPY'})
WHERE r.daily_macro IS NOT NULL AND abs(r.daily_macro) > 1.0
RETURN n.title, r.daily_macro, n.created
ORDER BY abs(r.daily_macro) DESC
LIMIT 20
```

### Price series for market index
```cypher
MATCH (d:Date)-[p:HAS_PRICE]->(m:MarketIndex {ticker: 'SPY'})
WHERE d.date >= $start_date AND d.date <= $end_date
RETURN d.date, p.open, p.high, p.low, p.close, p.volume, p.daily_return
ORDER BY d.date
```

## Price Series (OHLCV)

### Price series for company
```cypher
MATCH (d:Date)-[p:HAS_PRICE]->(c:Company {ticker: $ticker})
WHERE d.date >= $start_date AND d.date <= $end_date
RETURN d.date, p.open, p.high, p.low, p.close, p.volume, p.daily_return
ORDER BY d.date
```

### Price series for sector/industry
```cypher
MATCH (d:Date)-[p:HAS_PRICE]->(s:Sector {name: $sector_name})
WHERE d.date >= $start_date AND d.date <= $end_date
RETURN d.date, p.open, p.high, p.low, p.close, p.volume, p.daily_return
ORDER BY d.date
```

### Latest price for company
```cypher
MATCH (d:Date)-[p:HAS_PRICE]->(c:Company {ticker: $ticker})
RETURN d.date, p.close, p.volume
ORDER BY d.date DESC
LIMIT 1
```

## Dividends

### Dividends for company
```cypher
MATCH (c:Company {ticker: $ticker})-[:DECLARED_DIVIDEND]->(d:Dividend)
RETURN d.declaration_date, d.ex_dividend_date, d.pay_date,
       d.cash_amount, d.dividend_type, d.frequency
ORDER BY d.declaration_date DESC
```

### Dividends in date range
```cypher
MATCH (c:Company {ticker: $ticker})-[:DECLARED_DIVIDEND]->(d:Dividend)
WHERE d.declaration_date >= $start_date AND d.declaration_date <= $end_date
RETURN d.declaration_date, d.cash_amount, d.dividend_type, d.frequency
ORDER BY d.declaration_date
```

### Dividends via Date node
```cypher
MATCH (dt:Date)-[:HAS_DIVIDEND]->(d:Dividend)<-[:DECLARED_DIVIDEND]-(c:Company {ticker: $ticker})
WHERE dt.date >= $start_date AND dt.date <= $end_date
RETURN dt.date, d.cash_amount, d.dividend_type
ORDER BY dt.date
```

## Splits

### Splits for company
```cypher
MATCH (c:Company {ticker: $ticker})-[:DECLARED_SPLIT]->(s:Split)
RETURN s.execution_date, s.split_from, s.split_to
ORDER BY s.execution_date DESC
```

### Splits in date range
```cypher
MATCH (c:Company {ticker: $ticker})-[:DECLARED_SPLIT]->(s:Split)
WHERE s.execution_date >= $start_date AND s.execution_date <= $end_date
RETURN s.execution_date, s.split_from, s.split_to
```

## Date/Calendar

### Trading days in range
```cypher
MATCH (d:Date)
WHERE d.date >= $start_date AND d.date <= $end_date
  AND d.is_trading_day = '1'
RETURN d.date, d.market_open_current_day, d.market_close_current_day
ORDER BY d.date
```

### Next/previous trading day
```cypher
MATCH (d:Date {date: $date})-[:NEXT]->(next:Date)
WHERE next.is_trading_day = '1'
RETURN next.date AS next_trading_day
```

## Data Analysis

### Companies by sector with details
```cypher
MATCH (c:Company) WHERE c.sector IS NOT NULL
RETURN c.ticker, c.name, c.sector, c.industry, c.mkt_cap
ORDER BY c.sector, c.ticker LIMIT 20
```

### All stock splits with ratios
```cypher
MATCH (c:Company)-[:DECLARED_SPLIT]->(s:Split)
RETURN c.ticker, s.split_from, s.split_to, s.execution_date
ORDER BY s.execution_date DESC
```

### Companies with incomplete profile information
```cypher
MATCH (c:Company)
WHERE c.sector IS NULL OR c.industry IS NULL OR c.mkt_cap IS NULL OR c.employees IS NULL
RETURN c.ticker, c.name,
       CASE WHEN c.sector IS NULL THEN 'Missing' ELSE c.sector END as sector,
       CASE WHEN c.industry IS NULL THEN 'Missing' ELSE c.industry END as industry,
       CASE WHEN c.mkt_cap IS NULL THEN 'Missing' ELSE c.mkt_cap END as mkt_cap,
       CASE WHEN c.employees IS NULL THEN 'Missing' ELSE c.employees END as employees
LIMIT 20
```

### Companies with market cap > 10 billion
```cypher
MATCH (c:Company)
WHERE c.mkt_cap IS NOT NULL
  AND toFloat(replace(c.mkt_cap, ',', '')) > 10000000000
RETURN c.ticker, c.name, c.mkt_cap, c.sector
ORDER BY toFloat(replace(c.mkt_cap, ',', '')) DESC LIMIT 20
```

### Quarterly dividend payers
```cypher
MATCH (c:Company)-[:DECLARED_DIVIDEND]->(d:Dividend)
WHERE LOWER(d.frequency) = 'quarterly'
WITH c, COUNT(d) as dividend_count
WHERE dividend_count > 2
RETURN c.ticker, c.name, dividend_count
ORDER BY dividend_count DESC LIMIT 20
```

### Recent dividend declarations with amounts
```cypher
MATCH (c:Company)-[:DECLARED_DIVIDEND]->(d:Dividend)
WHERE datetime(d.declaration_date) > datetime() - duration('P180D')
  AND d.cash_amount IS NOT NULL
RETURN c.ticker, d.cash_amount, d.ex_dividend_date, d.pay_date, d.dividend_type
ORDER BY toFloat(d.cash_amount) DESC LIMIT 20
```

### Stock splits with execution dates via Date
```cypher
MATCH (d:Date)-[:HAS_SPLIT]->(s:Split)<-[:DECLARED_SPLIT]-(c:Company)
RETURN c.ticker, d.date, s.split_from, s.split_to, s.execution_date
ORDER BY d.date DESC
```

### Companies in Technology sector
```cypher
MATCH (c:Company) WHERE c.sector = 'Technology'
RETURN c.ticker, c.name, c.industry, c.mkt_cap
ORDER BY toFloat(replace(c.mkt_cap, ',', '')) DESC LIMIT 50
```

### Recent dividend declarations
```cypher
MATCH (c:Company)-[:DECLARED_DIVIDEND]->(d:Dividend)
WHERE datetime(d.declaration_date) > datetime() - duration('P90D')
RETURN c.ticker, d.cash_amount, d.ex_dividend_date, d.pay_date
ORDER BY d.declaration_date DESC LIMIT 20
```

### Market index relationships
```cypher
MATCH (m:MarketIndex)
OPTIONAL MATCH (m)<-[:BELONGS_TO]-(s:Sector)
OPTIONAL MATCH (m)<-[:BELONGS_TO]-(i:Industry)
OPTIONAL MATCH (m)<-[:BELONGS_TO]-(c:Company)
RETURN m.ticker, m.name,
       COUNT(DISTINCT s) as sector_count,
       COUNT(DISTINCT i) as industry_count,
       COUNT(DISTINCT c) as company_count
ORDER BY m.ticker
```

### Stock splits in last year
```cypher
MATCH (c:Company)-[:DECLARED_SPLIT]->(s:Split)
WHERE datetime(s.execution_date) > datetime() - duration('P365D')
RETURN c.ticker, s.split_from, s.split_to, s.execution_date
ORDER BY s.execution_date DESC LIMIT 10
```

## Notes
- `Company.ticker` has no index but count is small (~796); exact match scans are acceptable.
- `HAS_PRICE` relationship contains OHLCV data as properties.
- All date fields are Strings (not Date type).
- `daily_return` on HAS_PRICE is a percentage (5.06 means 5.06%).
- `Company.mkt_cap` is stored as numeric string with commas (e.g., "81,035,171,840").

## Known Data Gaps
| Date | Gap | Affected | Mitigation |
|------|-----|----------|------------|

---
*Version 1.1 | 2026-01-11 | Added self-improvement protocol*
