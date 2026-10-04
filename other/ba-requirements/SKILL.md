---
name: ba-requirements
description: Use when user needs, constraints, alternatives, prior art, or requirements need to be discovered, refined, challenged, and validated before system design.
argument-hint: "[ความต้องการ เอกสาร หรือขอบเขตที่ต้องการตกผลึก]"
---

# BA Requirements

Turn understood needs and evidence into validated NEED / REQUIREMENT / CONSTRAINT records that are sufficiently clear for design.

Before any `.ba/` mutation, read `${CLAUDE_PLUGIN_ROOT}/shared/contract-core.md`, `${CLAUDE_PLUGIN_ROOT}/shared/contract-records.md`, and `${CLAUDE_PLUGIN_ROOT}/shared/contract-snapshots.md`. Read `${CLAUDE_PLUGIN_ROOT}/shared/contract-changes.md` when `.ba/changes/` exists or approved truth may be changing.
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

Preferred input is a valid Phase 1 baseline. Externally supplied background/problem evidence is allowed when sufficient. A missing Phase 1 baseline is a Soft Guard, not a hard lock: recommend `/ba-understand`, but if the user explicitly proceeds with trustworthy external input, record provenance and never fabricate Phase 1 approval.

Read `PROJECT.md`, the latest relevant Phase 1 handoff, and canonical records on demand. Preserve an active PIPELINE handoff; otherwise enter `REQUIREMENTS` in DIRECT mode. Resume durable state instead of repeating discovery.

## Source Gate

- project fact → inspect project artifacts,
- external fact/prior art → research evidence,
- user knowledge/value → ask,
- research never automatically becomes a requirement.

## Answerability Gate

Use the shared Question Contract. Questions must pass Source Fit, Comprehension Fit, Decision Fidelity, and User-Effort Fit. Decision-critical questions are adaptive and one-at-a-time; batch only 2–4 tightly related low-risk facts when answers do not change each other.

## What this phase owns

- user needs,
- requirements and constraints,
- acceptance/verification intent,
- decision-relevant prior art,
- alternatives and recommendations,
- unknown-unknown discovery,
- design-driving decisions,
- open risks / out-of-scope.

Do not own detailed system architecture or implementation planning.

## Progressive references

Load only when useful:

- [references/requirement-refinement.md](references/requirement-refinement.md)
- [references/research-routing.md](references/research-routing.md)
- [references/unknown-unknowns.md](references/unknown-unknowns.md)

## Working method

Separate NEED, REQUIREMENT, and CONSTRAINT. Trace material statements to origin/evidence. Compare alternatives before turning a preference into a requirement. Seek counter-evidence for consequential research. Keep unresolved items explicit rather than forcing false completeness.

Persist canonical records following the shared contract. If the user pauses, preserve exact current activity and Next Focus, then stop.

## Exit

Before approval, perform a quiet coverage sweep and summarize confirmed needs/requirements/constraints, material decisions, open items, risks, out-of-scope, and **Design Drivers** with supporting REQ/DEC IDs.

Ask for explicit **Requirement Alignment** approval. Before creating the snapshot, present the **approval scope** explicitly, allow **selective correction** or named open items, and obtain explicit user approval. The approved snapshot must contain the standard `## Approval` block from `${CLAUDE_PLUGIN_ROOT}/shared/contract-snapshots.md`; never invent approver identity, timestamp, or scope.

Only after approval:

1. create the append-only Phase 2 snapshot,
2. include compact handoff + Design Drivers,
3. keep non-blocking open items visible,
4. update Project Brain baselines/Next Focus,
5. stop in DIRECT mode or return to `/ba-discovery` in PIPELINE mode.

Never enter Design silently.
