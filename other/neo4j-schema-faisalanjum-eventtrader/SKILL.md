---
name: neo4j-schema
description: Core Neo4j schema reference with all labels, relationships, data types, and indexes. Use when exploring database structure, checking field types, or understanding the financial knowledge graph schema.
---

# Neo4j Schema Reference

## Scope and Validation
- Validated on 2026-01-04 against bolt://localhost:30687 (Neo4j 5.26.4).
- Counts from: `CALL db.stats.retrieve('GRAPH COUNTS')`.
- Types from: `CALL apoc.meta.nodeTypeProperties` and `CALL apoc.meta.relTypeProperties`.
- Counts are for orientation only (data coverage), not for logic.

## Read This First (No Assumptions)
1. **Returns live on relationships**, not nodes: `PRIMARY_FILER`, `INFLUENCES`, `REFERENCED_IN`.
2. **All timestamps are Strings** (Report.created, News.created, Transcript.conference_datetime, Date.*).
3. **JSON is stored as Strings** (Report.items, Report.exhibit_contents, Report.extracted_sections, News.channels/tags/authors).
4. **Numeric-looking fields are Strings** (Company.mkt_cap, Company.shares_out, Company.employees, Fact.value).
5. **XBRL booleans are Strings**: Fact.is_numeric/is_nil, Dimension.is_explicit/is_typed, Unit.is_simple_unit/is_divide.
6. **Returns are percentages** (5.06 means 5.06%, not 0.0506).
7. **INFLUENCES alias trap**: using `inf` as the alias breaks (`inf` is treated as infinity). Use `r`.
8. **NaN exists** in return fields (PRIMARY_FILER: 4 rows; INFLUENCES: 1 row). Filter with `isNaN()`.
9. **hourly_stock is usually Float** but appears once as `LIST OF FLOAT` on PRIMARY_FILER; handle list-or-float.
10. **Some Facts lack Context**: 12,939 Facts have no `IN_CONTEXT` relationship; exclude unless needed.
11. **Period end_date can be string 'null'** for `period_type='instant'` (2,776 rows).

## Schema Discovery (Run First If Unsure)
```cypher
CALL db.labels() YIELD label RETURN label ORDER BY label
CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType ORDER BY relationshipType
CALL apoc.meta.schema()
```

## Core Labels (Counts + Key Properties)

### Event + Company
| Label | Count | Key properties (type) |
|------|-------|------------------------|
| **Report** | 33,947 | `id`, `accessionNo`, `formType`, `created` (String); `items` (String JSON); `market_session` |
| **Company** | 796 | `ticker`, `symbol`, `name` (String); `mkt_cap`/`shares_out`/`employees` (String) |
| **News** | 186,206 | `title`/`teaser`/`body` (String); `channels`/`tags`/`authors` (String JSON); `created`/`updated` (String) |
| **Transcript** | 4,387 | `id`, `conference_datetime`, `created`/`updated` (String); `fiscal_quarter`/`fiscal_year` |
| **QAExchange** | 79,651 | `exchanges`, `questioner`/`responders`, `sequence` (String); `embedding` (float[]) |
| **PreparedRemark** | 4,253 | `content` (String) |
| **Dividend** | 4,282 | `declaration_date`, `cash_amount`, `dividend_type` (String) |
| **Split** | 33 | `execution_date`, `split_from`, `split_to` (String) |

### Market + Calendar
| Label | Count | Key properties (type) |
|------|-------|------------------------|
| **MarketIndex** | 1 | `name`, `ticker`, `etf` (String) |
| **Sector** | 11 | `name`, `etf` (String) |
| **Industry** | 115 | `name`, `etf` (String) |
| **Date** | 946 | `date`, `is_trading_day`, `market_open_*`, `market_close_*`, `pre_market_*`, `post_market_*` (String) |

## Relationship Overview (Counts + Purpose)

### Returns and Impact
| Relationship | Count | Notes |
|-------------|-------|-------|
| **PRIMARY_FILER** | 32,942 | `Report -> Company`. Returns stored here (Double). |
| **INFLUENCES** | 864,234 | `News/Transcript/Report -> Company/Sector/Industry/MarketIndex`. Returns stored here (Double). |
| **REFERENCED_IN** | 1,075 | `Report -> Company`. Returns often populated (1,010/1,075). |
| **HAS_PRICE** | 551,563 | `Date -> Company/Sector/Industry/MarketIndex`. OHLCV on relationship. |

### Event Content
HAS_SECTION (Report -> ExtractedSectionContent), HAS_EXHIBIT, HAS_FINANCIAL_STATEMENT, HAS_FILING_TEXT,
HAS_TRANSCRIPT, HAS_QA_EXCHANGE, HAS_PREPARED_REMARKS, HAS_FULL_TEXT, HAS_QA_SECTION, NEXT_EXCHANGE,
IN_CATEGORY (Report -> AdminReport), HAS_SUB_REPORT.

### Company Classification and Actions
BELONGS_TO, RELATED_TO (properties: relationship_type, source_ticker, target_ticker, bidirectional),
DECLARED_DIVIDEND, HAS_DIVIDEND, DECLARED_SPLIT, HAS_SPLIT, NEXT (Date -> Date).

## Returns: What Lives Where (Validated Counts)

INFLUENCES returns depend on target label:
- **To Company**: total 190,593; daily_stock 188,806; daily_industry 190,363; daily_sector 190,593; daily_macro 190,593.
- **To Industry**: total 224,561; daily_industry 224,304; daily_stock 0.
- **To Sector**: total 224,540; daily_sector 224,540; daily_stock 0.
- **To MarketIndex**: total 224,540; daily_macro 224,540; daily_stock 0.

**Rule**: Use the Company-target INFLUENCES edge if you want both stock and benchmark returns on one relationship.

- **daily_stock only on Company targets**: By design, Sector/Industry/MarketIndex edges don't have daily_stock.
- **Data gaps**: Some Company edges missing daily_stock (News: 1,746; Transcript: 41).

## Data Type Alerts and Anomalies (Validated)
- **Report.items** is JSON string. Example: `["Item 2.02: Results of Operations and Financial Condition", "Item 9.01: Financial Statements and Exhibits"]`.
- **News.channels** is JSON string. Example: `["News", "Guidance"]`.
- **Report.created** is ISO string with TZ. Example: `2023-01-04T13:48:33-05:00`.
- **NaN returns** exist. Use `WHERE r.daily_stock IS NOT NULL AND NOT isNaN(r.daily_stock)`.
- **hourly_stock** appears once as list-of-float on PRIMARY_FILER; handle list-or-float.

## Indexes and Search Capabilities
- Range/unique indexes: `Report.id`, `News.id`, `Transcript.id`, `Company.id`.
- Fulltext: `abstract_ft` (Abstract.label), `concept_ft` (Concept.label/qname), `company_ft` (Company.name/displayLabel),
  `exhibit_content_ft` (ExhibitContent.content/exhibit_number), `extracted_section_content_ft` (ExtractedSectionContent.content/section_name),
  `fact_textblock_ft` (Fact.value/qname), `filing_text_content_ft` (FilingTextContent.content/form_type),
  `financial_statement_content_ft` (FinancialStatementContent.value/statement_type), `full_transcript_ft` (FullTranscriptText.content),
  `news_ft` (News.title/body/teaser), `prepared_remarks_ft` (PreparedRemark.content), `qa_exchange_ft` (QAExchange.exchanges),
  `question_answer_ft` (QuestionAnswer.content), `search` (Memory.name/type/observations).
- Vector: `news_vector_index` (News.embedding), `qaexchange_vector_idx` (QAExchange.embedding).
- No index on `Company.ticker`. Company count is small; exact match scans are acceptable.

**Generic fulltext query**:
```cypher
CALL db.index.fulltext.queryNodes($index_name, $query)
YIELD node, score
RETURN labels(node), node.id, score
ORDER BY score DESC
LIMIT 20
```

## IGNORE these Labels and Relationships (0 count)
**Labels**: AdminSection, FinancialStatement, Guidance, HyperCube, LineItems, Other, Memory, XBRLMapping, ExtractionPattern, ConceptMapping,
GeoMapping, ProductMapping, ConceptPattern, GeoPattern, MetricRule, GeoRule, Extraction, Pattern, NewsExtraction, TranscriptExtraction,
TestAbstract, TestFact, Framework, ConceptGroup, Benefit, Tutorial, LearningStep, ExampleApplication, _Bloom_Perspective_, _Bloom_Scene_,
TestNode, TestContentNode_1754141732.
**Relationships**: HAS_EXTRACTION, MAPS_TO_FACT, COULD_MAP_TO_REAL_FACT, POTENTIAL_XBRL_MATCH, TEST_REL, TEST_EDGE, REFERENCES, _Bloom_HAS_SCENE_.

## Validation Queries (Re-run if DB changes)
```cypher
CALL db.stats.retrieve('GRAPH COUNTS')

CALL apoc.meta.nodeTypeProperties({includeLabels: ['Report','Company','News','Transcript','Fact','Concept','XBRLNode']})
CALL apoc.meta.relTypeProperties({includeRels: ['PRIMARY_FILER','INFLUENCES','REFERENCED_IN','HAS_PRICE']})

MATCH (n:News)-[r:INFLUENCES]->(:Company)
WHERE r.daily_stock IS NULL AND r.daily_industry IS NOT NULL
RETURN count(r) AS news_anomaly_count

MATCH ()-[r:PRIMARY_FILER]->()
WHERE r.hourly_stock IS NOT NULL
RETURN apoc.meta.cypher.type(r.hourly_stock) as t, count(*) as c
```

## Domain Query Skills

For query patterns beyond schema discovery, see these specialized skills:

| Skill | Scope | Key Queries |
|-------|-------|-------------|
| **neo4j-entity** | Company, Sector, Industry, MarketIndex, prices, dividends, splits | Company lookups, price series, dividend/split history, market relationships |
| **neo4j-report** | Report (8-K/10-K/10-Q), sections, exhibits, financial statements | Filing searches, Item 2.02 earnings, press releases (EX-99.1), PRIMARY_FILER returns |
| **neo4j-news** | News articles, INFLUENCES returns, fulltext/vector search | News impact analysis, return divergence, market movers, embedding coverage |
| **neo4j-transcript** | Transcript, QAExchange, PreparedRemark | Earnings calls, Q&A searches, analyst questions, embedding queries |
| **neo4j-xbrl** | XBRLNode, Fact, Concept, Context, Period, Unit, Dimension | Financial metrics (EPS, Revenue), segment analysis, period types |

**Usage**: Load `neo4j-schema` + domain skill for targeted queries. Schema provides structure; domain skills provide patterns.

## Known Data Gaps
| Date | Gap | Affected | Mitigation |
|------|-----|----------|------------|
| 2026-01-11 | Property is `formType` not `form_type` (camelCase) | Report queries | Use `r.formType` not `r.form_type` |
| 2026-01-11 | `get_neo4j_schema` shows incomplete relationship targets | Schema queries | Verify: `MATCH ()-[r:TYPE]->(t) RETURN DISTINCT labels(t)` |

---
*Version 3.4 | 2026-01-11 | Added self-improvement protocol*
