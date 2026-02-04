---
name: artifact-query
description: |
  Search the Artifact Index for relevant historical context using semantic
  full-text search. Returns handoffs, plans, and continuity ledgers ranked
  by relevance using BM25.

trigger: |
  - Need to find similar past work before starting a task
  - Want to learn from previous successes or failures
  - Looking for historical context on a topic
  - Planning a feature and want precedent

skip_when: |
  - Working on completely novel functionality
  - Simple task that doesn't benefit from historical context
  - Artifact index not initialized (run artifact_index.py --all first)

sequence:
  before: [writing-plans, executing-plans]

related:
  similar: [exploring-codebase]
---

# Artifact Query

## Overview

Search Ring's Artifact Index for relevant historical context. Uses SQLite FTS5 full-text search with BM25 ranking to find:

- **Handoffs** - Completed task records with what worked/failed
- **Plans** - Implementation design documents
- **Continuity** - Session state snapshots with learnings

**Query response time:** < 100ms for typical searches

**Announce at start:** "I'm searching the artifact index for relevant precedent."

## When to Use

| Scenario | Use This Skill |
|----------|---------------|
| Starting a new feature | Yes - find similar implementations |
| Debugging a recurring issue | Yes - find past resolutions |
| Writing a plan | Yes - learn from past approaches |
| Simple one-liner fix | No - overhead not worth it |
| First time using Ring | No - index is empty |

## The Process

### Step 1: Formulate Query

Choose relevant keywords that describe what you're looking for:
- Feature names: "authentication", "OAuth", "API"
- Problem types: "error handling", "performance", "testing"
- Components: "database", "frontend", "hook"

### Step 2: Run Query

```bash
python3 default/lib/artifact-index/artifact_query.py "<keywords>" [options]
```

**Options:**
- `--mode search|planning` - Query mode (planning for structured precedent)
- `--type handoffs|plans|continuity|all` - Filter by artifact type
- `--outcome SUCCEEDED|FAILED|...` - Filter handoffs by outcome
- `--limit N` - Maximum results (1-100, default: 5)
- `--json` - Output as JSON for programmatic use
- `--stats` - Show index statistics

### Planning Mode (Recommended for write-plan)

For structured precedent when creating implementation plans:

```bash
python3 default/lib/artifact-index/artifact_query.py --mode planning "feature topic" --json
```

Returns:
- **successful_handoffs**: Past implementations that worked (reference these)
- **failed_handoffs**: Past implementations that failed (avoid these patterns)
- **relevant_plans**: Similar past plans for reference
- **query_time_ms**: Performance metric (target <200ms)
- **is_empty_index**: True if no historical data available

Empty index returns:
```json
{
  "is_empty_index": true,
  "message": "No artifact index found. This is normal for new projects."
}
```
This is NOT an error - proceed with standard planning.

### Step 3: Interpret Results

Results are ranked by relevance (BM25 score). For each result:

1. **Check outcome** - Learn from successes, avoid failures
2. **Read what_worked** - Reuse successful approaches
3. **Read what_failed** - Don't repeat mistakes
4. **Note file paths** - Can read full artifact if needed

### Step 4: Apply Learnings

Use historical context to inform current work:
- Reference successful patterns in your implementation
- Avoid approaches that failed previously
- Cite the precedent in your plan or handoff

## Examples

### Find Authentication Implementations

```bash
python3 default/lib/artifact-index/artifact_query.py "authentication OAuth JWT" --type handoffs
```

### Find Successful API Designs

```bash
python3 default/lib/artifact-index/artifact_query.py "API design REST" --outcome SUCCEEDED
```

### Get Index Statistics

```bash
python3 default/lib/artifact-index/artifact_query.py --stats
```

### Search Plans Only

```bash
python3 default/lib/artifact-index/artifact_query.py "context management" --type plans --json
```

## Integration with Planning

When creating plans (writing-plans skill), query the artifact index first:

1. Search for similar past implementations
2. Note which approaches succeeded vs failed
3. Include historical context in your plan
4. Reference specific handoffs that inform decisions

This enables RAG-enhanced planning where new plans learn from past experience.

## Initialization

If the index is empty, initialize it:

```bash
python3 default/lib/artifact-index/artifact_index.py --all
```

This indexes:
- `docs/handoffs/**/*.md` - Handoff documents
- `docs/plans/*.md` - Plan documents
- `.ring/ledgers/*.md` and `CONTINUITY*.md` - Continuity ledgers

## Remember

- Query before starting significant work
- Learn from both successes AND failures
- Cite historical precedent in your work
- Keep the index updated (hooks do this automatically)
- Response time target: < 100ms
