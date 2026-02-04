---
name: neo4j-xbrl
description: Query XBRL financial metrics (EPS, Revenue, etc.) from Neo4j. Use when fetching structured financial data from 10-K/10-Q filings.
---

# Neo4j XBRL Queries

Queries for XBRLNode, Fact, Concept, Context, Period, Unit, Dimension, Domain, and Member nodes.

## XBRL Labels
| Label | Count | Key properties (type) |
|------|-------|------------------------|
| **XBRLNode** | 8,189 | `id`, `report_id`, `accessionNo`, `primaryDocumentUrl` (String) |
| **Fact** | 9,930,840 | `value` (String), `is_numeric`/`is_nil` (String), `period_ref`, `unit_ref` |
| **Concept** | 467,963 | `qname`, `label`, `type_local`, `period_type` |
| **Context** | 3,021,535 | `context_id`, `period_u_id`, `member_u_ids` (String) |
| **Period** | 9,919 | `period_type`, `start_date`, `end_date` (String) |
| **Unit** | 6,146 | `name`, `namespace`, `unit_reference` (String); `is_simple_unit`/`is_divide` (String) |
| **Dimension** | 878,021 | `qname`, `label`, `network_uri` (String); `is_explicit`/`is_typed` (String) |
| **Domain** | 120,488 | `qname`, `label`, `level` (String) |
| **Member** | 1,240,344 | `qname`, `label`, `level` (String) |
| **Abstract** | 50,354 | `label`, `qname` (String) |

## XBRL Relationships
HAS_XBRL, REPORTS, HAS_CONCEPT, IN_CONTEXT, HAS_PERIOD, HAS_UNIT, FACT_MEMBER, FACT_DIMENSION,
HAS_DOMAIN, HAS_MEMBER, PARENT_OF, PRESENTATION_EDGE, CALCULATION_EDGE, FOR_COMPANY.

## When to Use XBRL vs Non-XBRL
- **Need numeric metrics (EPS, revenue)**: Use XBRL (10-K/10-Q only).
- **Need narrative or 8-K**: Use ExtractedSectionContent or ExhibitContent.
- **8-K has no XBRL**: Use sections/exhibits instead.

## Basic XBRL Queries

### Get XBRL node for report
```cypher
MATCH (r:Report {id: $report_id})-[:HAS_XBRL]->(x:XBRLNode)
RETURN x.id, x.accessionNo, x.primaryDocumentUrl
```

### XBRL reports for company
```cypher
MATCH (r:Report)-[:PRIMARY_FILER]->(c:Company {ticker: $ticker})
WHERE r.formType IN ['10-K', '10-Q']
MATCH (r)-[:HAS_XBRL]->(x:XBRLNode)
RETURN r.id, r.formType, r.periodOfReport, x.id
ORDER BY r.periodOfReport DESC
```

## Financial Metrics

### XBRL metrics (EPS and Revenue, context-safe)
```cypher
MATCH (r:Report)-[:PRIMARY_FILER]->(c:Company {ticker: $ticker})
WHERE r.formType IN ['10-K','10-Q']
WITH r ORDER BY r.periodOfReport DESC LIMIT 1
MATCH (r)-[:HAS_XBRL]->(x:XBRLNode)<-[:REPORTS]-(f:Fact)
MATCH (f)-[:IN_CONTEXT]->(:Context)
MATCH (f)-[:HAS_CONCEPT]->(con:Concept)
WHERE con.qname IN [
  'us-gaap:EarningsPerShareDiluted',
  'us-gaap:EarningsPerShareBasic',
  'us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',
  'us-gaap:Revenues'
]
  AND f.is_numeric = '1'
RETURN con.qname, con.label, f.value, f.period_ref
```

### Get specific metric
```cypher
MATCH (r:Report)-[:PRIMARY_FILER]->(c:Company {ticker: $ticker})
WHERE r.formType IN ['10-K','10-Q']
WITH r ORDER BY r.periodOfReport DESC LIMIT 1
MATCH (r)-[:HAS_XBRL]->(x:XBRLNode)<-[:REPORTS]-(f:Fact)
MATCH (f)-[:IN_CONTEXT]->(:Context)
MATCH (f)-[:HAS_CONCEPT]->(con:Concept)
WHERE con.qname = $concept_qname  // e.g., 'us-gaap:NetIncomeLoss'
  AND f.is_numeric = '1'
RETURN con.label, toFloat(f.value) AS value, f.period_ref
```

### Multiple metrics from latest filing
```cypher
MATCH (r:Report)-[:PRIMARY_FILER]->(c:Company {ticker: $ticker})
WHERE r.formType IN ['10-K','10-Q']
WITH r ORDER BY r.periodOfReport DESC LIMIT 1
MATCH (r)-[:HAS_XBRL]->(x:XBRLNode)<-[:REPORTS]-(f:Fact)
MATCH (f)-[:IN_CONTEXT]->(:Context)
MATCH (f)-[:HAS_CONCEPT]->(con:Concept)
WHERE con.qname IN $concept_list  // Pass list of qnames
  AND f.is_numeric = '1'
RETURN con.qname, con.label, toFloat(f.value) AS value, f.period_ref
```

## Total vs Segmented Values

### Total only (no dimensions)
```cypher
MATCH (f:Fact)-[:HAS_CONCEPT]->(con:Concept)
WHERE con.label CONTAINS 'Revenue'
  AND f.is_numeric = '1'
  AND NOT EXISTS((f)-[:FACT_MEMBER]->())
RETURN con.label, f.value LIMIT 10
```

### With dimensions (segmented)
```cypher
MATCH (f:Fact)-[:FACT_MEMBER]->(m:Member)
MATCH (f)-[:HAS_CONCEPT]->(con:Concept)
WHERE con.label CONTAINS 'Revenue'
  AND f.is_numeric = '1'
RETURN m.label AS segment, con.label, f.value LIMIT 10
```

### Segment breakdown for metric
```cypher
MATCH (r:Report)-[:PRIMARY_FILER]->(c:Company {ticker: $ticker})
WHERE r.formType IN ['10-K','10-Q']
WITH r ORDER BY r.periodOfReport DESC LIMIT 1
MATCH (r)-[:HAS_XBRL]->(x:XBRLNode)<-[:REPORTS]-(f:Fact)
MATCH (f)-[:HAS_CONCEPT]->(con:Concept)
WHERE con.qname = $concept_qname
  AND f.is_numeric = '1'
OPTIONAL MATCH (f)-[:FACT_MEMBER]->(m:Member)
RETURN con.label, m.label AS segment, toFloat(f.value) AS value, f.period_ref
ORDER BY segment
```

## Context and Period

### Facts with period details
```cypher
MATCH (f:Fact)-[:IN_CONTEXT]->(ctx:Context)-[:HAS_PERIOD]->(p:Period)
MATCH (f)-[:HAS_CONCEPT]->(con:Concept)
WHERE con.qname = $concept_qname
RETURN con.label, f.value, p.period_type, p.start_date, p.end_date
```

### Facts for specific period
```cypher
MATCH (f:Fact)-[:IN_CONTEXT]->(ctx:Context)-[:HAS_PERIOD]->(p:Period)
WHERE p.end_date = $period_end_date
  AND p.period_type = 'duration'
MATCH (f)-[:HAS_CONCEPT]->(con:Concept)
WHERE f.is_numeric = '1'
RETURN con.qname, con.label, toFloat(f.value) AS value
LIMIT 50
```

## Dimension Analysis

### Get dimensions for a fact
```cypher
MATCH (f:Fact)-[:FACT_DIMENSION]->(dim:Dimension)
MATCH (f)-[:FACT_MEMBER]->(m:Member)
MATCH (f)-[:HAS_CONCEPT]->(con:Concept)
WHERE f.id = $fact_id
RETURN con.label, dim.label AS dimension, m.label AS member, f.value
```

### Available dimensions for concept
```cypher
MATCH (f:Fact)-[:HAS_CONCEPT]->(con:Concept {qname: $concept_qname})
MATCH (f)-[:FACT_DIMENSION]->(dim:Dimension)
RETURN DISTINCT dim.qname, dim.label
```

## Fulltext Search

### Search concepts
```cypher
CALL db.index.fulltext.queryNodes('concept_ft', $query)
YIELD node, score
RETURN node.qname, node.label, score
ORDER BY score DESC
LIMIT 20
```

### Search fact values (text blocks)
```cypher
CALL db.index.fulltext.queryNodes('fact_textblock_ft', $query)
YIELD node, score
RETURN node.qname, substring(node.value, 0, 300), score
ORDER BY score DESC
LIMIT 10
```

## Common Concepts (qnames)

### Income Statement
- `us-gaap:Revenues`
- `us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax`
- `us-gaap:CostOfGoodsAndServicesSold`
- `us-gaap:GrossProfit`
- `us-gaap:OperatingIncomeLoss`
- `us-gaap:NetIncomeLoss`
- `us-gaap:EarningsPerShareBasic`
- `us-gaap:EarningsPerShareDiluted`

### Balance Sheet
- `us-gaap:Assets`
- `us-gaap:Liabilities`
- `us-gaap:StockholdersEquity`
- `us-gaap:CashAndCashEquivalentsAtCarryingValue`
- `us-gaap:AccountsReceivableNetCurrent`
- `us-gaap:InventoryNet`
- `us-gaap:LongTermDebt`

### Cash Flow
- `us-gaap:NetCashProvidedByUsedInOperatingActivities`
- `us-gaap:NetCashProvidedByUsedInInvestingActivities`
- `us-gaap:NetCashProvidedByUsedInFinancingActivities`
- `us-gaap:PaymentsOfDividends`
- `us-gaap:PaymentsForRepurchaseOfCommonStock`

## Data Analysis

### XBRL processing status distribution
```cypher
MATCH (r:Report) WHERE r.xbrl_status IS NOT NULL
RETURN r.xbrl_status, COUNT(r) as count ORDER BY count DESC
```

### Period type distribution
```cypher
MATCH (p:Period) RETURN p.period_type, COUNT(p) as count ORDER BY count DESC
```

### Facts by numeric status
```cypher
MATCH (f:Fact) RETURN f.is_numeric, COUNT(f) as count ORDER BY count DESC
```

### Top concepts by fact count
```cypher
MATCH (f:Fact)-[:HAS_CONCEPT]->(c:Concept)
RETURN c.label, COUNT(f) as fact_count ORDER BY fact_count DESC LIMIT 20
```

### Context structures coverage
```cypher
MATCH (ctx:Context)
RETURN COUNT(ctx) as total_contexts,
       COUNT(ctx.period_u_id) as has_period,
       COUNT(ctx.member_u_ids) as has_members
```

### Dimensions with domain counts
```cypher
MATCH (d:Dimension) OPTIONAL MATCH (d)-[:HAS_DOMAIN]->(dom)
RETURN d.name, d.label, COUNT(dom) as domain_count
ORDER BY domain_count DESC LIMIT 20
```

### Reports with XBRL by form type
```cypher
MATCH (r:Report)-[:HAS_XBRL]->(x:XBRLNode)
RETURN r.formType, COUNT(DISTINCT r) as report_count ORDER BY report_count DESC
```

### Recent 10-K XBRL with filing returns
```cypher
MATCH (c:Company)<-[pf:PRIMARY_FILER]-(r:Report)-[:HAS_XBRL]->(x:XBRLNode)
WHERE r.formType = '10-K' AND datetime(r.created) > datetime() - duration('P180D')
RETURN c.ticker, r.created, r.accessionNo, pf.daily_stock as filing_day_return
ORDER BY r.created DESC LIMIT 20
```

### Count total XBRL nodes
```cypher
MATCH (x:XBRLNode) RETURN COUNT(x) as total_xbrl_nodes
```

### Companies with recent completed XBRL filings
```cypher
MATCH (c:Company)<-[:PRIMARY_FILER]-(r:Report)
WHERE r.xbrl_status = 'COMPLETED' AND datetime(r.created) > datetime() - duration('P90D')
RETURN c.ticker, r.formType, r.xbrl_status, r.created
ORDER BY r.created DESC LIMIT 20
```

### Facts with non-null values
```cypher
MATCH (f:Fact) WHERE f.value IS NOT NULL AND f.value <> '0'
RETURN f.qname, f.value, f.is_numeric LIMIT 20
```

### Facts with numeric values
```cypher
MATCH (f:Fact) WHERE f.is_numeric = '1' AND f.value IS NOT NULL AND f.value <> '0'
RETURN f.qname, f.value, f.decimals LIMIT 20
```

### Instant vs duration period counts
```cypher
MATCH (p:Period)
RETURN p.period_type, COUNT(p) as count
ORDER BY count DESC
```

### Measurement units in use
```cypher
MATCH (u:Unit)
RETURN u.name, u.unit_reference, COUNT(u) as usage_count
ORDER BY usage_count DESC LIMIT 20
```

### Common US-GAAP financial concepts
```cypher
MATCH (c:Concept) WHERE c.qname STARTS WITH 'us-gaap:'
RETURN DISTINCT c.qname, c.label ORDER BY c.qname LIMIT 30
```

### XBRL nodes with report information
```cypher
MATCH (r:Report)-[:HAS_XBRL]->(x:XBRLNode)
WHERE r.formType IN ['10-K', '10-Q']
RETURN r.formType, r.accessionNo, x.id, x.cik LIMIT 20
```

## Notes
- **Fact.value** is String even for numeric facts; use `toFloat()` when `is_numeric='1'`.
- **is_numeric/is_nil** are string booleans ('0'/'1').
- **Dimension.is_explicit/is_typed** are string booleans ('0'/'1').
- **Unit.is_simple_unit/is_divide** are string booleans ('0'/'1').
- **Some Facts lack Context**: 12,939 Facts have no `IN_CONTEXT` relationship; filter with `MATCH (f)-[:IN_CONTEXT]->(:Context)`.
- **Period.end_date** can be string 'null' for `period_type='instant'` (2,776 rows).
- **XBRL only in 10-K/10-Q**: 8-K filings have no XBRL data.
- Fulltext indexes: `concept_ft` (label/qname), `fact_textblock_ft` (value/qname), `abstract_ft` (label).

## Known Data Gaps
| Date | Gap | Affected | Mitigation |
|------|-----|----------|------------|
| 2026-01-11 | Revenue values comma-formatted | HRL Revenue facts | Use `f.value` as string; `toFloat()` fails on "2,898,810,000" |

---
*Version 1.1 | 2026-01-11 | Added self-improvement protocol*
