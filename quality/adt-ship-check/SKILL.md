---
name: ship-check
description: Verify work before committing, pushing, or requesting review
triggers:
  - check before ship
  - pre-commit check
  - verify before push
  - ready to commit
  - quality gate
---

# Ship Check

Run the repo's own verification commands and report pass/fail with evidence — before any git operation.

## Steps

1. **Inspect changes** — review staged and unstaged files, diff summary
2. **Discover verification commands** — look for lint, typecheck, test, build scripts
3. **Run each command** — capture exact output and exit codes
4. **Report results** — pass/fail per command with evidence

## Output

```text
Files changed: <count>
Lint:          PASS | FAIL
Typecheck:     PASS | FAIL | N/A
Tests:         PASS | FAIL | N/A
Build:         PASS | FAIL | N/A
Blockers:      <list or none>
```

## Rules

- Never invent tests or build commands that don't exist in the repo
- Never mark work ready when verification was skipped
- Refuse to claim success without command output evidence
- Report blockers explicitly instead of hiding failures
