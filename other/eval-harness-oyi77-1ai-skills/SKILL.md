---
name: eval-harness
description: Use when setting up eval-driven development (EDD) for AI-assisted workflows, defining pass/fail criteria for agent task completion, measuring reliability with pass@k metrics, creating regression suites for prompt or agent changes, or benchmarking performance across model versions.
domain: meta
subdomain: self-improvement
category: meta
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- evaluation
- edd
- benchmarking
- regression-testing
- pass-at-k
- prompt-engineering
triggers:
- eval harness
- evaluate agent
- benchmark skill
- pass at k
- edd
- eval driven development
argument-hint: "[eval name or feature]"
---

# Eval Harness

## Overview

Formal evaluation framework implementing eval-driven development (EDD). Evals are the unit tests of AI development: define expected behavior BEFORE implementation, run continuously during development, track regressions with each change, measure reliability with pass@k metrics.

## When to Use

**Trigger phrases:**
- "eval harness", "evaluate agent", "benchmark skill"
- "pass@k", "eval driven development", "regression eval"

Use directly when:
- Setting up EDD for a new agent workflow or skill.
- Defining pass/fail criteria before shipping a prompt or agent change.
- Measuring reliability across model versions or harnesses.
- Creating regression suites for skill modifications.
- Comparing candidate vs baseline skill output (blind eval).

## When NOT to Use

- Ordinary code test suites → use `test-driven-development` or language-native runners.
- One-off manual checks with no repeatability requirement.
- Production monitoring → use `observability` skills.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll eyeball the output, no need for formal evals." | Eyeballing doesn't survive model updates. A saved eval catches regressions automatically next week. |
| "Evals take too long to set up." | A 5-case eval takes 10 minutes and pays back on every subsequent change. Unmeasured changes ship blind. |
| "One passing run proves it works." | LLMs are stochastic. Run pass@k (typically k=5) to measure reliability, not luck. |
| "Grading by another LLM is cheating." | LLM-as-judge is standard practice for subjective outputs. Pin the judge model version and use rubrics for consistency. |

## Workflow

### 1. Define Success Criteria (Before Implementation)

```markdown
[EVAL: feature-name]
Task: Description of what the agent should accomplish
Inputs: Fixture files, prompts, or API mocks
Success Criteria:
  - [ ] Criterion 1 (binary: met / not met)
  - [ ] Criterion 2
  - [ ] Criterion 3
Expected Output Shape: Schema or example
```

Every criterion must be mechanically checkable or rubric-scored—never "looks good".

### 2. Choose Grader Type

| Grader | Use For | Method |
|---|---|---|
| **Code-based** | Deterministic outputs (files, JSON, build artifacts) | Bash/python assertion scripts |
| **Exact-match** | Fixed strings, IDs, enum values | String equality |
| **LLM-as-judge** | Subjective quality (writing, design rationale) | Rubric + pinned judge model |
| **Human review** | Gold-standard calibration only | Sample 10% of runs monthly |

Prefer code-based graders. Reserve LLM judges for genuinely subjective dimensions.

### 3. Build the Eval Runner

Minimal Python harness pattern:

```python
import json, subprocess, sys
from pathlib import Path

CASES = sorted(Path("evals/cases").glob("*.json"))
passed = 0
for case_path in CASES:
    case = json.loads(case_path.read_text())
    # run agent/command under test
    result = subprocess.run(
        [sys.executable, "run_task.py", "--input", str(case_path)],
        capture_output=True, text=True, timeout=120,
    )
    ok = all(check(result.stdout, c) for c in case["criteria"])
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {case_path.name}")
print(f"\npass@1: {passed}/{len(CASES)}")
```

Store cases as JSON fixtures under `evals/cases/`; one file per scenario.

### 4. Measure Reliability (pass@k)

Run each case k times (default k=5):
- **pass@1**: single-run success rate
- **pass@k**: probability at least one of k runs succeeds
- **cons@k**: all k runs succeed (stability metric)

Track deltas between baseline and candidate:

```text
Baseline (main):   pass@1 = 80%, cons@5 = 60%
Candidate (feat):  pass@1 = 90%, cons@5 = 75%
Verdict:           SHIP — both reliability and stability improved
```

### 5. Regression Eval After Changes

```markdown
[REGRESSION EVAL: feature-name]
Baseline: git SHA or checkpoint tag
Cases: N total
Result: X/N passed (previously Y/N)
New failures: [list]
Flaky failures: [list — passed on rerun]
```

Any new hard failure blocks the merge until fixed or the eval is proven wrong.

### Prompt Hill-Climb (one change, one measurement)

Use this when optimizing a system prompt, tool description, or agent instruction. It is a controlled experiment, not an open-ended rewrite.

1. **Freeze baseline:** save prompt text/hash, model/config, tool definitions, eval-set version, and current scores.
2. **Name the failure:** choose one observed failure category (missing field, hallucination, wrong tool, scope drift, injection, verbosity/cost). Add a fixture if the failure is not represented.
3. **Propose one edit:** identify the smallest prompt section that could cause the failure. Do not change model, tool set, prompt, and grader together.
4. **Run blind baseline + candidate** over the same fixture set. For stochastic tasks use k≥5 runs per case, interleaved/randomized order when practical.
5. **Compare:** task pass rate, critical regression count, rubric score, input/output tokens, latency, cost per completed task, and cache-read tokens where available.
6. **Keep or revert:** keep only if the target improves and protected criteria do not regress. If tied, prefer the shorter/clearer prompt. Record the result and rationale.
7. **Promote:** add any discovered failure as a regression fixture before changing the production prompt.

```markdown
[PROMPT EXPERIMENT: missing-citations-v2]
Baseline: prompts/research-v1.txt @ sha256:...
Candidate: prompts/research-v2.txt @ sha256:...
Changed variable: output contract now requires evidence[] and unknowns[]
Eval set: evals/research-v3 (12 cases, k=5)
Baseline: pass@1 0.78 | cons@5 0.58 | 920 input tok | 1.8s | $0.004/task
Candidate: pass@1 0.93 | cons@5 0.83 | 960 input tok | 1.9s | $0.004/task
Regressions: none on protected cases
Decision: keep; add missing-citation case to permanent regression set
```

Grader guidance: code/schema checks first; LLM judge only for genuinely subjective output. Pin judge model + rubric, and calibrate against human labels before trusting score deltas. Never tune on the test set: use train/validation for iteration, holdout test once for final confirmation.

## Eval Types

| Type | Purpose | Frequency |
|---|---|---|
| **Capability eval** | Prove the agent CAN do something new | Before shipping a feature |
| **Regression eval** | Prove nothing broke | Every PR touching prompts/skills |
| **Benchmark eval** | Compare models/harnesses/skills | Weekly or on model version bump |
| **Blind A/B eval** | Candidate vs baseline without knowing which is which | Skill style/rule changes |

## Skill Quality Gates (3-Tier)

When the thing being evaluated is a **skill** (not a prompt or task), run gates in this order. Pattern adapted from [NVIDIA/SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator); in 1ai-skills the tiers map to tools that already exist in `scripts/`.

### Tier 1 — Validation (safety, well-formedness, harness compatibility)

A skill must parse, follow the standard, and not carry unsafe declarations before anything else matters:

```bash
python3 scripts/validate-skill-schema.py     # frontmatter schema conformance
python3 scripts/lint-skills.py               # required sections, description quality
python3 scripts/test-skills.py               # structure + cross-references
```

Gate: **0 errors** required. `--write` (lint) syncs SKILLS.json. Anything failing Tier 1 does not proceed to Tier 2 — measuring a malformed skill wastes eval budget.

### Tier 2 — Deduplication (semantic overlap detection)

Before creating a skill, detect near-duplicates among the existing set; before merging, detect overlap a candidate introduces:

```bash
python3 scripts/lint-skills.py --overlap
# Narrow review to one domain when triaging a large result set:
python3 scripts/lint-skills.py --overlap --category content
```

The linter compares description tokens, activation language, and tags. Its findings are **candidates**, not automatic deletion decisions. Classify every flagged pair:

1. **Duplicate** — same workflow + same triggers: extend the existing skill; do not add another.
2. **Adjacent** — complementary triggers or different outputs: keep both and cross-link them.
3. **Distinct** — shared vocabulary only: keep both and record why the overlap is superficial.

Gate: a new skill must name the skills it overlaps with and state why it is not a duplicate of each.

### Tier 3 — Live Evaluation (agent impact in a sandbox)

Does the skill measurably change agent outcomes? This is an eval-harness run where the treatment is "skill loaded" vs "skill not loaded":

1. Pick N representative tasks with code-based graders (see Grader Type above).
2. Run baseline (agent without skill) and candidate (agent with skill), blind to which is which where possible.
3. Score with `pass@k` (k≥5); compare tiers.

Gate: ship only if candidate ≥ baseline on pass@1 without regressing cons@k. Record the numbers in the skill's PR — a skill that changes nothing measurable is documentation, not capability.

### Async review/eval feedback (Plannotator pattern)

A human review or slow Tier-3 run should **not hold the agent session open**. Submit the candidate, persist an eval ID, finish the current turn, and resume when the verdict arrives as a message/event. Tier-1 validation remains synchronous and blocking; it is fast and deterministic.

```text
1. Validate (Tier 1) synchronously. If it fails, stop and fix.
2. Create eval record: {eval_id, candidate_sha, baseline_sha, cases, status="queued"}.
3. Dispatch candidate-vs-baseline runs; return eval_id immediately. Do not poll in a tight loop.
4. On completion, persist {pass@1, cons@k, failures, artifacts, verdict}.
5. Notify the originating agent/session with the structured result.
6. Resume: compare results against the recorded gate; ship, revise, or reject.
```

Example result payload (portable across hooks, CLI, and MCP transports):

```json
{
  "eval_id": "eval-2026-001",
  "candidate_sha": "abc1234",
  "baseline_sha": "def5678",
  "status": "complete",
  "pass_at_1": 0.92,
  "cons_at_5": 0.80,
  "new_failures": ["case-07: expected citation missing"],
  "verdict": "revise",
  "artifacts": ["evals/results/eval-2026-001.json"]
}
```

**Resume contract:** the resumed agent reloads the eval record and candidate diff; it must not rely on conversational memory. A notification is a wake signal, not approval. If a reviewer denies/rejects, attach their structured feedback and the changed-lines diff; revise only those lines, then re-run the affected cases + regression suite.

**Failure / timeout behavior:**
- No verdict before deadline → mark `timed_out`, notify agent; never silently assume pass.
- Human denies → mark `rejected`, preserve comments, no merge/ship.
- Worker crashes → mark `failed` with logs; retry once only if failure is transient.
- Duplicate notification → dedupe by `eval_id` + terminal status; do not apply twice.
- Do not launch background evals unless the harness can persist state and deliver a completion event. If unavailable, run synchronously and say so.

### CI flow

Wire Tier 1 into pre-commit/CI (fast, deterministic); run Tier 2 (`python3 scripts/lint-skills.py --overlap`) on skill additions only; run Tier 3 on demand or weekly. Provide one `doctor`-style entry point that runs Tiers 1–2 locally and reports Tier 3 as skipped/queued — never imply the live eval ran when it did not.

## Verification

- [ ] Success criteria defined BEFORE implementation
- [ ] All criteria mechanically checkable or rubric-scored
- [ ] Code-based grader preferred over LLM judge where possible
- [ ] pass@k measured with k >= 5 for stochastic tasks
- [ ] Baseline recorded before candidate runs
- [ ] Regression suite updated with any newly discovered failure mode
- [ ] Eval fixtures committed to repo (`evals/cases/`)
- [ ] Skill quality gates run in order (Tier 1 → 2 → 3) when evaluating a skill
- [ ] Tier 1 gate passed with 0 errors before spending eval budget on Tiers 2–3
- [ ] Tier 2 overlap verdict recorded for any new or merged skill
- [ ] Tier 3 candidate-vs-baseline numbers recorded; no cons@k regression