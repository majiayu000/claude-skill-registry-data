---
name: surrealdb
description: Comprehensive SurrealDB patterns for hybrid RAG, including vector search, graph traversal, timeline queries, and combined semantic-graph-temporal operations.
---

# SurrealDB Skill

This skill provides comprehensive guidance for working with SurrealDB in the Bookstrap framework, covering database patterns, query strategies, and hybrid retrieval-augmented generation (RAG).

## SurrealDB Overview

SurrealDB is a multi-model database that combines:
- **Document storage**: JSON-like records
- **Graph database**: Native relationships with RELATE statements
- **Vector search**: Native embedding support with MTREE indexes
- **SQL-like queries**: Familiar SurrealQL syntax

This makes it ideal for book writing, where you need:
- Semantic search (find similar content)
- Graph traversal (character relationships, citation chains)
- Timeline queries (chronological events, sequences)
- Combined queries (semantic + graph + timeline)

## Core Database Patterns

### 1. Hybrid RAG Architecture

**Hybrid RAG** combines three retrieval strategies:

```
Semantic Search    +    Graph Traversal    +    Timeline Queries
     (vectors)              (relationships)           (sequences)
        ↓                        ↓                         ↓
                   Combined Context
                        ↓
                  Writing/Editing
```

**Why Hybrid?**
- **Semantic alone**: Misses explicit relationships
- **Graph alone**: Misses conceptual similarity
- **Timeline alone**: Misses both semantics and structure
- **Combined**: Comprehensive context retrieval

### 2. Vector Search Pattern

SurrealDB uses MTREE indexes for efficient k-nearest neighbor (kNN) search.

**Basic Vector Search**:
```surql
-- Find similar sections by semantic meaning
SELECT *, vector::similarity::cosine(embedding, $query_vector) AS similarity
FROM section
WHERE vector::similarity::cosine(embedding, $query_vector) > 0.7
ORDER BY similarity DESC
LIMIT 5;
```

**Vector Index Configuration**:
```surql
DEFINE INDEX idx_section_embedding
    ON section
    FIELDS embedding
    MTREE DIMENSION 1536 DIST COSINE TYPE F32;
```

**Important**: Embedding dimensions must match your provider:
- Gemini `text-embedding-004`: 768 dims
- OpenAI `text-embedding-3-small`: 1536 dims
- Ollama `nomic-embed-text`: 768 dims

### 3. Graph Traversal Pattern

Use `->` and `<-` operators to traverse relationships.

**Outbound Traversal** (following relationships):
```surql
-- Get all sections where character Anna appears
SELECT ->appears_in->section.*
FROM character:anna;
```

**Inbound Traversal** (reverse relationships):
```surql
-- Get all characters in a section
SELECT <-appears_in<-character.*
FROM section:ch3_s2;
```

**Multi-hop Traversal**:
```surql
-- Get characters known by Anna's friends
SELECT ->knows->character->knows->character.*
FROM character:anna;
```

### 4. Timeline Query Pattern

Use sequence fields and datetime for chronological ordering.

**Sequence-Based**:
```surql
-- Get events before current point
SELECT * FROM event
WHERE sequence < $current_sequence
ORDER BY sequence DESC
LIMIT 10;
```

**Date-Based**:
```surql
-- Get events in date range
SELECT * FROM event
WHERE date >= $start_date
  AND date <= $end_date
ORDER BY date ASC;
```

## Query Strategy Selection

Choose query strategy based on retrieval goal:

| Goal | Strategy | Example Query |
|------|----------|---------------|
| Find similar content | Vector search | "Find sections about training" |
| Get related entities | Graph traversal | "Get Anna's relationships" |
| Timeline context | Sequence query | "Events before chapter 5" |
| Comprehensive context | Hybrid (all three) | "Anna's training: similar content + relationships + timeline" |

## Pre-Write Query Workflow

Before writing a section, gather context using hybrid queries:

### Step 1: Semantic Search
Find conceptually similar content:
```surql
-- Find related sections by theme
SELECT *, vector::similarity::cosine(embedding, $query_embedding) AS similarity
FROM section
WHERE vector::similarity::cosine(embedding, $query_embedding) > 0.7
ORDER BY similarity DESC
LIMIT 5;
```

### Step 2: Graph Context
Get related entities and relationships:
```surql
-- Get characters and their relationships
SELECT
    c.name,
    c.description,
    ->knows->character.name AS knows,
    ->appears_in->section.id AS appears_in
FROM character c
WHERE c.id IN $character_ids;
```

### Step 3: Timeline Context
Get chronological context:
```surql
-- Get recent events
SELECT * FROM event
WHERE sequence < $current_sequence
ORDER BY sequence DESC
LIMIT 10;
```

### Step 4: Citation Chain
Get source support:
```surql
-- Get sources for concept
SELECT
    <-supports<-source.title,
    <-supports<-source.reliability,
    <-supports<-source.url
FROM concept:wireless_protocols;
```

## Hybrid Query Patterns

Combine multiple strategies for comprehensive context.

### Pattern 1: Semantic + Graph
```surql
-- Find similar sections that mention Anna
SELECT
    s.*,
    vector::similarity::cosine(s.embedding, $query_embedding) AS similarity
FROM section s
WHERE vector::similarity::cosine(s.embedding, $query_embedding) > 0.7
  AND s->appears_in->character:anna
ORDER BY similarity DESC
LIMIT 5;
```

### Pattern 2: Semantic + Timeline
```surql
-- Find similar sections before current point
SELECT
    s.*,
    vector::similarity::cosine(s.embedding, $query_embedding) AS similarity
FROM section s
WHERE vector::similarity::cosine(s.embedding, $query_embedding) > 0.7
  AND s.sequence < $current_sequence
ORDER BY similarity DESC, s.sequence DESC
LIMIT 5;
```

### Pattern 3: Graph + Timeline
```surql
-- Get Anna's appearances in chronological order
SELECT
    s.*,
    s.sequence
FROM character:anna->appears_in->section s
WHERE s.sequence < $current_sequence
ORDER BY s.sequence ASC;
```

### Pattern 4: Full Hybrid (Semantic + Graph + Timeline)
```surql
-- Comprehensive context query
SELECT
    s.*,
    vector::similarity::cosine(s.embedding, $query_embedding) AS similarity,
    s.sequence
FROM section s
WHERE vector::similarity::cosine(s.embedding, $query_embedding) > 0.7
  AND s->appears_in->character IN $character_ids
  AND s.sequence < $current_sequence
ORDER BY similarity DESC, s.sequence DESC
LIMIT 10;
```

## Entity Extraction and Storage

When ingesting sources or writing sections, extract and store entities.

### Character Extraction
```surql
-- Create character with embedding
CREATE character SET
    name = "Anna",
    description = "SOE wireless operator, recruited 1942",
    embedding = $character_embedding,
    status = "alive",
    introduced_in = section:ch1_s3;
```

### Location Extraction
```surql
-- Create location
CREATE location SET
    name = "Beaulieu Manor",
    description = "SOE training facility in Hampshire",
    embedding = $location_embedding,
    introduced = true;
```

### Event Extraction
```surql
-- Create event with timeline info
CREATE event SET
    name = "Anna begins training",
    description = "Wireless operator course starts at Beaulieu",
    embedding = $event_embedding,
    sequence = 5,
    date = "1942-08-15T00:00:00Z";
```

### Relationship Creation
```surql
-- Link character to section
RELATE character:anna->appears_in->section:ch3_s2;

-- Link section to location
RELATE section:ch3_s2->located_in->location:beaulieu;

-- Link section to source
RELATE section:ch3_s2->cites->source:soe_manual;

-- Timeline relationship
RELATE event:training_begins->precedes->event:deployment;
```

## Query Optimization

### 1. Use Vector Indexes
Ensure MTREE indexes exist for all embedding fields:
```surql
-- Check existing indexes
INFO FOR TABLE section;

-- Create missing index
DEFINE INDEX idx_section_embedding
    ON section
    FIELDS embedding
    MTREE DIMENSION 1536 DIST COSINE TYPE F32;
```

### 2. Filter Before Vector Search
Apply filters before vector operations when possible:
```surql
-- Efficient: Filter first, then vector search
SELECT * FROM section
WHERE chapter = $chapter_id
  AND vector::similarity::cosine(embedding, $query_vector) > 0.7;

-- Less efficient: Vector search entire table
SELECT * FROM section
WHERE vector::similarity::cosine(embedding, $query_vector) > 0.7
  AND chapter = $chapter_id;
```

### 3. Limit Results Early
Use LIMIT to reduce processing:
```surql
SELECT * FROM section
WHERE vector::similarity::cosine(embedding, $query_vector) > 0.7
ORDER BY vector::similarity::cosine(embedding, $query_vector) DESC
LIMIT 5;  -- Only process top 5
```

### 4. Use LET for Reusable Queries
Store intermediate results:
```surql
-- Store character list
LET $characters = (
    SELECT * FROM character WHERE id IN $character_ids
);

-- Reuse in multiple queries
SELECT * FROM section
WHERE ->appears_in->character IN $characters;
```

## Common Query Patterns

### Find Uncited Claims
```surql
SELECT * FROM section
WHERE count(->cites->source) = 0
  AND length(content) > 100;
```

### Get Citation Chain
```surql
SELECT
    s.id,
    s.content,
    ->cites->source.title AS sources,
    ->cites->source.reliability AS reliability
FROM section s
WHERE s.id = $section_id;
```

### Character Relationship Graph
```surql
SELECT
    c1.name AS character,
    ->knows->character.name AS knows,
    <-knows<-character.name AS known_by
FROM character c1;
```

### Timeline Consistency Check
```surql
-- Find events with contradictory sequence and dates
SELECT
    e1.name,
    e1.sequence,
    e1.date,
    e2.name,
    e2.sequence,
    e2.date
FROM event e1, event e2
WHERE e1.sequence < e2.sequence
  AND e1.date > e2.date;
```

## Database Schema Reference

See `schema.surql` for the complete database schema including:
- Table definitions (chapter, section, source, character, location, event, concept)
- Field types and constraints
- Vector indexes (MTREE configuration)
- Edge tables (appears_in, located_in, cites, supports, precedes, follows, knows, related_to)

## Query Pattern Files

This skill includes specialized query pattern files:

- **`semantic.surql`**: Vector search patterns with examples
- **`graph.surql`**: Graph traversal patterns for relationships
- **`timeline.surql`**: Timeline and sequence query patterns

Load these files when you need specific query types.

## Best Practices

1. **Always use embeddings**: Generate embeddings for all content
2. **Create relationships**: Use RELATE for explicit connections
3. **Track sequences**: Maintain timeline order with sequence fields
4. **Verify indexes**: Ensure MTREE indexes exist before vector queries
5. **Combine strategies**: Use hybrid queries for comprehensive context
6. **Limit results**: Don't retrieve more than you need
7. **Store metadata**: Track created_at, updated_at for debugging
8. **Use transactions**: Group related operations for consistency

## Error Handling

### Common Errors

**Vector dimension mismatch**:
```
Error: Vector dimensions do not match (expected 1536, got 768)
```
**Fix**: Ensure config embedding dimensions match schema indexes.

**Missing index**:
```
Error: No vector index found on field 'embedding'
```
**Fix**: Create MTREE index with `DEFINE INDEX`.

**Invalid relationship**:
```
Error: Cannot RELATE records of incompatible types
```
**Fix**: Verify edge table schema matches record types.

## Supporting Files

- `schema.surql` — Complete database schema reference
- `semantic.surql` — Vector search query patterns
- `graph.surql` — Graph traversal examples
- `timeline.surql` — Timeline query patterns
