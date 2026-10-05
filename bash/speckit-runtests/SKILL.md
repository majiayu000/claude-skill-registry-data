---
name: "speckit-runtests"
description: "Run the shell-scripted integration tests for the currently active feature spec. Executes tc-*.sh scripts via run-all.sh and reports results. Run after /speckit-scripttest."
argument-hint: "Optional TC filter or flags — e.g. 'tc-010 tc-011' to run specific cases, or leave blank to run all"
compatibility: "Requires spec-kit project structure with .specify/ directory and spec-integration-tests/run-all.sh (run /speckit-scripttest first)"
metadata:
  author: "aeai-project"
user-invocable: true
disable-model-invocation: false
---

## Purpose

`speckit-runtests` runs the Bash test scripts for a single feature spec. It finds the active feature's `spec-integration-tests/` directory, ensures prerequisites are met, executes `run-all.sh` (or a filtered subset of `tc-*.sh` scripts), and presents a clean pass/fail summary.

---

## User Input

```text
$ARGUMENTS
```

- If empty: run all `tc-*.sh` scripts via `run-all.sh`
- If one or more TC names: e.g. `tc-010 tc-011` — pass them as arguments to `run-all.sh`
- If a plain number: e.g. `10` — expand to `tc-010`
- If `--list`: print the available TC scripts and their first-line description, then stop without running

---

## Execution Steps

### Step 1 — Locate the feature

Run `.specify/scripts/bash/check-prerequisites.sh --json` from repo root and parse `FEATURE_DIR`.

Set `SCRIPTS_DIR="$FEATURE_DIR/spec-integration-tests"`.

If `SCRIPTS_DIR` does not exist or contains no `tc-*.sh` files:
- Stop and tell the user: "No test scripts found at `{SCRIPTS_DIR}`. Run `/speckit-scripttest` to generate them."

If `run-all.sh` does not exist in `SCRIPTS_DIR`:
- Stop and tell the user: "`run-all.sh` is missing from `{SCRIPTS_DIR}`. Run `/speckit-scripttest` to regenerate it."

### Step 2 — Handle `--list`

If `$ARGUMENTS` is `--list`:

```bash
echo "Available test scripts in {SCRIPTS_DIR}:"
for f in {SCRIPTS_DIR}/tc-*.sh; do
  head -2 "$f" | grep "^#" | tail -1
done
```

Print the list and stop.

### Step 3 — Check environment prerequisites

Warn (do not block) if any of these are unset or empty in the environment:

| Variable | Source | Impact if missing |
|---|---|---|
| `PP` | `config.env` | All HTTP tests will fail |
| `IDENTITY` | `config.env` | Auth tests will fail |
| `PG_CONN` | `config.env` | DB assertion tests will fail |

Check whether required tools are available:

```bash
command -v curl  || echo "WARN: curl not found"
command -v jq    || echo "WARN: jq not found — JSON assertions will fail"
command -v psql  || echo "WARN: psql not found — DB tests will fail"
```

Print a one-line env summary before running:
```
PP=https://localhost:7234  IDENTITY=https://localhost:5243  TOKEN=[set/unset]
```

### Step 4 — Run the tests

Build the command from `$ARGUMENTS`:

```bash
# No filter — run everything
bash "{SCRIPTS_DIR}/run-all.sh"

# With TC filter
bash "{SCRIPTS_DIR}/run-all.sh" tc-010 tc-011
```

Execute using `run_in_terminal`. Stream output to the user as it arrives.

### Step 5 — Parse and display results

After the run completes, parse the `TEST SUMMARY` block from the output:

- Extract `Passed`, `Failed`, `Skipped`, `Total` counts
- List every `FAIL` line with the TC name
- List every `SKIP` / `????` line

Display as a formatted table:

```
┌─────────────────────────────────────────────────────┐
│  speckit-runtests — {feature folder name}           │
├──────────┬──────────┬──────────┬──────────┬─────────┤
│  PASS    │  FAIL    │  SKIP    │  TOTAL   │  STATUS │
│  {N}     │  {N}     │  {N}     │  {N}     │  ✓/✗   │
└──────────┴──────────┴──────────┴──────────┴─────────┘
```

If `FAIL > 0`, list the failing TCs:
```
Failures:
  ✗ tc-022.sh — TC-022: Spend below balance succeeds
    Last output line: FAIL: net_balance expected=0 actual=80
```

If all pass: print "All {N} test cases passed."

### Step 6 — Exit guidance

- On failure: suggest "Run `/speckit-runtests tc-022` to re-run a single failing case."
- If many SKIPs: suggest "Some tests require manual verification — check MANUAL: comments in the scripts."
