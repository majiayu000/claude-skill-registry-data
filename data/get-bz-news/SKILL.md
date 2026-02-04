---
name: get-bz-news
description: Fetch Benzinga news with significant daily returns from Neo4j
context: fork
allowed-tools:
  - mcp__neo4j-cypher__read_neo4j_cypher
---

# Get Benzinga News

Fetch news where |daily_adj| >= threshold. Default threshold is 1.5σ of trailing adjusted volatility.

## Arguments

`$ARGUMENTS` = `TICKER START_DATE END_DATE [THRESHOLD]`

- THRESHOLD optional: `1.5s` (default), `2s`, or fixed like `3` (percent)

Example: `AAPL 2024-01-01T00:00:00 2024-04-01T00:00:00`

## Steps

### Step 1: Calculate Volatility

```cypher
MATCH (d:Date)-[r:HAS_PRICE]->(c:Company {ticker: $ticker})
WHERE d.date >= date($start) - duration('P365D') AND d.date < date($start)
MATCH (d)-[m:HAS_PRICE]->(idx:MarketIndex {ticker: 'SPY'})
WHERE r.daily_return IS NOT NULL AND m.daily_return IS NOT NULL
RETURN stdev(r.daily_return - m.daily_return) AS adj_vol, count(*) AS days
```

**Fail if < 60 days:** Return `INSUFFICIENT_HISTORY: {days} days (need 60+)`

### Step 2: Compute Threshold

Parse THRESHOLD argument:
- `1.5s` → `threshold = 1.5 × adj_vol` (default)
- `2s` → `threshold = 2.0 × adj_vol`
- `3` → `threshold = 3.0` (fixed percent, ignore volatility)

### Step 3: Fetch News

Use `threshold` and `adj_vol` as literal parameters (no subquery):

```cypher
MATCH (n:News)-[inf:INFLUENCES]->(c:Company {ticker: $ticker})
WHERE n.created >= $start AND n.created < $end
  AND inf.daily_stock IS NOT NULL AND inf.daily_macro IS NOT NULL
  AND abs(inf.daily_stock - inf.daily_macro) >= $threshold
RETURN n.id AS news_id,
       n.created AS date,
       n.title AS title,
       n.teaser AS teaser,
       n.body AS body,
       n.market_session AS market_session,
       inf.daily_stock AS daily_stock,
       (inf.daily_stock - inf.daily_macro) AS daily_adj,
       (inf.daily_stock - inf.daily_sector) AS sector_adj,
       (inf.daily_stock - inf.daily_industry) AS industry_adj,
       abs(inf.daily_stock - inf.daily_macro) / $adj_vol AS z_score
ORDER BY n.created ASC
```

## Output

Return JSON with:
- `query`: parameters used (ticker, dates, threshold_pct, adj_vol)
- `results`: array of news items with z_score

If no results: `NO_NEWS_FOUND`
