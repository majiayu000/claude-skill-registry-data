---
name: rebuild-wikilink-cache
description: Rebuild the wikilink entities cache. Triggers on "rebuild cache", "rebuild wikilink cache", "update cache", "refresh wikilinks". Optionally uses Flywheel MCP for enhanced entity detection.
auto_trigger: true
trigger_keywords:
  - "rebuild cache"
  - "rebuild wikilink cache"
  - "rebuild wikilinks"
  - "update cache"
  - "refresh cache"
  - "refresh wikilinks"
  - "update wikilink cache"
  - "rebuild entities"
allowed-tools: mcp__flywheel__get_all_entities, Write, Glob, Read
---

# Rebuild Wikilink Cache

Rebuild the wikilink entities cache by scanning the vault for pages.

## When to Use

Invoke when:
- You've added many new wikilinks
- Cache seems out of sync with your vault
- Want to ensure wikilink detection uses latest entities
- After adding aliases to note frontmatter
- Weekly/monthly maintenance routine

## Process Overview

### With Flywheel MCP (Recommended)

```
🪞 Flywheel MCP get_all_entities
  ↓
Returns ALL entities + aliases
  ↓
Categorize by type
  ↓
Write to .claude/wikilink-entities.json
  ↓
Report results
```

### Without Flywheel MCP (Fallback)

```
Glob for all *.md files
  ↓
Extract page names
  ↓
Categorize by type
  ↓
Write to .claude/wikilink-entities.json
  ↓
Report results
```

---

## Implementation

### Step 1: Get All Entities

**With Flywheel MCP:**
Call `mcp__flywheel__get_all_entities`:

```json
{
  "entity_count": 2388,
  "entities": [
    {
      "name": "Claude Code",
      "path": "tech/tools/Claude Code.md",
      "is_alias": false
    },
    {
      "name": "CC",
      "path": "tech/tools/Claude Code.md",
      "is_alias": true
    }
  ]
}
```

**Without Flywheel MCP:**
Use Glob to find all .md files, extract page names.

### Step 2: Categorize Entities

Apply heuristics to categorize wikilinks:

**Technologies** - Contains tech keywords:
- databricks, api, code, azure, sql, git, node, react
- powerbi, excel, copilot, fabric, apim, endpoint
- obsidian, claude, powershell, adf, adb, net, python

**Acronyms** - All uppercase, 2-6 characters:
- API, SQL, AWS, GCP

**People** - Two capitalized words:
- First Last format

**Projects** - Multi-word capitalized:
- Multi-word project names

**Other** - Everything else (proper nouns only)

**Exclusions:**
```python
EXCLUDE_SINGLE_WORDS = {
    'work', 'build', 'create', 'update', 'add', 'remove',
    'read', 'write', 'edit', 'view', 'show', 'hide',
    'today', 'tomorrow', 'yesterday', 'week', 'month',
    'the', 'and', 'for', 'with', 'from', 'this', 'that',
    'log', 'record', 'track', 'monitor', 'observe'
}
```

### Step 3: Save Cache

Write to `.claude/wikilink-entities.json`:

```json
{
  "technologies": ["Claude Code", "Azure", ...],
  "acronyms": ["API", "SQL", ...],
  "people": ["Person Name", ...],
  "projects": ["Project Name", ...],
  "other": [...],
  "_metadata": {
    "total_entities": 2388,
    "generated_at": "2025-12-31T04:38:00Z",
    "source": "flywheel",
    "generator": "flywheel v1.0.0"
  }
}
```

### Step 4: Report Results

```
🖋️ Flywheel - Cache Rebuilt
═══════════════════════════════════════════════
✅ Retrieved N entities

📋 Categorized:
   • Technologies: X entities
   • People: Y entities
   • Projects: Z entities
   • Acronyms: W entities
   • Other: V entities

💾 Saved to: .claude/wikilink-entities.json
═══════════════════════════════════════════════
```

---

## Benefits

1. **Fast Lookup**: Cache enables instant entity matching
2. **Includes Aliases**: Frontmatter aliases included (with Flywheel MCP)
3. **Categorized**: Organized by type for reporting
4. **Configurable**: Works with or without Flywheel MCP

## When to Rebuild

- After adding many new notes
- Weekly/monthly maintenance
- After major vault reorganization
- After adding aliases to frontmatter
- When wikilink suggestions seem outdated

## Six Gates Compliance

| Gate | Implementation |
|------|----------------|
| 1. Read Before Write | Reads vault entities via MCP before writing cache |
| 2. File Exists | N/A (creates cache file if missing) |
| 3. Chain Validation | N/A (single operation) |
| 4. Mutation Confirmation | Reports entity count before saving |
| 5. Health Check | Uses MCP get_all_entities for vault access |
| 6. Post Validation | Reports cache file location and stats |

---

**Version:** 1.0.0 (Flywheel)
