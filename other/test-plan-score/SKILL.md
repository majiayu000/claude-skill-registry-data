---
name: test-plan-score
description: Score an existing test plan using the quality rubric without triggering auto-revision. Use for standalone quality assessment of test plans or evaluating test plans created outside the automated generation pipeline.
argument-hint: <feature_dir>
user-invocable: true
model: claude-sonnet-4-6
allowedTools:
  - Read
  - Bash
  - Glob
  - Skill
---

# Test Plan Scorer

Score an existing test plan using the 5-criteria quality rubric (Specificity, Grounding, Scope Fidelity, Actionability, Consistency). This is the user-facing entrypoint for rubric evaluation.

## Usage

```
/test-plan-score <feature_dir>
```

Examples:
- `/test-plan-score kagenti_agent_templates`
- `/test-plan-score mcp_catalog`

## Inputs

### From arguments
Parse `$ARGUMENTS` to extract:
1. **Feature directory** (required): path to directory containing `TestPlan.md`

## Process

### Step 0: Python dependencies

Install the test-plan package (makes all scripts importable):
```bash
bash "${CLAUDE_SKILL_DIR}/../../scripts/bootstrap.sh" --layout "${CLAUDE_SKILL_DIR}" || exit 1
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv sync --extra dev)
```

If installation fails, inform the user and do NOT proceed. Once installed, all Python scripts will work from any directory.

### Step 1: Read Test Plan and Resolve Source Strategy

1. Read `<feature_dir>/TestPlan.md`
2. Read frontmatter to extract `source_key`:
   ```bash
   source_key=$(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && \
                uv run python scripts/frontmatter.py read <feature_dir>/TestPlan.md source_key)
   ```
3. Resolve the source strategy via the shared resolver — snapshot-primary: reads
   `<feature_dir>/.source-strategy.md` if `test-plan.create` already saved one, otherwise fetches
   from Jira and saves it there for next time. No degraded mode: if neither is available, this is
   a hard failure.
   ```bash
   repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
   resolve_result=$(cd "$repo_root" && uv run python scripts/resolve_strategy.py <feature_dir> "$source_key")
   resolve_exit=$?

   if [ "$resolve_exit" -ne 0 ]; then
       echo "ERROR: scripts/resolve_strategy.py failed to resolve the source strategy — stopping." >&2
       echo "$resolve_result" >&2
       exit 1
   fi

   strategy_path=$(printf '%s\n' "$resolve_result" | jq -r '.strategy_file')
   ```

   The resolver is read-only with respect to Jira. It preserves typed Jira request failures and
   returns the stable `jira_fetch_failed` error instead of exposing request URLs, server details, or
   accepting a partial strategy.

   `strategy_path` is the persistent, local-only snapshot — it is never deleted.

4. Compute AC/NFR citation validity, coverage, bidirectional scope coverage, and actionability evidence deterministically (mirrors `test-plan.review` Step 1.5) via [`scripts/build_citation_inputs.py`](../../scripts/build_citation_inputs.py), which derives `ac_count`/`nfr_categories` from `strategy_path` and calls the validators directly:

   ```bash
   gate_result=$(cd "$repo_root" && uv run python scripts/build_citation_inputs.py <feature_dir> --strategy-file "$strategy_path") || {
       echo "ERROR: scripts/build_citation_inputs.py failed to construct citation gate inputs — stopping." >&2
       echo "$gate_result" >&2
       exit 1
   }

   interface_coverage_result=$(printf '%s\n' "$gate_result" | jq -c '.interface_coverage_result')
   ac_citations_result=$(printf '%s\n' "$gate_result" | jq -c '.ac_citations_result')
   ac_coverage_result=$(printf '%s\n' "$gate_result" | jq -c '.ac_coverage_result')
   scope_coverage_result=$(printf '%s\n' "$gate_result" | jq -c '.scope_coverage_result')
   actionability_result=$(printf '%s\n' "$gate_result" | jq -c '.actionability_result')
   ```

   A nonzero exit means gate-input construction itself failed (unreadable strategy file, a parsing bug) — that's an execution failure, not data about the test plan, so stop rather than silently falling back to degraded mode. The interface coverage result distinguishes missing/blank Section 6.2 rows in `missing_in_6_2` from declared interfaces with a populated row that contains neither a `TC-E2E-*` nor a `TC-UI-*` reference in `missing_e2e_or_ui_in_6_2`; each populated Section 6.2 row must contain at least one `TC-E2E-*` or `TC-UI-*` reference. Use both fields in the consistency assessment. Empty pre-create-cases Section 6.2 remains valid and is skipped by the validator.

   For Actionability, only `bare_tbd` and `missing_details` are blocking; `advisory_gaps` are
   visible follow-up items. Section 3.1 must contain substantive environment/configuration
   evidence, not only vague or unavailable text. The same occurrence-level TBD rule applies to
   Sections 3.1–3.3, RBAC must name a role, permissions, and a concrete resource, and
   `all`/`any`/`every` collections or wildcard resources are not concrete. Test-data examples must
   use explicit example labels/table columns or `e.g.,`/`for example` clauses.

5. Resolve `additional_docs` from TestPlan.md frontmatter:

   ```bash
   additional_docs_raw=$(cd "$repo_root" && uv run python scripts/resolve_additional_docs.py <feature_dir>) || {
       echo "ERROR: scripts/resolve_additional_docs.py failed — stopping." >&2
       echo "$additional_docs_raw" >&2
       exit 1
   }

   additional_docs_result=$(printf '%s\n' "$additional_docs_raw" | jq -c '.docs')
   ```

6. Compute scope/boilerplate results (mirrors `test-plan.review` Step 1):

   ```bash
   team_list=$(cd "$repo_root" && uv run python scripts/get_component_test_dir.py --teams-only <feature_dir>) || {
       echo "ERROR: scripts/get_component_test_dir.py --teams-only failed — stopping." >&2
       echo "$team_list" >&2
       exit 1
   }

   scope_check_result=$(cd "$repo_root" && uv run python scripts/validate_test_scope.py <feature_dir>/TestPlan.md \
       --include-teams="$team_list" --checks-dir=scripts/checks) || {
       echo "ERROR: scripts/validate_test_scope.py failed — stopping." >&2
       echo "$scope_check_result" >&2
       exit 1
   }

   boilerplate_result=$(cd "$repo_root" && uv run python scripts/detect_boilerplate.py <feature_dir>/TestPlan.md \
       --include-teams="$team_list" --checks-dir=scripts/checks) || {
       echo "ERROR: scripts/detect_boilerplate.py failed — stopping." >&2
       echo "$boilerplate_result" >&2
       exit 1
   }
   ```

### Step 2: Score (fork)

Load calibration examples from the shared review skill tree (fail closed — stop on nonzero
exit). Adding a pair is dropping a file in that `calibration/core/`, optional
`calibration/ui/`, or `calibration/<team>/`.

```bash
calibration_raw=$(cd "$repo_root" && uv run python scripts/load_calibration.py \
    "${CLAUDE_SKILL_DIR}/../test-plan-review/calibration" --include-teams="$team_list") || {
    echo "ERROR: scripts/load_calibration.py failed — stopping." >&2
    echo "$calibration_raw" >&2
    exit 1
}

calibration_text=$(printf '%s\n' "$calibration_raw" | jq -r '.calibration_text')
printf '%s\n' "$calibration_raw" | jq -r '.warnings[]?' >&2
```

Read the score agent prompt from `skills/test-plan-review/prompts/score-agent.md`.

Launch a **forked** score agent with substitutions:
- `{FEATURE_DIR}` = feature directory path
- `{TEST_PLAN_PATH}` = `<feature_dir>/TestPlan.md`
- `{STRATEGY_FILE_PATH}` = `strategy_path` from Step 1
- `{CALIBRATION_TEXT}` = `calibration_text` from `load_calibration.py` above
- `{INTERFACE_COVERAGE_RESULT}` = JSON from Step 1 (`interface_coverage_result`)
- `{AC_CITATIONS_RESULT}` = JSON from Step 1 (`ac_citations_result`)
- `{AC_COVERAGE_RESULT}` = JSON from Step 1 (`ac_coverage_result`)
- `{SCOPE_COVERAGE_RESULT}` = JSON from Step 1 (`scope_coverage_result`)
- `{ACTIONABILITY_RESULT}` = JSON from Step 1 (`actionability_result`)
- `{ADDITIONAL_DOCS_CONTENT}` = JSON from Step 1 (`additional_docs_result`)
- `{SCOPE_CHECK_RESULT}` = JSON from Step 1 (`scope_check_result`)
- `{BOILERPLATE_RESULT}` = JSON from Step 1 (`boilerplate_result`)

### Step 2.5: Enforce Score Caps

The score agent is instructed to apply the deterministic Scope Fidelity/Specificity/Actionability
rules above — but LLM compliance isn't guaranteed, and this skill writes no `TestPlanReview.md` for
a gate to correct after the fact (unlike `test-plan.review`, which re-applies the rule via
`enforce_citation_gate.py` once the file exists). Re-apply them directly against the agent's
self-reported scores (each 0-2, from the Score Table in Step 2), before presenting anything.

Write the five rubric scores from the Score Table as a JSON object (use `scope_fidelity` with an underscore, matching the rubric key):

```json
{"specificity": N, "grounding": N, "scope_fidelity": N, "actionability": N, "consistency": N}
```

Then pass to the deterministic validator:

```bash
repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
scores_json='{"specificity": N, "grounding": N, "scope_fidelity": N, "actionability": N, "consistency": N}'
cap_result=$(cd "$repo_root" && uv run python scripts/cap_scope_fidelity.py \
    --scores-json "$scores_json" \
    --ac-citations-result "$ac_citations_result" --ac-coverage-result "$ac_coverage_result" \
    --scope-check-result "$scope_check_result" --boilerplate-result "$boilerplate_result" \
    --scope-coverage-result "$scope_coverage_result" --actionability-result "$actionability_result") || {
    echo "ERROR: scripts/cap_scope_fidelity.py failed — stopping." >&2
    echo "$cap_result" >&2
    exit 1
}
cap_status=$(printf '%s\n' "$cap_result" | jq -r '.status')
if [ "$cap_status" = "error" ]; then
    echo "ERROR: scripts/cap_scope_fidelity.py returned error — stopping." >&2
    echo "$cap_result" >&2
    exit 1
fi
```

The Python helper validates that `scores_json` contains exactly five integer scores (0-2 each) before processing — malformed or out-of-range values produce a structured error, not a shell failure. If `cap_status` is `overridden`, Step 3 below presents `cap_result`'s `scores`/`score`/`verdict`/`pass` — not the agent's own numbers. The presentation must explicitly report every corrected criterion, including an **Actionability cap to 1/2** when `cap_result.actionability_capped` is `true`. The cap is based only on `actionability_result.bare_tbd` and `actionability_result.missing_details`; valid evidence preserves the scorer's 0/1, and `advisory_gaps` never cap or lower a score. For an Actionability cap, replace the score agent's original Evidence and Notes with a deterministic rationale built from the blocking fields.

### Step 3: Present Results

Parse the score agent's output and present the results to the user, substituting the Step 2.5 correction where it applies:

```markdown
## Test Plan Score — {feature_name}

### Rubric Scores

| Criterion | Score | Notes |
|-----------|-------|-------|
| Specificity | {n}/2 | {brief rationale, or "Automatically corrected — boilerplate check failed" if Step 2.5 overrode it} |
| Grounding | {n}/2 | {brief rationale} |
| Scope Fidelity | {n}/2 | {brief rationale, or "Automatically corrected — citation/coverage/scope checks failed" if Step 2.5 overrode it} |
| Actionability | {n}/2 | {brief rationale when not corrected; otherwise "Automatically corrected to 1/2 — deterministic blocking actionability evidence failed: {bare_tbd and/or missing_details}"; advisory gaps may remain visible without lowering this score} |
| Consistency | {n}/2 | {brief rationale} |

**Total: {sum}/10**

### Verdict

{If `cap_status` was `overridden`: use `cap_result.verdict`/`cap_result.pass` directly — do not re-derive from the total.}
{Otherwise — If >= 8, no zeros, and actionability == 2: "**Ready** — proceed to test case generation"}
{If >= 7, no zeros (but not meeting Ready bar): "**Revise** — minor improvements needed. Re-run via `/test-plan-create` flow to apply auto-revision, or invoke the internal `test-plan.review` workflow from automation."}
{If < 7 or any zero: "**Rework** — significant issues. Re-run via `/test-plan-create` flow for remediation, or use automation that calls internal `test-plan.review`."}

### Grounding Cross-Reference
{Include the full grounding cross-reference table from the scorer}
```

## What This Skill Does NOT Do

- Does NOT write a TestPlanReview.md file
- Does NOT trigger auto-revision
- Does NOT modify the test plan
- For scoring + auto-revision, use `/test-plan-create` flow (which calls internal `test-plan.review`)

$ARGUMENTS
