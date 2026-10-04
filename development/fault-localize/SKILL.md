---
name: fault-localize
description: >
  Find the earliest decisive failure in an agent run trace and propose an
  evidence-backed targeted repair. Load when a run failed, results are wrong,
  or the user asks what went wrong in an agent session. Also triggers on
  "localize the fault", "first incorrect step", "debug this run", "trace
  attribution", "why did the agent fail", or after run-trace captures errors.
  Pairs with debug-and-fix for code defects and dynamic-routing for plan faults.
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: REFLECT arXiv 2606.09071, LADYBUG EDBT 2025, Watson arXiv 2411.03455
  resources:
    references:
      - LOCALIZATION.md
      - examples.md
---
# Fault Localize

You find the **earliest decisive divergence** in a trace, hypothesize cause from evidence, apply a **targeted repair**, replay from that point, and verify an **outcome flip**. No vague retries.

## Hard Rules

Require a trace file (`.agent-loom/traces/<run-id>.jsonl`) or reconstruct from session tool history.
Follow `references/LOCALIZATION.md` — earliest error/divergence wins.
Hypothesis must cite `output_ref` or `error` from the trace record.
Replay from suspected step — not full blind restart unless plan-layer fault.
Record attribution with `outcome_flip` boolean.
Route code defects to `debug-and-fix`; plan faults to `dynamic-routing`.

---

## Workflow

### Step 1 — Load trace

Run `trace_query.py timeline` and `errors`. If no trace, build minimal timeline from session history.

### Step 2 — Identify suspected step

Earliest record with `error` or output contradicting expected. State `suspected_step_id`.

### Step 3 — Write hypothesis

Three lines max — cite evidence. Classify layer.

### Step 4 — Propose targeted repair

One intervention matched to layer. Not a kitchen-sink fix.

### Step 5 — Replay and verify

Re-run from suspected step. Compare outcome.

### Step 6 — Attribute

Write attribution record. If no flip, consider next candidate step.

---

## Gotchas

- Latest error ≠ earliest cause — always scan chronologically.
- Fixing symptoms downstream masks upstream plan errors.
- Flaky tests need two replays before attributing.

---

## Output Format

```markdown
## Fault localization — [run_id]

Suspected step: **Sx** @ [ts]
Hypothesis: [evidence-cited]
Layer: [tooling|code|plan|environment]

Proposed repair: [one intervention]
Replay result: [pass|fail]
Outcome flip: [true|false]

Attribution: `.agent-loom/traces/[run_id]-attribution.json`
Next: [resume plan | debug-and-fix | escalate]
```

---

## Examples

Teaser: Trace shows S1 pass, S2 npm test fail → hypothesize missing env → repair .env.example → replay S2 → flip true.

Full pairs: `references/examples.md`

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Last error is the cause" | Downstream errors are often symptoms. |
| "Retry whole run" | Expensive; masks localized fix opportunity. |
| "Guess and patch" | Hypothesis without evidence → wrong attribution. |
| "Trace is optional" | Localization without trace is reconstruction guesswork. |
| "One flip proves root cause" | Flaky tests need confirmatory replay. |

## Verification

- [ ] Suspected step is earliest divergence
- [ ] Hypothesis cites trace evidence
- [ ] Attribution record written
- [ ] Layer-appropriate handoff if not fixed

## Red Flags

- Hypothesis with no trace citation
- Full rerun without identifying suspected step
- outcome_flip true on single flaky test

## Prune Log
Last pruned: 2026-07-05
- Initial release from high-leverage skill spec (Skill 4 family)

## Impact Report

```
Localize: [run_id] | Suspected: [step] | Flip: [bool] | Layer: [layer]
```
