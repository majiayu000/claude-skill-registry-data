---
name: prd-format
description: >-
  PRD (Product Requirements Document) formatting skill for Linear issues.
  Use when creating or updating Linear issues to ensure consistent,
  AI-parseable structure with all required sections. Provides templates,
  defaults, and validation rules for issue quality.
---

# PRD Format Skill

Format Linear issues using PRD structure for AI-parseable, comprehensive issue documentation.

## Required Sections (All Issues)

Every Linear issue MUST include these 9 sections:

| Section | Required Content | Default if Empty |
|---------|------------------|------------------|
| Overview > The Problem | What is broken/missing/needed | ABORT - cannot be empty |
| Overview > Why It Matters | User/Business/Technical impact | ABORT - cannot be empty |
| Overview > Context | Background, related issues | "No additional context identified." |
| Out of Scope | What is NOT included | "TBD - to be refined during implementation" |
| Solution > Approach | How this will be solved | ABORT - cannot be empty |
| Solution > User Stories | Who benefits and how | Include for features; omit for bugs |
| Technical Requirements | Constraints, dependencies, code refs | See defaults below |
| Acceptance Criteria | Checkbox success criteria | ABORT - minimum 1 criterion |
| Open Questions | Unknowns to investigate | "No open questions identified." |

## PRD Template

```markdown
## Overview

### The Problem
[1-2 sentences describing the issue, bug, or opportunity]

### Why It Matters
- **User Impact**: [How this affects users]
- **Business Impact**: [Why this is important]
- **Technical Impact**: [System/codebase implications]

### Context
[Background, links to discussions, related issues]

## Out of Scope

The following are explicitly NOT part of this issue:
- [Item 1]
- [Item 2]

## Solution

### Approach
[High-level description of how this will be solved]

### User Stories
- **US-1**: As a [role], I want [action] so I can [outcome]

### Key Implementation Notes
- [Technical note 1]
- [Files/components to modify]

## Technical Requirements

### Constraints
- **Must use**: [Required technology/pattern]
- **Must preserve**: [Backward compatibility needs]

### Dependencies
- **Related**: [Similar issues]

### Code References
- Files to modify: `[paths]`
- Components affected: `[names]`

## Acceptance Criteria

- [ ] [Specific, measurable outcome 1]
- [ ] [Specific, measurable outcome 2]
- [ ] All type checks passing (`npm run typecheck`)
- [ ] All linting passing (`npm run lint`)

## Open Questions

- **Q1**: [Question needing investigation]
  - Status: To investigate
  - Decision: TBD

---

## AI Metadata

```json
{
  "complexity": "simple|moderate|complex",
  "createdBy": "Claude Code /creatework",
  "createdAt": "[ISO timestamp]",
  "prdVersion": "2.0"
}
```
```

## Default Content

### Out of Scope (when nothing specific)

```markdown
## Out of Scope

The following are explicitly NOT part of this issue:
- TBD - to be refined during implementation
- Future enhancements beyond core requirements
```

### Technical Requirements (when no constraints)

```markdown
## Technical Requirements

### Constraints
- **Must follow**: Existing codebase patterns and conventions
- **Must preserve**: Backward compatibility with existing functionality

### Dependencies
- **Related**: None identified

### Code References
- Files to modify: TBD during implementation
- Components affected: TBD during implementation
```

### Open Questions (when none identified)

```markdown
## Open Questions

No open questions identified at this time.

If questions arise during implementation, they should be:
1. Added to this issue as comments
2. Discussed with stakeholders before proceeding
```

## Adaptations by Issue Type

### Bug Fixes
- **Overview**: "The Bug" + current vs expected behavior
- **Out of Scope**: What's NOT being fixed
- **Solution**: Root cause + fix approach
- **Acceptance Criteria**: Bug no longer reproduces + regression test

### Features
- Full template with user stories
- Comprehensive acceptance criteria
- Include all technical requirements

### Error-Fix Issues
- **Overview**: Error count and types
- **Technical Requirements**: Specific error codes, file locations
- **Acceptance Criteria**: All errors resolved + validation passing

## Validation Rules

1. **NEVER omit sections** - use defaults instead
2. **NEVER use "N/A"** - use specific defaults
3. **ALWAYS include AI Metadata** - auto-generated
4. **Checkboxes required** - use `- [ ]` format for acceptance criteria
5. **Bold keywords** - use `**Must**`, `**Cannot**`, `**Requires**`

## Compliance Check

Before submitting, verify:
- [ ] All 9 sections present
- [ ] No empty required sections
- [ ] At least 1 acceptance criterion
- [ ] AI Metadata included
- [ ] Proper markdown formatting
