---
name: neo4j-graphiti-migration
description: Assists with migrating data from Neo4j Memory to Graphiti temporal knowledge graphs
alwaysAllow:
  - Read
  - Write
  - mcp__docker__read_graph
  - mcp__docker__search_memories
  - mcp__docker__find_memories_by_name
  - mcp__graphiti-local__add_memory
  - mcp__graphiti-local__search_nodes
  - mcp__graphiti-local__search_memory_facts
  - mcp__graphiti-local__get_episodes
  - mcp__graphiti-local__get_status
---

# Neo4j Memory to Graphiti Migration Skill

## When to Use This Skill

Invoke this skill when the user asks about:
- Migrating data from Neo4j Memory to Graphiti
- Converting entities to episodes
- Episode format templates
- Migration validation
- Group ID classification
- Rate limiting strategies

## Core Concepts

### Source System: Neo4j Memory (MCP_DOCKER)
- Entity-first architecture (direct node creation)
- Observations as array properties on entities
- Simple typed relationships
- No temporal tracking, no embeddings

### Target System: Graphiti (graphiti-local)
- Episode-first architecture (LLM extraction)
- Temporal tracking (valid_at, invalid_at)
- group_id namespace isolation
- Auto-generated embeddings

## Entity-to-Episode Conversion Templates

### Person Entities (source: text)
```
{Name} is a {role/title} with {experience summary}.
{Key professional details}.

Key observations:
- {observation 1}
- {observation 2}
- {observation N}
```

### Experience Entities (source: json)
```json
{
  "name": "Role/Position Name",
  "type": "Experience",
  "years": "YYYY-YYYY",
  "duration": "N years",
  "company": "Company Name",
  "details": ["detail 1", "detail 2"]
}
```

### Organization Entities (source: text)
```
{Organization Name} is a {type} organization.
{Description and context}.

Key divisions/teams:
- {division 1}
- {division 2}

Leadership: {key people and roles}
```

### JobPosting Entities (source: json)
```json
{
  "title": "Job Title",
  "company": "Company",
  "salary_range": "$XXK-$YYK",
  "requirements": ["req1", "req2"],
  "posted_date": "YYYY-MM"
}
```

### Pattern/Architecture Entities (source: text)
```
{Pattern Name} Pattern

Description: {what it does}

When to use:
- {use case 1}
- {use case 2}

Trade-offs:
- Pros: {benefits}
- Cons: {limitations}

Related patterns: {related}
```

## Group ID Classification Rules

| Entity Type | group_id |
|-------------|----------|
| Don Branson, Experience, Skills, Credentials | don_branson_career |
| Organization (Disney*), Team, BuyingCenter | disney_knowledge |
| JobPosting, Recruiter | career_opportunities |
| Pattern, Architecture | technical_patterns |
| research, Project (other) | ai_engineering_research |

## Rate Limiting

### Sequential Mode (don_branson_career)
- 1 episode at a time
- 2 second pause between calls
- For CRITICAL priority data

### Batch Mode (all others)
- Up to 10 episodes per batch
- 0.3 second delay within batch
- 3 second pause between batches

### Exponential Backoff on 429 Errors
Base delay → 2x → 4x → 8x → 16x (max 60s)

## Validation Queries

After each group_id migration, verify:

1. **Episode count**: `get_episodes(group_ids=[group_id])`
   - Pass threshold: ≥80% of expected

2. **Entity discovery**: `search_nodes(query="entity name", group_ids=[group_id])`
   - Pass threshold: ≥80% of key entities found

3. **Relationship extraction**: `search_memory_facts(query="relationship query")`
   - Pass threshold: ≥3 relevant facts per query

## Migration State File

Location: `migration/progress/migration_state.json`

```json
{
  "started_at": "ISO timestamp",
  "current_phase": 1,
  "completed_groups": ["group1"],
  "in_progress_group": "group2",
  "completed_episodes": {"group1": ["entity1", "entity2"]},
  "validation_results": {"group1": {...}},
  "last_checkpoint": "ISO timestamp"
}
```

## Quick Reference Commands

```bash
# Dry run
uv run python migration/orchestrate_migration.py --dry-run

# Run specific phase
uv run python migration/orchestrate_migration.py --phase 1

# Resume from checkpoint
uv run python migration/orchestrate_migration.py --resume

# Verbose logging
uv run python migration/orchestrate_migration.py -v
```

## Rollback

Per-group rollback (DANGEROUS - requires confirmation):
```python
# Clear specific namespace
mcp__graphiti-local__clear_graph(group_ids=["group_id"])
```

Source Neo4j Memory remains unchanged as read-only reference.
