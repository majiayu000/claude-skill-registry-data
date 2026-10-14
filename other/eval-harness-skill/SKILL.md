---
name: eval-harness-skill
description: Evaluate code quality, skill effectiveness, and implementation correctness against defined criteria with scoring and improvement suggestions
license: Apache-2.0
compatibility: opencode
metadata:
  protocol: autoresearch-opt-in
category: Agent Optimization
---

## What I do

Structured evaluation framework: define measurable criteria → run checks → score 0-10 per criterion → report pass/fail vs thresholds → suggest improvements for failures. Unlike `verification-loop-skill` (gate execution), this skill owns **scoring rubrics and thresholds**.

**Trigger phrases**: "evaluate this code", "run eval", "score this implementation", "quality check", "benchmark against criteria".

## Default Criteria (0-10 each, thresholds customizable per run)

| Criterion | Threshold | Key questions |
|-----------|-----------|---------------|
| Correctness | 7 | Does it do what it should? Edge cases? Error paths? |
| Code Quality | 7 | Conventions, readability, abstractions without over-engineering |
| Test Coverage | 7 | Tests present? Edge cases covered? Maintainable? |
| Performance | 6 | Efficient algorithms, no wasted computation, caching where applicable |
| Security | 7 | Input validation, no injection, proper authn/authz |

Score ranges: 9-10 excellent · 7-8 good · 5-6 adequate · 3-4 below standard · 1-2 poor · 0 failed. Overall = sum + percentage; verdict from thresholds.

## Scope Variants

Single file · module/directory · skill output (`skill:<name>`) · PR diff (`pr:<num>`) · acceptance criteria (`issue:<num>`).

## Workflow

1. **Define criteria** for the target (use defaults, add domain-specific ones). Criteria must be measurable ("functions under 20 lines", not "clean code") and consistent across comparable runs.
2. **Execute**: static analysis (lint, types, complexity) → pattern/anti-pattern checks → test run + coverage → score each criterion → gap analysis.
3. **Report**: per-criterion table (score / threshold / status) + overall + per-failure findings with concrete fix suggestions (priority, effort, expected impact).
4. **Gate semantics**: evaluations can gate PRs — a failed critical criterion blocks merge. Judge trends across runs, not absolute scores; note exceptions when a criterion doesn't apply.

Criteria starters: code quality — naming per language convention, function ≤20 lines, cyclomatic <10, no silent catches, DRY. Skill effectiveness — task completion, output production-readiness, consistency, graceful failure, integration. Acceptance criteria — each criterion checked with evidence, no partial completions, no regressions.

## Integration

- `verification-loop-skill` — canonical gate contract; eval supplies scoring rubrics, not gate execution
- `continuous-learning-skill` — learn which patterns score well
- `civiltekk-context-optimization-skill` — compact preserves eval results
- `linting-workflow-skill` / `code-smells-skill` / `solid-principles-skill` — signals feeding the quality criterion

## References

- `verification-loop-skill` — gates and verification during implementation
- `continuous-learning-skill` — learning from evaluation results
- `civiltekk-context-optimization-skill` — preserving eval context

## Iteration Protocol (opt-in)

**DO NOT execute any of the following unless `AUTORESEARCH_PROTOCOL=1` is set in your environment.** When unset, this skill behaves exactly as documented in all sections above; the Iteration Protocol block is descriptive only.

When `AUTORESEARCH_PROTOCOL=1`:

1. **Gate check**: confirm env var is set; if unset, follow default behavior above.
2. **Auto-detection**: if this skill is invoked on a task that looks iterative (multiple cycles expected), prompt ONCE per session: "This looks iterative. Enable autoresearch protocol? (y/n)". On "y", continue; on "n", default behavior. Cache the answer for the session.
3. **5-stage loop**: cycle Understand → Hypothesize → Experiment → Evaluate → Log & Iterate. See `autoresearch-core-skill/SKILL.md`.
4. **Evaluator contract**: emit `{"pass":bool,"score":N}` JSON from a mechanical evaluator. Pass determines keep/revert; score logged to `eval-harness-results.tsv`. See `autoresearch-core-skill/references/evaluator-contract.md`.
5. **Stuck detection**: 3 consecutive non-improving iterations → strategy pivot; 5 consecutive → paradigm shift. See `autoresearch-core-skill/references/stuck-detection.md`.
6. **Audit trail**: append every iteration to `eval-harness-results.tsv` (8-column: iteration, commit, metric, delta, status, description, timestamp, evaluator_output). See `autoresearch-core-skill/references/audit-trail.md`.
7. **Crash recovery**: syntax errors → fix immediately (don't count); runtime → max 3 fix attempts then skip; timeout → revert + log; OOM → smaller variant. See `autoresearch-core-skill/references/crash-recovery.md`.
8. **Git-as-memory**: commit before each verify; auto-revert (`git reset --hard HEAD~1`) on `pass:false`.
9. **Iteration safety**: bounded-by-default (`Iterations: 25`); safety blocks `.env`, `node_modules/`, `rm -rf`, `git push --force`. See `autoresearch-core-skill/references/iteration-safety.md`.

### Skill-specific override

**TSV audit trail.** Append every eval run to `eval-harness-results.tsv`. Overnight persistence via `autoresearch-core-skill/scripts/autoresearch-loop.sh` (detects available CLI tool). Score is the eval metric; pass = meets target threshold.

### Max iterations
- Default: 25 iterations
- Hard cap: 100 (explicit `Iterations: unlimited` overrides)

> **Removal note (2026-09-19, #409 trim per LEARNINGS #383 recipe):** dropped the worked criteria/report markdown examples, the evaluation-templates section (compressed to criteria starters), the Example Usage section, and Best Practices prose (compressed into the workflow). Kept verbatim: frontmatter, criteria/threshold/score tables, workflow contract, Iteration Protocol section.
