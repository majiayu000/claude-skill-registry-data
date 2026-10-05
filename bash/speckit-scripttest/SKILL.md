---
name: "speckit-scripttest"
description: "Generate shell scripts that automate the test cases in a feature's test plan markdown files. Spawns one sub-agent per independent markdown file for parallelism."
argument-hint: "Optional markdown file name or TC filter (e.g. 'api', 'TC-010', or leave blank to process all test plan files)"
compatibility: "Requires spec-kit project structure with .specify/ directory and a test-plan.md (run /speckit-testplan first)"
metadata:
  author: "aeai-project"
user-invocable: true
disable-model-invocation: false
---

## Purpose

`speckit-scripttest` reads the feature's test plan markdown file(s) and generates one `tc-{NNN}.sh` Bash script per test case, plus an updated `run-all.sh` orchestrator. Scripts are written to `FEATURE_DIR/spec-integration-tests/`.

Every generated test script must verify its prerequisite data before running the main test body. If a test depends on seeded rows, lookup-table entries, auth tokens, or other preloaded fixtures, the script must check for them explicitly and skip or fail fast when they are missing.

Sub-agents are spawned in parallel — one per independent markdown source file — so large test plans generate scripts without blocking the main conversation.

---

## User Input

```text
$ARGUMENTS
```

If a file name or TC filter is provided, process only the matching markdown file(s) or test cases. If empty, process all test plan markdown files.

---

## Execution Steps

### Step 1 — Locate the feature

Run `.specify/scripts/bash/check-prerequisites.sh --json` from repo root and parse `FEATURE_DIR` and `AVAILABLE_DOCS`. All paths must be absolute.

### Step 2 — Discover markdown test sources

Collect the set of **source markdown files** that contain test cases:

1. `FEATURE_DIR/test-plan.md` — primary source (if exists)
2. Any `FEATURE_DIR/checklists/*.md` file whose content contains `### TC-` headings
3. Any other `FEATURE_DIR/*.md` file whose content contains `### TC-` headings

If no TC-### headings are found anywhere, stop and tell the user: "No test cases found. Run `/speckit-testplan` first to generate test-plan.md."

Apply the `$ARGUMENTS` filter: if non-empty, restrict to files whose basename matches the argument (case-insensitive), or to TC numbers matching the filter.

Read `FEATURE_DIR/spec-integration-tests/config.env` if it exists — use its variable names (`$PP`, `$IDENTITY`, `$PG_CONN`, `$TOKEN`, `$BOB_TOKEN`, `$ALICE_ID`) in generated scripts. If it does not exist, use those same defaults and note that the user should create `config.env`.

### Step 3 — Spawn sub-agents (one per markdown file)

For **each markdown file** identified in Step 2, launch a parallel sub-agent with this prompt:

> You are generating Bash test scripts for a feature test plan. Your inputs are:
> - Source markdown file: `{absolute path to markdown file}`
> - Scripts output directory: `{FEATURE_DIR}/spec-integration-tests/`
> - config.env path: `{FEATURE_DIR}/spec-integration-tests/config.env`
>
> Instructions:
> 1. Read the markdown file.
> 2. Find every `### TC-{NNN}: {name}` heading and its content block (steps, curl commands, expected outcomes) up to the next heading.
> 3. For each TC, generate a file named `tc-{NNN}.sh` in the scripts output directory using the script template below.
> 4. Do NOT overwrite an existing script unless its TC heading or Expected outcome has changed — add a `# [UPDATED]` comment on line 2 if overwriting.
> 5. Return a JSON summary: `{ "source": "{filename}", "generated": [{tc_id, script_path, status}] }`

**Script template** for each `tc-{NNN}.sh`:

```bash
#!/usr/bin/env bash
# tc-{NNN}.sh — {TC name from heading}
# Source: {markdown file basename}, {CHK ref if present}
source "$(dirname "$0")/config.env"

echo "=== TC-{NNN}: {TC name} ==="

# ── Setup ────────────────────────────────────────────────────────────────────
# Verify prerequisite data before exercising the scenario.
# {Any prerequisite noted in the TC — e.g. "Requires TOKEN to be set", "Requires seeded lookup entries", "Requires existing wallet row"}

{Executable prerequisite checks translated from the TC and surrounding markdown.
 Rules:
 - Verify required env vars, auth tokens, seeded reference data, and fixture rows before the main test body.
 - Use curl, psql, jq, or other shell checks to confirm the prerequisite data exists and is readable.
 - If a prerequisite is missing, echo "SKIP: prerequisite data missing" and exit 0 before any assertions.
 - If the prerequisite cannot be checked automatically, emit a MANUAL comment only after the prerequisite check block.}

PASS=true

# ── Test body ────────────────────────────────────────────────────────────────
{Translated steps: each Step becomes a shell command or comment.
 Rules:
 - curl commands from the markdown → use verbatim, replacing literal URLs with $PP/$IDENTITY
 - psql commands → use $PG_CONN
 - "Expected: HTTP 200" → capture HTTP status with curl -w "%{http_code}" and assert
 - "Expected: JSON field X = Y" → pipe to jq -r '.field' and compare with [ "$ACTUAL" = "Y" ]
 - "Expected: COUNT = N" → compare psql output
 - For each assertion that fails → echo "FAIL: {what was expected} actual=${ACTUAL}"; PASS=false
 - If no curl/psql can be derived (purely manual/visual step) → emit a comment:
     # MANUAL: {description of what to check} }

# ── Result ───────────────────────────────────────────────────────────────────
if [ "$PASS" = "true" ]; then
  echo "PASS: TC-{NNN} {TC name}"
else
  echo "FAIL: TC-{NNN} {TC name}"
fi
```

**Additional per-script rules**:
- Every automated TC must include at least one prerequisite-data check before any scenario action.
- Auth-required TCs: add `source "$(dirname "$0")/get-token.sh"` guard — check `$TOKEN` is non-empty, skip with `echo "SKIP: TOKEN not set"` if missing
- TCs that reference Bob's token: also source `get-bob-token.sh` check
- TCs that reference Alice's sub claim: check `$ALICE_ID` is non-empty
- Concurrent/race-condition TCs (two simultaneous requests): use `&` + `wait` to launch both in background and capture both exit codes
- DB-only TCs (psql, no HTTP): skip the curl block entirely

### Step 4 — Collect sub-agent results

Wait for all sub-agents to complete. For each result JSON:
- Log any TC that failed to generate (missing steps, ambiguous expected outcome)
- Collect the full list of `{tc_id, script_path, status}` entries

### Step 5 — Generate or update run-all.sh

Write `FEATURE_DIR/spec-integration-tests/run-all.sh`:

```bash
#!/usr/bin/env bash
# run-all.sh — Run all TC-* scripts in order and print a summary
#
# USAGE:
#   ./run-all.sh                      # run every test case
#   ./run-all.sh tc-010 tc-011        # run specific test cases by name

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Determine which scripts to run
if [[ $# -gt 0 ]]; then
  SCRIPTS=()
  for arg in "$@"; do
    SCRIPTS+=("${arg%.sh}.sh")
  done
else
  SCRIPTS=(tc-*.sh)
fi

PASS=0
FAIL=0
SKIP=0
RESULTS=()

run_script() {
  local script="$1"
  if [[ ! -f "$SCRIPT_DIR/$script" ]]; then
    echo "⚠️  $script not found — skipping"
    RESULTS+=("SKIP  $script")
    ((SKIP++)) || true
    return
  fi

  echo ""
  echo "────────────────────────────────────────"
  local output
  output=$(bash "$SCRIPT_DIR/$script" 2>&1)
  local exit_code=$?
  echo "$output"

  if echo "$output" | grep -q "^PASS"; then
    RESULTS+=("PASS  $script")
    ((PASS++)) || true
  elif echo "$output" | grep -q "^FAIL"; then
    RESULTS+=("FAIL  $script")
    ((FAIL++)) || true
  else
    RESULTS+=("????  $script  (no PASS/FAIL printed)")
    ((SKIP++)) || true
  fi
}

for script in "${SCRIPTS[@]}"; do
  run_script "$script"
done

echo ""
echo "════════════════════════════════════════"
echo "  Test Summary"
echo "════════════════════════════════════════"
for r in "${RESULTS[@]}"; do echo "  $r"; done
echo ""
echo "  PASS: $PASS   FAIL: $FAIL   SKIP/MANUAL: $SKIP"
echo "════════════════════════════════════════"

[[ $FAIL -eq 0 ]]
```

If `run-all.sh` already exists, overwrite it — it is always regenerated from the current TC set. Set `chmod +x` on all generated scripts.

### Step 6 — Summary report

Print:

```
Scripts generated in FEATURE_DIR/spec-integration-tests/

| Source File     | TC Cases | Generated | Skipped (manual) |
|-----------------|----------|-----------|------------------|
| test-plan.md    | 32       | 28        | 4                |
| …               | …        | …         | …                |
| **Total**       | **N**    | **M**     | **K**            |

Skipped (manual-only steps, no automatable assertions):
  - tc-005.sh: TC-005 "Visually verify dashboard layout" — no HTTP/DB assertion
  …

Run: cd FEATURE_DIR/scripts && ./run-all.sh
```

List any TCs that could only be partially automated (MANUAL comments in the script) so the user knows which ones still need human eyes.
