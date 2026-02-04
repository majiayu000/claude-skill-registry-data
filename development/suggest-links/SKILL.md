---
name: vault-suggest
description: Suggest wikilinks for current note using Flywheel MCP. Triggers on "suggest links", "link suggestions", "what should I link", "wikilink suggestions".
auto_trigger: true
trigger_keywords:
  - "suggest links"
  - "link suggestions"
  - "what should I link"
  - "wikilink suggestions"
  - "suggest wikilinks"
  - "recommendations for links"
  - "what to link"
  - "find linkable"
  - "linkable entities"
  - "add links to this"
  - "should be linked"
  - "linkify"
  - "autolink"
  - "link opportunities"
  - "where to link"
  - "improve linking"
allowed-tools: mcp__flywheel__suggest_wikilinks, mcp__flywheel__get_unlinked_mentions, Read, Edit, AskUserQuestion
---

# Suggest Wikilinks Skill

Suggest wikilinks for the current note using Flywheel MCP's intelligent analysis.

## Purpose

This skill analyzes the current note and suggests:
- Entities mentioned but not linked
- Relevant concepts based on content
- Similar note connections
- Tag-based link opportunities

Enhanced with `get_unlinked_mentions` for targeted entity linking.

## When to Use

Invoke when you want to:
- **Improve current note linking**: "suggest links" or "what should I link"
- **Find missed connections**: "link suggestions" or "wikilink suggestions"
- **Link specific entity**: "suggest links for databricks"
- **After writing**: "what to link" after completing a note

## Process

### 1. Get Current Note

Extract current note path from context or ask user:
- If in editor context: Use active note path
- If unclear: Ask user which note

### 2. Call MCP Tool

```
Call: mcp__flywheel__suggest_wikilinks
Parameters: {
  text: note_content
}
```

### 3. Enhance with Unlinked Mentions

For each high-confidence suggestion:
```
Call: mcp__flywheel__get_unlinked_mentions
Parameters: {entity: "Databricks"}
```

This provides:
- Exact locations where entity is mentioned
- Context around each mention
- Line numbers for precise linking

### 4. Display Suggestions

```
Wikilink Suggestions for: work/projects/etl-pipeline.md

Found 8 linkable entities:

HIGH CONFIDENCE (90+%)
  1. Databricks (95%)
     "Working with Databricks on the ETL pipeline"
     Target: tech/data/Databricks.md
     Occurrences: 3 mentions in this note

  2. Azure (88%)
     "Deploy to Azure production environment"
     Target: tech/cloud/Azure.md
     Occurrences: 2 mentions in this note

MEDIUM CONFIDENCE (70-89%)
  3. Python (82%)
     "Write Python scripts for data transformation"
     Target: tech/languages/Python.md
     Occurrences: 1 mention

LOW CONFIDENCE (50-69%)
  4. Spark (65%)
     "Use Spark for distributed processing"
     Target: tech/data/Spark.md
     Occurrences: 1 mention

Options:
1. Apply all high-confidence links (2 entities, 5 total mentions)
2. Review and select links individually
3. Apply all links (8 entities)
4. Cancel
```

### 5. Apply Links (If User Confirms)

**Option 1 (High Confidence Only):**
- Apply links for high-confidence entities
- Skip medium/low confidence
- Safe, conservative approach

**Option 2 (Review Each):**
- For each suggestion:
  - Show context
  - Ask: "Link this entity? (y/n/skip-all)"
  - Apply if yes

**Option 3 (Apply All):**
- Link all entities across all mentions
- Aggressive linking approach
- May create some false positives

## Implementation Details

### Confidence Scoring

Flywheel MCP provides confidence scores:

```
90-100%: Very high confidence
  - Exact title match
  - Clear context
  - Unambiguous entity

70-89%: High confidence
  - Good title match
  - Relevant context
  - Minor ambiguity possible

50-69%: Medium confidence
  - Partial match
  - Ambiguous context
  - Multiple candidates possible

Below 50%: Low confidence (don't suggest)
```

### Safe Linking Rules

When applying links automatically:

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
- Link only FIRST occurrence per entity (convention)
- Validate link target exists

## Related Skills

- **unlinked-mentions**: Find mentions of specific entity (this skill uses it!)
- **backlinks**: See existing connections
- **orphans**: Find notes with no backlinks
- **fix-links**: Fix broken links (this creates new links)

## Related Hooks

- **wikilink-auto.py** (PostToolUse hook): Auto-applies wikilinks after edits
  - This skill is the MANUAL version
  - Hook uses cache, this skill uses MCP (more accurate)
  - Hook is automatic, this skill requires invocation

## Six Gates Compliance

| Gate | Implementation |
|------|----------------|
| 1. Read Before Write | Reads note content before suggesting links |
| 2. File Exists | Validates note and link targets exist |
| 3. Chain Validation | N/A (single operation) |
| 4. Mutation Confirmation | Shows suggestions with confidence scores, user selects |
| 5. Health Check | Uses MCP suggest_wikilinks for vault access |
| 6. Post Validation | Reports count of wikilinks applied |

## Performance

- **MCP call (suggest)**: ~500ms-1s depending on note length
- **MCP call (unlinked_mentions)**: ~200ms per entity
- **File edit**: ~100ms
- **Total**: 2-5 seconds for typical note with 5-10 suggestions
