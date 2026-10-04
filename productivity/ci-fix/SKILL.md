---
name: ci-fix
description: Diagnose and fix CI failures without leaving your editor.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: all
  audience: developers
  workflow: automation
  since: "2026-02-24"
---

## What I do

I help you diagnose and fix failing CI runs without switching context to the GitHub Actions UI:

1. **Auto-Fetch** — detect the latest failed run on your current branch via `gh run view --log-failed`, or target a specific run by ID
2. **Classify** — identify the failure type: lint/format, pre-commit, lock file out of sync, test assertion, or environment issue
3. **Auto-Fix (high confidence)** — for lint, formatting, pre-commit, and lock file failures: apply the fix and stage the corrected files automatically
4. **Diagnose (lower confidence)** — for test logic and environment failures: explain the root cause and propose a concrete fix with rationale
5. **Summarise** — output a structured diagnosis summary so you know exactly what happened and what was done

Supporting files in this skill:
- `assets/diagnosis-output.template` — structured summary rendered at the end of every invocation

## When to use me

Use when you want to:

- Fix a failing CI run without opening the GitHub Actions UI
- Auto-fix lint, formatting, pre-commit, or lock file CI failures in one command
- Understand why a test is failing based on CI log output
- Get a proposed fix with rationale for test failures — not just "what" but "why"
- Investigate a specific CI run by its run ID

## Use Instead [if available]

- Use `ruff` when you want a dedicated, local Python lint/format cleanup flow outside CI triage.
- Use `uv` when dependency/lock operations are the primary task in a uv-managed project.
- Use `poetry` when dependency/lock operations are the primary task in a Poetry-managed project.

## Example usage

"Fix my failing CI"
"Why is CI failing on my branch?"
"Diagnose the test failure in CI"
"/ci-fix"
"/ci-fix 9823456"

---

## Workflow

### Step 0: Auto-Fetch CI Run

Two modes depending on invocation:

**Mode A — Auto-detect (no argument given)**

Run the following to find the latest failed run on the current branch:

```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
gh run list --branch "$BRANCH" --status failure --limit 1 --json databaseId,workflowName,conclusion,createdAt
```

Extract the `databaseId` from the JSON result, then fetch the failed log output:

```bash
gh run view <databaseId> --log-failed
```

**Mode B — Specific run ID (`/ci-fix <run-id>`)**

If a run ID is provided as an argument, skip auto-detection and fetch directly:

```bash
gh run view <run-id> --log-failed
```

If the run ID is invalid or inaccessible, report clearly:
> "Run ID `<run-id>` could not be fetched. Verify the ID is correct and that `gh auth status` shows an authenticated session."

**Fallback — `gh` unavailable or unauthenticated**

If `gh` is not installed or `gh auth status` fails:

1. Inform the developer: "The `gh` CLI is not available or not authenticated. Run `gh auth status` to diagnose."
2. Ask: "Please paste the relevant CI log section from the GitHub Actions UI (the failed step output)."
3. Continue from Step 1 with the pasted content — the rest of the workflow is identical.

---

### Step 1: Classify Failure Type

Scan the log output for these patterns to identify the failure category:

**Lint violations** — look for tool name + violation codes:
- `ruff`: lines containing `E[0-9]{3}`, `F[0-9]{3}`, `W[0-9]{3}` codes (e.g., `E501 line too long`, `F401 imported but unused`)
- `flake8`: same code pattern — **note: flake8 is read-only, cannot auto-fix; treat as propose-only**
- `eslint`: lines with `error` or `warning` + rule name (e.g., `no-unused-vars`)

**Formatting failures** — look for "would reformat" or diff output:
- `black`: `would reformat <file>`
- `ruff format`: `Would reformat: <file>`
- `prettier`: diff output from `prettier --check`

**Pre-commit hook failures** — look for:
- Lines containing `hook id:` followed by `Failed`
- Pre-commit output with `[ERROR]` markers or exit code annotations

**Lock file out of sync** — look for these exact log signals:

| Log signal | Package manager |
|-----------|----------------|
| `uv.lock is not up to date` | uv |
| `poetry.lock is not consistent` | poetry |
| `package-lock.json` mismatch or `npm ci` failure mentioning lock file | npm |
| `yarn.lock` out of date | yarn |
| `Cargo.lock needs to be updated` | cargo |
| `go.sum` mismatch or `go mod tidy` required | go modules |

**Test assertion failures** — look for test runner output:
- `pytest`: `FAILED`, `AssertionError`, lines starting with `E   assert`
- `jest`: `FAIL`, `● Test name`, `Expected:` / `Received:`
- `cargo test`: `thread '...' panicked at`
- `go test`: `--- FAIL:`, lines starting with `FAIL\t`

**Environment / infrastructure** — look for:
- Missing secret: `Secret 'FOO' not found`, `undefined environment variable`
- Runner error: process exit without code output, infrastructure-level messages
- Network: `connection refused`, `timeout`, `Could not resolve host`

**Routing**:
- Lint (ruff, eslint) / formatting / pre-commit / lock file → **Step 2 (auto-fix)**
- Lint (flake8) / test assertion / environment → **Step 3 (diagnose)**

---

### Step 2: High-Confidence Auto-Fix

Apply the fix determined in Step 1 and stage the result. The rule: **re-run the tool that reported the failure**.

**Lint violations (ruff, eslint)**:
```bash
ruff check --fix .        # ruff — applies all auto-fixable violations
eslint --fix <file>       # eslint — applies auto-fixable rules
```
Note: `flake8` has no `--fix` flag — route flake8 failures to Step 3 instead.

**Formatting (black, ruff format, prettier)**:
```bash
black .                   # black
ruff format .             # ruff format
npx prettier --write .    # prettier
```

**Pre-commit**:
```bash
pre-commit run --all-files
```

**Lock file** — use the package manager identified in Step 1:
```bash
uv lock                              # uv

poetry lock --no-update              # poetry 1.x (≥1.2) — regenerates without upgrading
# If --no-update is not recognised (poetry 2.x, flag removed):
poetry lock                          # poetry 2.x — safe by default; existing packages not updated

npm install                          # npm
yarn install                         # yarn
cargo update                         # cargo
go mod tidy                          # go modules
```

After the fix runs, stage only the files related to the CI fix:
```bash
git status --porcelain
git add <expected-files-from-fix>
```

Never use `git add .` in this workflow — it can stage unrelated local work.

Then proceed to **Step 4**.

---

### Step 3: Lower-Confidence Diagnosis

**For test assertion failures**:

1. Extract from the log:
   - **Test name**: the failing test identifier (e.g., `test_checkout_total`, `● Cart › calculates discount`)
   - **Failure message**: the exact assertion error or exception (quote directly from the log)
   - **File and line number** (if shown in the output)

2. Infer the root cause — what does the assertion tell you about the mismatch? Consider:
   - A return value that changed (did a recent refactor change behaviour?)
   - A missing or incorrect fixture or mock
   - A data dependency that is now different
   - A timing or ordering issue

3. Compose a proposed fix:
   - State **what** to change (specific file, function, line if determinable)
   - Explain **why** this resolves the root cause — not just describes the symptom

4. If multiple tests fail: group related failures (same module or same root cause) and address the primary root cause first.

5. Populate the diagnosis summary with `action: proposed`.

Example output:
```
Test failed: test_checkout_total
Failure: AssertionError: expected 95.0, got 100.0

Root cause: The discount logic in checkout.apply_discount() no longer applies the
5% member discount — likely removed in the recent refactor of the pricing module.

Proposed fix: In src/checkout.py line 42, restore the discount multiplier:
  total *= (1 - discount_rate)
This resolves the assertion because the expected value (95.0) assumes 5% is applied.
```

**For environment / infrastructure failures**:

1. Identify the category:
   - **Missing secret/env var**: name the missing variable; direct the developer to configure it in GitHub repo → Settings → Secrets and variables → Actions
   - **Runner/infrastructure error**: flag as potentially transient; suggest re-running the CI job first before investigating further
   - **Network timeout**: note that the external service may be temporarily unavailable; suggest re-running or checking service status

2. State clearly: "This failure cannot be resolved by a code change."

3. Suggest the next action — who to contact or what to check (DevOps, repository admin, re-run the job).

4. Populate the diagnosis summary with `action: explained`.

---

### Step 4: Output Diagnosis Summary

Fill and render the `diagnosis-output.template`:

```
## CI Diagnosis Summary

**Workflow**: <workflow name>
**Run ID**:   <run id>
**Branch**:   <branch name>

**Failure type**: <lint | format | pre-commit | lock-file | test | environment>

**Root cause**:
> <quoted excerpt from the CI log that identifies the failure>

**Action**: <fixed-and-staged | proposed | explained>

**What was done / proposed**:
<description of the fix applied or proposed>

**Why this resolves it**:
<rationale — why the fix addresses the root cause, not just what was changed>

**Next step**:
<review staged changes with `git diff --staged` then commit>
— OR —
<apply proposed fix, then push>
— OR —
<contact [person/team] / re-run CI job>
```

If files were staged automatically, remind: "Run `git diff --staged` to review the changes before committing."

---

### Delegation notes

- Keep this skill as the CI triage orchestrator (fetch logs, classify, route, summarize).
- For deep tool-specific remediation details, defer to specialized skills when available:
  - Python lint/format policy and commands: `ruff`
  - uv lock and environment behavior: `uv`
  - Poetry lock and environment behavior: `poetry`

---

## Tips for Success

- **Always review staged changes** — run `git diff --staged` before committing any auto-applied fix; confirm only the expected files changed
- **Check `gh auth status` first** — if `gh` isn't authenticated, the skill falls back to manual log paste; authenticating once eliminates this friction
- **Flake8 can't auto-fix** — it's a read-only linter; consider switching to `ruff` for auto-fixable lint, or fix violations manually
- **Lock file diffs need scrutiny** — after auto-regenerating a lock file (especially `package-lock.json`), scan the diff for unexpected major version bumps in transitive dependencies before committing
- **Re-run the job first for infra failures** — many runner failures are transient; try a GitHub Actions re-run before investigating further
- **Paste logs as fallback** — if `gh` is unavailable, copy the failed step output from the GitHub Actions UI and paste it; the diagnosis workflow is identical
- **One root cause at a time** — if multiple unrelated failures exist in the same run, fix and push the highest-confidence one first, then re-run CI before addressing the next
