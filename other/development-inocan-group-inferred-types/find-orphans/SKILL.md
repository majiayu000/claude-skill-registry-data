---
name: vault-orphans
description: Find orphan notes (notes with no backlinks). Triggers on "orphans", "orphan notes", "disconnected notes", "isolated notes", "notes with no links".
auto_trigger: true
trigger_keywords:
  - "orphans"
  - "orphan notes"
  - "disconnected notes"
  - "isolated notes"
  - "unlinked notes"
  - "notes with no backlinks"
  - "notes with no links"
  - "find orphans"
  - "show orphans"
  - "lonely notes"
  - "notes nobody links to"
  - "floating notes"
  - "unconnected"
  - "no links to"
  - "stranded notes"
  - "unloved notes"
allowed-tools: mcp__flywheel__find_orphan_notes, AskUserQuestion
---

# Orphans Skill

Find orphan notes - notes that have no backlinks (no other notes link to them).

## Purpose

Orphan notes represent disconnected knowledge that isn't integrated into your vault's knowledge graph. Finding orphans helps you:
- Identify notes that may be forgotten or lost
- Connect isolated knowledge to related concepts
- Improve vault connectivity
- Discover notes that might need better naming/tagging

## When to Use

Invoke when you want to:
- **Find disconnected notes**: "orphans" or "orphan notes"
- **Audit vault connectivity**: "show orphans" or "find isolated notes"
- **Improve linking**: "disconnected notes" before linking campaign
- **Vault maintenance**: Part of quarterly vault gardening

## Process

### 1. Call MCP Tool

```
Call: mcp__flywheel__find_orphan_notes
Parameters: { folder: optional }
```

### 2. Categorize Orphans

Group orphans by type for better analysis:

**By Folder:**
```
tech/: 50 orphans
work/: 80 orphans
personal/: 30 orphans
daily-notes/: 40 orphans
other: 50 orphans
```

**By Age:**
```
Recent (last 30 days): 20 orphans (may still need time)
Medium (30-90 days): 50 orphans (needs attention)
Old (90+ days): 180 orphans (likely forgotten)
```

### 3. Display Report

```
Orphan Notes Report
═══════════════════════════════════════════════

Found 250 orphan notes (25% of vault)
Total notes: 1,000

BREAKDOWN BY FOLDER:
  work/: 80 orphans (32%)
  tech/: 50 orphans (20%)
  daily-notes/: 40 orphans (16%)
  personal/: 30 orphans (12%)
  other: 50 orphans (20%)

BREAKDOWN BY AGE:
  Recent (<30 days): 20 (8%)
  Medium (30-90 days): 50 (20%)
  Old (90+ days): 180 (72%) ⚠️

HIGH-PRIORITY ORPHANS (20 shown):
📄 work/projects/data-platform.md
   Created: 2024-05-15 | Modified: 2024-05-15
   Tags: #work #project
   → CRITICAL: Major project with no links!

Options:
1. Show full list (all orphans)
2. Filter by folder/age/tags
3. Export to CSV for manual review
═══════════════════════════════════════════════
```

## Implementation Details

### Orphan Criteria

A note is an orphan if:
- ✅ It exists in the vault
- ✅ It has zero backlinks (no other notes link to it)
- ❌ Excluded: Template files
- ❌ Excluded: System files (.claude/, .obsidian/)

### Priority Scoring

Score orphans by importance (0-100):

```python
priority_score = 0

# Deduct for age (older = lower priority)
days_old = (today - created_date).days
if days_old < 30:
    priority_score += 30  # Recent
elif days_old < 90:
    priority_score += 20  # Medium
else:
    priority_score += 10  # Old

# Add for folder importance
if 'projects' in path:
    priority_score += 40
elif 'work' in path:
    priority_score += 30
elif 'tech' in path:
    priority_score += 20
else:
    priority_score += 10

# Add for tags
important_tags = ['project', 'goal', 'person', 'client']
priority_score += len([t for t in tags if t in important_tags]) * 10
```

## Related Skills

- **backlinks**: Shows existing backlinks (orphans have ZERO)
- **unlinked-mentions**: Find mentions not yet linked (helps connect orphans)
- **health**: Overall vault health (orphan % is key metric)
- **hubs**: Opposite of orphans (highly connected notes)

## Performance

- **MCP call**: ~500ms-1s for large vaults
- **Categorization**: ~200ms for 250 orphans
- **Total**: Usually <2 seconds
