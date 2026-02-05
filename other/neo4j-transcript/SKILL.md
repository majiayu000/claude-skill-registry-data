---
name: neo4j-transcript
description: Query earnings call transcripts, Q&A exchanges, and prepared remarks from Neo4j. Use when fetching transcript or earnings call data.
---

# Neo4j Transcript Queries

Queries for Transcript, QAExchange, PreparedRemark, and related content.

## Transcript Content Labels
| Label | Count | Key properties | Relationship |
|-------|-------|----------------|--------------|
| **FullTranscriptText** | 28 | `content` | Transcript-[:HAS_FULL_TEXT]-> |
| **QuestionAnswer** | 41 | `content`, `speaker_roles` | Transcript-[:HAS_QA_SECTION]-> |

**Note**: Company-[:HAS_TRANSCRIPT]->Transcript (4,387) links companies to their earnings calls.

## Basic Transcript Queries

### Transcripts for company
```cypher
MATCH (t:Transcript)-[:INFLUENCES]->(c:Company {ticker: $ticker})
RETURN t.id, t.conference_datetime, t.fiscal_quarter, t.fiscal_year, t.company_name
ORDER BY t.conference_datetime DESC
```

### Transcripts in date range
```cypher
MATCH (t:Transcript)-[:INFLUENCES]->(c:Company {ticker: $ticker})
WHERE t.conference_datetime >= $start_date AND t.conference_datetime <= $end_date
RETURN t.id, t.conference_datetime, t.fiscal_quarter, t.fiscal_year
ORDER BY t.conference_datetime
```

### Latest transcript for company
```cypher
MATCH (t:Transcript)-[:INFLUENCES]->(c:Company {ticker: $ticker})
RETURN t.id, t.conference_datetime, t.fiscal_quarter, t.fiscal_year
ORDER BY t.conference_datetime DESC
LIMIT 1
```

## Q&A Exchanges

### Q&A exchanges for transcript
```cypher
MATCH (t:Transcript {id: $transcript_id})-[:HAS_QA_EXCHANGE]->(qa:QAExchange)
RETURN qa.questioner, qa.questioner_title, qa.responders, qa.responder_title, qa.exchanges
ORDER BY toInteger(qa.sequence)
```

### Q&A with pagination
```cypher
MATCH (t:Transcript {id: $transcript_id})-[:HAS_QA_EXCHANGE]->(qa:QAExchange)
RETURN qa.questioner, qa.questioner_title, qa.exchanges
ORDER BY toInteger(qa.sequence)
SKIP $offset
LIMIT $limit
```

### Follow exchange chain
```cypher
MATCH (t:Transcript {id: $transcript_id})-[:HAS_QA_EXCHANGE]->(first:QAExchange)
WHERE first.sequence = '1'
MATCH path = (first)-[:NEXT_EXCHANGE*0..10]->(qa:QAExchange)
RETURN qa.sequence, qa.questioner, qa.exchanges
ORDER BY toInteger(qa.sequence)
```

### Search Q&A by questioner
```cypher
MATCH (t:Transcript)-[:INFLUENCES]->(c:Company {ticker: $ticker})
MATCH (t)-[:HAS_QA_EXCHANGE]->(qa:QAExchange)
WHERE qa.questioner CONTAINS $analyst_name
RETURN t.conference_datetime, qa.questioner, qa.questioner_title, qa.exchanges
ORDER BY t.conference_datetime DESC
```

## Prepared Remarks

### Prepared remarks for transcript
```cypher
MATCH (t:Transcript {id: $transcript_id})-[:HAS_PREPARED_REMARKS]->(pr:PreparedRemark)
RETURN pr.content
```

### Full transcript text
```cypher
MATCH (t:Transcript {id: $transcript_id})-[:HAS_FULL_TEXT]->(ft:FullTranscriptText)
RETURN ft.content
```

## Fulltext Search

### Search Q&A exchanges
```cypher
CALL db.index.fulltext.queryNodes('qa_exchange_ft', $query)
YIELD node, score
RETURN node.questioner, node.exchanges, score
ORDER BY score DESC
LIMIT 20
```

### Search Q&A for company
```cypher
CALL db.index.fulltext.queryNodes('qa_exchange_ft', $query)
YIELD node, score
MATCH (t:Transcript)-[:HAS_QA_EXCHANGE]->(node)
MATCH (t)-[:INFLUENCES]->(c:Company {ticker: $ticker})
RETURN t.conference_datetime, node.questioner, node.exchanges, score
ORDER BY score DESC
LIMIT 20
```

### Search prepared remarks
```cypher
CALL db.index.fulltext.queryNodes('prepared_remarks_ft', $query)
YIELD node, score
RETURN substring(node.content, 0, 500), score
ORDER BY score DESC
LIMIT 10
```

### Search full transcripts
```cypher
CALL db.index.fulltext.queryNodes('full_transcript_ft', $query)
YIELD node, score
RETURN substring(node.content, 0, 500), score
ORDER BY score DESC
LIMIT 10
```

## Vector Search

### Semantic search Q&A exchanges
```cypher
CALL db.index.vector.queryNodes('qaexchange_vector_idx', $k, $embedding)
YIELD node, score
RETURN node.questioner, node.exchanges, score
ORDER BY score DESC
```

### Semantic search Q&A for company
```cypher
CALL db.index.vector.queryNodes('qaexchange_vector_idx', $k, $embedding)
YIELD node, score
MATCH (t:Transcript)-[:HAS_QA_EXCHANGE]->(node)
MATCH (t)-[:INFLUENCES]->(c:Company {ticker: $ticker})
RETURN t.conference_datetime, node.questioner, node.exchanges, score
ORDER BY score DESC
```

## Transcript with Returns

### Transcript impact on stock
```cypher
MATCH (t:Transcript)-[r:INFLUENCES]->(c:Company {ticker: $ticker})
WHERE t.conference_datetime >= $start_date AND t.conference_datetime <= $end_date
RETURN t.id, t.conference_datetime,
       r.daily_stock, r.daily_industry, r.daily_sector, r.daily_macro
ORDER BY t.conference_datetime
```

## Data Analysis

### Analyze Q&A exchange sequences
```cypher
MATCH (qa1:QAExchange)-[:NEXT_EXCHANGE]->(qa2:QAExchange)
WHERE qa1.questioner IS NOT NULL AND qa2.questioner IS NOT NULL
RETURN qa1.questioner, qa1.sequence, qa2.questioner, qa2.sequence, qa1.transcript_id
LIMIT 20
```

### Count Q&A exchanges with embeddings
```cypher
MATCH (qa:QAExchange) WHERE qa.embedding IS NOT NULL
RETURN COUNT(qa) as embedded_qa_count
```

### Q&A exchanges with embeddings sample
```cypher
MATCH (qa:QAExchange) WHERE qa.embedding IS NOT NULL
RETURN qa.questioner, qa.sequence, qa.transcript_id LIMIT 20
```

### Q&A embedding dimensions
```cypher
MATCH (qa:QAExchange) WHERE qa.embedding IS NOT NULL
WITH qa, SIZE(qa.embedding) as embedding_size
RETURN COUNT(qa) as qa_with_embeddings, MIN(embedding_size) as min_size, MAX(embedding_size) as max_size
LIMIT 1
```

### Recent earnings call transcripts (via HAS_TRANSCRIPT)
```cypher
MATCH (c:Company)-[:HAS_TRANSCRIPT]->(t:Transcript)
WHERE datetime(t.created) > datetime() - duration('P90D')
RETURN c.ticker, t.company_name, t.conference_datetime, t.fiscal_quarter
ORDER BY t.created DESC LIMIT 20
```

### Recent earnings calls by conference date
```cypher
MATCH (c:Company)-[:HAS_TRANSCRIPT]->(t:Transcript)
WHERE t.conference_datetime IS NOT NULL
RETURN c.ticker, t.company_name, t.conference_datetime, t.fiscal_quarter, t.fiscal_year
ORDER BY t.conference_datetime DESC LIMIT 20
```

### Recent earnings transcripts with fiscal info
```cypher
MATCH (c:Company)-[:HAS_TRANSCRIPT]->(t:Transcript)
WHERE datetime(t.created) > datetime() - duration('P90D')
RETURN c.ticker, t.company_name, t.conference_datetime, t.fiscal_quarter, t.fiscal_year
ORDER BY t.created DESC LIMIT 20
```

## Transcript Impact Analysis

### Transcripts with Negative Stock Reaction
```cypher
MATCH (t:Transcript)-[rel:INFLUENCES]->(c:Company)
WHERE rel.daily_stock < -3.0
  AND rel.daily_stock IS NOT NULL
RETURN c.ticker, t.conference_datetime,
       rel.daily_stock as stock_return,
       rel.daily_macro as market_return,
       rel.daily_stock - rel.daily_macro as excess_return
ORDER BY rel.daily_stock
LIMIT 20
```

### Positive Earnings Call Reactions
```cypher
MATCH (t:Transcript)-[rel:INFLUENCES]->(c:Company)
WHERE rel.session_stock > 5.0
  AND rel.session_stock IS NOT NULL
RETURN c.ticker, t.conference_datetime,
       rel.session_stock as session_return,
       rel.daily_stock as daily_return
ORDER BY rel.session_stock DESC
LIMIT 20
```

### Recent Earnings Calls Across Market
```cypher
MATCH (c:Company)-[:HAS_TRANSCRIPT]->(t:Transcript)
WHERE datetime(t.conference_datetime) > datetime() - duration('P30D')
RETURN c.ticker, c.name, t.conference_datetime,
       t.fiscal_quarter, t.fiscal_year
ORDER BY datetime(t.conference_datetime) DESC
LIMIT 20
```

## Notes
- **Two relationships connect Transcripts to Companies**:
  - `INFLUENCES`: Has return data (daily_stock, session_stock, hourly_stock, daily_macro, etc.)
  - `HAS_TRANSCRIPT`: Navigation only (no properties). Use for simple lookups.
- `Transcript.conference_datetime` is an ISO string.
- `QAExchange.sequence` is a String; use `toInteger()` for ordering.
- `QAExchange.exchanges` contains the full Q&A text as a string.
- `QAExchange.embedding` is a float[] for vector search.
- **Data gap**: 41 Transcript→Company edges (0.9%) have `daily_industry` but `daily_stock` is NULL.
- Fulltext indexes: `qa_exchange_ft`, `prepared_remarks_ft`, `full_transcript_ft`.
- Vector index: `qaexchange_vector_idx` on `QAExchange.embedding`.
- `NEXT_EXCHANGE` relationship chains Q&A exchanges in order.

## Known Data Gaps
| Date | Gap | Affected | Mitigation |
|------|-----|----------|------------|
| 2026-01-11 | Common user error: wrong schema for transcripts | Transcript queries | Use `:INFLUENCES` or `:HAS_TRANSCRIPT` (not `:COMPANY`), `conference_datetime` (not `event_datetime`), `:HAS_QA_EXCHANGE` (not `:HAS_EXCHANGE`), `:QAExchange` (not `:Exchange`), `:PreparedRemark` (not `:PreparedRemarks`). |

---
*Version 1.1 | 2026-01-11 | Added self-improvement protocol*
