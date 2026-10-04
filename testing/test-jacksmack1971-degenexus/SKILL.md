---
name: test
description: Run DegenExus pytest planning and regression workflow with Prove-It, FSV-AAA, and edge-case evidence.
disable-model-invocation: true
argument-hint: "[test scope or behavior]"
---

# Test Workflow

`test-engineer` is the canonical owner for DegenExus test authoring and coverage analysis. `test-writer` is a read-only deprecated alias and must not be routed for new work.

## Required References

- `.claude/rules/synergy-contract.yml`
- `.claude/rules/evidence-schema.yml`
- `.claude/skills/test-regression/SKILL.md`
- `.claude/skills/fsv-verify/SKILL.md`
- `.claude/skills/edge-case-audit/SKILL.md`

## Steps

1. Identify the source of truth and current test patterns.
2. For bugs, write or describe the failing regression first and record `failing_before`.
3. Use FSV-AAA where practical: PRE source-of-truth read, one ACT, POST reread, expected DIFF assertion.
4. Cover boundary/equivalence classes: empty/zero, min/max boundary, malformed/adversarial input, and ordering/concurrency where applicable.
5. Use `pytest-mock`'s `mocker` fixture; do not import `unittest.mock` directly.
6. Mock LLM providers, yfinance/network calls, time, and randomness.
7. Run targeted pytest first, then broader regression tests when feasible.
8. Emit `.claude/rules/evidence-schema.yml` fields with `edge_cases`, `failing_before`, and `passing_after` evidence when applicable.
