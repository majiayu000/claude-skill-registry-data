---
name: test
description: Run the pytest test suite with coverage. Accepts optional filter flags. Use after making changes to verify nothing broke.
---

Run tests from the project root:

```bash
just test $ARGUMENTS
```

For a faster parallel run on large suites:

```bash
just ntest $ARGUMENTS
```

Examples:
- `just test` — full suite
- `just test -k 'test_name'` — single test
- `just ntest` — parallel execution

Report: pass/fail count, any failures with full error output, and the coverage summary for `server/` and `scripts/`. If tests fail, investigate the root cause before proposing fixes.
