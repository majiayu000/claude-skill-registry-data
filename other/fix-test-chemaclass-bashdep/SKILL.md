---
name: fix-test
description: Debug and fix failing bashdep tests systematically
allowed-tools: Read, Edit, Bash, Grep, Glob
---

# Fix Test

Systematically debug and fix failing test(s) in `tests/unit/bashdep_test.sh`.

## Workflow

### 1. Identify Failures

```bash
make test 2>&1
# Or, narrower:
lib/bashunit tests --filter <test_name>
```

Parse: which test functions fail, what assertions, what the actual vs
expected was.

### 2. Categorize Each Failure

- **Test bug** - wrong expected value, missing `set_up` reset, leaky state
- **Implementation bug** - `bashdep` doesn't match expected behavior
- **Snapshot drift** - output legitimately changed; snapshot needs updating
- **Environment issue** - missing `$TEST_DIR`, hardcoded path that doesn't
  exist, missing fixture
- **Bash 3.2 compat regression** - code uses a Bash 4+ feature
- **Mode-flag leak** - `BASHDEP_*` global from a prior test wasn't reset

### 3. Fix

- **Test bug:** correct the assertion, fixture, or `set_up`
- **Implementation bug:** minimal fix in `bashdep`, follow TDD
  (regression test must already exist or be added now)
- **Snapshot drift:** confirm the new output is correct, then
  `lib/bashunit --update-snapshots tests/`. Review the diff before committing
- **Environment:** fix the fixture path; never hardcode `/tmp/...` outside
  snapshot tests
- **Bash 3.2 compat:** swap to a 3.2-safe construct
  (see `.claude/rules/bash-style.md`)
- **Mode-flag leak:** add the reset to `set_up`, or scope the change to
  the single test

### 4. Verify

```bash
lib/bashunit tests --filter <test_name>   # Specific test
make test                                  # Full suite
make sa && make lint                       # Static checks
```

### 5. Prevent Regression

- Document the root cause in the commit message body when non-obvious
- Add an edge-case test if the failure exposed a missing case
- If the bug crossed mode-flag boundaries, add tests for each mode
  (`dry-run`, `silent`, `verbose`, `force`)

## Debugging Tips

- Use `--filter "test_name"` to run a single test in isolation
- Add `printf 'DEBUG: %s\n' "$var" >&2` temporarily - strip before commit
- If a test passes alone but fails in the suite, suspect a leaked
  `BASHDEP_*` global; reset in `set_up`
- For snapshot mismatches, diff the snapshot file vs current stdout
  before regenerating
