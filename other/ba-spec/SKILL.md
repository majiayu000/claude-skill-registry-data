---
name: ba-spec
description: Use when current valid requirements, decisions, research, and approved design need to be consolidated into an implementation-ready FRD or final specification.
argument-hint: "[ขอบเขตหรือรูปแบบ final spec ที่ต้องการ]"
---

# BA Spec

**Consolidate; do not invent.**

Before any `.ba/` mutation, read `${CLAUDE_PLUGIN_ROOT}/shared/contract-core.md`, `${CLAUDE_PLUGIN_ROOT}/shared/contract-records.md`, and `${CLAUDE_PLUGIN_ROOT}/shared/contract-snapshots.md`. Read `${CLAUDE_PLUGIN_ROOT}/shared/contract-changes.md` when `.ba/changes/` exists or approved truth may be changing.
Before asking or interpreting user answers, read `${CLAUDE_PLUGIN_ROOT}/shared/question-contract.md`.


## Pending change guard

If relevant OPEN changes exist, treat them as visible **pending** context, not approved truth. Do not silently fold candidate meaning into canonical phase work. If the requested work is primarily changing already-approved truth, route the user to `/ba-change`.

Pending truth may drive provisional reasoning only when the dependency is explicit and traceable; do not present provisional output as approved.

## Structural validation

When Python 3 is available, run:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ba_lint.py" --project "${CLAUDE_PROJECT_DIR}"
```

Use it on resume before trusting durable state and before presenting an approval-ready checkpoint. If Python 3 is unavailable, say plainly that **deterministic lint was not run**. The BA conversation may continue, but never claim structural validation without command evidence.

## Entry

Preferred input is a valid Phase 3 design baseline plus current canonical requirements, decisions, and research. Externally approved design evidence is allowed when sufficient and provenance-tracked. Missing preferred baselines are Soft Guards, never permission to invent missing design.

Read `PROJECT.md`, the latest valid design handoff, and referenced canonical records. Preserve active PIPELINE mode; otherwise enter `SPEC` in DIRECT mode. Resume durable state when present.

## Consistency Gate

Before any final consistency claim, run the linter when available. A **lint ERROR** is a structural blocker: route the defect to the owning artifact/phase and **do not claim final structural consistency** until the error is resolved and lint is rerun.

Check before drafting:

- every material requirement has design coverage,
- design decisions do not contradict current requirements,
- superseded/invalidated baselines are not treated as current truth,
- assumptions/open decisions remain visible,
- bypass provenance remains visible.

If requirement truth is materially unresolved, route to `/ba-requirements`. If design coverage is materially missing, route to `/ba-design`. Do not silently repair either gap inside the FRD.

## Final specification

Include at minimum:

- background/problem and goals,
- scope/non-goals,
- validated requirements/constraints,
- approved system design/workflows,
- data/integration boundaries,
- material decisions and rationale,
- failure/recovery expectations,
- acceptance/verification expectations,
- implementation inputs,
- approved technical choices,
- still-open implementation decisions,
- risk areas and relevant baseline references.

Ask user questions only for legitimate unresolved user decisions/values; inspect or research facts available elsewhere first.

If the user pauses, persist current activity/Next Focus and stop.

## Exit

Present the consolidated FRD/spec for explicit approval. Before creating the snapshot, present the **approval scope** explicitly, allow **selective correction** or named open items, and obtain explicit user approval. The approved snapshot must contain the standard `## Approval` block from `${CLAUDE_PLUGIN_ROOT}/shared/contract-snapshots.md`; never invent approver identity, timestamp, or scope.

Only after approval:

1. create the append-only Phase 4 snapshot/final baseline,
2. update Project Brain Current Baselines,
3. in DIRECT mode stop,
4. in PIPELINE mode return to `/ba-discovery`, which may mark the target COMPLETE.

After an approved final baseline exists, `/ba-report` may be suggested as an optional presentation artifact. Never generate it silently.
