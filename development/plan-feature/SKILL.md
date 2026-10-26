---
name: plan-feature
description: Turn an approved spec into plan.md + tasks.md ready for implementation — after running the S/M/L sizing gate. Use when a spec exists and the user says "plan", "how should we build", "break this down", or names a spec number. Resolves open questions, checks conflicts with other active specs, inventories existing code to reuse, and maps every acceptance criterion to a test before any code is written.
argument-hint: [spec number or slug]
allowed-tools: Read Grep Glob Write AskUserQuestion
---

## Context

- Specs: !`ls -1 specs | grep -E '^[0-9]' || echo "none"`
- Active slices: !`ls -1 src/features 2>/dev/null`

## Task

Plan spec **$ARGUMENTS**: produce `plan.md` and `tasks.md` next to its `spec.md`.

### Step 0 — SIZING GATE (mandatory; prevents process-overkill — ADR-0006 / ADR-0005)

Classify the work and SAY the classification out loud:

- **S (small)** — bug fix, copy change, single-component tweak. → **STOP planning.** No plan, no tasks. Tell the user: "This is S-size; implement it directly with a regression test." Planning docs for small work are waste.
- **M (story)** — one feature slice, ≤ ~2 days. → produce `plan.md` (lean) + `tasks.md`.
- **L (large)** — multi-slice, native config changes, new architecture. → full `plan.md` (with ADR if needed) + `tasks.md`.

If material ambiguities remain in the spec, run `/clarify` first (≤5 questions), then continue.

### Step 1 — Gate on the spec

Read the spec. If _Open questions_ is non-empty or ACs are untestable, stop and resolve them with the user (AskUserQuestion) — update the spec first. Planning against an ambiguous spec produces confident garbage.

### Step 2 — Ground in architecture + inventory existing code

Read `docs/architecture/overview.md`, `docs/architecture/module-boundaries.md`, the conventions relevant to the work, and skim `src/features/tasks/` as the canonical slice. **Inventory the existing code the work touches** and list it in `plan.md` as "Already exists — reuse, do not recreate" with file paths (regenerating existing code as duplicates is a known agent failure mode; this section is the guard). If the plan needs a new dependency, a boundary exception, or a native module, draft the ADR (in `docs/architecture/decisions/`, copy `_template.md`) as part of the plan — never bury an architectural decision inside a feature plan.

### Step 3 — Conflict check

Compare this spec's _areas touched_ against every other spec with status `active` in `specs/README.md`. Overlap → flag it in `plan.md`'s _Overlap check_ with a resolution (sequence, coordinate, or split), and tell the user.

### Step 4 — Write plan.md

From `specs/TEMPLATE/plan.md`. The AC→verification table is the heart: every AC names the exact test (`__tests__/*.test.ts(x)` or `.maestro/flows/<slug>.yaml` step) that will prove it. An AC with no test is a planning failure, not a detail. Hard cap: 2 pages — a plan longer than the diff it produces is a smell.

### Step 5 — Write tasks.md

From `specs/TEMPLATE/tasks.md`: ordered, ≤30-min tasks, files named, done-check per task, `[P]` where parallel-safe. Test tasks come before their implementation tasks; every AC maps to ≥1 task (unmapped AC → open question, not invented work). Phases: setup → core behavior → verification → review & ship.

### Step 6 — Flip status + hand off

Flip the spec to `active` in `specs/README.md`. Report: size verdict, reuse inventory, plan summary (3 lines), risk list, and "run `/implement-feature $ARGUMENTS` to execute". **Do not start coding.**

Plans are reviewed by humans — keep both files lean enough to be read honestly in five minutes.
