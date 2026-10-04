---
name: auditing-canon
description: >-
  Verifies canon status, naming compliance, frontmatter completeness, writing
  standards, and cross-reference validity across worldbuilding files. Use when
  checking naming consistency, verifying frontmatter, auditing prose standards,
  or when user says "canon audit", "check names", "verify frontmatter", "writing
  standards check", or "naming audit". Does NOT check physics equations — use
  /auditing-physics for that.
model: sonnet
effort: high
---

# Auditing Canon

Verify naming, frontmatter, writing standards, and cross-references.

## Prerequisites

Read CLAUDE.md for locked spellings, naming conventions, and writing rules.

## Chain of Draft Mode

```
Name check. Human term found. Science dir. #### VIOLATION.
Frontmatter. status field missing. #### VIOLATION.
Spelling. Variant found. #### VIOLATION: use canonical form.
Cross-ref. Link resolves. #### PASS.
```

## Checks

### Naming
1. In-universe terminology used correctly per directory type
2. Locked spellings match CLAUDE.md table

### Frontmatter
3. Every file has YAML frontmatter: title, tags, status
4. Status is one of: canon, draft, needs-review, superseded

### Writing Standards (science files only)
5. Academic third-person prose throughout
6. No meta-commentary ("This section establishes...")
7. No narrative content in science directories
8. Citations use consistent format with ## References section

### Cross-References
9. All markdown links resolve to existing files
10. GLOSSARY.md entries exist for key terms

## Output

- **STYLE** — writing standard violation
- **META** — self-referential document language
- **DRIFT** — spelling or naming inconsistency
- **ORPHAN** — referenced entity has no file
- **BROKEN-REF** — link to nonexistent file

Do NOT fix anything. Report only.

## Out of Scope

Does NOT check physics consistency or equations (use /auditing-physics).
Does NOT treat cross-civilization differences as contradictions.
