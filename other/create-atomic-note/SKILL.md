---
name: create-atomic-note
description: Use this skill when saving a single-topic documentation note to docs/kb-exports/ for later knowledge base ingestion.
---

# Skill: create-atomic-note

## Purpose

Save a single-topic documentation note to `docs/kb-exports/` for periodic ingestion into the `TTA-notes` knowledge base.

## When to Use

After completing any significant task: new feature, bug fix, architectural decision, research finding, or outstanding TODO.

## Rules

1. **One topic per file.** Two topics = two files.
2. **Filename:** `YYYY-MM-DD_<kebab-case-slug>.md`
   - Example: `2026-03-04_persistence-primitives-design.md`
3. **YAML frontmatter is mandatory.** Every note must include all required fields (see template).
4. **Length limit:** ~300 lines max. If longer, split into multiple notes.
5. **Never write narrative prose for its own sake.** Be dense and factual.

## Required Frontmatter

```yaml
---
type: <note-type>
priority: <1|2|3>
status: draft
tags: [tta-dev]
source_agent: claude-code
date: YYYY-MM-DD
related_files: []
---
```

### Field Reference

| Field | Values | Notes |
|-------|--------|-------|
| `type` | `architecture` `decision` `bug-fix` `feature` `research` `todo` | Pick the closest match |
| `priority` | `1` `2` `3` | 1 = action needed now, 2 = medium, 3 = reference/low |
| `status` | `draft` `review` `stable` | New notes start as `draft` |
| `tags` | array | Always include `tta-dev`; add topic tags: `dev-todo` `learning-todo` `ops-todo` `template-todo` |
| `source_agent` | string | `claude-code`, `cline`, `copilot`, `gemini`, etc. |
| `date` | `YYYY-MM-DD` | Today's date |
| `related_files` | array of repo paths | Files this note documents; can be empty |

## Content Structure

```markdown
# <Short, Specific Title>

## Summary
One paragraph: what this is and why it matters.

## Context
What led to this? What problem was being solved?

## Decision / Finding
The actual content — be specific and dense.

## Consequences / Next Steps
What does this enable? What should happen next?
```

## Full Example

**Filename:** `2026-03-04_uow-abstract-base-class-design.md`

```markdown
---
type: architecture
priority: 2
status: draft
tags: [tta-dev, dev-todo]
source_agent: claude-code
date: 2026-03-04
related_files:
  - platform/primitives/src/tta_dev_primitives/persistence/uow.py
  - tests/unit/test_uow.py
---

# Unit of Work: Abstract Base Class Design

## Summary
AbstractUnitOfWork defines the contract for transactional boundaries in TTA.dev
persistence primitives. All concrete UoW implementations (Supabase, in-memory, fake)
inherit from it.

## Context
Needed a standard interface so workflow primitives can swap persistence backends
without changing business logic. Inspired by the Repository + UoW pattern from
Domain-Driven Design.

## Decision / Finding
- `AbstractUnitOfWork` exposes `commit()`, `rollback()`, and `__aenter__`/`__aexit__`
- `FakeUnitOfWork` ships in the testing module for use in unit tests
- No direct Supabase coupling in the abstract class

## Consequences / Next Steps
- Any new persistence backend just implements AbstractUnitOfWork
- TODO: add Dolt backend (see platform/dolt/)
```

## Where to Save

Always save to: `docs/kb-exports/<YYYY-MM-DD_slug>.md`

The `TTA-notes` repo ingests this directory periodically. Do not create subdirectories inside `kb-exports/`.
