---
name: rite-clarify
description: Audit a completed spec for missing decisions before strategy or architecture. Use after /rite-spec when coverage is incomplete or stale; not for spec writing.
argument-hint: "[feature-slug]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/afk-hitl.md","rite-clarify/reference/decision-coverage.md","rite-clarify/reference/anti-patterns.md"],"triggers":{"agents":["devrites-lib/reference/standards/agents.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md","decision-coverage.md"],"workspaceByRole":{"evidence-scout":["brief.md","spec.md","state.md","questions.md"]},"rootOnly":["devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/afk-hitl.md"]} -->
> Read-set manifest: `devrites-engine context --skills-root .pi/skills <slug> --phase clarify` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-clarify: resolve product decisions

Run this required pass between spec and strategy. If the spec covers every material
decision, ask no questions. Otherwise stay until each material decision has an
owner. This phase settles behavior and constraints; `/rite-define` settles
implementation.

Reuse [`devrites-interview`](../devrites-interview/SKILL.md) in `/clarify mode`. Write
`decision-coverage.md` as scan evidence, not an interview transcript.

## Rules consulted

Read [`core.md`](../devrites-lib/reference/standards/core.md), its [`afk-hitl.md`](../devrites-lib/reference/standards/afk-hitl.md), and
[`reference/decision-coverage.md`](reference/decision-coverage.md). Fresh evidence
dispatch uses
[`agents.md`](../devrites-lib/reference/standards/agents.md).

## Rules

- Search code/docs/contracts first. Facts and reversible implementation/test choices
  are agent-owned; ask only about product, scope, policy, irreversible risk, or human-only access.
- Enumerate the full topology before details so no sibling surface is omitted.
- Ask one coherent human-owned decision packet at a time. One packet may close several rows
  only when owner and trade-off match; never ask permission for routine repair/retry.
- One scan may cap at five packets for cognitive load, but readiness has no question cap:
  re-scan until clear.
- Material assumptions carry evidence, confidence, owner, validation, and consequence.
- Refuse the rationalizations in [`anti-patterns`](reference/anti-patterns.md).

## Workflow

1. **Orient.** Read `.devrites/ACTIVE`, `state.md`, and `spec.md`. Require
   `state.md` `spec_gate: passed` (legacy `Spec gate: passed` line accepted); otherwise stop at `/rite-spec`. Apply the native cursor
   protocol below before changing workspace artifacts.
2. **Enumerate the topology.** From the spec, live code, contracts, references,
   and recorded decisions, list every material stakeholder/priority, invariant, actor,
   journey/component, state, data lifecycle, integration, failure/recovery path,
   operation, proof surface, applicability row, and must-NOT boundary.
3. **Scan coverage.** Apply `devrites-interview` in clarify mode and mark each
   material surface `closed`, `agent-owned`, `not-applicable`,
   `deferred-nonblocking`, or `open` with evidence and an owner. Use native repository search
   first. Ask the host to run `devrites-evidence-scout` only for a bounded missing
   fact, then reconcile its cited result.
4. **Close decisions.** Record facts and reversible technical choices directly.
   Ask one coherent option packet only for product, scope, policy, irreversible
   risk, or human-only access. Persist answers in the owning artifacts and repeat
   the scan until no blocking `open` row or unowned material assumption
   remains.
5. **Write the verdict.** Write `Decision coverage: CLEAR` only after re-reading all inputs and confirming
   every material row has current evidence and an owner. Normal flow sets `phase=clarify` and
   `next_action=/rite-temper`. A low-stakes spec — the significance trigger temper itself
   skips (rite-temper step 1) — sets `next_action=/rite-define` instead. A contract-neutral later-phase return uses
   the native restore below; changed behavior or acceptance routes to
   `/rite-plan repair` instead. Stop without starting the next phase.

## Native clarify cursor protocol

The controlling root edits only cursor rows in `state.md`; it must preserve unrelated Markdown and the file's existing table/bullet presentation.

- **Normal entry from Spec:** set `phase=clarify`, `status=running`, and
  `next_action=/rite-clarify <slug>`; omit both return fields.
- **Already in Clarify:** no-op. Do not overwrite an existing valid return
  cursor.
- **Later-phase entry:** only `temper`, `define`, `plan`, `vet`, `build`,
  `converge`, `prove`, `polish`, `review`, `seal`, or `ship` may return. First
  copy the current `phase` and non-empty `next_action` to `return_phase` and
  `return_next_action`; then set `phase=clarify`, `status=running`, and
  `next_action=/rite-clarify <slug>`. Missing/unknown cursor values fail closed
  before any write.
- **Contract-neutral restore:** after a fresh `Decision coverage: CLEAR`, require
  `phase=clarify`, both return fields, a recognized later `return_phase`, and a
  non-empty `return_next_action`. Restore those values to `phase` and
  `next_action`, set `status=running`, and remove both return fields in the same
  rewrite. Re-read the cursor and confirm the return rows are absent.
- **Contract changed:** do not restore the saved cursor. Record drift and route
  through `/rite-plan repair`, which owns the changed plan and next action.

Never normalize or rewrite the rest of `state.md` while applying this protocol.

## Output

```text
Done: decision coverage closed for <slug>; <n> topology surfaces scanned.
Changed: decision-coverage.md, spec.md, decisions.md, assumptions.md, questions.md
Evidence: Decision coverage: CLEAR; human packets <n>; agent-owned facts <n>
Open: none blocking; deferred-nonblocking <n>
Next: /rite-temper (or /rite-define for a low-stakes spec temper skips)
Record: .devrites/work/<slug>/decision-coverage.md
↻ Hygiene: /clear — decision coverage is persisted in decision-coverage.md
```

If not clear, name the exact rows and next genuine decision packet. An objective spec defect
or factual search task never routes through `/rite-resolve`.
