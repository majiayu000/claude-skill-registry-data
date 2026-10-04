---
name: workflow-status
user-invocable: true
version: 3.9.1
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
argument-hint: "[--json-only] [--last-envelope <json|path>] [--compact]"
description: >
  Read-only workflow sensor: run the deterministic script, read the fixed
  machine envelope, interpret the recommendation. Never edits. Triggers:
  "workflow-status", "workflow status", "what can I build next".
---

# Workflow Status (the orchestrator's sensor)

One read-only pass that answers, in a single fixed JSON envelope: **what exists,
what is blocked on what, what is startable right now, and what the recommended
next command is.** The **script is the deterministic producer**:
`scripts/workflow-status.mjs` executes the published `SENSOR_CORE` sequence
(steps 1–9 including 6a) and prints the envelope. This skill runs the script,
reads the JSON, interprets it against the references below, and prints the human
report — it never assembles the envelope by hand.

## Turn contract — verify before ending the turn

```
✓ The script was RUN — `bun scripts/workflow-status.mjs [--json-only]
  [--last-envelope <json|path>] [--compact]` (node is the fallback when bun is
  absent, per the repository's runtime convention); the envelope is the script's
  stdout, never assembled by the model
✓ Nothing was edited, committed, pushed, or created — read-only, always
✓ `next.recommended` is non-bare (carries the unit's slug/NN, never a bare
  `/unit-lane`) AND the script computed it from the unit's resolved status:
  `idea`/`defined` → `/unit-lane <slug>` (or `/unit-lane --fix <n>` for a fix);
  `planned`/`in-progress` → `/execute-phase <NN>` (its triage block is the
  authority; no separate plan-receipt currency check, step 6a)
✓ `detail.crash_recovery` carries a verdict from the decision table and the
  envelope `state` matches it (CLEAN→OK, RESUMABLE→CONTINUE,
  AMBIGUOUS→NEEDS_INPUT)
✓ Every `detail.design_candidates[].next` begins with `/unit-lane `
✓ Every degraded dimension is named in `detail.degradations` as
  `unavailable-<source>-<cause>` — and, when `--last-envelope` was supplied, the
  no-progress guard's `workflow_observations` note is present (never a silently
  repeated bland recommendation)
✓ The envelope is emitted on **every** invocation, including a same-session
  natural-language follow-up about state — never replaced by prose
✓ The human-readable summary is printed, then the machine envelope (the script's
  JSON) is the ABSOLUTE last output
```

With `--json-only`, skip the human-readable summary: print the envelope alone.

## Compact mode — `--compact`

`--compact` emits the same envelope with repository history dropped (~half the
bytes on a mature repo); the exact keep/drop set is in
[envelope fields](references/ENVELOPE_FIELDS.md).

## When to use

- Between orchestration steps: an external driver runs it to decide the next
  command and model tier without parsing prose.
- Before picking work manually: "what can I start right now?"
- **Not** for judging quality (`review-change`/`audit-pr`) or product health
  (`product-audit`) — this skill reports state, it never judges.

## Step 0 — Discover the project (always first)

Per the agent guide's **Workflow conventions** + **documentation map**. The
script reads what THIS skill needs (`docs/features/ROADMAP.md`, the fix index
`docs/fix/README.md`, every in-flight feature folder's `TASKS.md` +
`progress.md` + `review-findings.md`, and `docs/workflow/REPOSITORY_STATE.md`);
read them yourself only to interpret a field the script emitted.

## Progressive loading — fixed sensor route

The reference allowlist is exactly the seven linked paths below. Never invent or
read another `references/` path. This skill is a read-only sensor.

1. [sensor core](references/SENSOR_CORE.md) — the sequence the script executes
2. [crash recovery](references/CRASH_RECOVERY.md)
3. [envelope core](references/ENVELOPE_CORE.md)
4. [envelope fields](references/ENVELOPE_FIELDS.md)
5. [pre-execution evidence](references/PRE_EXECUTION.md)
6. [guardrails](references/GUARDRAILS.md)

Add [sensor signals](references/SENSOR_SIGNALS.md) only when a unit, issue,
finding, or recommendation exists; an empty project skips that file but still
emits the empty shapes defined by envelope fields. Add
[portability](references/PORTABILITY.md) only when the platform actually lacks a
named primitive. `--json-only` does not skip any baseline file.

## Portability

The sensor uses repository and forge commands only. When a named agent feature
is unavailable, follow [portability](references/PORTABILITY.md) without changing
the JSON contract.

## Relationship to other skills

- The **sensor** counterpart to `advance`'s conductor: an external
  orchestrator (or `advance` itself) calls `workflow-status` → routes on the
  envelope → invokes `unit-lane` / `execute-phase` / `review-change` /
  `audit-pr` / `triage-issue` directly, choosing the model per step — the same
  loop without the in-agent autopilot.
- Read-only sibling of `audit-docs` (which judges coherence and can fix) and
  `product-audit` (which judges health): this one only reports state.
- Schema owner: `orchestration-envelope` (internal).

## Done when

- The script ran and every claim in the report comes from its envelope — nothing
  inferred from memory, nothing assembled by hand.
- `detail.design_candidates`, `detail.features`, `detail.fixes`,
  `detail.startable_now`, `detail.blocked_units`, `detail.open_prs`,
  `detail.untriaged_issues`, `detail.urgent`, `detail.degradations`, and
  `detail.crash_recovery` were read from the envelope, and the envelope `state`
  matches the crash-recovery verdict.
- With `--last-envelope` supplied: the no-progress guard ran — a stalled
  `/unit-lane` hint surfaces as a `workflow_observations`
  note, never a silent bland repeat, with no new write path introduced.
- The human summary (unless `--json-only`) and the envelope are printed, envelope
  last.
- Nothing was modified anywhere.
- When the envelope carries `next.continuation`, the next-command echo **quotes the
  emitted `next.continuation`** (`rendering` for display), never author exact command
  tokens; the human-facing prose `→ Next:` block below stays.

→ Next: the envelope's `next.recommended` command — it is computed from the
  actual state, so it IS the recommendation
  · a human overview → read the printed table
  · orchestrating programmatically → parse the script's JSON
