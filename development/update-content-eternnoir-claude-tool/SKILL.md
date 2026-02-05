---
name: update-content
description: Update existing files in knowledge base with directory governance. Use when user wants to modify, edit, or update existing content. Reads RULE.md to maintain format consistency and follows update rules.
---

# Update Content Skill

Generic file update Skill that respects RULE.md constraints and maintains format consistency.

## When to use this Skill

- User says "update", "edit", "modify", "change"
- User references existing file or content
- User requests content revision
- User mentions specific file to update

## Workflow

### 1. Identify Target File

**If user provides file path**:
- Verify file exists
- Confirm with user if ambiguous

**If user provides topic/title only**:
- Search for file using Grep or Glob
- Pattern: `**/*keyword*.md`
- If multiple matches: present list, ask user to choose
- If no matches: report not found, offer to create instead

**Search strategies**:
1. Filename match: `find . -name "*keyword*"`
2. Content match: `grep -r "keyword" .`
3. README.md index: Search README.md files for references

### 2. Read Current Content

**Load existing file**:
- Use Read tool to load full content
- Understand current structure:
  - Frontmatter (if present)
  - Section headings
  - Content organization
  - Formatting style

**Analyze format**:
- Identify markdown structure
- Note any special formatting
- Detect metadata or frontmatter
- Understand content layout

### 3. Read Directory RULE.md

**Locate and read RULE.md**:
1. Check file's directory for RULE.md
2. If not found, check parent directories (inheritance)
3. Parse RULE.md for update rules

**Check for**:
- Are updates allowed? (some directories may be append-only or immutable)
- Format requirements to maintain
- Required fields that must be preserved
- Update workflow (e.g., "always add changelog entry")
- Versioning requirements

**Example RULE.md update rules**:
```markdown
## Update Rules
- Preserve frontmatter fields: title, date, tags
- Add "Last updated" timestamp to frontmatter
- Append changes to "Changelog" section
- Maintain markdown heading structure
```

### 4. Execute Update

**Apply requested changes**:
- Use Edit tool for targeted changes
- Or Write tool for complete rewrites (if needed)
- Maintain existing format per RULE.md
- Preserve required fields/structure

**Update modification metadata**:
- Update "Last updated" field (if present)
- Update modification timestamp in frontmatter
- Add changelog entry (if RULE.md requires)
- Preserve original creation date

**Maintain consistency**:
- Keep same formatting style (indentation, line breaks, etc.)
- Preserve markdown structure (headings hierarchy)
- Maintain frontmatter format (if present)
- Keep cross-references valid

### 5. Governance Update

**Update README.md**:
1. Read current README.md
2. Find entry for this file
3. Update description if content changed significantly
4. Update "Last modified" timestamp
5. Add to "Recent Changes" section
6. Save README.md

**Update parent README.md if needed**:
- If file significance changed
- If file moved to different category

**Verify updates**:
- Check README.md is valid markdown
- Ensure timestamps are current
- Verify file is still listed correctly

### 6. Report to User

**Confirm update complete**:
```
✅ File updated successfully

File: [path to file]
Changes: [summary of changes made]
Format: [maintained per RULE.md]

README.md updated:
- [directory]/README.md

What changed:
[Brief description of modifications]
```

## Special Cases

### Frontmatter Updates

If file has YAML frontmatter:

```yaml
---
title: Original Title
date: 2025-10-20
updated: 2025-10-28  # ← Update this
tags: [ai, ml]
---

[Content]
```

**Update process**:
1. Parse frontmatter
2. Preserve required fields (per RULE.md)
3. Update modification fields
4. Update content
5. Regenerate frontmatter with updates

### Versioned Content

If RULE.md requires versioning:

```markdown
## Changelog

### v1.2.0 (2025-10-28)
- [Changes made]

### v1.1.0 (2025-10-25)
- [Previous changes]
```

**Update process**:
1. Read current version
2. Increment version number (per RULE.md versioning scheme)
3. Add changelog entry
4. Update content
5. Update version in frontmatter

### Structured Content

If content has specific structure (sections, tables, etc.):

**Preserve structure**:
1. Identify section to modify
2. Update only targeted section
3. Maintain heading hierarchy
4. Keep other sections unchanged
5. Ensure valid markdown

### Append-Only Updates

If RULE.md specifies append-only (like logs):

```markdown
## RULE.md says: "This directory is append-only"
```

**Update process**:
1. Read current content
2. Append new content at end
3. Don't modify existing content
4. Add timestamp for new entry
5. Update README.md

### Cross-Reference Updates

If file contains links to other files:

**After update**:
1. Verify cross-references still valid
2. If file renamed/moved: update references
3. Check both directions (incoming and outgoing links)
4. Report any broken links

## Error Handling

### File Not Found
```
User: "Update the transformer note"
→ Search for file with "transformer" keyword
→ No matches found
→ Ask: "I couldn't find a file about transformers. Would you like to create one instead?"
```

### Multiple Matches
```
User: "Update the transformer note"
→ Find 3 files with "transformer":
  1. Research/AI/2025-10-28-transformer-architecture.md
  2. Research/AI/2025-10-20-transformer-applications.md
  3. Work/Projects/transformer-project.md
→ Present list: "I found 3 files. Which one?"
→ User selects → Proceed
```

### RULE.md Forbids Updates
```
RULE.md says: "This directory is immutable"
→ Warn user: "RULE.md indicates this directory should not be modified"
→ Ask: "Do you want to proceed anyway (override rule)?"
→ If yes: update and note rule override in README.md
→ If no: cancel operation
```

### Format Unclear
```
Current file has unusual format
→ Ask user: "This file has custom formatting. Should I:
  1. Maintain exact current format
  2. Apply standard format per RULE.md
  3. Let you specify format"
```

### Conflicting Changes
```
File was modified since user last viewed
→ Warn: "This file was modified recently (timestamp)"
→ Show recent changes
→ Ask: "Proceed with update or review changes first?"
```

### Update Breaks Structure
```
Proposed update would break markdown structure or frontmatter
→ Warn: "This update would create invalid structure"
→ Suggest: "I can apply a modified version that maintains structure"
→ Ask for confirmation
```

## Integration with Governance

This Skill automatically invokes the governance protocol:

**Before update**:
- Locate and read RULE.md
- Validate update is allowed
- Check format requirements

**During update**:
- Maintain format per RULE.md
- Preserve required fields
- Follow update workflows

**After update**:
- Update README.md
- Update modification timestamps
- Verify structure maintained

## Examples

### Example 1: Simple Update

**User**: "Update the transformer architecture note with new information about attention mechanisms"

**Skill workflow**:
1. Searches for file → Finds `Research/AI/2025-10-28-transformer-architecture.md`
2. Reads current content
3. Reads Research/AI/RULE.md → Updates allowed, maintain frontmatter
4. Applies changes using Edit tool
5. Updates "updated" field in frontmatter to 2025-10-28
6. Updates Research/AI/README.md timestamp
7. Reports: "✅ Updated transformer-architecture.md with attention mechanisms section"

### Example 2: Append-Only Log

**User**: "Add today's entry to my worklog"

**Skill workflow**:
1. Finds Work/WorkLog/2025/Q4/10-October/2025-10-28.md
2. Reads current content
3. Reads Work/WorkLog/RULE.md → Append-only, add timestamp
4. Appends new entry at end with timestamp
5. Updates hierarchical README.md files
6. Reports: "✅ Added entry to today's worklog"

### Example 3: Versioned Document

**User**: "Update the project spec with new requirements"

**Skill workflow**:
1. Finds Work/Projects/project-spec.md
2. Reads current version → v1.1.0
3. Reads Work/Projects/RULE.md → Requires versioning and changelog
4. Increments version → v1.2.0
5. Adds changelog entry:
   ```markdown
   ### v1.2.0 (2025-10-28)
   - Added new requirements section
   ```
6. Updates content
7. Updates frontmatter version field
8. Updates README.md
9. Reports: "✅ Updated project-spec.md to v1.2.0"

## Best Practices

1. **Always preserve existing structure** - Don't reformat unless requested
2. **Read RULE.md first** - Understand update constraints
3. **Use Edit for precision** - Target specific changes, don't rewrite entire file
4. **Maintain metadata** - Update timestamps, versions, changelog
5. **Update README.md immediately** - Keep index current
6. **Verify cross-references** - Ensure links still work
7. **Report clearly** - User should know what changed
8. **Handle conflicts gracefully** - Warn about concurrent modifications

## Notes

- This Skill works with any file structure by reading RULE.md
- Preserves format by default, changes only what's requested
- Respects update rules defined in RULE.md
- Automatically maintains README.md index
- Works in parallel with CLAUDE.md subagents
- Never updates RULE.md itself (that requires explicit permission via governance agent)
