---
name: vault-unlinked-mentions
description: Find places where an entity is mentioned but not wikilinked. Triggers on "unlinked mentions", "where is X mentioned", "link X everywhere", "mentions of X".
auto_trigger: true
trigger_keywords:
  - "unlinked mentions"
  - "unlinked mentions of"
  - "where is"
  - "where mentioned"
  - "link everywhere"
  - "mentions of"
  - "mentions for"
  - "find mentions"
  - "unlinked references"
  - "references to"
  - "mentioned but not linked"
  - "plain text mentions"
  - "could be linked"
  - "linkable text"
  - "should have links"
  - "potential links"
allowed-tools: mcp__flywheel__get_unlinked_mentions, Read, Edit, AskUserQuestion
---

# Unlinked Mentions Skill

Find all places where an entity (note title or alias) is mentioned in vault text but not yet wikilinked.

## Purpose

This skill helps you:
- Find "orphan references" (entity mentioned but never linked)
- Complete your wikilink graph
- Discover implicit connections in your vault
- Apply consistent linking for important entities

## When to Use

Invoke when you want to:
- **Find where an entity is mentioned**: "where is Databricks mentioned"
- **Link entity everywhere**: "link Databricks everywhere"
- **Check unlinked references**: "unlinked mentions of Claude Code"
- **Audit entity usage**: "find mentions of John Smith"

## Process

### 1. Identify Entity

Extract entity name from user's question:
- "unlinked mentions of **Databricks**" → Entity: "Databricks"
- "where is **Claude Code** mentioned" → Entity: "Claude Code"

If entity is ambiguous, use AskUserQuestion to clarify.

### 2. Call MCP Tool

```
Call: mcp__flywheel__get_unlinked_mentions
Parameters: { entity: "Databricks" }
```

### 3. Display Results

Show formatted report:

```
Unlinked Mentions: [[Databricks]]
═══════════════════════════════════════════════

Found 5 unlinked mentions across 3 notes:

📄 daily-notes/2025-12-30.md:42
   > Working with Databricks today

📄 work/projects/data-migration.md:15
   > Using Databricks for ETL pipeline

📄 tech/tutorials/spark-intro.md:23
   > Databricks provides a managed Spark environment

═══════════════════════════════════════════════

Options:
1. Apply wikilinks automatically (safe - no code/frontmatter)
2. Review each mention individually
3. Cancel
```

### 4. Apply Wikilinks (Optional)

If user chooses option 1 or 2:

**Option 1 (Automatic):**
- Read each file
- Apply wikilinks using safe patterns (skip code blocks, frontmatter, URLs)
- Edit files with new links
- Report: "Applied 5 wikilinks across 3 notes"

**Option 2 (Review):**
- For each mention:
  - Show context (3 lines before/after)
  - Ask: "Link this mention? (y/n)"
  - Apply if yes, skip if no
- Report: "Applied 3 wikilinks, skipped 2"

## Implementation Details

### Entity Resolution

If entity doesn't exist as exact note title:
- Check for aliases (frontmatter)
- Suggest similar entities
- Ask user to confirm or choose alternative

### Safe Linking Rules

When applying wikilinks automatically:

**NEVER link inside:**
- YAML frontmatter (between --- markers)
- Code blocks (triple backtick fenced)
- Inline code (single backticks)
- Existing wikilinks
- Markdown links
- Bare URLs

**ALWAYS:**
- Use word boundaries (don't partial match)
- Preserve original capitalization
- Match case-insensitive but preserve case
- Link only FIRST occurrence per file (avoid over-linking)

### Example Edit Pattern

**Before:**
```
Working with Databricks today on the ETL pipeline.
Need to check Databricks documentation.
```

**After:**
```
Working with [[Databricks]] today on the ETL pipeline.
Need to check Databricks documentation.
```

Note: Only first occurrence linked (convention to avoid cluttering text).

## Use Cases

### 1. Entity Audit
**Scenario:** You created a new note and want to find all mentions.
**Command:** "unlinked mentions of My Topic"
**Result:** Finds places where "My Topic" appears but isn't linked

### 2. Consistency Check
**Scenario:** You have a person note but sometimes reference differently in text.
**Command:** "where is John mentioned"
**Result:** Finds unlinked text, applies aliased links

### 3. Retroactive Linking
**Scenario:** You just created a new concept note after writing about it for months.
**Command:** "link My New Concept everywhere"
**Result:** Finds all historical mentions and creates proper wikilinks

## Related Skills

- **backlinks**: Shows existing backlinks (this skill finds MISSING links)
- **suggest**: Suggests wikilinks for current note (this skill targets specific entity)
- **fix-links**: Fixes broken links (this skill creates NEW links)
- **rebuild-wikilink-cache**: Updates entity cache (run before this if cache is stale)

## Six Gates Compliance

| Gate | Implementation |
|------|----------------|
| 1. Read Before Write | Reads each file before applying wikilinks |
| 2. File Exists | Validates entity note exists before linking |
| 3. Chain Validation | N/A (single operation) |
| 4. Mutation Confirmation | Shows mentions found, user chooses auto or review |
| 5. Health Check | Uses MCP get_unlinked_mentions for vault access |
| 6. Post Validation | Reports count of wikilinks applied per file |

## Performance

- **MCP call**: ~200-500ms for typical entity
- **File edits**: ~100ms per file
- **Total**: Usually <5 seconds for 10-20 mentions
