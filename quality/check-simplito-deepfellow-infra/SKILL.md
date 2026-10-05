---
name: check
description: Run the full static analysis suite — ruff lint, ruff format check, pyright type check, auth analysis, license headers. Use before committing or to verify code quality after changes.
---

Run the full quality check pipeline from the project root:

```bash
just check
```

This runs in order: license header check → ruff lint → ruff format check → pyright type check → auth static analysis → auth runtime analysis.

If any step fails, report the specific errors and their locations. Fix all issues before marking the task done. After `just check` passes, run `just test` to confirm the test suite is also green.
