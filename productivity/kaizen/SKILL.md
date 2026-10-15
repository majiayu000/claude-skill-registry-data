---
name: kaizen
description: Continuous-improvement ritual — capture one small improvement, attribute the object that actually improved, and emit a recursion-evidence receipt. Use after shipping a fix, workflow upgrade, or harness improvement; during retrospectives when improvements are named; or when an RSI/compounding claim needs evidence. [Maps to RE1.]
version: 0.1.0
execution-mode: side_effecting
argument-hint: "<what improved> [--target TARGET] [--lead human|agent|mixed] [--structural present|absent|unknown] [--effective present|absent|unknown] [--successor improved|unchanged|degraded|unknown]"
category: fleet-ops
status: candidate
---

# kaizen — Continuous Improvement (RE1)

Small improvements compound only when they are *captured and attributed*.
`kaizen` turns "we fixed X" into a durable receipt that says **what object
improved**, whether the improvement is structural or effective recursion, who
led it, and whether it changed the next improvement cycle.

One receipt per improvement. Small by design — a kaizen receipt for a renamed
variable is correct; a missing receipt for a shipped improvement is the bug.

## When to Use

- After shipping any improvement — code, skill, workflow, harness, doc, process
- During `/aar` or `/retrospective` when an improvement is named
- When an RSI or compounding claim needs evidence instead of assertion
- Before `/end-session` if the session shipped improvements

## When to Skip

- No improvement shipped — activity is not gain. Do not receipt effort.
- The claim is "the model got smarter" — `recursive_target: model` claims need
  model-level evidence; capture the harness/workflow/skill that actually changed.

## Execution

### 1. Name the improved object — `recursive_target`

Attribute the improvement to what actually changed:

```
model | prompt | memory | skill | workflow | harness |
evaluator | curriculum | exploration_policy | infrastructure | organization
```

Do not infer `model` when the real target is the harness, memory, exploration
policy, or organization. Multiple targets are allowed when the change is
genuinely compound.

### 2. Classify the recursion

- `structural` — can the improvement loop now reach the thing that produces
  improvements? (the system can change its change-maker)
- `effective` — is there evidence improvement *n* increased the ability to
  produce or verify improvement *n+1*?

Ordinary iteration does not qualify as effective recursion. `unknown` is a
valid answer — do not manufacture certainty.

### 3. Record the work attribution

- `task_lead`: `human` | `agent` | `mixed` | `unknown`
- `human_interventions`: count of human interventions required
- `successor_cycle_effect`: did this change the *next* valid improvement
  cycle? `improved` | `unchanged` | `degraded` | `unknown`

### 4. Fill evaluator provenance

Who or what admits this claim — identity, funder, selection/removal authority,
access/evaluation/publication scope, conflicts, and whether the candidate
system can modify its own evaluator or eval data. External ≠ independent.

### 5. Emit the receipt

Append one JSONL line to:

```
~/.agents/_state/rsi/recursion-evidence.jsonl
```

conforming to `docs/schemas/evals/recursion-evidence-receipt.v1.md`
(`schema_version: recursion-evidence-receipt.v1.0.0`). Corrections are new
lines with `supersedes: <prior receipt_id>` — never edit a written line.

### 6. Verify the write

```bash
tail -1 ~/.agents/_state/rsi/recursion-evidence.jsonl
```

A missing line means the write failed silently — re-emit before reporting.

## Examples

```bash
# Improvement to a workflow, agent-led, effect on next cycle unknown
kaizen "index freshness check added to end-session" \
  --target workflow --lead agent --structural present --effective unknown

# Skill improvement with clear successor effect
kaizen "skill-creator now emits provider-neutral frontmatter" \
  --target skill --lead mixed --structural present --effective present \
  --successor improved --interventions 1
```

## Constraints

- `unknown` / `underdetermined` is an allowed terminal state — never upgrade a
  guess into a claim.
- No automatic authority expansion, TierShift, deployment, merge, or release
  follows from any receipt.
- Fleet activity (agent count, task volume, AI work-share) is NOT recursive
  gain — receipt the object that improved, not the motion.
- Corrections supersede; they never rewrite history.

## Skill Chains

### Mandatory

- None — kaizen is a leaf capture ritual.

### Advisory

- **Before kaizen**: `/aar`, `/retrospective` (improvement source)
- **After kaizen**: `/rsi-dashboard` (verify encoding lands in metrics),
  `/ledger` (if the improvement reveals a durable pattern)

## Authority

- **T1 (TRUSTED)**: May run without restriction
- **T2 (Active/High)**: May run without restriction
- **T3 (Medium)**: Operator approval before writing receipts
- **T4 (Probationary)**: BLOCKED — cannot write receipts
- **Operator**: Override any restriction
