---
name: ba-understand
description: Use when a project problem, current reality, business context, goals, pain points, or foundational assumptions are not yet sufficiently understood before requirements or solution design.
argument-hint: "[ปัญหา บริบท หรือระบบที่ต้องการทำความเข้าใจ]"
---

# BA Understand

Establish an evidence-based shared understanding of the real problem before committing to requirements or solutions.

Before any `.ba/` mutation, read `${CLAUDE_PLUGIN_ROOT}/shared/contract-core.md` and `${CLAUDE_PLUGIN_ROOT}/shared/contract-snapshots.md`. Load `${CLAUDE_PLUGIN_ROOT}/shared/contract-records.md` when persisting structured records. Read `${CLAUDE_PLUGIN_ROOT}/shared/contract-changes.md` when `.ba/changes/` exists or approved truth may be changing.
Before asking or interpreting user answers, read `${CLAUDE_PLUGIN_ROOT}/shared/question-contract.md`.


## Pending change guard

If relevant OPEN changes exist, treat them as visible **pending** context, not approved truth. Do not silently fold candidate meaning into canonical phase work. If the requested work is primarily changing already-approved truth, route the user to `/ba-change`.

## Structural validation

When Python 3 is available, run:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ba_lint.py" --project "${CLAUDE_PROJECT_DIR}"
```

Use it on resume before trusting durable state and before presenting an approval-ready checkpoint. If Python 3 is unavailable, say plainly that **deterministic lint was not run**. The BA conversation may continue, but never claim structural validation without command evidence.

## Entry

Accept a new idea/problem, a brownfield project, or a resumable Phase 1 state. Read `${CLAUDE_PROJECT_DIR}/.ba/PROJECT.md` first when present. If this is not an active pipeline handoff, use `workflow_mode: DIRECT`; otherwise preserve `PIPELINE` and its target.

If state does not exist and actual BA work is starting, bootstrap `.ba/` exactly as the shared contract specifies.

## Source Gate

Before every question decide who can legitimately answer it:

- project fact → inspect code/docs/config/data first,
- external fact → research credible evidence first,
- user knowledge/value → ask the user,
- unresolved interpretation → clarify only after inspecting available evidence.

Unknown does not mean “ask the user.”

## Answerability Gate

For user questions verify:

1. Source Fit,
2. Comprehension Fit,
3. Decision Fidelity,
4. User-Effort Fit.

Use the shared Question Contract for source routing, answerability, pacing, transformation, and post-answer classification. Decision-critical questions are adaptive and one-at-a-time. Batch only 2–4 tightly related low-risk facts when answers do not change each other.

## What this phase owns

- current state/workflow,
- problem and why it matters,
- desired outcome,
- pain points,
- known constraints,
- foundational assumptions,
- relevant project evidence,
- blind spots/open foundational questions.

Do not finalize requirements or select architecture here.

## Progressive references

Load only when useful:

- [references/brownfield.md](references/brownfield.md) for an existing system/codebase.
- [references/probing-patterns.md](references/probing-patterns.md) when a question is too abstract or the user struggles to answer.

## Persistence

Update Project Brain only for material shared truth. Keep evidence, assumptions, inference, and user statements distinguishable. If the user pauses, preserve safe state, current activity, and Next Focus, then stop.

## Exit

When background/problem understanding is sufficient:

Before creating the snapshot, present the **approval scope** explicitly, allow **selective correction** or named open items, and obtain explicit user approval. The approved snapshot must contain the standard `## Approval` block from `${CLAUDE_PLUGIN_ROOT}/shared/contract-snapshots.md`; never invent approver identity, timestamp, or scope.

1. summarize the proposed Phase 1 baseline,
2. expose meaningful open items/risks,
3. ask for explicit **Background Alignment** approval,
4. only after approval create the append-only Phase 1 snapshot with `## Handoff to Next Phase`,
5. update `PROJECT.md` Current Baselines / Next Focus,
6. in DIRECT mode stop; in PIPELINE mode return control to `/ba-discovery`.

Never enter Requirements silently.
