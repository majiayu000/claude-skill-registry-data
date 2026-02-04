---
name: trait-learning
description: >-
  Use when working with trait extraction, place enrichment, or the learning loop.
  Load for understanding how the system learns from gameplay, how traits are
  extracted from Nominatim + player sessions, async queue processing, and LLM
  prompt configuration. Covers update_place_traits, pgmq, and edge function flow.
---

# Trait Learning

How the system learns from gameplay and enriches places with traits.

> **Announce:** "I'm using trait-learning to understand the learning mechanism."

## Learning Loop Overview

```
Player completes game
        ↓
    Trigger fires (on correct submission)
        ↓
    Job queued to pgmq.trait_extraction
        ↓
    Edge function called via pg_net
        ↓
    update_place_traits() executes
        ↓
    LLM curates traits from all sources
        ↓
    Place traits replaced with new set
```

## Data Sources for Learning

The LLM receives all available context when extracting traits:

```sql
-- 1. Nominatim data (class, type, extratags)
v_nominatim_data := game_logic.fetch_nominatim_place(v_place.osm_id);

-- 2. Session descriptions (what players typed)
SELECT array_agg(DISTINCT description)
FROM game_sessions
WHERE place_id = p_place_id;

-- 3. Game answers (confirmed yes/no from gameplay)
-- Format: "+ trait text" for yes, "- trait text" for no
SELECT array_agg(
  CASE WHEN ga.answer = 'yes' THEN '+ ' || t.clause
       WHEN ga.answer = 'no' THEN '- ' || t.clause
  END
)
FROM game_answers ga
JOIN traits t ON t.id = ga.trait_id;

-- 4. Existing traits (for review/curation)
SELECT array_agg(t.clause)
FROM place_traits pt
JOIN traits t ON t.id = pt.trait_id;
```

## Trait Table Schema

```sql
-- Traits are deduplicated by embedding
CREATE TABLE traits (
  id UUID PRIMARY KEY,
  clause TEXT NOT NULL,           -- "Built in 1889"
  embedding_id UUID UNIQUE        -- Links to embeddings table
);

-- Many-to-many link
CREATE TABLE place_traits (
  place_id UUID REFERENCES places,
  trait_id UUID REFERENCES traits,
  PRIMARY KEY (place_id, trait_id)
);

-- Embeddings with source text deduplication
CREATE TABLE embeddings (
  id UUID PRIMARY KEY,
  embedding vector(384),
  source_text TEXT UNIQUE         -- Prevents duplicate embeddings
);
```

## Core Function: update_place_traits

Location: `supabase/db/game_logic/functions/places/update_place_traits.sql`

```sql
-- Key steps:
1. Fetch Nominatim data for place
2. Gather session descriptions
3. Gather game answers (yes/no from gameplay)
4. Get existing traits
5. Build LLM prompt with all context
6. Call LLM via call_llm_api()
7. Parse JSON response {"traits": [...]}
8. DELETE all existing place_traits for this place
9. For each trait:
   - Generate embedding (passage type)
   - Insert trait (ON CONFLICT updates)
   - Link place to trait
10. Update place.pending_review = FALSE
```

**Important:** LLM output is authoritative. Existing traits are REPLACED, not merged.

## Async Queue Processing

Trait extraction is async to avoid blocking game flow:

```sql
-- Queue table via pgmq
SELECT pgmq.create('trait_extraction');

-- Job added after successful game
INSERT INTO pgmq.trait_extraction (message)
VALUES ('{"place_id": "...", "function_name": "update_place_traits"}');

-- Backup processor for orphaned jobs (every 60 seconds)
SELECT cron.schedule(
  'process-orphaned-trait-jobs',
  '60 seconds',
  'SELECT game_logic.process_orphaned_trait_jobs();'
);
```

## Edge Function: process-trait-extraction

Location: `supabase/functions/process-trait-extraction/index.ts`

```typescript
// Receives fire-and-forget from pg_net
// Validates whitelisted function (security)
// Calls RPC to execute trait extraction
// Archives queue message on success

const ALLOWED_FUNCTIONS = ['update_place_traits'] as const

// Call the database function
const { error } = await supabase.rpc(function_name, params)

// Clean up queue
await supabase.rpc('archive_trait_queue_by_place', { p_place_id: placeId })
```

## LLM Prompt Configuration

All prompts are in `game_logic.config`:

```sql
-- Key config entries
'llm.trait_extraction.model'           -- Which model to use
'llm.trait_extraction.temperature'     -- Low for precision (0.15)
'llm.trait_extraction.max_traits'      -- Cap per place (20)
'llm.trait_extraction.prompt'          -- Full prompt template

-- Template placeholders
{place_name}           -- Place name
{lat}, {lng}          -- Coordinates
{country}             -- From Nominatim address
{place_type}          -- From Nominatim type
{nominatim_text}      -- Filtered extratags
{existing_traits}     -- Current traits
{session_descriptions} -- Player descriptions
{game_answers}        -- Confirmed yes/no answers
{max_traits}          -- Limit
```

## Trait Quality Guidelines

The LLM prompt includes quality rules:

**Good traits:**
- Specific facts: "Built 1889", "Over 300 meters tall"
- Material/structure: "Made of iron", "Has a lattice structure"
- Heritage status: "UNESCO World Heritage since 1991"

**Bad traits (filtered by prompt):**
- Redundant: Multiple traits testing same property
- Raw data: URLs, Wikidata IDs, hex colors
- Useless: Floor count, wheelchair access, hours
- Generic: "Tourism attraction", "Historic landmark"

## Embedding Types

```sql
-- Query embeddings (user input)
get_embedding(description, 'query')

-- Passage embeddings (traits being matched)
get_embedding(trait_clause, 'passage')
```

The `input_type` affects the embedding model's prefix. Use `'passage'` for traits since they're being searched, not searching.

## Testing Trait Learning

```sql
-- Manually trigger trait extraction
SELECT game_logic.update_place_traits('place-uuid-here');

-- View traits for a place
SELECT t.clause, e.source_text
FROM place_traits pt
JOIN traits t ON t.id = pt.trait_id
LEFT JOIN embeddings e ON e.id = t.embedding_id
WHERE pt.place_id = 'place-uuid-here';

-- Check queue status
SELECT * FROM pgmq.read('trait_extraction', 30, 5);
```

## Anti-Patterns

### DON'T: Add Traits Without Embedding

```sql
-- WRONG: Trait without embedding won't match
INSERT INTO traits (id, clause)
VALUES (gen_random_uuid(), 'Some trait');

-- CORRECT: Always generate embedding
v_embedding_id := get_embedding(v_clause, 'passage');
INSERT INTO traits (id, clause, embedding_id)
VALUES (gen_random_uuid(), v_clause, v_embedding_id);
```

### DON'T: Merge Instead of Replace

```sql
-- WRONG: Merging creates trait bloat
INSERT INTO place_traits ... ON CONFLICT DO NOTHING;

-- CORRECT: LLM curates, we replace
DELETE FROM place_traits WHERE place_id = p_place_id;
-- Then insert new curated set
```

### DON'T: Skip Queue for Sync Processing

```sql
-- WRONG: Blocks game completion
SELECT game_logic.update_place_traits(p_place_id);

-- CORRECT: Queue for async processing
SELECT pgmq.send('trait_extraction', 
  jsonb_build_object('place_id', p_place_id));
```

## Related Skills

- `game-scoring` - How traits affect candidate scoring
- `postgres-vectors` - Embedding storage and similarity
- `edge-functions` - Edge function patterns
