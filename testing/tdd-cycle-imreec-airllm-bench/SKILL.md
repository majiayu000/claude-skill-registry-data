---
name: tdd-cycle
description: |
  Use this skill when implementing any new feature, function, class, or module. Triggers include:
  "implement", "let's build", "add a feature", "write a function", "create a class",
  "add a method", "let's code", "now build", "let's write".
  Always apply for any new code that has logic — skip only for pure config/data files.
---

# TDD Cycle (Red → Green → Refactor)

Strict test-first discipline. ≥90% coverage on the deterministic core emerges as a side effect.

> **HW5 note:** the pure Tier-1 modules (`metrics`, `economics`, `roofline`, `harness` against the
> `mock` runner) are fully TDD-able keyless. The real `runners` (torch/airllm/llama.cpp) are thin and
> hardware-bound — exercised by the Tier-2 committed runs, marked `@pytest.mark.hardware`, excluded
> from CI. Put the *logic* in pure modules so it's testable; keep the runners as thin adapters.

## The cycle (one concern at a time)

### RED — write the failing test first
1. Create/open the matching `tests/unit/test_<module>/test_<thing>.py`.
2. Write a test describing **behavior**, with a descriptive name
   (`test_breakeven_is_monotonic_in_volume`, not `test_econ`).
3. Run it — it MUST fail meaningfully (missing attr, wrong value), not an unrelated import error:
   ```bash
   uv run pytest tests/unit/test_economics/test_breakeven.py::test_breakeven_is_monotonic_in_volume -xvs
   ```
4. **Commit RED:** `git commit -m "test(economics): failing test for monotonic break-even"`

### GREEN — minimal code to pass
1. Write only enough to pass — nothing the tests don't demand.
2. Re-run the test (`1 passed`), then the suite (`uv run pytest -x`).
3. **Commit GREEN:** `git commit -m "feat(economics): break-even curve from cost components"`

### REFACTOR — improve without changing behavior
Extract helpers, improve names, add docstrings, keep files < 150 lines. Tests stay green. Optional.

## Rules

1. One concern per cycle — don't implement two functions off one test.
2. No skipping RED. Code-first → delete, write the test, re-implement.
3. Verify each phase by reading pytest output, not by trusting it.
4. No `pytest.skip` to defer work — write it now or remove it.
5. Coverage is a side effect, not the goal.

## Unit vs integration vs hardware

- `tests/unit/` — one pure module in isolation (metrics, economics, roofline, sampler-with-fake-clock).
- `tests/integration/` — composition (harness driving the `mock` runner end-to-end → `RunResult` → metrics).
- `@pytest.mark.hardware` — needs the GPU box; excluded from CI, run manually for Tier-2.

## Verify before signaling success

`make test` and `make lint` both green. If either fails, the cycle isn't complete.
