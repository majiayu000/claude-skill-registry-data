---
name: spec-lint
owner: baseline
description: Preflight a spec draft without saving. Runs the same checks as the write-boundary hooks — PlantUML syntax, required diagram presence, AC-to-sequence traceability, Design calls quality floor, and System delta row resolution — and prints a compact pass/fail table. Use while iterating so the hooks don't bite on save.
---

> Checker config (tier-dial:read-path): this checker's floor/ceiling come from the tier dial at `.claude/hooks/lib/tier-dial.mjs` via `resolveCheckerThreshold('spec')`. Advisory only this slice (v1 piece 2); blocking is piece 5.

# spec-lint — preflight a spec draft

Invocable by both user (`/spec-lint <slug>`) and Claude (when iterating on a spec and wanting to check status before writing).

## What it checks

Five checks always run, same logic as the hooks, but advisory (no writes are blocked). One more
appears only when its trigger fires.

Checks are identified by **row name**, in the order the report prints them. Ordinals are deliberately
absent: they have already drifted once — `lint.mjs` labels the codesign check "#4" in its own comment
while the report prints it last — and a number that means one thing in the source and another in the
table is worse than no number.

| Check | Row name | Hook it mirrors |
|---|---|---|
| Every ```plantuml``` fence parses under `plantuml -checkonly` | `plantuml_syntax` | `plantuml_syntax_guard` |
| Required diagram kinds present (config: `project.json → artifacts.required_diagrams.spec`) | `diagram_presence` | `spec_diagram_presence_guard` |
| Every `AC-NNN` row in the Acceptance criteria table references a `§Behavior #N` section that exists | `ac_traceability` | (no hook — unique to the lint) |
| Each `## Design calls` row carries a populated Reference target and Quality criteria | `design_calls` | `spec_design_calls_guard` |
| Each `## System delta` row resolves — an `add` anchors inside the governed surface, a `change`/`remove` names an existing element | `system_delta` | (no hook — the guard checks only that the section is present) |

| Conditional check | Row name | Fires when |
|---|---|---|
| A `## Decisions` section is present | `codesign_decisions` | `workflow.json → codesign_mode` is `true` |

`system_delta` reports `SKIP` when `project.json → memory.architecture_map.enabled` is not `true`. The
corpus at `docs/system/` is opt-in, so a project that has not adopted it declares no delta and the
check has nothing to resolve.

## Invocation

`/spec-lint <slug>` — where `<slug>` corresponds to `docs/specs/<slug>.md`.

## Steps

1. Validate the slug: `docs/specs/<slug>.md` must exist.
2. Run:
   ```
   node .claude/skills/spec-lint/lint.mjs <slug>
   ```
3. Print the script's output verbatim to the user. It is a table with one row per check and a final summary line.

## Output format

```
check                              status
---------------------------------- ------
plantuml_syntax                    PASS
diagram_presence                   FAIL  (missing: c4_component, dependency_graph)
ac_traceability                    FAIL  (AC-002 → §Behavior #2 not found)
design_calls                       PASS
system_delta                       FAIL  (add row foo-guard: anchor docs/notes/x.md falls outside the governed surface)
---------------------------------- ------
overall                            FAIL
```

Exit 0 on overall PASS, 1 on overall FAIL. Intended for use in CI or a pre-commit loop as well as interactively.

## Prerequisites

- `plantuml` CLI on PATH for check #1 (if absent, #1 is reported as `SKIP (no plantuml)`; the rest still run).

## Notes

- Unlike the hooks, `spec-lint` runs against the on-disk file, not proposed content. Save or use the hooks to validate an unsaved draft.
- `spec-lint` does not render. Use `/spec-render <slug>` for that.
