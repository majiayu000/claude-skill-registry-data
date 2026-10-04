---
name: ba-design
description: Use when sufficiently understood or externally approved requirements need to be translated into system boundaries, workflows, data ownership, integrations, rules, and architecture trade-offs.
argument-hint: "[requirements หรือขอบเขตการออกแบบ]"
---

# BA Design

Convert sufficient design input into an implementation-neutral, traceable system design.

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

Preferred input is a valid Phase 2 requirements baseline. External/user-provided approved requirements are allowed when sufficient.

Ask two separate questions internally:

1. Was the BA Requirements phase completed?
2. Is there enough trustworthy design input to proceed?

A missing Phase 2 baseline is a Soft Guard. Recommend `/ba-requirements`; if the user explicitly proceeds with approved external input, record DESIGN provenance and never fabricate Phase 2 history.

Read `PROJECT.md`, relevant requirements/decisions/research, and the latest requirement handoff. Preserve active PIPELINE mode; otherwise enter `DESIGN` in DIRECT mode. Resume durable state when present.

## Source + Answerability Gates

Inspect project facts and existing interfaces before asking. Research material external technical facts. Ask the user for business decisions, authority, values, or trade-offs only when they are the legitimate source.

Translate architecture consequences into user-answerable choices when needed. Preserve technical distinctions without requiring architecture jargon.

## What this phase owns

- system boundaries and major components,
- primary workflows and rules,
- data ownership/source-of-truth choices,
- integration boundaries,
- failure/recovery behavior,
- requirement-to-design mapping,
- material architecture decisions/trade-offs,
- design risks and unresolved implementation choices.

If design exposes a foundational problem/requirement contradiction, do not patch it silently. Mark affected truth for reconfirmation and route to the appropriate prior phase.

## Progressive references

Load only when useful:

- [references/system-boundaries.md](references/system-boundaries.md)
- [references/tradeoff-analysis.md](references/tradeoff-analysis.md)

## Exit

Summarize design, traceability, material decisions, risks, open choices, and any bypass provenance. Ask for explicit **System Design** approval.

Before creating the snapshot, present the **approval scope** explicitly, allow **selective correction** or named open items, and obtain explicit user approval. The approved snapshot must contain the standard `## Approval` block from `${CLAUDE_PLUGIN_ROOT}/shared/contract-snapshots.md`; never invent approver identity, timestamp, or scope.

Only after approval:

1. persist material decisions/current projections,
2. create the append-only Phase 3 snapshot with handoff to final spec,
3. keep unresolved implementation choices visible,
4. update Project Brain baselines/Next Focus,
5. stop in DIRECT mode or return to `/ba-discovery` in PIPELINE mode.

Never enter Final Spec silently.
