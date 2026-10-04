---
name: skip-tdd
description: >
  Temporarily bypass the TDD commit gate. Use for documentation changes,
  CI/CD config, dependency updates, or hotfixes. Logs the reason for
  accountability. Bypass auto-clears after the next commit.
  Triggers on: skip tdd, bypass tests, no-tdd.
---

## Skip TDD

Creates a `.tdd-skip` file so the TDD gate hook allows the next commit without test files.

### Usage
`/skip-tdd <reason>`

### Execute
Run:
```bash
REASON="$ARGUMENTS"
[ -z "$REASON" ] || [ "$REASON" = "\$ARGUMENTS" ] && REASON="No reason provided"
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
printf 'TDD bypass active\nReason: %s\nBranch: %s\nTime: %s\n' \
  "$REASON" "$BRANCH" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > .tdd-skip
```

Ensure `.tdd-skip` is in `.gitignore`.

After the commit, delete `.tdd-skip` to re-enable the gate.

### Valid Reasons
- `docs-only change`
- `CI/CD config update`
- `dependency update / lockfile`
- `hotfix — tests in follow-up`
- `refactoring with existing coverage`
