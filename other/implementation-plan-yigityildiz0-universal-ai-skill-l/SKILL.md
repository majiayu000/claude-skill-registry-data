---
name: implementation-plan
description: "Produce a decision-complete, repository-grounded implementation plan with scope, architecture, file-level changes, data/API impacts, tests, migration, rollout, rollback, risks, and acceptance criteria. Use before substantial changes or when the user asks for a plan; inspect the actual project and infer safe details instead of running a fixed interview. Turkish triggers: uygulama planı hazırla, dosya bazlı teknik plan, test ve geri alma adımları."
license: MIT
---

# Implementation Plan

## Discover

Read project instructions, relevant tree/files, manifests, tests, configs, data contracts, recent history, and dirty-worktree state. Trace the current behavior and identify consumers. Verify external/library behavior from installed or current official sources when it can drift.

Ask only for a genuinely blocking choice that cannot be discovered or safely inferred. Otherwise state assumptions and continue.

## Plan content

```markdown
# Goal and measurable acceptance criteria
## Current behavior and evidence
## Scope in / out
## Assumptions and constraints
## Proposed design and alternatives rejected
## File-by-file changes
## API, schema, data, config, dependency, and security impacts
## Implementation sequence and dependencies
## Test and validation matrix
## Migration, compatibility, rollout, observability, and rollback
## Risks, edge cases, and unresolved decisions
```

Every step must identify the outcome, likely files/symbols, prerequisites, behavior preserved, validation, and rollback. Separate read-only diagnosis, local edits, and external/deployment actions; planning does not authorize publishing or production changes.

## Quality gate

- paths and current behavior were verified;
- acceptance criteria are observable;
- data/API compatibility and failure modes are covered;
- security/privacy/authorization boundaries are explicit;
- tests include normal, boundary, regression, and failure cases;
- migration is reversible and operational signals are defined;
- no placeholder "decide later" remains on the critical path.

Invoke through natural language or the active host's documented skill mechanism. Do not assume an external command file or slash command exists.
