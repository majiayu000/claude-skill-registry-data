---
name: bookstrap-query
description: Execute ad-hoc database queries to explore the book's knowledge base using natural language questions that translate to semantic search, graph traversal, timeline queries, or hybrid queries
argument-hint: [natural language question]
disable-model-invocation: true
allowed-tools: Bash, Read
---

# /bookstrap-query - Ad-hoc Database Exploration

Execute ad-hoc queries against the Bookstrap database for exploration and verification. This command accepts natural language questions and translates them into appropriate SurrealDB queries (semantic search, graph traversal, timeline queries, or hybrid combinations) to retrieve and format results.

## Purpose

Enable interactive exploration of the book's knowledge base. Useful for:
- Understanding what the database knows about specific topics
- Verifying source coverage for claims
- Exploring character relationships and appearances
- Checking timeline consistency
- Finding related content and entities
- Debugging knowledge gaps

## Input Arguments

Accept a natural language question about the book's content, entities, or sources:

```
/bookstrap-query What do we know about Anna's time in Lyon?
/bookstrap-query Show me all scenes with character:erik
/bookstrap-query What sources support the claim about wireless protocols?
/bookstrap-query Timeline of events in chapter 3
```

## Query Translation

Analyze the natural language question to determine the appropriate query type:

### 1. Semantic Search Queries

**Indicators**: "What do we know about", "Find information on", "Tell me about", "Show content related to"

**Translation Pattern**:
```surql
-- Semantic search for theme/topic
SELECT * FROM section
WHERE embedding <|5|> $query_vector
ORDER BY vector::similarity(embedding, $query_vector) DESC;
```

Generate embedding for the user's question, then search for similar content.

**Example**:
```
User: "What do we know about Anna's time in Lyon?"

1. Generate embedding for "Anna's time in Lyon"
2. Execute semantic search across sections and sources
3. Return top matches with similarity scores
```

### 2. Graph Traversal Queries

**Indicators**: "Show relationships", "Who knows", "What appears in", "Connected to", "Related entities"

**Translation Pattern**:
```surql
-- Character relationships and appearances
SELECT
  ->appears_in->section.content,
  ->knows->character.name,
  ->knows->character.description
FROM character:anna;

-- Source support chain
SELECT
  <-supports<-source.title,
  <-supports<-source.reliability,
  <-supports<-source.url
FROM concept:wireless_protocols;
```

**Example**:
```
User: "Show me all scenes with character:erik"

SELECT
  section.content,
  section.chapter,
  section.sequence
FROM character:erik->appears_in->section
ORDER BY section.sequence;
```

### 3. Timeline Queries

**Indicators**: "Timeline", "Chronological", "Before", "After", "Sequence", "Order of events"

**Translation Pattern**:
```surql
-- Events before a point
SELECT * FROM event
WHERE sequence < $current_sequence
ORDER BY sequence DESC
LIMIT 10;

-- Chronological section order
SELECT * FROM section
WHERE chapter = $chapter
ORDER BY sequence;
```

**Example**:
```
User: "Timeline of events in chapter 3"

SELECT
  event.name,
  event.description,
  event.sequence,
  event.date
FROM event
WHERE ->located_in->section.chapter = 3
ORDER BY event.sequence;
```

### 4. Source Citation Queries

**Indicators**: "What sources", "Citations for", "Where is this from", "Support for", "References"

**Translation Pattern**:
```surql
-- Find sources supporting a claim or concept
SELECT
  source.title,
  source.url,
  source.reliability,
  source.source_type
FROM source
WHERE embedding <|5|> $query_vector
ORDER BY vector::similarity(embedding, $query_vector) DESC;

-- Or for specific concept
SELECT
  <-supports<-source.title,
  <-supports<-source.url,
  <-supports<-source.content
FROM concept WHERE name = $concept_name;
```

**Example**:
```
User: "What sources support the claim about wireless protocols?"

1. Search for concept:wireless_protocols
2. Traverse source->supports->concept relationships
3. Return all sources with reliability ratings
```

### 5. Hybrid Queries

**Indicators**: Complex questions combining multiple aspects

**Translation Pattern**:
```surql
-- Semantic + graph + timeline combined
SELECT * FROM section
WHERE embedding <|3|> $query_vector
AND ->appears_in->character:anna
AND sequence < 5
ORDER BY sequence;

-- Character knowledge grounded in sources
SELECT
  character.name,
  character.description,
  ->appears_in->section.content,
  ->appears_in->section->cites->source.title
FROM character
WHERE embedding <|5|> $query_vector;
```

**Example**:
```
User: "What do we know about Anna's wireless training, and what sources do we have?"

1. Generate embedding for "Anna wireless training"
2. Execute hybrid query:
   - Semantic search for related content
   - Graph traversal for Anna's appearances
   - Concept extraction for "wireless training"
   - Source citation for supporting documents
3. Combine and format results
```

## Query Execution Workflow

### 1. Parse Natural Language Question

Analyze the user's question to identify:
- Query type (semantic, graph, timeline, citation, hybrid)
- Entity references (character:anna, location:lyon, concept:wireless)
- Temporal constraints (before, after, chapter N)
- Relationship types (knows, appears_in, supports, cites)

### 2. Generate Embeddings (if needed)

For semantic or hybrid queries:
```bash
python scripts/generate-embedding.py --text "$user_question" --config bookstrap.config.json
```

### 3. Build SurrealDB Query

Construct the appropriate query based on parsed components:

```bash
# Read configuration
CONFIG=$(cat bookstrap.config.json)
DB_NAME=$(echo $CONFIG | jq -r '.surrealdb.database')
NAMESPACE=$(echo $CONFIG | jq -r '.surrealdb.namespace')

# Execute query
surreal sql --conn http://localhost:2665 \
  --user root --pass root \
  --ns $NAMESPACE --db $DB_NAME \
  --query "$CONSTRUCTED_QUERY"
```

### 4. Format Results

Transform raw query results into readable output:
- Group related entities
- Show source citations
- Display similarity scores for semantic searches
- Present timeline in chronological order
- Highlight key relationships

## Output Format

### Semantic Search Results

```
SEMANTIC SEARCH: "What do we know about Anna's time in Lyon?"
================================================================

MATCHING SECTIONS (5 results):
-------------------------------

[1] Similarity: 0.87 | Chapter 3, Section 2
───────────────────────────────────────────
Anna arrived in Lyon on a cold November morning. The safehouse
on Rue de la République had been compromised the week before...

Source: [SOE Lyon Network History] (primary, high reliability)
URL: https://example.com/soe-lyon

[2] Similarity: 0.82 | Chapter 3, Section 5
───────────────────────────────────────────
The wireless room in the Lyon safehouse was barely larger than
a closet. Anna practiced her encryption protocols...

Source: [Wireless Operator Protocols 1943] (primary, high reliability)
URL: https://archive.org/details/soe-wireless

[Additional results...]
```

### Graph Traversal Results

```
GRAPH QUERY: "Show me all scenes with character:erik"
======================================================

CHARACTER: Erik Schmidt
Description: German counter-intelligence officer stationed in Lyon

APPEARANCES (7 sections):
─────────────────────────

Chapter 2, Section 4 (sequence: 8)
  Erik watched from across the café as the woman entered...

Chapter 3, Section 1 (sequence: 12)
  The Gestapo office on Place Bellecour was frigid...

Chapter 3, Section 7 (sequence: 18)
  Erik's suspicions about the wireless operator had grown...

RELATIONSHIPS:
──────────────
→ knows: Anna Dubois (met: Chapter 2, Section 4)
→ knows: Pierre Rousseau (interrogated: Chapter 3, Section 2)
→ located_in: Lyon Gestapo Office (primary location)
```

### Timeline Results

```
TIMELINE QUERY: "Events in chapter 3"
=====================================

CHRONOLOGICAL SEQUENCE:
───────────────────────

Event #12: Anna arrives in Lyon
  Date: November 8, 1943
  Description: Anna reaches the Lyon safehouse via train from Paris
  Sources: [SOE Operations Log 1943], [Lyon Resistance Network]

Event #13: First wireless transmission
  Date: November 10, 1943
  Description: Anna sends coded message to London headquarters
  Sources: [Wireless Operator Protocols 1943]

Event #14: Safehouse compromise
  Date: November 14, 1943
  Description: Gestapo raids previous safehouse, network relocates
  Sources: [Lyon Resistance Network], [Gestapo Activity Reports]

[Additional events...]

PRECEDES/FOLLOWS RELATIONSHIPS:
───────────────────────────────
Event #12 → precedes → Event #13
Event #13 → precedes → Event #14
```

### Citation Results

```
SOURCE QUERY: "What sources support wireless protocols?"
=========================================================

SUPPORTING SOURCES (4 found):
─────────────────────────────

[1] Wireless Operator Protocols 1943
    Type: primary
    Reliability: high
    URL: https://archive.org/details/soe-wireless
    Ingested: 2025-01-15

    Supports concepts:
      - wireless protocols
      - encryption methods
      - transmission security

    Citations: 8 sections cite this source

[2] SOE Training Manual - Wireless Section
    Type: secondary
    Reliability: high
    URL: https://example.com/soe-training
    Ingested: 2025-01-15

    Supports concepts:
      - wireless training
      - code procedures

    Citations: 5 sections cite this source

[Additional sources...]
```

### Hybrid Results

```
HYBRID QUERY: "Anna's wireless training with sources"
======================================================

CHARACTER KNOWLEDGE:
────────────────────
Name: Anna Dubois
Description: SOE wireless operator trained at Beaulieu
Status: active

RELEVANT CONTENT (semantic search):
───────────────────────────────────

[1] Similarity: 0.91 | Chapter 1, Section 3
Anna's wireless training at Beaulieu had been intensive. Six
weeks of Morse code practice, encryption protocols...

  Sources cited:
    • [SOE Training Manual] (primary, high)
    • [Beaulieu Training Records] (primary, high)

[2] Similarity: 0.85 | Chapter 2, Section 1
She carried her suitcase wireless set, identical to the one
she'd practiced with during training...

  Sources cited:
    • [Wireless Operator Equipment Guide] (secondary, medium)
    • [SOE Field Manual 1943] (primary, high)

TIMELINE CONTEXT:
─────────────────
• Training begins: August 1943 (Event #3)
• Training completes: October 1943 (Event #7)
• First field deployment: November 1943 (Event #12)

SUPPORTING SOURCES:
───────────────────
Total sources about "wireless training": 6
  - Primary sources: 4 (high reliability)
  - Secondary sources: 2 (medium reliability)
```

## Error Handling

| Error | Response |
|-------|----------|
| Database not running | `Error: Database not accessible. Run: docker-compose up -d` |
| No results found | `No results found for query. Try broader search terms or check entity names.` |
| Invalid entity reference | `Entity not found: character:unknown. List entities with: SELECT * FROM character;` |
| Embedding generation fails | `Error generating embedding. Check API key configuration.` |
| Query timeout | `Query timeout. Try narrowing the search scope or using specific entity IDs.` |
| Ambiguous query | `Query is ambiguous. Did you mean: [suggestions]?` |

## Configuration

Query execution uses settings from `bookstrap.config.json`:

```json
{
  "surrealdb": {
    "host": "localhost",
    "port": 2665,
    "namespace": "bookstrap",
    "database": "my_book"
  },
  "embeddings": {
    "provider": "gemini",
    "model": "text-embedding-004",
    "dimensions": 768
  }
}
```

## Example Queries

### Character Exploration

```bash
/bookstrap-query "What do we know about Anna?"
/bookstrap-query "Who does Erik know?"
/bookstrap-query "Show all characters in Lyon"
/bookstrap-query "Anna's relationships and appearances"
```

### Source Verification

```bash
/bookstrap-query "What sources do we have about SOE training?"
/bookstrap-query "Citations for wireless protocols"
/bookstrap-query "Primary sources about Lyon resistance"
/bookstrap-query "What supports the claim about November 1943?"
```

### Timeline Questions

```bash
/bookstrap-query "Events in chronological order"
/bookstrap-query "What happens before the safehouse raid?"
/bookstrap-query "Timeline of Anna's activities in chapter 3"
/bookstrap-query "Events in November 1943"
```

### Content Search

```bash
/bookstrap-query "Scenes with wireless transmissions"
/bookstrap-query "Sections about Gestapo investigations"
/bookstrap-query "Content similar to: encryption and security"
/bookstrap-query "Where is the Lyon safehouse mentioned?"
```

### Knowledge Gaps

```bash
/bookstrap-query "Unresolved knowledge gaps"
/bookstrap-query "What gaps are blocking chapter 4?"
/bookstrap-query "High priority research needs"
```

### Hybrid Queries

```bash
/bookstrap-query "Anna's training timeline with source citations"
/bookstrap-query "Erik's investigation of Anna, chronologically"
/bookstrap-query "All wireless-related content in Lyon scenes with sources"
```

## Implementation Notes

### Query Optimization

- Use LIMIT clauses to prevent overwhelming results
- Cache embeddings for repeated queries
- Prefer specific entity IDs when available
- Use indexes for common query patterns

### Result Relevance

For semantic searches:
- Show similarity scores
- Filter results below 0.7 similarity threshold
- Group by chapter/section for context
- Always include source citations

### Interactive Refinement

If query is ambiguous, suggest clarifications:
```
Did you mean:
  1. Character information about "Anna"
  2. Sections where "Anna" appears
  3. Timeline of events involving "Anna"
  4. Sources about "Anna"

Specify with: /bookstrap-query "character:anna information"
```

### Performance

- Default result limit: 10 items
- Timeout: 30 seconds
- Show partial results if query runs long
- Offer to refine query if too many results

## Pre-requisites

- **Database running**: SurrealDB must be accessible
- **Schema initialized**: Database schema must be loaded
- **Content ingested**: At least some sources must be in the database
- **Embeddings configured**: If using semantic search

## Related Commands

- `/bookstrap-status` - View overall database statistics
- `/bookstrap-ingest` - Add more sources to query
- `/bookstrap-research` - Fill knowledge gaps discovered via queries
- `/bookstrap-write` - Use query results to inform writing

## Advanced Query Patterns

### Entity Lists

```surql
-- List all characters
SELECT name, description, status FROM character ORDER BY name;

-- List all locations
SELECT name, description, introduced FROM location ORDER BY name;

-- List all events
SELECT name, sequence, date FROM event ORDER BY sequence;
```

### Relationship Counts

```surql
-- Character appearance frequency
SELECT
  character.name,
  count(->appears_in->section) as section_count
FROM character
GROUP BY character.name
ORDER BY section_count DESC;

-- Source citation frequency
SELECT
  source.title,
  count(<-cites<-section) as citation_count
FROM source
GROUP BY source.title
ORDER BY citation_count DESC;
```

### Coverage Analysis

```surql
-- Chapters with most sources
SELECT
  chapter,
  count(->cites->source) as source_count
FROM section
GROUP BY chapter
ORDER BY source_count DESC;

-- Concepts without sources
SELECT name FROM concept
WHERE count(<-supports<-source) = 0;
```

### Consistency Checks

```surql
-- Dead characters still appearing
SELECT
  character.name,
  character.death_sequence,
  ->appears_in->section.sequence as appearance_sequence
FROM character
WHERE status = 'dead'
  AND appearance_sequence > death_sequence;

-- Locations used before introduction
SELECT
  location.name,
  ->located_in->section.sequence as first_use
FROM location
WHERE introduced = false
  AND count(->located_in->section) > 0;
```

## Troubleshooting

### No results returned

1. Verify entity exists: `SELECT * FROM character WHERE name CONTAINS "Anna"`
2. Check spelling of entity references
3. Try semantic search instead of exact match
4. Verify database has ingested content

### Too many results

1. Add filters: chapter, date range, sequence constraints
2. Use higher similarity threshold for semantic searches
3. Specify entity type: `character:anna` not just `anna`
4. Limit to specific relationships

### Slow queries

1. Add LIMIT clause
2. Use indexed fields (id, sequence, chapter)
3. Avoid multiple embeddings in one query
4. Query specific tables rather than全table scans

### Embedding errors

1. Check API key: `echo $GEMINI_API_KEY`
2. Verify embedding config in `bookstrap.config.json`
3. Test embedding generation: `python scripts/generate-embedding.py --test`
4. Fall back to keyword search if embeddings fail

## Tips for Effective Queries

1. **Be specific**: Use entity IDs when known (`character:anna` vs "Anna")
2. **Combine methods**: Hybrid queries give best context
3. **Check sources**: Always verify source citations for factual claims
4. **Use timeline**: Sequence queries prevent anachronisms
5. **Explore relationships**: Graph queries reveal unexpected connections
6. **Iterate**: Start broad, then refine based on results

## Query Result Export

For future enhancement, allow exporting query results:

```bash
/bookstrap-query "Timeline of chapter 3" --export json > timeline.json
/bookstrap-query "All sources" --export csv > sources.csv
/bookstrap-query "Character relationships" --export graph > graph.dot
```

## Natural Language Understanding

The query parser should recognize:

- **Entity types**: character, location, event, concept, source
- **Relationships**: knows, appears in, cites, supports, precedes, follows
- **Temporal**: before, after, during, timeline, chronological
- **Similarity**: similar to, related to, about, concerning
- **Quantifiers**: all, most, top N, first, last
- **Filters**: in chapter N, from source X, with reliability Y

Continuously improve parsing based on common query patterns.
