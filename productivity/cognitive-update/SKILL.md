---
name: cognitive-update
agent: none
description: Conservative close-parity updates to GOAL_STACK, BELIEF_STATE, SELF_MODEL, and PROCEDURES. Writes only explicit or mechanically evidenced deltas; ambiguity means no write.
allowed-tools: Read, Write, Bash
user-invocable: true
status: PRODUCTION - conservative and source-referenced
triggers:
  - cognitive update
  - update cognitive state
  - runtime state update
---

# /cognitive-update

Nightly uses this shared protocol after `/system-check`. It never infers a
durable state change from one agent-authored claim.

## Ownership fence

This protocol may update only:

- `vault/memory/runtime/GOAL_STACK.json`
- `vault/memory/runtime/BELIEF_STATE.jsonl` (append-only)
- `vault/memory/runtime/SELF_MODEL.json`
- `vault/memory/runtime/PROCEDURES.jsonl` (append-only)

The documented `memory/` fallback is valid for minimal installations. This
protocol never writes `ACTIVE_STATE.json` or `STATE_EVENTS.jsonl`; the runtime
state daemon owns those products. It never writes Dream or measurement ledgers.

## Evidence admission

Direct updates require one of:

- the operator's explicit goal, belief, or procedure statement with a durable
  source reference;
- a repository-owned command or test invoked with explicit arguments and a
  literal exit code;
- an external artifact that directly decides the claim;
- two independent observed occurrences for a recurring capability or failure.

Capsules and Session Log entries are discovery sources. They cannot verify
their own confident claims. If evidence is incomplete, skip the durable update
and stage an observation through the nightly evidence flow.

## File rules

### GOAL_STACK.json

Move, append, or update only explicit goals, blockers, next actions, and
completions. Completion requires success criteria plus an external artifact or
operator confirmation. Preserve unknown fields and unrelated arrays.

### BELIEF_STATE.jsonl

Append only. A revision reuses the original id and includes `revision_note`; a
new belief receives max numeric `bNNN` plus one. Do not use line count. Serialize
UTF-8 JSON and parse the appended line.

### SELF_MODEL.json

Update only named capability, limitation, recurring-failure, reliability-risk,
or achieved-learning-goal fields. When alias arrays coexist, update each alias
pair in lockstep or fail `SELF_MODEL_ALIAS`. A one-off result is not a durable
capability.

### PROCEDURES.jsonl

Append only when the sequence occurred at least twice, the operator explicitly
made it standing, or a non-obvious workflow was mechanically proven. Allocate
max numeric `pNNN` plus one and parse after append.

## Write discipline

Hash every source immediately after read and compare again before write. A hash
change aborts rather than clobbering newer state. Preserve JSON formatting where
practical; always serialize JSONL.

A nightly fire uses the immutable snapshot created by `nightly-pass begin`.
For explicit use, create an operating-system temp snapshot:

```text
node daemons/nightly-contracts.mjs snapshot --root <aigent-root> \
  --out <os-temp>/cognitive-contract-before.json
```

After any updates:

```text
node daemons/nightly-contracts.mjs cognitive --root <aigent-root> \
  --snapshot <os-temp>/cognitive-contract-before.json \
  --new-belief-ids <csv> --new-procedure-ids <csv> \
  --self-alias-additions <csv>
```

Only `COGNITIVE_CONTRACT PASS` is green. The validator re-parses all four
products, proves append-only suffixes, derives allocated ids, validates new-row
schemas, and derives alias additions and removals.

Return:

```text
COGNITIVE_UPDATE PASS goals=<N> beliefs=<N> self_model=<N> procedures=<N> skipped=<N>
```

