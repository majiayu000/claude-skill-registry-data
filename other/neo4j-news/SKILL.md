---
name: neo4j-news
description: Query news articles from Neo4j with fulltext and vector search. Use when fetching news data or searching news content.
---

# Neo4j News Queries

Queries for News nodes with fulltext and vector search capabilities.

## Basic News Queries

### News for company in date range
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company {ticker: $ticker})
WHERE n.created >= $start_date AND n.created <= $end_date
RETURN n.id, n.title, n.teaser, n.created, n.channels
ORDER BY n.created DESC
```

### News around filing (with anomaly filter)
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company {ticker: $ticker})
WHERE n.created >= $start_date AND n.created <= $end_date
  AND r.daily_stock IS NOT NULL AND NOT isNaN(r.daily_stock)
RETURN n.title, n.channels, n.created, r.daily_stock, r.daily_macro
ORDER BY n.created
```

### News by channel
```cypher
MATCH (n:News)-[:INFLUENCES]->(c:Company {ticker: $ticker})
WHERE n.channels CONTAINS $channel  // e.g., 'Guidance', 'Earnings', 'M&A'
RETURN n.title, n.created, n.channels
ORDER BY n.created DESC
```

### News with highest impact
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company {ticker: $ticker})
WHERE n.created >= $start_date AND n.created <= $end_date
  AND r.daily_stock IS NOT NULL AND NOT isNaN(r.daily_stock)
RETURN n.title, n.created, r.daily_stock, r.daily_macro,
       abs(r.daily_stock - r.daily_macro) AS impact
ORDER BY impact DESC
LIMIT 10
```

### Latest news for company
```cypher
MATCH (n:News)-[:INFLUENCES]->(c:Company {ticker: $ticker})
RETURN n.title, n.teaser, n.created, n.channels
ORDER BY n.created DESC
LIMIT 10
```

## Fulltext Search

### Search news by keyword
```cypher
CALL db.index.fulltext.queryNodes('news_ft', $query)
YIELD node, score
RETURN node.title, node.created, score
ORDER BY score DESC
LIMIT 20
```

### Search news for company
```cypher
CALL db.index.fulltext.queryNodes('news_ft', $query)
YIELD node, score
MATCH (node)-[:INFLUENCES]->(c:Company {ticker: $ticker})
RETURN node.title, node.created, score
ORDER BY score DESC
LIMIT 20
```

### Search news body
```cypher
CALL db.index.fulltext.queryNodes('news_ft', $query)
YIELD node, score
RETURN node.title, node.teaser, substring(node.body, 0, 500) AS body_preview, score
ORDER BY score DESC
LIMIT 10
```

## Vector Search

### Semantic search (requires embedding)
```cypher
CALL db.index.vector.queryNodes('news_vector_index', $k, $embedding)
YIELD node, score
RETURN node.title, node.created, score
ORDER BY score DESC
```

### Semantic search for company
```cypher
CALL db.index.vector.queryNodes('news_vector_index', $k, $embedding)
YIELD node, score
MATCH (node)-[:INFLUENCES]->(c:Company {ticker: $ticker})
RETURN node.title, node.created, score
ORDER BY score DESC
```

## News with Returns

### News impact on stock
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company {ticker: $ticker})
WHERE n.created >= $start_date AND n.created <= $end_date
  AND r.daily_stock IS NOT NULL
RETURN n.title, n.created,
       r.daily_stock, r.daily_industry, r.daily_sector, r.daily_macro
ORDER BY n.created
```

### Aggregate news impact
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company {ticker: $ticker})
WHERE n.created >= $start_date AND n.created <= $end_date
  AND r.daily_stock IS NOT NULL AND NOT isNaN(r.daily_stock)
RETURN count(n) AS news_count,
       avg(r.daily_stock) AS avg_stock_return,
       avg(r.daily_stock - r.daily_macro) AS avg_excess_return
```

## Return Analysis

### Hourly vs daily return divergence
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE r.hourly_stock IS NOT NULL AND r.daily_stock IS NOT NULL
  AND ((r.hourly_stock > 0 AND r.daily_stock < 0) OR (r.hourly_stock < 0 AND r.daily_stock > 0))
RETURN c.ticker, n.title, r.hourly_stock, r.daily_stock, n.created
ORDER BY abs(r.hourly_stock - r.daily_stock) DESC
LIMIT 20
```

### Companies outperforming market
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE r.daily_stock IS NOT NULL AND r.daily_macro IS NOT NULL
  AND r.daily_stock > r.daily_macro + 5.0
RETURN c.ticker, n.title, r.daily_stock, r.daily_macro,
       r.daily_stock - r.daily_macro AS excess_return
ORDER BY excess_return DESC
LIMIT 20
```

### Multi-level return coverage check
```cypher
MATCH ()-[r:INFLUENCES]->()
WITH count(*) AS total,
     count(r.daily_stock) AS has_daily_stock,
     count(r.hourly_stock) AS has_hourly_stock,
     count(r.daily_industry) AS has_daily_industry,
     count(r.daily_sector) AS has_daily_sector,
     count(r.daily_macro) AS has_daily_macro
RETURN total,
       round(100.0 * has_daily_stock / total) AS daily_stock_pct,
       round(100.0 * has_hourly_stock / total) AS hourly_stock_pct,
       round(100.0 * has_daily_industry / total) AS daily_industry_pct,
       round(100.0 * has_daily_sector / total) AS daily_sector_pct,
       round(100.0 * has_daily_macro / total) AS daily_macro_pct
```

## Data Analysis

### Count all INFLUENCES relationships
```cypher
MATCH ()-[r:INFLUENCES]->() RETURN count(r)
```

### Count news with embeddings
```cypher
MATCH (n:News) WHERE n.embedding IS NOT NULL RETURN COUNT(n) as embedded_news
```

### News embedding coverage
```cypher
MATCH (n:News) WHERE n.embedding IS NOT NULL
WITH COUNT(n) as embedded_count
MATCH (n2:News)
WITH embedded_count, COUNT(n2) as total_count
RETURN embedded_count, total_count, ROUND(100.0 * embedded_count / total_count) as coverage_pct
```

### Find relationships with null returns
```cypher
MATCH ()-[r:INFLUENCES]->()
WHERE r.daily_stock IS NULL OR r.hourly_stock IS NULL
RETURN COUNT(*) as null_count
```

### News with maximum daily_stock values
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE r.daily_stock IS NOT NULL AND r.daily_stock <> 'NaN'
WITH n, c, toFloat(r.daily_stock) as daily_return
WHERE NOT isNaN(daily_return)
RETURN n.title, c.ticker, daily_return ORDER BY daily_return DESC LIMIT 10
```

### News causing extreme market movements (>10%)
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE r.daily_stock IS NOT NULL AND ABS(toFloat(r.daily_stock)) > 10.0
RETURN n.title, c.ticker, r.daily_stock, r.daily_industry, r.daily_sector, r.daily_macro,
       r.hourly_stock, r.session_stock, n.created
ORDER BY ABS(toFloat(r.daily_stock)) DESC LIMIT 20
```

### News causing extreme positive movements (>8%)
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE r.daily_stock IS NOT NULL AND r.daily_stock <> 'NaN' AND toFloat(r.daily_stock) > 8.0
RETURN n.title, c.ticker, r.daily_stock, n.created
ORDER BY toFloat(r.daily_stock) DESC LIMIT 20
```

### Count news with daily_stock > 10%
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE r.daily_stock IS NOT NULL AND r.daily_stock <> 'NaN' AND toFloat(r.daily_stock) > 10.0
RETURN COUNT(n) AS news_count
```

### News driving stocks below market (-3%)
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE r.daily_stock < r.daily_macro - 3.0
RETURN n.title, c.ticker, r.daily_stock, r.daily_macro
ORDER BY r.daily_stock LIMIT 20
```

### Opposite hourly vs daily returns (with NaN handling)
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE r.hourly_stock IS NOT NULL AND r.hourly_stock <> 'NaN'
  AND r.daily_stock IS NOT NULL AND r.daily_stock <> 'NaN'
WITH n, c, r, toFloat(r.hourly_stock) as hourly_return, toFloat(r.daily_stock) as daily_return
WHERE NOT isNaN(hourly_return) AND NOT isNaN(daily_return)
  AND ((hourly_return > 0 AND daily_return < 0) OR (hourly_return < 0 AND daily_return > 0))
RETURN n.title, c.ticker, hourly_return, daily_return, n.created
ORDER BY abs(hourly_return - daily_return) DESC LIMIT 20
```

### Complete return path (all levels)
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE r.daily_stock IS NOT NULL AND r.daily_industry IS NOT NULL
  AND r.daily_sector IS NOT NULL AND r.daily_macro IS NOT NULL
  AND ABS(toFloat(r.daily_stock)) > 3.0
RETURN n.title, c.ticker,
       r.daily_stock as stock_return, r.daily_industry as industry_return,
       r.daily_sector as sector_return, r.daily_macro as market_return
ORDER BY ABS(toFloat(r.daily_stock)) DESC LIMIT 20
```

### Companies with same-day report and news impact
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)
WITH c, r, date(datetime(r.created)) as report_date
MATCH (n:News)-[rel:INFLUENCES]->(c)
WHERE date(datetime(n.created)) = report_date AND rel.daily_stock IS NOT NULL
RETURN c.ticker, r.formType, n.title, rel.daily_stock
ORDER BY ABS(toFloat(rel.daily_stock)) DESC LIMIT 20
```

### News impact on SPY market index
```cypher
MATCH (n:News)-[r:INFLUENCES]->(m:MarketIndex)
WHERE m.ticker = 'SPY' AND r.daily_macro IS NOT NULL AND ABS(toFloat(r.daily_macro)) > 1.0
RETURN n.title, r.daily_macro, n.created
ORDER BY ABS(toFloat(r.daily_macro)) DESC LIMIT 20
```

### SPY daily returns from news
```cypher
MATCH (n:News)-[r:INFLUENCES]->(m:MarketIndex)
WHERE m.ticker = 'SPY' AND r.daily_macro IS NOT NULL
RETURN n.title, r.daily_macro, n.created
ORDER BY ABS(toFloat(r.daily_macro)) DESC LIMIT 20
```

### Hourly sector returns for tech vs healthcare
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE r.hourly_sector IS NOT NULL AND r.hourly_sector <> 'NaN'
  AND datetime(n.created) > datetime() - duration('P30D')
  AND (c.sector = 'Technology' OR c.sector = 'Healthcare')
WITH n, c, r, toFloat(r.hourly_sector) as hourly_sector_return
WHERE NOT isNaN(hourly_sector_return)
RETURN c.sector, n.title, c.ticker, hourly_sector_return, n.created,
       CASE WHEN hourly_sector_return > 0 THEN 'Positive'
            WHEN hourly_sector_return < 0 THEN 'Negative' ELSE 'Neutral' END as return_direction
ORDER BY c.sector, hourly_sector_return DESC LIMIT 50
```

### Companies with news outperforming macro in last 30 days
```cypher
MATCH (n:News)-[rel:INFLUENCES]->(c:Company)
WHERE datetime(n.created) > datetime() - duration('P30D')
  AND rel.daily_stock IS NOT NULL AND rel.daily_stock <> 'NaN'
  AND rel.daily_stock > rel.daily_macro AND rel.daily_macro > 0
RETURN DISTINCT c.ticker, n.title, rel.daily_stock, rel.daily_macro
ORDER BY rel.daily_stock DESC LIMIT 20
```

### Recent news with populated data (last 7 days)
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE datetime(n.created) > datetime() - duration('P7D')
  AND n.title IS NOT NULL AND n.title <> ''
  AND c.ticker IS NOT NULL AND c.ticker <> ''
  AND r.daily_stock IS NOT NULL AND r.daily_stock <> 'NaN'
WITH n, c, toFloat(r.daily_stock) as daily_return
WHERE NOT isNaN(daily_return)
RETURN n.title, c.ticker, daily_return
ORDER BY datetime(n.created) DESC LIMIT 20
```

### News events from past week with market impact
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE datetime(n.created) > datetime() - duration('P7D') AND r.daily_stock IS NOT NULL
RETURN n.title, c.ticker, r.daily_stock, n.created
ORDER BY ABS(toFloat(r.daily_stock)) DESC LIMIT 30
```

### Industries with divergent company vs industry returns
```cypher
MATCH (n:News)-[r:INFLUENCES]->(c:Company)
WHERE r.hourly_industry IS NOT NULL AND r.hourly_industry <> 'NaN'
  AND r.hourly_stock IS NOT NULL AND r.hourly_stock <> 'NaN'
  AND datetime(n.created) > datetime() - duration('P7D')
WITH n, c, r, toFloat(r.hourly_industry) as industry_return, toFloat(r.hourly_stock) as stock_return
WHERE NOT isNaN(industry_return) AND NOT isNaN(stock_return)
  AND industry_return < 0 AND stock_return > 0
RETURN DISTINCT c.industry LIMIT 100
```

## News by Market Session

### Pre-Market News Impact
```cypher
MATCH (n:News)-[rel:INFLUENCES]->(c:Company)
WHERE n.market_session = 'pre_market'
  AND ABS(rel.session_stock) > 2.0
RETURN n.title, c.ticker, n.created,
       rel.session_stock as pre_market_impact,
       rel.daily_stock as full_day_impact
ORDER BY ABS(rel.session_stock) DESC
LIMIT 20
```

### Post-Market News Impact
```cypher
MATCH (n:News)-[rel:INFLUENCES]->(c:Company)
WHERE n.market_session = 'post_market'
  AND ABS(rel.session_stock) > 2.0
RETURN n.title, c.ticker, n.created,
       rel.session_stock as post_market_impact,
       rel.daily_stock as full_day_impact
ORDER BY ABS(rel.session_stock) DESC
LIMIT 20
```

### Industry-Wide News Events
```cypher
MATCH (n:News)-[rel:INFLUENCES]->(i:Industry)
WHERE ABS(rel.daily_industry) > 2.0
RETURN n.title, i.name as industry,
       rel.daily_industry as industry_impact,
       n.created
ORDER BY ABS(rel.daily_industry) DESC
LIMIT 20
```

### Sector-Wide News Events
```cypher
MATCH (n:News)-[rel:INFLUENCES]->(s:Sector)
WHERE ABS(rel.daily_sector) > 1.0
RETURN n.title, s.name as sector,
       rel.daily_sector as sector_impact,
       n.created
ORDER BY ABS(rel.daily_sector) DESC
LIMIT 20
```

## News Around Earnings Calls
```cypher
MATCH (c:Company {ticker: $ticker})-[:HAS_TRANSCRIPT]->(t:Transcript)
WITH c, t, datetime(t.conference_datetime) as call_date
ORDER BY call_date DESC
LIMIT 1
MATCH (n:News)-[:INFLUENCES]->(c)
WHERE datetime(n.created) > call_date - duration('P2D')
  AND datetime(n.created) < call_date + duration('P2D')
RETURN n.title, n.created,
       CASE
         WHEN datetime(n.created) < call_date THEN 'Before Call'
         ELSE 'After Call'
       END as timing
ORDER BY n.created
LIMIT 20
```

## Notes
- `News.channels` is a JSON string. Use `CONTAINS` for filtering. Example: `["News", "Guidance"]`.
- `News.tags` and `News.authors` are also JSON strings.
- `News.created` and `News.updated` are ISO strings.
- `News.market_session` values: `in_market`, `pre_market`, `post_market`, `market_closed`.
- **Data gap**: 1,746 News→Company edges (0.9%) have `daily_industry` but `daily_stock` is NULL.
- Returns on INFLUENCES depend on target: Company edges have daily_stock; Sector/Industry/MarketIndex edges don't.
- Vector index: `news_vector_index` on `News.embedding` (float[]).
- Fulltext index: `news_ft` covers title, body, teaser.

## Known Data Gaps
| Date | Gap | Affected | Mitigation |
|------|-----|----------|------------|
| 2026-01-11 | Common user error: using `published_utc` instead of `created` | News date filtering | Property is `n.created` (ISO string), not `n.published_utc`. Use `date(n.created)` for date comparisons. |

---
*Version 1.1 | 2026-01-11 | Added self-improvement protocol*
