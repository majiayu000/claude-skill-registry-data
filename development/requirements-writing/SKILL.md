---
name: requirements-writing
category: pm
description: Use when capturing what a feature must do - write testable user-story requirements that state WHAT and WHY, never HOW, with assumptions made explicit
---
# Requirements Writing

## Overview

A requirement is a promise about behavior, written so QA can later prove it and a developer can build it without guessing. The recurring failures are requirements that specify implementation (HOW), bundle several behaviors into one, or hide assumptions that later surface as defects.

**Core principle:** State WHAT and WHY. HOW belongs to the architect and developers.

## The shape

- **User story:** As [persona], I want [capability], so that [outcome].
- **Context:** why now, what problem it solves.
- **Constraints:** hard limits (locale, performance, compliance) treated as given.
- **Assumptions:** stated explicitly — an unstated assumption becomes a defect.

## Rules

- **WHAT/WHY, not HOW — but field-aware.** `description` and `acceptance_criteria` state WHAT and WHY: "Users can export tasks to CSV" — not "add a `/export` endpoint using library X." Endpoints, files and tables belong only in `technical_description`, only once verified with code tools (`get_repo_tree`, `codebase_search`/`grep_code`), and only for small direct tasks you write yourself. A criterion may name an endpoint only when the API itself is the product surface (see acceptance-criteria-gwt's API-surface example) — not as a stand-in for what a user sees.
- **Independently testable.** If a requirement contains "and", consider splitting.
- **No solutioning in `description`/`acceptance_criteria`.** Naming a datastore, framework, or endpoint there is an architect/dev decision leaking in, even though the same name is correct in `technical_description`.

## Worked Example

```
❌ "Add a Redis cache to the task list endpoint so it's fast."
   (HOW — names the tech; "fast" is untestable)

✅ Story: As a project member, I want the task list to load quickly,
          so that I can scan my board without waiting.
   Context: boards with 500+ tasks feel sluggish today.
   Constraint: list renders < 500ms at p95 for 1000 tasks.
   Assumption: 1000 tasks is the realistic upper bound per project.
```

The architect chooses caching vs indexing vs pagination — the requirement fixes only the outcome and the bound.

## Common Mistakes

- Prescribing the implementation.
- "Fast/intuitive/robust" with no measurable target.
- One requirement covering three behaviors.
- Assumptions left unstated.

## Red Flags

- The requirement names a library, table, or endpoint.
- You can't say how QA would prove it.
- An adjective where a number belongs.
