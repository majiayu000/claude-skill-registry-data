---
name: writing-alto-skills
description: Use when creating or editing ALTO skills (skills/*/SKILL.md) or agents (agents/*.md). Guide for skill structure, frontmatter format, and content organization.
---

# Writing ALTO Skills

---

## Frontmatter Schema

```yaml
---
name: skill-name
type: discipline | technique | reference
triggers:
  - when [condition 1]
  - before [action 2]
word_limit: 300  # optional, default by type
---
```

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Skill identifier |
| `type` | Yes | Determines required sections |
| `triggers` | Yes | When skill activates (NOT workflow) |
| `word_limit` | No | Target word count |

### Types

| Type | Purpose | Default limit | Required sections |
|------|---------|---------------|-------------------|
| `discipline` | Enforce behavior rules | 300 | Hard rule, Warning signs |
| `technique` | How-to guides | 500 | Process/steps |
| `reference` | Lookup information | 800 | Quick reference table |

## Discipline Skills

For skills that enforce rules (TDD, verification, handoff format):

```markdown
## Hard Rule

[State the non-negotiable in one line]

## Warning Signs

If you catch yourself thinking:
- "[rationalization 1]"
- "[rationalization 2]"

STOP. [What to do instead].
```

Build warning signs from **observed failures**, not hypotheticals.

## Before Merging

Run skill through `alto-dev` subagent:

```
Test this skill: [paste skill content]
Scenario: [describe situation that should trigger it]
```

Observe:
- Did it read full skill or just triggers?
- Did it follow the process?
- What rationalizations did it attempt?

Add counters for any observed failures.

## Validation

Hook checks on commit:
- [ ] `triggers:` field present (not in description)
- [ ] Word count under limit for type
- [ ] Required sections present for type
- [ ] Description doesn't contain workflow words (then, next, after)
