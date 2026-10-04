---
name: verify
description: Run full quality gate suite before committing or creating a PR
triggers:
  - verify
  - quality check
  - run tests
  - before commit
  - before PR
---

# Verify

Run all quality gates. Do not commit or PR until all pass.

## Gates (run in order)

```bash
npm run lint         # or: ruff check . / golangci-lint run / cargo clippy
npm run type-check   # or: tsc --noEmit / mypy . / go build ./...
npm test             # or: pytest / go test ./... / cargo test
npm run build        # confirm no build errors
```

## Rules

- Fix lint errors before moving on — don't suppress
- If tests fail, determine root cause before changing the test
- Coverage below threshold = a problem to fix, not a number to ignore
- Security: `npm audit --audit-level=high` for any dependency changes

## Output

Report status for each gate:
```text
✓ lint        — passed
✓ type-check  — passed
✓ tests       — 142 passed, 87% coverage
✓ build       — succeeded
```
