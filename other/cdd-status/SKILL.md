---
name: cdd-status
description: "Generate a project progress dashboard from workflow-catalog.yaml. Reads current stage, required steps, artifact evidence, validation gaps, writes production/project-roadmap.md after approval, and mirrors to memory_bank/t2_execution/current_roadmap.md only when the Memory Bank root exists and that path and effect are covered."
argument-hint: "[optional: --dry-run | --write]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
model: haiku
---
Read and apply `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`,
`standards/evidence-lifecycle.md` and `standards/notes-adr-sync.md` for scoped
authority, exact evidence and decision ownership. Existing named authority
continues; analysis is read-only and report-only excludes input/index/state writes.


## User Guide

- When to use: Generate a project progress dashboard from workflow-catalog.yaml. Reads current stage, required steps, artifact evidence, validation gaps, writes production/project-roadmap.md after approval, and mirrors to memory_bank/t2_execution/current_roadmap.md only when the Memory Bank root exists and that path and effect are covered.
- Inputs: Command arguments: `/cdd-status [optional: --dry-run | --write]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank reads: existing laws/current-state/workflow-contract/adapter-state.
- Memory-bank writes: only with initialized Memory Bank and the separately covered `memory_bank/t2_execution/current_roadmap.md` mirror; no law/current-state/workflow-contract/adapter-state writes.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# CDD Status Dashboard

Generate a concise progress dashboard and a durable roadmap at
`production/project-roadmap.md`. For the expected shape, see
`docs/examples/project-roadmap.example.md`.

When `memory_bank/` exists and its exact mirror effect is covered, maintain
`memory_bank/t2_execution/current_roadmap.md`. This mirror is for project
memory and does not replace `production/project-roadmap.md`.

`memory_bank/t2_execution/adapter_state.yaml` is recorded by
`/constitute-check`. `/cdd-status` reads and displays that record but never
recomputes freshness and never writes or owns the adapter-state file.

This skill bridges `/help` and `/project-stage-detect`:
- `/help` gives one next required step.
- `/project-stage-detect` performs a full audit.
- `/cdd-status` creates a saved progress dashboard from the catalog.

## Collaboration Rule

Draft the roadmap and disclose actual paths/effects first. Reuse existing named
roadmap authority across retries. Missing scope asks: "May I write `production/project-roadmap.md` and the named
`memory_bank/t2_execution/current_roadmap.md` mirror?" The named mirror may be maintained or created when the
Memory Bank root exists and that path and effect are covered. The mirror
is a distinct effect, never a hidden gift from
report-only approval. An explicit `--write` flag or write instruction covers only its
documented requested effects; disclose them and ask only for any material new scope.
`--dry-run` always writes nothing. Without Memory Bank, write only the covered
roadmap and report mirror skipped; no initialization is required or performed.
Optional advice when governance setup is requested: "Run `/constitute` to establish the memory_bank governance control plane".
This is a suggestion only: do not invoke it, initialize Memory Bank, change default
QA handling, or make independent reporting/qualification depend on optional setup.
All other law/contract/adapter/session/sprint/stage/index effects remain excluded.

## 1. Read Authoritative Inputs

Read these files when present:
- `workflow/workflow-catalog.yaml`
- `production/stage.txt`
- `production/sprint-status.yaml`
- `production/session-state/active.md`
- `memory_bank/t0_core/basic_law_index.md`
- `memory_bank/t0_core/current_state.md`
- `memory_bank/t2_execution/workflow_contract.md`
- `memory_bank/t2_execution/adapter_state.yaml`
- `design/cdd/game-concept.md`
- `design/cdd/product-concept.md`
- `design/ux/surface-profile.md`

Detect domain from substantive concept bodies and configured values under
`standards/technical-preferences.md`, including valid populated legacy Product
aliases. Report Game, Product or Unknown for the current scope. Conflicting
concepts or mixed scope need a concrete Game or Product selection before dependent
catalog filtering/routing; do not auto-select Both or qualify completion from
this choice. Missing concepts never default Game; actual legacy Product remains
Product. Independent neutral reporting continues.

Report four facts independently:
1. Declared phase: actual `production/stage.txt` content or owner statement, including conflicts.
2. Observed bodies/locators/status projections and omitted inputs.
3. Candidate phase: advisory ongoing-work indicators under `/project-stage-detect`.
4. Qualified state: only exact governing checks/decisions/reviews/transition or
   completion authority actually verified; otherwise unverified.

Detect recorded adapter freshness when the state file exists:
- Read `status`, `checked_commit`, `checked_at`, `manifest_digest`, and
  `source_digest`.
- Display `fresh`, `stale`, or `uninitialized` as a recorded value, not a live
  check. If the file is absent, display `not initialized`.
- For `stale`, `uninitialized`, or missing state, add a risk recommending
  `/constitute-check`.
- Do not change the catalog-derived blocker or reorder the next three commands
  because of adapter state.

## 2. Parse The Workflow Catalog

Use `workflow/workflow-catalog.yaml` as the only required-step source of
truth.

For each phase:
- Keep steps with no `applies_to`.
- Keep `applies_to: [game]` only for Game projects.
- Keep `applies_to: [product]` only for Product projects.
- For Unknown projects, label domain-specific steps as applicability pending.
  Hold dependent single-domain routing/completion claims until a concrete Game or
  Product scope resolves; independent neutral reporting continues.

For each step, extract:
- `id`
- `name`
- `command`
- `required`
- `required_when`
- `artifact.glob`
- `artifact.min_count`
- `artifact.note`
- `description`

## 3. Check Completion

Classify every required step:

| Status | Meaning |
| ------ | ------- |
| COMPLETE | Actual governing required checks/decisions/reviews/completion authority verified against exact evidence |
| PARTIAL | Artifacts observed, but required content/evidence or qualification incomplete/unverified |
| MISSING | No artifact or manual evidence was found |
| N/A | `required_when` is false and a rationale exists, usually in `design/ux/surface-profile.md` |
| MANUAL | The step has no machine-checkable artifact; report what must be verified |

Rules:
- Globs/counts/patterns are catalog structural observations. Read substantive
  bodies and actual required dependency closure before qualified COMPLETE;
  missing/failed/unexecuted required checks retain their actual state.
- Resolve explicitly referenced direct/indirect inputs to their actual paths
  and read their bodies, including ignored or untracked attachments. A discovery
  glob or ignore-aware search omission does not establish absence. Check each
  claimed missing path directly and retain its individual result; a silent test
  in an aggregate command is not a path-specific absence observation. Confirmed
  absence, unread inputs and inaccessible inputs remain distinct. Unread or
  inaccessible required inputs keep the affected check Pending/unverified.
- If a step has `required_when`, evaluate it from the domain and
  `design/ux/surface-profile.md` when available.
- If applicability is ambiguous, mark the step `MANUAL`, not `COMPLETE`.
- Catalog governs workflow step ordering/applicability; owning CDD/Story/decisions
  govern actual required evidence. Do not invent requirements or erase real ones.

## 4. Determine The Blocker And Next Commands

Find the first incomplete required step in the current phase.

If all current-phase required steps are complete:
- The current blocker is the phase gate, e.g. `/gate-check technical-setup`.
- The next commands are the first required commands in the next phase.

If a required step is incomplete:
- The current blocker is that step.
- The first next command is its `command`.
- The next two commands are the following required commands in phase order.

## 5. Build The Roadmap

Write a roadmap with this structure:

```markdown
# Project Roadmap

> Generated by `/cdd-status` from `workflow/workflow-catalog.yaml`.
> Last updated: [date]

## Snapshot

- Domain: [Game/Product/Unknown]
- Declared phase: [source/value or absent]
- Observed work / candidate phase: [body evidence and advisory candidate]
- Qualified state: [verified scope/evidence or unverified]
- Catalog structural observations: [observed / actual applicable denominator]
- Qualified required progress: [verified complete / actual applicable denominator]
- Current blocker: [step or gate]
- Adapter freshness (recorded): [fresh/stale/uninitialized/not initialized]
- Adapter state checked: [checked_at at checked_commit, or never]

## Next Commands

1. `/command`
2. `/command`
3. `/command`

## Phase Progress

| Phase | Applicable Required | Observed | Qualified Complete | Missing/Pending |
| ----- | ------------------- | -------- | ------------------ | --------------- |
| ... |

## Current Phase Checklist

| Step | Required | Evidence | Status |
| ---- | -------- | -------- | ------ |
| ... |

## Product Surface Decisions

| Artifact | Status | Source |
| -------- | ------ | ------ |
| `design/ux/interaction-patterns.md` | REQUIRED / N/A / MISSING | `design/ux/surface-profile.md` or catalog |
| `design/design-system.md` | REQUIRED / N/A / OPTIONAL | surface profile / scope |
| `design/brand/style-guide.md` | OPTIONAL / REQUIRED BY SCOPE / N/A | surface profile / scope |

## After This Phase You Should Have

- [artifact glob or manual evidence generated from the catalog]

## Risks

- [missing critical evidence, stale sprint data, unresolved gate failure, or N/A without surface profile]
- [stale, uninitialized, or missing adapter state; recommend /constitute-check]

## Notes

- Catalog is authoritative.
- A risk acceptance/exception is separate; it cannot turn required FAIL/NotRun/
  Blocked/Pending/Unknown into PASS or qualified completion/transition.
```

Keep the console response under 60 lines. The saved roadmap may be longer.

When writing the T2 mirror, use the same roadmap content with this extra header:

```markdown
> Governance memory mirror generated by `/cdd-status` from
> `workflow/workflow-catalog.yaml`.
> Customer/team-facing roadmap: `production/project-roadmap.md`.
```

## 6. Product Surface Profile Handling

For Product projects, read `design/ux/surface-profile.md` when present.

Use it to decide whether these are applicable:
- `design/ux/interaction-patterns.md`
- `design/design-system.md`
- `design/brand/style-guide.md`

Populate the roadmap's `Product Surface Decisions` table for Product projects:
- `interaction-patterns.md`: `REQUIRED` when the product has any API, CLI,
  SDK/library, UI, admin, operator, docs-driven consumer journey, or other
  user/integrator-facing surface; `N/A` only with surface-profile rationale;
  `MISSING` when required and absent.
- `design-system.md`: `REQUIRED` for UI-heavy or multi-surface UI products,
  `N/A` for API-only, CLI-only, SDK/library, or internal headless products with
  rationale, otherwise `OPTIONAL`.
- `style-guide.md`: `REQUIRED BY SCOPE` when public brand, docs imagery,
  screenshots, diagrams, marketing/release visuals, or visual tone are in
  scope; otherwise `OPTIONAL` or `N/A` when explicitly ruled out.

If a project marks one of these N/A without `design/ux/surface-profile.md`,
flag a risk:

`Product surface requirement marked N/A without design/ux/surface-profile.md.`

Recommend creating it from `templates/surface-profile.md`.

## 7. Output

Always report:
- Domain
- Declared/observed/candidate/qualified phase facts
- Structural observations and qualified progress with actual denominator
- Current blocker
- Recorded adapter freshness and its checked commit/time, or `not initialized`
- Next 3 commands
- Product surface decision table when domain is Product
- Whether `production/project-roadmap.md` was written or only drafted
- Whether `memory_bank/t2_execution/current_roadmap.md` was written, skipped
  because `memory_bank/` is missing, or skipped because this was `--dry-run` or outside covered mirror authority

Do not mark any manual or structural step qualified complete without its actual
required exact evidence/authority. A recorded done status needs owning closure recheck.
Do not describe recorded adapter state as live evidence and do not let it
override the workflow catalog's phase ordering.

Recorded `source_digest` covers only manifest-declared classes; linked neutral
owners need independent exact identities. Displayed freshness is historical context,
not live runtime/skill/spec/category qualification. Runtime availability follows
actual metadata and `adapters/README.md`, not source files or adapter-state values.
