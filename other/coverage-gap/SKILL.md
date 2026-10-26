---
name: coverage-gap
description: Find untested code and fill the gaps that matter. Use when asked about test coverage, "what isn't tested", "add tests", or before splitting/refactoring a file that may have none.
---

# Finding and filling coverage gaps

## Measure

```bash
pytest tests/ -q --cov=backend --cov=frontend --cov-report=json:.coverage.json
python -m tools.refactor_audit.coverage_gate --report
```

Takes about six minutes. The report shows each area, its current percentage
and its floor, with `*` marking the money-critical ones.

## Read the number correctly

Overall coverage is ~37%, and that figure is close to meaningless on its own.
About 7,000 of ~34,000 statements are NiceGUI page bodies that cannot be
meaningfully unit-tested without a browser; they sit near 4% and drag the
global number down regardless of the trading logic.

What matters is the per-area picture:

| Band | Areas |
|---|---|
| Strong | `services/trading` 88 · `risk` 87 · `positions` 86 · `signals` 84 · `db` 92 |
| Middling | `broker` 58 · `telegram` 50 · `reversal_engine` 48 · `dpm` 46 |
| Weak | `controllers` 26 · `utils` 30 · `config` 15 · `backtest` 15 |
| By design | `frontend` 4 — covered by `tests/frontend/` import + boot tests |

## Pick gaps by risk, not by size

Order of priority:

1. **Zero-coverage security or money code.** `controllers/remote/` (token
   issuance, revocation, admin machines — 2,116 lines, no tests) is the
   standing example and the highest-value work in the repo.
2. **Anything you are about to refactor.** Tests first, then move. A split
   without tests cannot be verified.
3. **Branches in money-critical areas** — the `*` areas are already high, so
   what is missing there tends to be error paths, which are exactly the ones
   that matter at 3am.
4. Everything else.

Do **not** chase the global percentage. Adding tests for `utils/theme.py`
raises the number and protects nothing.

## Coverage is not proof

Coverage measures lines *executed*, not behaviour *verified*. A file at 90%
whose tests assert nothing is untested. Use coverage to find holes, never to
declare victory.

## Writing the tests

Follow `docs/system/rules/40-testing.md`:

- write it, **run it, watch it fail**, then make it pass
- every "there are zero X" assertion needs a negative control proving the
  detector can find one
- no test may place, close or modify a real or demo order
- name what the test protects in its docstring, not just what it calls

## After adding tests

```bash
python -m tools.checks all
python -m tools.refactor_audit.coverage_gate --update-baseline
```

Rebaselining after a genuine improvement is correct and expected — the ratchet
is meant to record progress. Say the numbers in the commit:

```
services/broker coverage 58% -> 71%: error paths in ea_bridge reconnect.
```

**Never** rebaseline downward to make a failure go away. The floor is the
record of what was once covered; lowering it erases the only evidence that
something regressed.
