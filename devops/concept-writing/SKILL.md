---
name: concept-writing
description: Ensure story concepts have complete content (title, description, user story). Use when heartbeat finds a concept-stage story or when explicit concept needs writing. Validates completeness and fills missing fields.
disable-model-invocation: true
---

# Concept Writing

Ensure story concepts have all required fields populated before vetting. This skill validates and completes concept-stage stories.

**Database:** `.claude/data/story-tree.db`

**Critical:** Use Python sqlite3 module, NOT sqlite3 CLI.

**Platform Note:** All Python commands use `python` (not `python3`) for cross-platform compatibility.

## Overview

A complete concept requires three fields:

1. **title** - Concise name for the story
2. **description** - Context explaining why this story exists, gap analysis, related work
3. **story** - User story in format: "As a [user], I want [goal], so that [benefit]"

This skill:
- Validates all three fields are present
- Generates missing fields by analyzing tree context
- Skips if concept is already complete
- Prepares story for vetting workflow

## Workflow

### Step 1: Load Story

```python
python -c "
import sqlite3, json
conn = sqlite3.connect('.claude/data/story-tree.db')
conn.row_factory = sqlite3.Row
story = conn.execute('''
    SELECT id, title, description, story, stage, hold_reason, terminus
    FROM story_nodes WHERE id = ?
''', ('STORY_ID',)).fetchone()
if story:
    print(json.dumps(dict(story), indent=2))
else:
    print('{}')
conn.close()
"
```

Replace `STORY_ID` with the target story ID.

### Step 2: Validate Story State

Check that:
- Story exists
- `stage = 'concept'`
- `hold_reason IS NULL` (not on hold)
- `terminus IS NULL` (not terminal)

If story doesn't meet criteria, skip with message explaining why.

### Step 3: Check Completeness

A concept is complete if:
- `title` is not empty
- `description` is not empty
- `story` is not empty and follows "As a... I want... so that..." format

If all fields are populated and non-empty, skip with message: "Concept already complete for story {id}"

### Step 4: Generate Missing Fields

If any required field is missing:

1. **Read tree context:**
   - Parent story (if exists)
   - Sibling stories at same level
   - Project goals and vision

2. **For missing title:**
   - Extract from description if available
   - Generate from parent context and story purpose
   - Keep concise (max 8-10 words)

3. **For missing description:**
   - Explain the context/gap this story addresses
   - Reference parent story and related work
   - Include "Related context:" section referencing commits, parent stories, or design docs
   - Typically 200-500 characters

4. **For missing story:**
   - Write in user story format: "As a [user], I want [goal], so that [benefit]"
   - Make specific and testable
   - Focus on user value, not implementation

### Step 5: Update Database

```python
python -c "
import sqlite3
conn = sqlite3.connect('.claude/data/story-tree.db')
conn.execute('''
    UPDATE story_nodes
    SET title = ?,
        description = ?,
        story = ?,
        updated_at = datetime('now')
    WHERE id = ?
''', ('TITLE', 'DESCRIPTION', 'STORY', 'STORY_ID'))
conn.commit()
conn.close()
print('Updated story STORY_ID')
"
```

### Step 6: Report Result

Output a summary:
```
CONCEPT WRITING COMPLETE
========================

Story: {id}
Title: {title}

Fields updated:
- title: {created|updated|unchanged}
- description: {created|updated|unchanged}
- story: {created|updated|unchanged}

Ready for vetting.
```

## Example: Complete Concept

```
ID: 1.1.2.1
Title: AI Categorization Using Command Line Context
Description: **Related context:** Parent story 1.1.2 implemented cmdline capture (tracker_windows_cmdline.py) and storage (database_schema_events.py:74-77). Vision states "AI-Powered Categorization: Intelligent activity classification" and "Context-Aware Categorization: capture rich contextual data" - cmdline provides that rich data, but it's not yet feeding into AI categorization logic. Gap: Data captured but not used for its intended purpose (matter matching).
Story: As a lawyer working on multiple matters simultaneously, I want the AI categorization system to analyze process command line arguments, so that activities can be accurately matched to matters based on file paths, Chrome profiles, and workspace contexts captured in cmdline
```

## Example: Incomplete Concept (Missing Story Field)

**Before:**
```
ID: 1.1.2.1.1
Title: Extract Matter Hints from Command Line Arguments
Description: **As a** lawyer using SyncoPaid...  (full user story in wrong field)
Story: (empty)
```

**After concept-writing:**
```
ID: 1.1.2.1.1
Title: Extract Matter Hints from Command Line Arguments
Description: **Related context:** Parent story 1.1.2.1 identifies the gap: cmdline data is captured (story 1.1.2) but not used by AI. Recent commits show vision_engine.py implements AI categorization but doesn't yet consume cmdline data. This story provides the extraction layer that prepares cmdline data for AI consumption - the first step before modifying vision_engine to actually use these hints.
Story: As a lawyer using SyncoPaid, I want AI to extract matter-related hints from command line arguments, so that AI can more accurately categorize activities to the correct matter
```

## Common Scenarios

### Scenario: Concept Already Complete

If all fields are populated:
```
Concept already complete for story 1.1.2.1
Skipping to vetting.
```

### Scenario: Story Field Improperly Formatted

If `story` exists but doesn't follow "As a... I want... so that..." format:
```
Story field exists but improperly formatted.
Regenerating in correct format...
```

### Scenario: Story on Hold

If `hold_reason IS NOT NULL`:
```
ERROR: Story 1.1.2.1 is on hold (hold_reason=polish)
Cannot write concept for held stories.
```

### Scenario: Wrong Stage

If `stage != 'concept'`:
```
ERROR: Story 1.1.2.1 is at stage 'planning'
This skill only works on concept-stage stories.
```

## References

- **Database:** `.claude/data/story-tree.db`
- **Schema:** `.claude/skills/story-tree/references/schema.sql`
- **Concept Workflow:** `.claude/skills/story-tree/references/workflow1-concept.md`
- **Next Step:** After concept-writing completes, run `/concept-vetting` (vet-concept.yml)
