---
name: document-formatting
description: Apply standard document formatting, metadata headers, and markdown structure when creating or updating project documents. Use when writing any document in the knowledge base.
---

# Document Formatting Standards

Apply these standards when creating or modifying any document in the project.

## YAML Frontmatter

Every document MUST have YAML frontmatter at the top:

### Intake Documents (to-process/)

```yaml
---
source: zoom|slack|jira|confluence|email|meeting|notes
original_filename: original-name.txt
intake_date: 2024-01-15
document_date: 2024-01-15
status: pending
participants:
  - Name One
  - Name Two
tags: []
source_confidence: high|medium|low
---
```

### Processed Documents (processed/)

```yaml
---
source: zoom|slack|jira|confluence|email|meeting|notes
original_filename: original-name.txt
intake_date: 2024-01-15
document_date: 2024-01-15
processed_date: 2024-01-15
status: processed
participants:
  - Name One
  - Name Two
tags:
  - topic1
  - topic2
extracted:
  tasks: 5
  definitions: 2
  people: 3
related_documents:
  - path/to/related.md
---
```

### Knowledge Base Entries

```yaml
---
type: task|definition|wiki|person|status|jira-draft
created: 2024-01-15
updated: 2024-01-15
sources:
  - processed/2024-01-15-zoom-sprint.md
tags:
  - tag1
  - tag2
---
```

## Document Structure by Type

### Task Entry

```markdown
---
type: task
created: 2024-01-15
updated: 2024-01-15
sources:
  - processed/2024-01-15-zoom-sprint.md
---

# Task: Brief Title

**Assignee:** Name or Unassigned
**Deadline:** YYYY-MM-DD or Not specified
**Priority:** High | Medium | Low | Not specified
**Status:** Pending | In Progress | Blocked | Done
**Project:** Project name

## Description

Clear description of what needs to be done.

## Source Context

> Original quote from source document

## Dependencies

- Depends on: [other task or item]
- Blocks: [what this blocks]

## Notes

Additional context or updates.
```

### Definition Entry

```markdown
---
type: definition
created: 2024-01-15
updated: 2024-01-15
sources:
  - processed/2024-01-15-zoom-sprint.md
---

# Term Name

**Also known as:** Alias1, Alias2 (if any)

## Definition

Clear, concise definition of the term.

## Context

How this term is used in the project context.

## Related Terms

- [[related-term-1]]
- [[related-term-2]]

## Sources

- First mentioned: [source document]
- Also appears in: [other documents]
```

### Person Profile

```markdown
---
type: person
created: 2024-01-15
updated: 2024-01-15
sources:
  - processed/2024-01-15-zoom-sprint.md
---

# Full Name

## Basic Info

| Field | Value |
|-------|-------|
| Role | Job Title |
| Team | Team Name |
| Expertise | Area1, Area2 |

## Responsibilities

- Responsibility 1
- Responsibility 2

## Document Mentions

| Date | Document | Context |
|------|----------|---------|
| 2024-01-15 | source.md | Brief context |

## Working Relationships

- Works with: Name1, Name2
- Reports to: Manager Name
```

### Project Status

```markdown
---
type: status
project: project-name
period: 2024-W03 or 2024-01-15
created: 2024-01-15
updated: 2024-01-15
sources:
  - processed/2024-01-15-zoom-sprint.md
---

# Project Name - Status Update

**Period:** Week of January 15, 2024
**Updated:** 2024-01-15

## Summary

Brief summary of current state.

## Progress

- Completed item 1
- Completed item 2

## In Progress

- Current work item 1
- Current work item 2

## Blockers

- Blocker 1
- Blocker 2

## Decisions Made

- Decision 1: Rationale
- Decision 2: Rationale

## Next Steps

- Upcoming item 1
- Upcoming item 2
```

### JIRA Draft

```markdown
---
type: jira-draft
created: 2024-01-15
source_document: processed/2024-01-15-zoom-sprint.md
suggested_project: PROJ
---

# [Draft] Ticket Title

**Type:** Story | Bug | Task | Epic
**Priority:** High | Medium | Low
**Suggested Assignee:** Name or Unassigned

## Summary

One-line summary for JIRA title.

## Description

Detailed description of the work.

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Source Context

> Original discussion that led to this ticket

**From:** [source document]

## Notes

Any additional context for ticket creation.
```

### Wiki Article

```markdown
---
type: wiki
created: 2024-01-15
updated: 2024-01-15
sources:
  - processed/2024-01-15-zoom-sprint.md
tags:
  - topic1
  - topic2
---

# Article Title

## Overview

Brief overview of the topic.

## Details

### Section 1

Content for section 1.

### Section 2

Content for section 2.

## Related

- [[related-article-1]]
- [[related-article-2]]

## Sources

- [Source Document](path/to/source.md)
```

### Proposed Update

```markdown
---
type: proposed-update
proposal_id: update-001
created: 2024-01-15
target_file: knowledge/tasks/project-tasks.md
change_type: update|add|merge|archive
source_document: processed/2024-01-15-zoom-sprint.md
confidence: high|medium|low
status: pending_review
---

# Proposed Update: Brief Title

## Target

**File:** knowledge/tasks/project-tasks.md
**Section:** Task status for "Implement auth"

## Change Type

`update` - Modify existing content

## Current Content

```markdown
**Status:** In Progress
```

## Proposed Content

```markdown
**Status:** Done
**Completed:** 2024-01-15
```

## Rationale

In the sprint review meeting, John confirmed this task was completed.

## Source Evidence

**Document:** processed/2024-01-15-zoom-sprint.md
**Quote:**
> "The authentication work is done, we merged it yesterday."

---

## Review Actions

- [ ] Approve and apply
- [ ] Modify and apply
- [ ] Reject
- [ ] Defer

**Reviewer Notes:**

```

## Naming Conventions

### File Names

- **Dates**: Always `YYYY-MM-DD` format
- **Sources**: Lowercase (`zoom`, `slack`, `jira`, `confluence`, `email`, `meeting`, `notes`)
- **Descriptions**: Lowercase, hyphens for spaces, max 50 characters
- **Full pattern**: `YYYY-MM-DD-<source>-<description>.md`

### Examples

```
2024-01-15-zoom-sprint-planning.md
2024-01-16-slack-data-pipeline-discussion.md
2024-01-17-jira-proj-1234-auth-bug.md
2024-01-18-email-quarterly-review.md
2024-01-19-meeting-architecture-review.md
2024-01-20-notes-research-findings.md
```

### Knowledge Base Files

- **Tasks**: `<project>-tasks.md` or `<topic>-tasks.md`
- **Definitions**: `<term>.md` (lowercase, hyphens)
- **People**: `<firstname>-<lastname>.md` (lowercase)
- **Wiki**: `<topic>.md` (descriptive name)
- **Status**: `<project>-status.md` or `<project>-YYYY-MM-DD.md`
- **JIRA drafts**: `draft-<brief-title>.md`

## Markdown Guidelines

1. **Headers**: Use `#` hierarchy (H1 for title, H2 for sections, etc.)
2. **Lists**: Use `-` for unordered, `1.` for ordered
3. **Code**: Use backticks for inline, triple backticks for blocks
4. **Links**: Use `[[internal-link]]` or `[text](path)` format
5. **Tables**: Use standard markdown table syntax
6. **Quotes**: Use `>` for quoted text from sources
7. **Checkboxes**: Use `- [ ]` for incomplete, `- [x]` for complete
