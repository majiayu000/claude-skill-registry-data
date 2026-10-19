---
name: trajectory-ledger
description: "Schema, grounding rules, outcome status and cost ledgers for agent trajectories. Use when an agent must record, replay or audit a multi-step run (task, tools, state transitions, cost, outcome) so that results are reproducible and auditable; not for logging application telemetry. Verified 2026-10-13."
compatibility: Python 3.10+, JSONL storage; verified 2026-10-09
license: MIT
---
# Trajectory Ledger

Trigger: recording, replaying or auditing a multi-step agent run so that the
result is reproducible and auditable.

## Core invariant
A free-form log is not a ledger. A ledger is a sequence of typed events where
every tool call is grounded (args + result recorded), every state carries a
`state_hash`, every terminal event carries evidence, and cost carries units.
Without those four properties the run cannot be replayed or audited.

## Procedure (numbered — follow in order)
1. **Define the schema first** — every trajectory is a JSONL file of events:
   `step`, `timestamp`, `type` (tool/think/observe), `tool`, `args`, `result`,
   `state_hash`, `cost`. Never free-form text in the ledger. The full field list
   and examples live in `references/schema.md`.
2. **Hash the state at every step** — `state_hash = sha256(canonical(state))`.
   A missing or mismatched hash means the trajectory was tampered with or the
   replay diverged. Canonicalise with
   `json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))`.
3. **Ground every tool call** — record the exact command and its exit code; a
   tool call with no recorded result is ungrounded and must be re-run. A `tool`
   event without `args` or without `result.exit_code` fails the audit.
4. **Track outcome status** — `pending` -> `running` -> `succeeded` | `failed` |
   `blocked` | `timeout`. Never mark `succeeded` without evidence. Each
   terminal outcome requires a specific field: `succeeded` needs `evidence`,
   `failed` needs `reason`, `blocked` needs `blocker`, `timeout` needs
   `elapsed_seconds`.
5. **Record cost** — tokens in/out, wall-clock, tool calls, retries. A cost
   ledger without a unit is not a ledger. The USD rate is pinned per model in
   the run header; never mix units. `scripts/ledger.py cost <ledger.jsonl>`
   returns JSON with `tokens_in`, `tokens_out`, `seconds`, `usd`.
6. **Enable replay** — given a trajectory and the same inputs, re-running must
   reproduce the same `state_hash` sequence. If it diverges, the run was not
   deterministic; record the first divergence as an `observe` event with
   `non_determinism: true` and stop the replay. Run
   `scripts/ledger.py replay <a.jsonl> <b.jsonl>`: exit 0 with
   `PASS: replay reproduces all N hashes`, exit 1 with
   `FAIL: replay diverges at step N`.
7. **Audit** — walk the ledger: every `succeeded` has a result, every `failed`
   has a reason, every hash matches, and the cost ledger sums. Run
   `scripts/ledger.py audit <ledger.jsonl>` (exit 0 = clean, 1 = any FAIL).
   The same binary also does `append`, `replay` and `cost`.

## Decision tables
- **Outcome status**: `succeeded` requires a recorded result; `failed` requires a
  reason; `blocked` requires the blocker; `timeout` requires the elapsed time.
- **Grounding**: tool call + result = grounded; tool call without result =
  ungrounded, re-run; no tool call = not grounded, mark `blocked`.
- **Replay**: hashes match = reproducible; first divergence = non-determinism,
  record it and stop the replay.
- **Cost units**: tokens = model counts; time = seconds; money = USD at the
  pinned rate. Never mix units.
- **Step monotonicity**: `step` must be strictly increasing across the file.
  A ledger whose steps are not a sequence cannot be replayed deterministically
  and is rejected by the audit.
- **Schema version**: the first event must declare `schema` equal to
  `trajectory-ledger-v1`. A ledger written against a draft schema cannot be
  replayed against the current one. Mixing versions in one file is rejected.

## Near-miss triggers (stop and re-check before proceeding)
- A `succeeded` event with no result -> fabricated success.
- A tool call whose `args` were not recorded -> the run is not reproducible.
- `state_hash` missing on any step -> the trajectory can be tampered with.
- Replay diverges at step 1 -> the environment is non-deterministic; record it.
- Cost recorded without units -> not auditable.
- A `tool` event with `type` but no `tool` field -> malformed event.

## Pitfalls from research
- P1: Free-form logs are not a ledger; they cannot be replayed or audited.
- P2: Missing state hashes let tampering go undetected.
- P3: `succeeded` without a recorded result is a fabricated success.
- P4: Unrecorded tool args make replay impossible.
- P5: Non-deterministic environments must be recorded, not hidden.
- P6: A cost field that mixes tokens and USD cannot be summed meaningfully.

## Verification checklist
- [ ] Schema defined and documented.
- [ ] Every step has a `state_hash`.
- [ ] Every tool call has recorded args and result.
- [ ] Outcome status has evidence for every terminal event.
- [ ] Cost has units.
- [ ] Replay reproduces the hash sequence (or divergence is recorded).
- [ ] Audit walk passes.
- [ ] Steps are strictly increasing (the ledger is a sequence).
- [ ] The schema version is `trajectory-ledger-v1` and is not mixed.
- [ ] A non-determinism record is appended with a step strictly greater than
  the last recorded step (scripts/ledger.py record-non-det rejects
  out-of-order steps).
- [ ] Cost carries all four units (tokens_in, tokens_out, seconds, usd) on every
  event that has a cost dict; `audit --strict` rejects partial cost.
- [ ] Total cost stays within the operator's `--max-usd` / `--max-seconds`
  budget on both `cost` and `audit`.

## Worked examples

### Good — grounded, replayable trajectory
A run calls `git diff`, writes a file, then reports success.

1. Each step is a typed event with `tool`, `args`, `result.exit_code`,
   `state_hash` and `cost` (tokens in/out, seconds).
2. The terminal event carries `outcome: "succeeded"` and `evidence`.
3. `scripts/ledger.py audit` walks the file: every tool call has args+result,
   every state_hash matches, every terminal event has its required field.

Result: the run is auditable and `replay` reproduces the hash sequence.

### Bad — free-form log
`"2026-10-12 agent ran git diff and it worked"`.

Why it fails: there is no tool, no args, no result, no hash and no outcome
field. The audit cannot ground a single call, so the run is neither
reproducible nor auditable. This is an application log, not a ledger.

### Bad — succeeded with no evidence
`{"outcome": "succeeded"}` with no `evidence` field.

Why it fails: `succeeded` requires `evidence`. The audit exits 1 and the
run cannot be trusted — a run that claims success without evidence is the
exact failure mode the ledger exists to prevent.
## Related skills
- [mcp-2026-07-28](../mcp-2026-07-28/SKILL.md) — an MCP round-trip is a tool call worth grounding in a trajectory.
- [skill-authoring-evals](../skill-authoring-evals/SKILL.md) — an eval run is a multi-step trajectory worth recording and auditing.

## References
- procedures: references/procedures.md
- schema: references/schema.md
- cost ledger: references/cost-ledger.md
- procedures (hardened thresholds & decision tables): references/procedures-hardening.md
- normalisation: references/normalisation.md
- incidents: references/incidents.md
- DESIGN: references/DESIGN.md
- EVALS: references/EVALS.md
- SOURCES: references/SOURCES.md
