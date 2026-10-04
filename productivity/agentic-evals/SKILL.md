---
name: agentic-evals
description: >
  Design evaluation contracts and test plans for agentic systems. Create
  deterministic tests, trajectory evals, quality dimensions, gold-set criteria,
  and CI gates before or after implementation. Use when asked for tests first,
  an eval plan, success criteria, non-deterministic testing, LLM-as-judge setup,
  or retrofitting evals. Do NOT use for routine test failure debugging, simple
  unit-test additions with established patterns, or merely running tests.
---

# Agentic Evals

Use this skill to define how an agentic feature will be judged before treating
it as correct. Keep deterministic tests separate from probabilistic evals.

## Workflow

1. Identify the target: `SPEC.md`, existing code, agent behavior, tool contract,
   or production workflow.
2. Split behavior into:
   - Deterministic: pure logic, schemas, permissions, parsing, API contracts.
   - Non-deterministic: planning, tool choice, summaries, ranking, judgment,
     multi-step recovery.
3. For deterministic behavior, write Arrange-Act-Assert test cases and expected
   failure modes.
4. For non-deterministic behavior, define evals across task completion,
   correctness, efficiency, and safety.
5. Use trajectory evals when tool choice, ordering, or recovery path matters.
6. Use LLM-as-judge only with a task-specific rubric and a small gold set; prefer
   pairwise comparison when comparing versions.
7. Generate `EVAL_PLAN.md` from `assets/templates/EVAL_PLAN.md`.

## Gate Design

- Level 1: fast PR checks such as schemas, fixtures, tool contract tests.
- Level 2: deeper nightly or pre-release evals with repeated trials.
- Level 3: deployment gate using acceptance thresholds and manual review for
  high-impact changes.

## References

Read `../agentic-engineering-sdlc/references/day4_security_and_evaluation.md`
for deeper evaluation, judge calibration, and trajectory guidance.

## Done Criteria

- Success criteria are measurable.
- Deterministic tests and non-deterministic evals are separated.
- Trial count, thresholds, and gold-set source are documented.
- CI gate ownership and failure response are clear.
