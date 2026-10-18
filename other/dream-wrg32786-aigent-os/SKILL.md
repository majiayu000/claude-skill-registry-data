---
name: dream
agent: none
description: Evidence-gated synthesis over recent operating evidence. Appends admitted lessons and a dated synthesis with propose-only improvement candidates.
allowed-tools: Read, Write, Bash
user-invocable: true
status: PRODUCTION - canonical writer and propose-only
triggers:
  - dream
  - offline consolidation
  - consolidation pass
  - improvement candidates
  - review recent sessions
---

# /dream - evidence-gated synthesis

`/dream` is the canonical writer for lessons and Dream synthesis. It never
applies an improvement, promotes its own proposal, edits system instructions,
or treats an agent-authored claim as verification.

## Canonical ownership

- Lessons: `vault/memory/runtime/LESSONS.jsonl`.
- Dream synthesis: `vault/memory/DREAM_LOG.md`.
- The documented `memory/` fallback is valid only for minimal installations.
- Any older `runtime/DREAM_LOG.md` copy is not an input or output.
- `/close` and `/nightly` invoke this protocol instead of carrying a competing
  inline writer.
- Candidate status transitions also go through this writer.

## Invocation

```text
/dream
/dream --window nightly
/dream --set-status <candidate-id> <approved|merged|rejected|blocked> \
  --operator-evidence "<direct operator reference>"
```

`proposed -> approved` always requires the operator's exact decision. Never
infer approval from silence, an automated status, another agent, or prior prose.

## Sources

Read, in order:

1. The newest five valid capsules by frontmatter `created_at`.
2. The newest five dated live Session Log blocks.
3. Open Trust Decay captures.
4. The newest three dated Honesty Ledger sessions.
5. Recent Failed Experiments and Failure Modes entries.
6. Existing Lessons JSONL for dedupe and prior evidence chains.
7. Staged `NIGHTLY_CAPTURE_CANDIDATES.jsonl` rows from the prior fire as
   discovery and pressure signals only.
8. Explicitly supplied local Git or command evidence.

Record exact source references. A capsule or Session Log entry can establish
that a claim occurred; it cannot prove the claim true.

## Lesson admission predicate

Append a lesson only when one is true:

- the same pattern appears in at least two independent source events;
- one explicit operator directive is paired with a separately observed
  outcome; or
- one mechanical red-before/green-after predicate supplies an artifact and
  literal exit codes.

Two retellings of one event are not independent. Discard one-off observations,
unverified causal stories, and self-confirmation.

Each admitted lesson has:

- `lesson_id`: next max numeric `lNNN` suffix plus one;
- `type`: `procedural | calibration | strategic | failure-mode | doctrine`;
- `confidence`: `0.0..1.0`, capped at `0.85` for one mechanical event;
- `source_events`: at least two refs unless an allowed exception applies;
- `created_at`: the configured local `YYYY-MM-DD`;
- `admission`: one of:
  - `{kind: "two-source"}`;
  - `{kind: "operator-outcome", operator_ref, outcome_ref}`;
  - `{kind: "mechanical-red-green", red_exit, green_exit: 0, artifact_ref}`.

Serialize UTF-8 JSON, parse the complete JSONL file after append, and confirm
the new line round-trips. Historical duplicate ids do not authorize a new
collision.

## Improvement candidate predicate

When evidence names a repeatable system gap, append this inside the same dated
Dream section:

```markdown
### ni-YYYYMMDD-NN - short name
- **status:** proposed
- **evidence:** source-ref-1; source-ref-2
- **failure class:** concise class
- **proposed_change:** smallest testable change
- **mutation proof:** break condition -> named red; restore -> named green
- **operator gate:** approve / reject / revise
- **operator evidence:** pending
```

Generated candidates always start with the literal field `status: proposed`.
Any generated `approved`,
`merged`, or self-ratifying wording is a hard failure.

## Canonical dated entry

Append one `## YYYY-MM-DD (...)` section every time synthesis runs, even with
zero admitted lessons. It must contain nonempty forms of all eight labels:

- Sources reviewed
- Lessons extracted
- Improvement candidates proposed
- Patterns observed
- Discarded as one-off
- Calibration miscalls
- Productive surprises
- Open trust-decay items to watch

A quiet run writes a minimal zero-lesson entry and appends no Lessons row.
Never overwrite an earlier entry.

## Executable postcondition

A nightly fire uses the snapshot created by `nightly-pass begin`. Explicit
`/dream` creates an operating-system temp snapshot first:

```text
node daemons/nightly-contracts.mjs snapshot --root <aigent-root> \
  --out <os-temp>/dream-contract-before.json
```

After writing:

```text
node daemons/nightly-contracts.mjs dream --root <aigent-root> \
  --date <YYYY-MM-DD> --snapshot <os-temp>/dream-contract-before.json
```

Only `DREAM_CONTRACT PASS` is green. The validator proves byte-prefix
preservation, parses JSONL, derives ids, validates admission, masks fenced
examples, requires the eight sections and current configured date, and rejects
a newly generated candidate that does not start `proposed`.

Return:

```text
DREAM PASS date=<YYYY-MM-DD> sources=<N> lessons=<N> candidates=<N>
```
