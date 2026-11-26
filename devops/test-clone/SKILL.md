---
name: "test-clone"
description: "Test the orchestrator library by deploying it into a target Go repository and running the test plan. Failures indicate bugs in the orchestrator code, "
---

# test-clone command

Apply this command workflow. Treat any text after its invocation as the command input.

# Command: Test Clone

Test the orchestrator library by deploying it into a target Go repository and running the test plan. Failures indicate bugs in the orchestrator code, which get fixed in this repository.

**Scope.** Run this from inside the orchestrator repository itself — the one that ships `test-plan.yaml` at its root and `pkg/orchestrator/` in its tree. It patches orchestrator source when a test fails, so it does nothing useful anywhere else.

## Arguments

$ARGUMENTS is a Go module reference in `module@version` format, or a local directory path.

Examples:
- `/test-clone github.com/<owner>/<module>@v0.20260214.1` — any Go module you can fetch
- `/test-clone /path/to/local/repo`

## Workflow

### 1. Read the test plan

Read `test-plan.yaml` from the orchestrator repo root. Parse preconditions and test cases.

### 2. Scaffold the target

```bash
ORCH_ROOT="$(pwd)"
```

If the argument contains `@`, it is a module@version. One command downloads, copies, git-initializes, and scaffolds:

```bash
REPO_DIR=$(mage scaffold:push "module@version")
```

If the argument is a local path, scaffold it directly:

```bash
REPO_DIR="$1"
mage scaffold:push "$REPO_DIR"
```

The scaffold copies `orchestrator.go` into magefiles/, detects project structure, generates `configuration.yaml`, wires `go.mod` with a replace directive, and verifies `mage -l`.

If scaffold fails, read the error and fix `$ORCH_ROOT/pkg/orchestrator/scaffold.go` before retrying.

Record the orchestrator repo state before running tests so you can verify it was not accidentally modified:

```bash
cd "$ORCH_ROOT"
ORCH_HASH_BEFORE=$(git rev-parse HEAD)
ORCH_DIRTY_BEFORE=$(git status --porcelain)
```

### 3. Verify preconditions

- On main branch with clean working tree
- `mage` available: `which mage`
- `configuration.yaml` present (created by scaffold)

### 4. Run test cases

Execute each test case from `test-plan.yaml` in order. For each:

1. Run setup commands in `$REPO_DIR`
2. Run the command
3. Check expected exit code
4. Verify expected state (directory existence, branch names, file contents, stdout)
5. Run `mage reset` between tests for clean state

Track results:

| # | Test name | Result | Notes |
|---|-----------|--------|-------|
| 1 | ...       | PASS/FAIL | ... |

### 5. Fix failures

Bugs are in the orchestrator library, not the target project.

1. Read the error output
2. Identify root cause in `$ORCH_ROOT/pkg/orchestrator/`
3. Fix the orchestrator code in `$ORCH_ROOT`
4. The replace directive picks up the fix immediately
5. Re-run the failing test in `$REPO_DIR`
6. Commit the fix: `cd "$ORCH_ROOT" && git add -A && git commit -m "Fix: <description>"`

If a fix breaks other tests, revert. After 3 attempts on a single test, mark it as unfixable and continue.

If the failure is a setup issue (not an orchestrator bug), fix it in `$REPO_DIR` and note it separately.

### 6. Full regression pass

After fixing failures, re-run ALL test cases. Repeat until clean.

### 7. Verify orchestrator repo is unchanged

After all tests pass, verify that the orchestrator repo was not accidentally modified by the test run:

```bash
cd "$ORCH_ROOT"
ORCH_HASH_AFTER=$(git rev-parse HEAD)
ORCH_DIRTY_AFTER=$(git status --porcelain)
```

Compare `ORCH_HASH_BEFORE` with `ORCH_HASH_AFTER` and `ORCH_DIRTY_BEFORE` with `ORCH_DIRTY_AFTER`. If the repo has new uncommitted changes or new commits that are not intentional fixes, report the unexpected modifications as a test failure.

Intentional fixes committed during step 5 will change the HEAD hash. That is expected. Untracked files, modified go.mod/go.sum, or changed configuration.yaml in the orchestrator repo are not expected and indicate a bug.

### 8. Report and clean up

Summarize:

1. Target module and version tested
2. Total test cases: run / passed / failed / skipped
3. Fixes applied to the orchestrator
4. Skipped tests (unfixable)
5. `mage stats` output from `$ORCH_ROOT`, where that target exists

```bash
rm -rf "$(dirname "$REPO_DIR")"
```

## Rules

- Orchestrator fixes go into THIS repo (`$ORCH_ROOT`). Commit them here.
- Target workspace (`$REPO_DIR`) is ephemeral.
- Do not push any changes. Everything is local.
