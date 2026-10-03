---
name: tech-debt
description: >-
  Scans and prioritizes tech debt and code-health cleanups. Use when asking what
  to clean up, assessing code health, planning refactors, or prioritizing debt.
  Do not use for a single design decision (architecture) or for implementing a
  chosen deepening refactor without a scan.
---

# Tech Debt

Surface debt, rank it, and propose small reversible cleanups — do not boil the ocean.

## Related

- Deepening opportunities with domain language → `improve-codebase-architecture`
- Single design choice → `architecture`

## Workflow

1. **Scope** — directory, service, or theme (testability, duplication, coupling).
2. **Collect signals** — hotspots, shallow modules, duplicated logic, missing tests, TODO/FIXME age, flaky tests, oversized files. See `references/debt-signals.md`.
3. **Rank** — impact × frequency × risk of change. Prefer high-leverage, low-blast-radius items.
4. **Propose slices** — each item: problem, proposed move, verification, estimated risk. One PR-sized slice per item when possible.
5. **Separate from features** — do not mix opportunistic cleanup into unrelated ticket PRs unless required for the change.

## Constraints

- Refactors preserve behavior by default unless the goal explicitly changes behavior.
- Prefer deleting pass-through abstractions over polishing them.
- No speculative generality “for later”.

## Verification

- [ ] Scope stated
- [ ] Ranked list with rationale
- [ ] Each proposed slice has a verification plan
- [ ] Non-goals / deferred items listed
