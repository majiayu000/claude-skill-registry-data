---
name: "run-full-suite"
description: "Discover and run all speckit shell test suites across every feature spec in the repository, then print a consolidated cross-spec summary."
argument-hint: "Optional filter — spec folder name or number (e.g. '004', 'token'), '--list' to preview without running, or '--fail-fast' to stop after first spec failure"
metadata:
  author: "aeai-project"
user-invocable: true
disable-model-invocation: false
---

## Purpose

`run-full-suite` scans every `specs/*/spec-integration-tests/` directory for a `run-all.sh` and/or `tc-*.sh` files, runs each suite in sequence, and produces a single consolidated report across all specs. This is the project-wide integration test runner equivalent of `dotnet test` for the speckit shell test layer.

---

## User Input

```text
$ARGUMENTS
```

- Empty: run every discovered spec suite
- Spec filter (e.g. `004`, `token`, `catalog`): run only suites whose parent folder name contains the filter (case-insensitive)
- `--list`: print all discovered suites with TC counts, do not run
- `--fail-fast`: stop after the first spec suite that has any FAIL result

---

## Execution Steps

### Step 1 — Discover all spec suites

From the repo root, find all feature scripts directories:

```bash
find specs -maxdepth 3 -name "run-all.sh" | sort
```

For each found `run-all.sh`, derive:
- `SPEC_DIR` — the parent `specs/{NNN}-{name}/` folder
- `SPEC_ID` — the `{NNN}-{name}` folder name
- `TC_COUNT` — number of `tc-*.sh` files in the same `spec-integration-tests/` directory
- `HAS_CONFIG` — whether `config.env` exists in the scripts directory

If no `run-all.sh` files are found anywhere under `specs/`, stop and tell the user:
"No runnable spec suites found. Run `/speckit-scripttest` on one or more features first."

Apply the `$ARGUMENTS` filter: keep only suites whose `SPEC_ID` contains the filter string (case-insensitive). If the filter matches nothing, tell the user which suites exist and stop.

### Step 2 — Handle `--list`

If `$ARGUMENTS` contains `--list`:

Print a discovery table and stop without running:

```
Discovered speckit test suites:

  #   Spec                           TC Scripts   config.env   Runnable
  ─── ────────────────────────────── ──────────── ──────────── ────────
  1   004-token-wallet-service        27           ✓            ✓
  2   005-token-adjusted-checkout      0           ✗            ✗ (no tc-*.sh yet)
  …

Run '/run-full-suite' to execute all runnable suites.
```

### Step 3 — Check shared prerequisites

Before running any suite, verify tools are available:

```bash
command -v curl  || echo "WARN: curl not found — HTTP tests will fail across all suites"
command -v jq    || echo "WARN: jq not found — JSON assertions will fail across all suites"
command -v psql  || echo "WARN: psql not found — DB tests will fail across all suites"
command -v docker || echo "WARN: docker not found — detect-ports.sh (env var refresh) will not be able to derive PG_CONN"
```

Print a one-line warning for any missing tool. Do not block execution — scripts will report their own FAILs.

### Step 4 — Run each suite

For each suite in discovery order (filtered if `$ARGUMENTS` specified):

1. Print a suite header:
   ```
   ════════════════════════════════════════════════════════
   Suite: 004-token-wallet-service  (27 scripts)
   ════════════════════════════════════════════════════════
   ```

2. **Refresh env vars before running.** If `specs/{SPEC_ID}/spec-integration-tests/detect-ports.sh` exists, run it with `--update` first so `config.env` reflects the current AppHost run's ports and connection strings (Aspire reassigns ports/passwords on every restart, so a stale `config.env` will cause spurious failures):
   ```bash
  bash "specs/{SPEC_ID}/spec-integration-tests/detect-ports.sh" --update
   ```
   If the script reports it cannot detect a running project (e.g. the AppHost isn't running), surface that warning to the user before continuing — the suite will likely fail without it.

3. Run the suite using `run_in_terminal`:
   ```bash
  bash "specs/{SPEC_ID}/spec-integration-tests/run-all.sh"
   ```

4. Parse stdout for the `TEST SUMMARY` block — extract `Passed`, `Failed`, `Skipped`, `Total`.

5. Store results as `{SPEC_ID, passed, failed, skipped, total, duration_seconds}`.

6. If `--fail-fast` is set and `failed > 0`: print the failure details for this suite, then stop and print the partial cross-spec summary (Step 5) with a note that execution was halted early.

7. Continue to the next suite regardless of failures (unless `--fail-fast`).

### Step 5 — Cross-spec summary report

After all suites have run, print the consolidated report:

```
════════════════════════════════════════════════════════════════════
  FULL SUITE REPORT — {ISO datetime}
════════════════════════════════════════════════════════════════════

  Spec                           PASS   FAIL   SKIP   TOTAL   Status
  ─────────────────────────────  ─────  ─────  ─────  ─────   ──────
  004-token-wallet-service        25     2      0      27      ✗ FAIL
  005-token-adjusted-checkout      —     —      —       —      ○ NO SCRIPTS
  …

  ─────────────────────────────────────────────────────────────────
  TOTALS                          {N}   {N}    {N}    {N}
  Overall status: {PASS / FAIL}
════════════════════════════════════════════════════════════════════
```

**Status key**:
- `✓ PASS` — all TCs in this suite passed
- `✗ FAIL` — one or more TCs failed (list them below the table)
- `○ NO SCRIPTS` — directory exists but has no `tc-*.sh` yet
- `⚠ SKIPPED` — suite was excluded by the filter argument

**Failure detail block** (printed below table if any failures):

```
Failures:
  004-token-wallet-service
    ✗ tc-022.sh — FAIL: net_balance expected=0 actual=80
    ✗ tc-043.sh — FAIL: HTTP 409 expected, got 200
```

### Step 6 — Exit guidance

- If all pass: "All {N} test cases passed across {M} spec suites."
- If failures exist:
  - "Run `/speckit-runtests` to re-run a single spec's suite."
  - "Run `/run-full-suite 004` to isolate a specific spec."
- If any suites show `NO SCRIPTS`: "Run `/speckit-scripttest` on those features to generate scripts."
- Exit code: surface the failed count — if any `FAIL > 0`, treat the overall run as failed (use `exit 1` semantics when running in terminal).
