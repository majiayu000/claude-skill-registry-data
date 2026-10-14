---
name: autoresearch-code-skill
description: >-
  Autonomous code optimization loop — modify, verify by benchmark, keep/revert
  against any metric (coverage, bundle size, runtime, error count).
  TDD-flavored.
license: Apache-2.0
compatibility: opencode
metadata:
  protocol: autoresearch-default-on
category: Autoresearch
---

## What I do

I run an autonomous code-optimization loop. Each iteration: read the audit trail → hypothesize one atomic code change → apply → commit → run the benchmark evaluator → run the Guard command → **run the Consumer Coverage check** → keep the commit if `{"pass":true,"score":N}` shows improvement AND the guard stays green AND no downstream consumer is broken, else `git reset --hard HEAD~1`. I am Tier 1 (mechanical evaluator) — every keep/revert decision comes from a program, never from LLM self-judgment. I overlap with `tdd-workflow-skill`, but I am autonomous-loop-flavored (iterate to a target overnight) where TDD is single-cycle (write-one-test-then-implement).

## Triggers

Load me (or route to `autoresearch-code-subagent`) when the user says any of:

- "optimize code", "optimize until", "iteratively improve"
- "test coverage", "increase coverage to N%"
- "bundle size", "reduce bundle"
- "performance", "reduce runtime", "speed up"
- "fix errors", "reduce error count", "drive failures to zero"
- "autoresearch code", "git-as-memory optimization"

Do **not** trigger for ML training (→ `autoresearch-ml-skill`) or literature review (→ `autoresearch-research-skill`).

## Citations

- `autoresearch-core-skill/references/evaluator-contract.md` — the `{"pass":bool,"score":N}` shape my benchmark evaluator emits.
- `autoresearch-core-skill/references/stuck-detection.md` — 3-strike pivot (switch from micro-opt to algorithmic change; target a different hotspot).
- `autoresearch-core-skill/references/iteration-safety.md` — Verify/Guard separation; never modify `.env`, `node_modules/`, or run `rm -rf`.
- `autoresearch-core-skill/references/audit-trail.md` — the 8-column TSV I append to (`<skill>-results.tsv`).
- `autoresearch-core-skill/references/crash-recovery.md` — syntax error → free fix; guard failure → revert.

## Skill-specific overrides

1. **TDD mapping (the key override).** When the metric is "test pass-count":
   - `pass: true`  **GREEN** (all targeted tests pass)
   - `pass: false`  **RED** (any targeted test fails)
   - `score`  **pass-count** (number of tests passing)
   - This makes `tdd-workflow-skill` and this skill mechanically equivalent when the metric is test-pass; the difference is I iterate to a target autonomously rather than running one RED→GREEN cycle.
2. **Verify vs Guard vs Consumer Coverage.** Verify emits `{"pass":bool,"score":N}` (e.g. `pytest --cov` → coverage %). Guard is a separate command that must stay green (e.g. `npm test`). **Consumer Coverage** is a third mandatory check that enumerates downstream callers of every changed symbol and forces revert on any broken reference. A failing Guard **or** a failing Consumer Coverage check forces revert **regardless of Verify** — you cannot trade test-green for a broken downstream consumer.
3. **Tier 1** (mechanical evaluator). No agent-as-evaluator fallback.
4. **Git-as-memory.** Commit before Verify so revert is one command. Never edit the working tree without committing first — an uncommitted change cannot be cleanly reverted.
5. **Bounded-by-default.** `Iterations: 25` default. Lower for fast benchmarks (e.g. `Iterations: 10` for `npm run build` cycles).
6. **Consumer Coverage sub-step** (mandatory, between Guard and Keep/Revert). Guard is necessary but **not sufficient** — Guard validates a fixed suite (e.g. `npm test`), but it cannot detect downstream breakage in code paths the suite does not exercise. The Consumer Coverage sub-step traces the actual call graph of the symbols this iteration touched:
   - With `.codegraph/`: `codegraph_callers` on each changed symbol; revert if any caller is broken.
   - Without `.codegraph/`: `grep -r`/`glob` for importers and references of each changed symbol; revert if any grep hit references the old (now-renamed/removed) symbol.
   - Log `discard` with `consumer-broken` note in `*-results.tsv` when this gate forces a revert. Cross-references the agent's implementation in `autoresearch-code-subagent.md` §Consumer Coverage Gate.

## Templates

- `autoresearch-code-skill/templates/benchmark.py.template` — emits `{"pass":bool,"score":N}` JSON; parameterized `{{COMMAND}}`, `{{METRIC_NAME}}`, `{{TARGET_VALUE}}`.
- `autoresearch-code-skill/templates/research.md.code-template` — inline Goal/Scope/Metric/Verify/Guard format with worked examples (coverage, bundle size, runtime).
- `autoresearch-code-skill/templates/guard.example.sh` — example safety-net pattern (`npm test` must pass while optimizing bundle size).

## NEVER STOP / NEVER ASK

Inherits the core autonomy directive. Once the loop has begun, do not pause to ask whether to continue. The evaluator answers keep/revert mechanically; the human expects you to work until the predicate is met, the plateau+ceiling both trip, or max iterations is reached.

## References

- **uditgoenka/autoresearch** (MIT) — methodology source (command structure, TSV format, keep/revert pattern). Full notice: `THIRD_PARTY_LICENSES.md`.
- **karpathy/autoresearch** (MIT) — source for the git-as-memory pattern (commit → verify → keep/reset). Full notice: `THIRD_PARTY_LICENSES.md`.
- **wjgoarxiv/autoresearch-skill** (MIT) — inspiration for the strict `{"pass":bool,"score":N}` evaluator contract. Full notice: `THIRD_PARTY_LICENSES.md`.
