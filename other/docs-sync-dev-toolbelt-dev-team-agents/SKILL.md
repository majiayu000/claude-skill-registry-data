---
name: docs-sync
description: Maintains docs/ — surgical patches, no duplicate content.
---

# Docs Sync

Agents call this skill after completing any task that changes project state. It patches the affected section in `docs/` — it never rewrites a whole file.

---

## Token Economy Rules

| Rule | Detail |
|------|--------|
| **Line budgets** | Each file has a hard max (see schemas below). Trim oldest or least-relevant entries when adding. `## Source References` does not count toward the budget. |
| **Tables over prose** | All structured data must be tables or bullet lists — never paragraphs. |
| **No duplicates** | If the information is in `CLAUDE.md`, do not repeat it here. |
| **No history** | Docs record current state only. Past decisions belong in git commits and ADRs. |
| **Surgical patches** | Read the current file first. Replace only the changed section using Edit — never Write the whole file. |
| **Freshness marker** | Every file has `<!-- last-updated: YYYY-MM-DD -->` on line 1. Update it on every write. |
| **No boilerplate** | Omit sections that are empty, N/A, or unknown. |
| **One source of truth** | If two docs would say the same thing, keep it in the more specific one and link from the other. |

---

## Document Schemas

### `docs/project.md` — max 80 lines

```markdown
<!-- last-updated: YYYY-MM-DD -->
# Project: [name]
## What It Does
## Type & Config
PROJECT_TYPE / TESTS_REQUIRED / CICD_PLATFORM
## Active Areas
| Directory | Purpose | Last Active |
## Key Constraints
```

### `docs/development/tech-stack.md` — max 60 lines

```markdown
<!-- last-updated: YYYY-MM-DD -->
# Tech Stack
| Layer | Technology | Version | Notes |
## Dev Setup
## Notable Dependencies
## Source References
```

### `docs/development/architecture.md` — max 100 lines

```markdown
<!-- last-updated: YYYY-MM-DD -->
# Architecture
## System Type
## Layers | Directory | Responsibility
## Module Map | Module/Service | Purpose | Key Entry Points
## API Contracts
## Source References
```

### `docs/development/code-standards.md` — max 80 lines

```markdown
<!-- last-updated: YYYY-MM-DD -->
# Code Standards
## Detected Config | Tool | Config File | Key Rules
## Naming Conventions
## Patterns in Use
## Anti-Patterns (project-specific)
## Source References
```

### `docs/backlog/README.md` — max 40 lines

```markdown
<!-- last-updated: YYYY-MM-DD -->
# Backlog
## Tracker
## Sprint Files | File | Sprint | Status
```

### `docs/design/design-system.md` — max 80 lines (UI projects only)

```markdown
<!-- last-updated: YYYY-MM-DD -->
# Design System
## UI Library / Color Tokens / Typography Scale / Component Inventory / Spacing Scale
```

---

## Task Closure Rule

**This is the canonical statement of the rule. Agents reference it; they do not restate it.**

After completing any task, check whether the work delivered triggers an entry in the Update
Triggers table below. If it does, apply the surgical patch to the relevant `docs/` file. Run it
in parallel with the commit — it is part of finishing the task, not a follow-up to it.

## When to Update What

Load `references/update-triggers.md` for: full trigger table (which work requires which doc), update protocol steps, and user-intent trigger patterns (convention signals, note-taking signals, approval signals).

Load `references/wiki-format.md` for: when to write wiki entries, entry format template, domain folder rules, wiki update protocol, and `wiki/README.md` format.
