---
name: test-plan-create-cases
description: Generate individual test case files from an existing test plan. Use after plan approval to produce TC specs with preconditions, steps, and expected results by category and priority.
argument-hint: "[FEATURE_SOURCE] [--output-dir PATH]"
user-invocable: true
model: claude-opus-4-6
allowedTools: Read, Write, Edit, Bash, AskUserQuestion
---

# Test Case Generator

Generate individual test case files from an existing test plan.

## Usage

```
/test-plan-create-cases [FEATURE_SOURCE] [--output-dir PATH]
```

Examples:
- `/test-plan-create-cases` (prompts for the feature directory)
- `/test-plan-create-cases mcp_catalog`
- `/test-plan-create-cases /path/to/feature_dir`
- `/test-plan-create-cases mcp_catalog --output-dir .` (contributor override)

## Runtime setup

Bootstrap before helpers. Use stdout for substitutions; stderr is diagnostics. Empty stdout is
valid for an absent `--output-dir`. Stop on nonzero exit.

```bash
bash "${CLAUDE_SKILL_DIR}/../../scripts/bootstrap.sh" --layout "${CLAUDE_SKILL_DIR}" || exit 1
```

## Inputs

If `$ARGUMENTS` is empty, set `FORCE_OUTPUT_DIR=false` and go to **Interactive fallback**.

If `$ARGUMENTS` is non-empty, parse **after** Step 0.1. Consume `--output-dir` before the positional feature source:

```bash
OUTPUT_DIR=$(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && \
  uv run python scripts/parse_skill_args.py --output-dir "$ARGUMENTS") || {
    echo "ERROR: scripts/parse_skill_args.py failed — stopping." >&2
    exit 1
}
FORCE_OUTPUT_DIR=false
if [ -n "$OUTPUT_DIR" ]; then
    FORCE_OUTPUT_DIR=true
fi
```

`--output-dir` is a contributor override. Still run marker and path validation in Steps 0.2.2–0.2.3;
it never permits package writes or Fullsend output outside `FULLSEND_TARGET_REPO_DIR`.
`FEATURE_SOURCE` is the positional argument or interactive answer; the flag's `PATH` only sets
`FORCE_OUTPUT_DIR`. No positional source → **Interactive fallback**.

### From arguments (optional)

After flags are consumed, if a remaining argument does not start with `--`, it is the feature source:
- Local directory path: `mcp_catalog` or `/path/to/mcp_catalog`
- GitHub branch: `https://github.com/org/repo/tree/test-plan/RHAISTRAT-400`
- GitHub PR: `https://github.com/org/repo/pull/5`

**Action:** Set `FEATURE_SOURCE` to that positional value and proceed to Step 0.2.

### Interactive fallback (no positional feature source)

If `$ARGUMENTS` is empty, or no positional feature source remains after flags, ask via
AskUserQuestion for a local path, GitHub branch URL, or PR URL. Capture as `FEATURE_SOURCE`
and proceed to Step 0.2.

## Process

### Step 0: Pre-flight Check

#### 0.1 Python dependencies

Install the test-plan package (makes all scripts importable):
```bash
repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
(cd "$repo_root" && uv sync --extra dev)
```

If installation fails, inform the user and do NOT proceed.

#### 0.2 Locate Feature Directory

1. **Use the shared locate-feature-dir utility** to resolve `FEATURE_SOURCE` (local path or GitHub branch/PR) into a local directory:
   ```bash
   if [ -n "${FULLSEND_TARGET_REPO_DIR:-}" ] && [[ "$FEATURE_SOURCE" == https://github.com/* ]]; then
       echo "ERROR: Fullsend case generation requires a local feature in the target workspace" >&2
       exit 1
   fi
   if [[ "$FEATURE_SOURCE" != https://github.com/* ]]; then
       FEATURE_SOURCE=$(python3 -c 'import os,sys; print(os.path.abspath(os.path.expanduser(sys.argv[1])))' "$FEATURE_SOURCE")
   fi
   result=$(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/repo.py locate-feature-dir "$FEATURE_SOURCE")
   if [ $? -ne 0 ]; then
       echo "$result"
       exit 1
   fi

   # Parse JSON output
   feature_dir=$(printf '%s\n' "$result" | jq -r '.feature_dir')
   source_type=$(printf '%s\n' "$result" | jq -r '.source_type')
   ```

2. **For local sources, validate the feature directory is self-contained** (was created by
   `/test-plan-create`, which always writes `<feature_dir>/.test-plan-output-dir.json`):
   ```bash
   if [ "$source_type" = "local" ]; then
       repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
       discover_feature_dir_script="$repo_root/scripts/discover_feature_dir.py"
       if [ "$(pwd -P)" != "$repo_root" ]; then
           discover_feature_dir_script=".odh-test-gen/scripts/discover_feature_dir.py"
       fi
       marker_result=$(uv run --project "$repo_root" python "$discover_feature_dir_script" "$feature_dir")
       if [ $? -ne 0 ]; then
           echo "$marker_result"
           exit 1
       fi
   fi
   ```

3. **Validate local paths against skill repository and Fullsend output root**:
   ```bash
   if [ "$source_type" = "local" ]; then
       if [ -n "${FULLSEND_TARGET_REPO_DIR:-}" ]; then
           FULLSEND_TARGET_REPO_DIR=$(cd "$FULLSEND_TARGET_REPO_DIR" && pwd -P) || exit 1
           export FULLSEND_TARGET_REPO_DIR
       fi
       (cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/repo.py validate-local-path "$feature_dir") || exit 1
   fi
   ```

**Note**: GitHub sources are always external repos, so no marker check or skill repo validation needed.

### Step 1: Read the Test Plan

1. Read `<feature_dir>/TestPlan.md` using the Read tool
2. Extract `source_key` from YAML frontmatter (used in Step 3.1)
3. Extract: Section 4 interfaces; Section 2 strategy; Section 3 environment; Section 5.2 naming;
   Section 1.2 scope; Section 1.3 objectives (every TC must cite at least one); Section 6 E2E
   scenarios if populated (preserve flow priorities on regen; else assign per Section 2.3)

### Step 1.5: Read Gaps (if available)

1. Check if `<feature_dir>/TestPlanGaps.md` exists (generated by `/test-plan-create`)
2. If it exists, read it to understand known limitations — do NOT create test cases for areas marked as pending or missing details
3. If it does not exist, proceed normally

### Step 1.6: Read Design Spec / Additional Docs (if available)

```bash
repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
source_key=$(cd "$repo_root" && uv run python scripts/frontmatter.py read \
  "$feature_dir/TestPlan.md" source_key) || exit 1
additional_docs_raw=$(cd "$repo_root" && \
  uv run python scripts/resolve_additional_docs.py "$feature_dir") || {
    echo "ERROR: resolve_additional_docs.py failed — stopping." >&2
    echo "$additional_docs_raw" >&2; exit 1
  }
additional_docs_result=$(echo "$additional_docs_raw" | jq -c '.docs')
# Refetch when missing (mirrors resolve_strategy).
if [ ! -f "$feature_dir/.source-design-spec.md" ] && [ -n "$source_key" ]; then
  (cd "$repo_root" && uv run python scripts/resolve_design_spec.py \
    --issue-key "$source_key" --feature-dir "$feature_dir" --snapshot) || exit 1
fi
```

Use `additional_docs_result` when generating cases. Read `.source-design-spec.md` if present.
Prefer it for **TC-UI-*** (one `J-*`, `SCR-*`/`TU-*`/`DATA-*`, keep objectives). No invented UI.

### Step 2: Read the Test Case Template

1. Read the template from `${CLAUDE_SKILL_DIR}/test-case-template.md` using the Read tool
2. Follow this template structure for every generated test case
3. **Line length**: Wrap all prose lines to a maximum of 100 characters. This does not apply to tables, code blocks, or headings — only paragraph text and list items.
4. Omit optional sections (Preconditions, Test Data, Expected Response, Validation) when they are empty or not applicable — do not include empty sections
5. Always leave **Automation Status** and **Notes** as placeholders — they are filled later in the process

### Step 2.5: Detect Regeneration Mode

1. **Check for existing test cases**:
   ```bash
   regen_check=$(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/tc_regeneration.py check "$feature_dir")
   mode=$(printf '%s\n' "$regen_check" | jq -r '.mode')
   existing_count=$(printf '%s\n' "$regen_check" | jq -r '.existing_count')
   ```

2. **If `mode = "regenerate"`** (existing test cases found):

   a. **Read all existing TC files** using Read tool (satisfies Write tool requirement):
      ```bash
      printf '%s\n' "$regen_check" | jq -r '.files[]' | while read file; do
          # Read each existing TC file
      done
      ```

   b. **Ask for confirmation** via AskUserQuestion:
      > **Regeneration Mode**
      >
      > Found <existing_count> existing test cases in `test_cases/`.
      >
      > **Regenerating will overwrite all existing test cases.**
      > You can review changes via `git diff` before publishing.
      >
      > Proceed with regeneration? [yes/no]

   c. If **no**: Exit without changes

   d. If **yes**: Continue to Step 3 with `REGENERATION_MODE=true`

3. **If `mode = "create"`** (no existing test cases):
   - Continue to Step 3 with `REGENERATION_MODE=false`

### Step 3: Design and Generate Test Cases

Process **one category at a time** from Section 5.2. For each category:

1. **Design** all test cases for that category:
   - Cover every interface from Section 4 relevant to this category
   - Include positive, negative, and boundary scenarios (per Section 2.2)
   - Assign priorities (P0/P1/P2) following the criteria in Section 2.3
   - Stay strictly within the scope defined in Section 1.2 — do NOT create test cases for out-of-scope items
   - Map each TC to the Section 1.3 objective(s) it validates — record as `objectives` in frontmatter (Step 3.1)
   - Before generating each TC, check all previously generated TCs across ALL categories. If another TC already verifies the same behavior (same preconditions, same verification target), do not create a duplicate — add the missing assertions to the existing TC instead
   - For **TC-UI-*** with a design spec, follow Step 1.6

2. **Write or Edit** the `TC-<CATEGORY>-<NUMBER>.md` files for that category immediately before moving to the next:

   - **If `REGENERATION_MODE=true`**: Use Edit tool for files that already exist (preserves git history), Write tool for new files
   - **If `REGENERATION_MODE=false`**: Use Write tool for all files

   Include YAML frontmatter at the top of each file:

   ```yaml
   ---
   test_case_id: TC-<CATEGORY>-<NUMBER>
   source_key: <STRAT_KEY_FROM_TEST_PLAN>
   objectives: [<N>, ...]
   priority: <P0|P1|P2>
   status: Draft
   automation_status: Not Started
   last_updated: "<today_date>"
   # upgrade_phase: pre|post|both   # see Step 3.4 — set for ANY TC whose expected results differ between upgrade states
   ---
   ```

   - `source_key`: use the value extracted from the test plan's frontmatter in Step 1
   - `objectives`: list of Section 1.3 objective numbers this TC validates (e.g., `[1, 3]`) — required, must be non-empty
   - `last_updated`: MUST be quoted string (e.g., "2026-05-04"), not unquoted date
   - If Section 7.2 is non-trivial, set `upgrade_phase` on every TC whose expected behaviour differs
     between versions (all categories, not only TC-UPG-*)
   - Write the frontmatter directly — validation happens in Step 5.7

3. **E2E/UI interface coverage (mandatory)**: After processing all categories, ensure every non-pending interface from Section 4 is represented in Section 6.2 with at least one `TC-E2E-*` or `TC-UI-*` reference:
   - Generate `TC-E2E-*.md` test cases for user journeys that require end-to-end system coverage
   - An appropriate existing or generated `TC-UI-*.md` test case may satisfy the interface row when UI coverage is the applicable path
   - Each E2E test case should represent a complete user journey, not just a single interface call
   - Use `TC-E2E-<NUMBER>` naming convention (e.g., TC-E2E-001, TC-E2E-002)

4. **NFR test cases (conditional)**: Only create a standalone TC-NFR when the NFR requires dedicated infrastructure or setup that no E2E scenario covers (e.g., a disconnected cluster for air-gap testing, a performance benchmark harness). If an NFR is naturally exercised during an E2E flow — such as RBAC (use different user personas in E2E steps), mTLS (verify certs on pods created by E2E), or namespace isolation (already covered by NEG scenarios) — add it as assertions within the relevant TC-E2E or TC-NEG, not as a separate TC-NFR.

5. **Upgrade test cases (conditional)**: If Section 7.2 has real upgrade behaviour (not N/A),
   generate upgrade-aware TCs. New-feature upgrades: mostly `post`, `pre` for disappearing state,
   `both` for regressions. Upgrade bugs: mostly `both` (pre baseline + post regression).
   - `pre`: old-version only (state source version). `post`: new-version only (state target).
   - `both`: should pass on both versions; E2E spanning upgrade uses `both`; include ≥1 UI TC with
     `both`. Omit phase only for TCs identical to a non-upgrade plan; in an upgrade plan, same
     expected results on both versions → `both` (signals intent).
   Tag by what the TC tests, not category. Pass old and new → `both`; new only → `post`; old only
   → `pre`. Put upgrade TCs under **"Upgrade Testing"** in INDEX.md.

**Expected Results quality:** Each Expected Result must be an observable fact that directly confirms the test objective. Avoid vague conclusions ("works as expected", "renders successfully"). Name the specific page state, URL pattern, response code, element, or resource field.

Before writing each assertion, ask: **"Is this testing what the TC is fundamentally about, or just a side effect?"** Two patterns follow from this:

- **Accessibility / reachability tests** (does this URL work? does this link open?): assert the *absence of error* — "page does not contain '500 Internal Server Error'", "response is HTTP 200", "page does not show 'Application is not available'". Do **not** assert presence of specific UI components (IDE editor pane, console window, specific layout element) — these vary by configuration, workbench image, and product version and will cause failures unrelated to the feature under test.

- **Content / format tests** (does this show the right value? did something change?): assert the *specific observable fact* — "URL contains hostname pattern X", "field value equals Y", "element Z is visible". Use this only when the content itself IS what is being verified.

A test that FAILs for the wrong reason is worse than no test at all. When in doubt, prefer the narrower assertion.

**Test case robustness rules:**
- **Background processes**: When a TC uses background loops (`&`),
  capture each PID (`PID_X=$!`), define a `cleanup()` function
  that kills each PID with `kill "$PID" 2>/dev/null || true`
  (so a dead PID does not fail the trap), and register it with
  `trap cleanup EXIT` before starting the loops. Use `EXIT`
  only — adding `INT` or `TERM` causes cleanup to run on the
  signal and then again on exit.
- **Query scoping**: When querying Prometheus or other shared
  data stores, scope queries to the labels the data store
  actually exposes (e.g., `namespace`, `job`, `container`,
  `pod`). Include only the labels that exist in the target
  metric or data source — do not mandate labels the store
  does not carry. Do not rely on cluster-wide queries that
  unrelated workloads could satisfy.
- **Validate all results**: When asserting label sets, response
  structure, or field presence, first confirm the result array
  is non-empty (e.g., `jq '.result | length > 0'`), then
  validate ALL entries (e.g., `jq '.result | length > 0 and
  all(...)'`). An empty result silently passes `all(...)`, so
  the length guard is required.
- **Synthetic credentials only**: Never specify production or
  real user credentials in preconditions or test data. Use
  test-only API keys, throwaway OIDC tokens from a test IdP,
  or synthetic identities.
- **No fallback masking**: When a TC's preconditions guarantee
  data exists (e.g., traffic is flowing), do not include
  `or vector(0)` or similar fallbacks in test queries — they
  mask broken pipelines as passing tests. Fallback behavior
  should be tested in dedicated edge-case TCs.

**Anti-hallucination rules:**
- Do NOT invent requirements or UI absent from the test plan / design-spec HTML / STRAT AC
- Do NOT create test cases for interfaces marked as "pending details" in Section 4
- If the test plan is ambiguous about what to test, ask the user via AskUserQuestion

### Step 4: Generate Index

After all categories are complete:

1. Create `<feature_dir>/test_cases/` directory if it doesn't already exist: `mkdir -p <feature_dir>/test_cases`
2. Each test case file must be **self-contained** — a tester should be able to execute it without reading the test plan
3. Use **realistic test data**, not placeholder values like "example.com" or "test123"
4. Generate `<feature_dir>/test_cases/INDEX.md` **atomically** (regenerate entire file):
   - Scan all TC-*.md files in test_cases/ directory
   - Extract test_case_id, priority, and title from each
   - Build complete INDEX.md with:
     - Quick stats (total test cases, P0/P1/P2 counts)
     - Test cases organized by category in tables (Test Case ID linked, Title, Priority)
     - Link to parent TestPlan.md
   - Write complete file in one operation (do NOT append incrementally)

### Step 5: Update the Test Plan

Update `<feature_dir>/TestPlan.md` using the Edit tool:
1. **Section 5** — Update the note to reflect test cases have been generated, with a link to `test_cases/INDEX.md`
2. **Section 5.1** — Fill in the Test Case Organization table with category, test case count, and priority distribution
3. **Section 6.1** — Fill in the E2E Scenario Summary table with the generated TC-E2E-* scenarios (ID, scenario name, interfaces covered, priority)
4. **Section 6.2** — Fill in the E2E Coverage Matrix mapping each interface from Section 4 to the applicable `TC-E2E-*` or `TC-UI-*` references
5. **Section 9.1** — Fill in the Test Case Summary table with counts per category and priority breakdown
6. **Section 9.2** — Fill in the Test Cases column with TC IDs mapped to each interface. Leave the Coverage column empty — it will be filled later by `/coverage-assessment`

### Step 5.5: Update README

Update `<feature_dir>/README.md` to add a link to the test cases index:
- Add a "Test Cases" section (or update existing) with a link to `test_cases/INDEX.md`
- Include the total test case count and priority breakdown

### Step 5.6: Coverage Validation

Run these coverage checks:

1. **Interface coverage**: Run `uv run python scripts/validate.py interface-coverage <feature_dir>/TestPlan.md` (deterministic table diff — do not eyeball Section 9.2/6.2 yourself). If `missing_in_9_2` is non-empty, those interfaces lack test case coverage — flag them as gaps. Interfaces marked "pending details" in Section 4 are listed under `pending` and are already excluded from `missing_in_9_2`, `missing_in_6_2`, and `missing_e2e_or_ui_in_6_2` by the validator.
2. **E2E-or-UI coverage**: From the same `interface-coverage` result, if `section_6_2_populated` is `true`, both `missing_in_6_2` and `missing_e2e_or_ui_in_6_2` must be empty. Each populated Section 6.2 row must contain at least one `TC-E2E-*` or `TC-UI-*` reference. For `missing_in_6_2`, generate the missing test case(s) and add the interface mapping; for `missing_e2e_or_ui_in_6_2`, add at least one appropriate `TC-E2E-*` or `TC-UI-*` reference to each populated row for every reported interface. Update Sections 6.2/9.2 and re-run the validator before proceeding. Both diagnostics already exclude `pending` interfaces, so this never regenerates cases for interfaces excluded by the anti-hallucination rule.
3. **Test objective coverage**: Check that every test objective from Section 1.3 is addressed by at least one test case. Flag any uncovered objectives.
4. **Priority distribution**: Verify that TC priorities align with the flow priorities in Section 6.1 — a P0 flow should not only have P2 test cases.
5. **Configurable coverage**: Check that every env var, config path, or configurable explicitly named in Section 3.1 has at least one TC that exercises a non-default value. If any is uncovered, flag it as a coverage gap.
6. **Objective traceability**: Check that every generated TC's `objectives` frontmatter field references at least one valid Section 1.3 objective number, and that every referenced objective has an AC citation. Flag any TC with a missing, empty, or invalid `objectives` field.
7. **Gap cross-reference**: If `TestPlanGaps.md` was read in Step 1.5, verify that no test cases were created for interfaces or areas flagged as pending/missing. If any were, remove them and flag the inconsistency.
8. **Append to TestPlanGaps.md**: If `<feature_dir>/TestPlanGaps.md` exists, append a `## Test Case Coverage Gaps` section with any coverage gaps found (uncovered interfaces, missing objectives, priority mismatches, missing E2E/UI interface coverage, uncovered configurables). If the file does not exist, create it with just this section.

### Step 5.7: Validate Frontmatter, Counts, Scope, and Traceability

Run:

```bash
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && \
 uv run python scripts/validate.py test-cases "$feature_dir" && \
 uv run python scripts/validate.py tc-counts "$feature_dir" && \
 uv run python scripts/validate.py tc-scope "$feature_dir" && \
 uv run python scripts/validate.py tc-traceability "$feature_dir" && \
 uv run python scripts/validate.py interface-coverage "$feature_dir/TestPlan.md")
```

If any check fails, fix the issue and re-run.

### What this skill does NOT do

- Does NOT modify the test plan's Sections 1-4, 7-8, or 9.3 — those are owned by `/test-plan-create` (Sections 9.1 and 9.2 ARE filled by this skill — see Steps 5.5/5.6)
- Does NOT fill Automation Status or Notes in TC files — those are filled later by `/coverage-assessment`
- Does NOT create test cases for out-of-scope items or pending interfaces

$ARGUMENTS
