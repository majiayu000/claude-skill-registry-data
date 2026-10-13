---
name: memory
description: "Core memory system definition. Defines the persistent memory schema, operations, and self-modification rules. All memories stored in the Supabase `memories` table. Referenced by all other memory skills and agents."
---

# Memory System - Core Definition

## Storage

All memories are stored in the Supabase `memories` table:

```sql
memories
  id UUID PK
  user_id UUID FK → auth.users
  category TEXT NOT NULL      -- 'project', 'preference', 'decision', 'knowledge'
  subcategory TEXT            -- project slug, topic name, or NULL
  key TEXT NOT NULL           -- slugified title (unique per user+category+subcategory)
  value TEXT NOT NULL         -- markdown content
  tags TEXT[]                 -- categorization tags
  confidence TEXT             -- 'high', 'medium', 'low'
  source TEXT                 -- 'explicit', 'inferred', 'rem-sleep', 'memory-init'
  deprecated BOOLEAN DEFAULT false
  created_at TIMESTAMPTZ
  updated_at TIMESTAMPTZ
  UNIQUE(user_id, category, subcategory, key)
```

## Data Storage Rules

- NEVER write memory data to local files (no `~/.claude/memory/` directory)
- Use ToolSearch to discover Supabase MCP tools, then INSERT/UPDATE/SELECT on the `memories` table
- Local files are not used — all memory is in the database
- Temp files in /tmp/ are acceptable for transient processing

## Category Mapping

| Content Type | category | subcategory | Examples |
|-------------|----------|-------------|----------|
| Project-specific decisions | `project` | `<project-slug>` | "We use Zustand for state" |
| Cross-project decisions | `decision` | NULL | "Always use conventional commits" |
| User preferences | `preference` | NULL or topic | "Prefer functional components" |
| General knowledge | `knowledge` | `<topic>` | "React 19 server components patterns" |

## Operations

### Write

1. Determine correct category and subcategory
2. Query existing memories for duplicates: `SELECT * FROM memories WHERE user_id = auth.uid() AND category = ... AND subcategory = ... AND key = ...`
3. If updating existing memory: UPDATE value and updated_at timestamp
4. If new memory: INSERT with proper fields
5. Assign confidence level and tags

### Read

1. Query by category and/or subcategory
2. Filter out entries where `deprecated = true` or `confidence = 'low'` (unless explicitly requested)
3. Order by updated_at DESC for recency

### Search

Query with text matching:
```sql
SELECT * FROM memories
WHERE user_id = auth.uid()
  AND (key ILIKE '%search_term%' OR value ILIKE '%search_term%')
  AND deprecated = false
ORDER BY updated_at DESC
```

## Self-Modification Rules

- **Never delete**: Set `deprecated = true` instead of deleting rows
- **Merge duplicates**: If two entries have >50% content overlap, consolidate into one and deprecate the other
- **One concept per entry**: If a memory covers multiple distinct topics, split into separate rows
- **Recency wins**: When content conflicts, prefer the newer entry

## Confidence Levels

| Level | Meaning | When to Use |
|-------|---------|-------------|
| `high` | Explicitly stated or repeatedly confirmed | User directly states preference, architectural decision |
| `medium` | Inferred from patterns | Observed behavior across multiple sessions |
| `low` | Single observation, uncertain | One-off comment, may be context-dependent |

## Project Name Derivation

To determine the current project name for the `subcategory` field:

```bash
# Priority 1: git remote basename
git remote get-url origin 2>/dev/null | sed 's|.*/||;s|\.git$||'

# Priority 2: current directory basename
basename "$PWD"
```

Always normalize to lowercase with hyphens (e.g., `Stories` → `stories`, `My Project` → `my-project`).
