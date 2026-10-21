---
name: test-plan-review
description: Reviews a generated test plan for completeness, consistency, and quality using a 5-criteria rubric. Scores, auto-revises, and re-scores (max 2 cycles). Use for automated quality assessment and iterative improvement of generated test plans.
user-invocable: false
model: claude-opus-4-6
allowedTools:
  - Read
  - Write
  - Bash
  - Glob
  - Skill
---

# Test Plan Reviewer

Internal orchestrator: scores five criteria (0–2 each), then auto-revises and re-scores failing plans up to twice.

## Usage

This skill is not user-invocable. It is called by:
- `test-plan.create` (Step 4)
- automation/orchestrator flows that need score + auto-revision behavior

## Inputs

### From arguments
Parse `$ARGUMENTS` to extract:
1. **Feature directory** (required): path to directory containing `TestPlan.md`

### Auto-detection
If `test-plan.create` just generated a plan in this session and no arguments were provided, use its feature directory.

## Process

### Model selection for review forks

For every score, review, and revise `Agent` call, including repeated cycles,
omit the `model` parameter so normal runtime resolution uses the active model
for this review skill. Never pass a per-call `inherit` value, model ID, or
family alias as a model override.

### Step 0: Python dependencies

Install the test-plan package (scripts are then importable anywhere):
```bash
bash "${CLAUDE_SKILL_DIR}/../../scripts/bootstrap.sh" --layout "${CLAUDE_SKILL_DIR}" || exit 1
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv sync --extra dev)
```

If installation fails, inform the user and do NOT proceed.

### Step 1: Read Test Plan and Resolve Source Strategy

1. Read `<feature_dir>/TestPlan.md`
2. Read frontmatter to extract `source_key`:
   ```bash
   source_key=$(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && \
                uv run python scripts/frontmatter.py read <feature_dir>/TestPlan.md source_key)
   ```
3. Resolve the strategy with the shared snapshot-primary resolver: use
   `<feature_dir>/.source-strategy.md` if saved by `test-plan.create`; otherwise fetch from Jira and
   save it. Fail if neither source is available.
   ```bash
   repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
   resolve_result=$(cd "$repo_root" && uv run python scripts/resolve_strategy.py <feature_dir> "$source_key")
   resolve_exit=$?

   if [ "$resolve_exit" -ne 0 ]; then
       echo "ERROR: scripts/resolve_strategy.py failed to resolve the source strategy — stopping review." >&2
       echo "$resolve_result" >&2
       exit 1
   fi

   strategy_file_path=$(printf '%s\n' "$resolve_result" | jq -r '.strategy_file')
   ```

   Jira access is read-only. The resolver preserves typed request failures and returns stable
   `jira_fetch_failed` without exposing request URLs/server details or accepting partial strategies.

   Keep `strategy_file_path` as a persistent local snapshot: never remove it, including at Step 5 or
   between cycles; reuse it unchanged for every Step 4e re-score.

4. Compute interface coverage, AC/NFR citation validity, bidirectional scope coverage, and
   actionability evidence deterministically (not as LLM judgments). [`scripts/build_citation_inputs.py`](../../scripts/build_citation_inputs.py)
   derives `ac_count`/`nfr_categories` from `strategy_file_path` and calls the validators:

   ```bash
   gate_result=$(cd "$repo_root" && uv run python scripts/build_citation_inputs.py <feature_dir> --strategy-file "$strategy_file_path") || {
       echo "ERROR: scripts/build_citation_inputs.py failed to construct citation gate inputs — stopping review." >&2
       echo "$gate_result" >&2
       exit 1
   }

   interface_coverage_result=$(printf '%s\n' "$gate_result" | jq -c '.interface_coverage_result')
   ac_citations_result=$(printf '%s\n' "$gate_result" | jq -c '.ac_citations_result')
   ac_coverage_result=$(printf '%s\n' "$gate_result" | jq -c '.ac_coverage_result')
   scope_coverage_result=$(printf '%s\n' "$gate_result" | jq -c '.scope_coverage_result')
   actionability_result=$(printf '%s\n' "$gate_result" | jq -c '.actionability_result')
   ```

   On nonzero exit, stop: gate-input construction failed (for example, unreadable strategy or parser
   bug), which is an execution failure, not plan data. Never fall back to degraded mode. Before
   create-cases, `valid: true` is expected: blank Section 9.2 Test Cases and unpopulated Section 6.2
   are skipped. Once Section 6.2 is populated, each populated row needs a `TC-E2E-*` or `TC-UI-*`
   reference. `missing_e2e_or_ui_in_6_2` identifies declared non-pending interfaces with populated
   rows lacking either reference;
   `missing_in_6_2` identifies absent, blank, or placeholder rows. Actionability `valid` covers only
   blocking `bare_tbd`/`missing_details`; `advisory_gaps` records missing/vague versions and
   incomplete test-data examples. Pass both to the score agent. Section 3.1 needs substantive
   environment/configuration evidence; headings and vague/unavailable-only statements block. The
   same occurrence-level TBD classifier applies to Sections 3.1–3.3: grounded
   `TBD — Resolution: ...`, including `derive` from a named overlay, is allowed; bare/unresolved TBD
   blocks. RBAC needs a role, permissions, and concrete resource (`all`/`any`/`every` collections and
   wildcard resources are not concrete). Count examples only in explicit example labels/table
   columns or `e.g.`/`for example` clauses.

5. Have Python read TestPlan.md frontmatter, validate `additional_docs` paths, and read those files;
   never trust the LLM to resolve paths:

   ```bash
   additional_docs_raw=$(cd "$repo_root" && uv run python scripts/resolve_additional_docs.py <feature_dir>) || {
       echo "ERROR: scripts/resolve_additional_docs.py failed — stopping review." >&2
       echo "$additional_docs_raw" >&2
       exit 1
   }

   additional_docs_result=$(printf '%s\n' "$additional_docs_raw" | jq -c '.docs')
   ```

6. Run deterministic scope (Section 2.1) and boilerplate (Sections 1.3/2.3/8) checks; results feed
   SCOPE FIDELITY and SPECIFICITY without an LLM call. Resolve team pattern overrides from
   TestPlan.md `components`, mapped to `COMPONENT_TEST_DIR_MAP` names by
   `get_component_test_dir.py --teams-only`:

   ```bash
   team_list=$(cd "$repo_root" && uv run python scripts/get_component_test_dir.py --teams-only <feature_dir>) || {
       echo "ERROR: scripts/get_component_test_dir.py --teams-only failed — stopping review." >&2
       echo "$team_list" >&2
       exit 1
   }

   scope_check_result=$(cd "$repo_root" && uv run python scripts/validate_test_scope.py <feature_dir>/TestPlan.md \
       --include-teams="$team_list" --checks-dir=scripts/checks) || {
       echo "ERROR: scripts/validate_test_scope.py failed — stopping review." >&2
       echo "$scope_check_result" >&2
       exit 1
   }

   boilerplate_result=$(cd "$repo_root" && uv run python scripts/detect_boilerplate.py <feature_dir>/TestPlan.md \
       --include-teams="$team_list" --checks-dir=scripts/checks) || {
       echo "ERROR: scripts/detect_boilerplate.py failed — stopping review." >&2
       echo "$boilerplate_result" >&2
       exit 1
   }
   ```

   `validate_test_scope.py`/`detect_boilerplate.py` return JSON and always exit 0. Nonzero means a
   script failure (such as bad path/config); stop as for other Step 1 execution failures.

### Step 2: Score (fork)

Load calibration examples and stop on nonzero exit. Add pairs under `calibration/core/`, optional
`calibration/ui/`, or `calibration/<team>/`; do not edit this skill for examples.

```bash
calibration_raw=$(cd "$repo_root" && uv run python scripts/load_calibration.py \
    "${CLAUDE_SKILL_DIR}/calibration" --include-teams="$team_list") || {
    echo "ERROR: scripts/load_calibration.py failed — stopping review." >&2
    echo "$calibration_raw" >&2
    exit 1
}

calibration_text=$(printf '%s\n' "$calibration_raw" | jq -r '.calibration_text')
printf '%s\n' "$calibration_raw" | jq -r '.warnings[]?' >&2
```

Read the score agent prompt from `${CLAUDE_SKILL_DIR}/prompts/score-agent.md`.

Launch a **forked** score agent with these substitutions and omit the Agent
`model` parameter so normal runtime resolution uses this review skill's active
model:
- `{FEATURE_DIR}` = feature directory path
- `{TEST_PLAN_PATH}` = `<feature_dir>/TestPlan.md`
- `{STRATEGY_FILE_PATH}` = `strategy_file_path` from Step 1
- `{CALIBRATION_TEXT}` = `calibration_text` from `load_calibration.py` above
- `{INTERFACE_COVERAGE_RESULT}` = JSON from Step 1 (`interface_coverage_result`)
- `{AC_CITATIONS_RESULT}` = JSON from Step 1 (`ac_citations_result`)
- `{AC_COVERAGE_RESULT}` = JSON from Step 1 (`ac_coverage_result`)
- `{SCOPE_COVERAGE_RESULT}` = JSON from Step 1 (`scope_coverage_result`)
- `{ACTIONABILITY_RESULT}` = JSON from Step 1 (`actionability_result`)
- `{ADDITIONAL_DOCS_CONTENT}` = JSON from Step 1 (`additional_docs_result`)
- `{SCOPE_CHECK_RESULT}` = JSON from Step 1 (`scope_check_result`)
- `{BOILERPLATE_RESULT}` = JSON from Step 1 (`boilerplate_result`)

The score agent returns rubric scores and a grounding cross-reference table.

**Completeness checks performed by the score agent:**

| Section | Check |
|---------|-------|
| 1.1 Purpose | Does it clearly state what is being tested and why? |
| 1.2 Scope | Are in-scope and out-of-scope explicitly defined? |
| 1.3 Test Objectives | Is there at least one objective per STRAT acceptance criterion (every AC covered), plus grounded NFR objectives where applicable? |
| 2.1 Test Levels | Are the selected levels appropriate for the feature type? |
| 2.3 Priorities | Are P0/P1/P2 definitions specific to this feature, not generic? |
| 3.1 Cluster Config | Is substantive environment/configuration evidence present, with versions/dependencies specified or unknowns recorded with an explicit resolution path? Vague/unavailable-only content and bare/unresolved TBDs are blocking; missing/vague versions remain advisory when the section is otherwise substantive. |
| 3.2 Test Data | Are test-data requirements concrete enough to act on, with incomplete format/examples retained as advisory gaps? |
| 4 Interfaces Under Test | Are entries grounded in source documents, not fabricated? |
| 6.1 E2E Scenarios | Is the E2E Scenario Summary populated with TC-E2E-* entries? (Note: expected to be empty until create-cases runs) |
| 6.2 E2E Coverage | Does each non-pending interface from Section 4 have at least one `TC-E2E-*` or `TC-UI-*` reference in each populated Section 6.2 row? Checked deterministically via `interface-coverage` (Step 1), not LLM table-reading. (Note: expected to be empty until create-cases runs) |
| 7.1 Disconnected | Addressed with testing considerations or explicitly marked Not Applicable with justification? |
| 7.2 Upgrade | Addressed with testing considerations or explicitly marked Not Applicable with justification? |
| 7.3 Performance | Addressed with testing considerations or explicitly marked Not Applicable with justification? |
| 7.4 RBAC | Addressed with testing considerations or explicitly marked Not Applicable with justification? |
| 7.5 Security | Addressed with testing considerations or explicitly marked Not Applicable with justification? |
| 8 Risks | Are risks specific to this feature, not boilerplate? |
| 9 Environment | Is there enough detail to set up a test environment? |

### Step 3: Review (fork)

Read the review agent prompt from `${CLAUDE_SKILL_DIR}/prompts/review-agent.md`.

Launch a **forked** review agent with these substitutions and omit the Agent
`model` parameter so normal runtime resolution uses this review skill's active
model:
- `{CLAUDE_SKILL_DIR}` = `${CLAUDE_SKILL_DIR}` (the selected review skill directory)
- `{FEATURE_DIR}` = feature directory path
- `{ASSESSMENT_TEXT}` = full output from the score agent (Step 2)
- `{FIRST_PASS}` = `true` (first assessment cycle)

The review agent writes rubric scores, feedback, and validated frontmatter to
`<feature_dir>/TestPlanReview.md`.

**Consistency checks performed by the review agent:**
- Do the interfaces in Section 4 align with the scope in Section 1.2?
- Do the test levels in Section 2.1 match the interface types in Section 4?
- Are priority assignments in Section 6.1 consistent with the definitions in Section 2.3?
- Does Section 9.2 list all interfaces from Section 4? (deterministic — from the `interface-coverage` result computed in Step 1, not re-derived)
- Are NFR categories in Section 7 consistent with the feature scope? (e.g., a feature that pulls images should not mark Disconnected as N/A)
- Does Section 6.2 E2E Coverage Matrix include all non-pending interfaces from Section 4 and at least one `TC-E2E-*` or `TC-UI-*` reference per populated interface row? (deterministic — from `missing_in_6_2` and `missing_e2e_or_ui_in_6_2` in the `interface-coverage` result; expected unpopulated until create-cases runs)

### Step 3.5: Enforce Citation Gate

Reapply Scope Fidelity/Specificity caps and the Actionability correction deterministically.
`enforce_citation_gate.py` always exits 0 and reports JSON: blocking evidence caps Actionability
above 1 to 1/2; valid evidence never raises 0/1. `actionability_capped` is true only if the cap
changes the score.

```bash
repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
gate_result=$(cd "$repo_root" && uv run python scripts/enforce_citation_gate.py <feature_dir> \
    --ac-citations-result "$ac_citations_result" --ac-coverage-result "$ac_coverage_result" \
    --scope-check-result "$scope_check_result" --boilerplate-result "$boilerplate_result" \
    --scope-coverage-result "$scope_coverage_result" --actionability-result "$actionability_result")
gate_status=$(printf '%s\n' "$gate_result" | jq -r '.status')

case "$gate_status" in
    overridden|ok|skip) ;;
    *)
        echo "ERROR: scripts/enforce_citation_gate.py failed — stopping review." >&2
        echo "$gate_result" >&2
        exit 1
        ;;
esac
```

If `overridden`, Step 4 uses corrected scores/feedback, not the agent's numbers. Any status besides
`overridden`/`ok`/`skip` means gate failure; stop.

### Step 4: Check Criteria and Revise (max 2 cycles)

After the review agent completes, read the review frontmatter:

```bash
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/frontmatter.py read <feature_dir>/TestPlanReview.md)
```

If all five `scores.*` are `2`, proceed to Step 5. The result can be Ready with non-empty
`actionability_result.advisory_gaps`; these are visible follow-ups, not revision failures.

If any `scores.*` is `< 2`, revise. Missing/vague OpenShift/RHOAI versions or incomplete test-data
format/examples in `advisory_gaps` alone do not trigger revision.

#### Revision Loop

Initialize cycle counter: `reassess_cycle=0`

**4a. Filter for revision:**

```bash
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/filter_for_revision.py <feature_dir>)
```

If output is `SKIP`, stop the loop and proceed to Step 5.

**4b. Launch revise agent (fork):**

Read the revise agent prompt from `${CLAUDE_SKILL_DIR}/prompts/revise-agent.md`.

Launch with substitutions and omit the Agent `model` parameter so normal
runtime resolution uses this review skill's active model:
- `{CLAUDE_SKILL_DIR}` = `${CLAUDE_SKILL_DIR}` (the selected review skill directory)
- `{FEATURE_DIR}` = feature directory path
- `{STRATEGY_FILE_PATH}` = `strategy_file_path` from Step 1
- `{ADDITIONAL_DOCS_CONTENT}` = `additional_docs_result` from Step 1 (refreshed by Step 4e on later cycles)

The revise agent edits TestPlan.md (only sections mapped to failing criteria) and sets `auto_revised=true`.

**4c. Check if reassessment is needed:**

```bash
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/frontmatter.py read <feature_dir>/TestPlanReview.md)
```

If `auto_revised` is `false`, stop; the revise agent found nothing to change.

Increment `reassess_cycle`. If `reassess_cycle >= 2`, stop — max cycles reached. Proceed to Step 5.

**4d. Save cumulative state:**

```bash
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/preserve_review_state.py save <feature_dir>)
```

**4e. Re-score:**

Delete the existing review file to force a clean re-assessment:
```bash
rm <feature_dir>/TestPlanReview.md
```

Recompute results against revised `TestPlan.md`; the revise agent may change Sections 4, 6.2, 9.2,
or citations, so refresh all four before re-scoring:

```bash
repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
gate_result=$(cd "$repo_root" && uv run python scripts/build_citation_inputs.py <feature_dir> --strategy-file "$strategy_file_path") || {
    echo "ERROR: scripts/build_citation_inputs.py failed — stopping review." >&2
    echo "$gate_result" >&2
    exit 1
}

interface_coverage_result=$(printf '%s\n' "$gate_result" | jq -c '.interface_coverage_result')
ac_citations_result=$(printf '%s\n' "$gate_result" | jq -c '.ac_citations_result')
ac_coverage_result=$(printf '%s\n' "$gate_result" | jq -c '.ac_coverage_result')
scope_coverage_result=$(printf '%s\n' "$gate_result" | jq -c '.scope_coverage_result')
actionability_result=$(printf '%s\n' "$gate_result" | jq -c '.actionability_result')

additional_docs_raw=$(cd "$repo_root" && uv run python scripts/resolve_additional_docs.py <feature_dir>) || {
    echo "ERROR: scripts/resolve_additional_docs.py failed — stopping review." >&2
    echo "$additional_docs_raw" >&2
    exit 1
}

additional_docs_result=$(printf '%s\n' "$additional_docs_raw" | jq -c '.docs')

team_list=$(cd "$repo_root" && uv run python scripts/get_component_test_dir.py --teams-only <feature_dir>) || {
    echo "ERROR: scripts/get_component_test_dir.py --teams-only failed — stopping review." >&2
    echo "$team_list" >&2
    exit 1
}

scope_check_result=$(cd "$repo_root" && uv run python scripts/validate_test_scope.py <feature_dir>/TestPlan.md \
    --include-teams="$team_list" --checks-dir=scripts/checks) || {
    echo "ERROR: scripts/validate_test_scope.py failed — stopping review." >&2
    echo "$scope_check_result" >&2
    exit 1
}

boilerplate_result=$(cd "$repo_root" && uv run python scripts/detect_boilerplate.py <feature_dir>/TestPlan.md \
    --include-teams="$team_list" --checks-dir=scripts/checks) || {
    echo "ERROR: scripts/detect_boilerplate.py failed — stopping review." >&2
    echo "$boilerplate_result" >&2
    exit 1
}
```

Repeat Step 2 with revised TestPlan.md and recomputed results; omit Agent `model` as above.

**4f. Re-review:** Omit the Agent `model` parameter as specified above.

Repeat Step 3 with `{FIRST_PASS}=false`, then Step 3.5 against the recomputed Step 4e results.

**4g. Restore before_scores and revision history:**

```bash
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/preserve_review_state.py restore <feature_dir>)
```

**4h. Check criteria again:**

Read review frontmatter. Stop if all criteria are `2`; return to 4a if any remain `< 2` and cycles
remain. Otherwise proceed to Step 5.

### Step 5: Present Results

Keep persistent `strategy_file_path` for future reviews and re-scores.

Read the final review file and present a summary to the user:

```markdown
## Test Plan Review — {feature_name}

**Score: {score}/10 — Verdict: {verdict}**

| Criterion | Score |
|-----------|-------|
| Specificity | {n}/2 |
| Grounding | {n}/2 |
| Scope Fidelity | {n}/2 |
| Actionability | {n}/2 |
| Consistency | {n}/2 |

{If before_score differs from score:}
**Delta: {before_score} → {score} ({+/-difference})**

{If verdict = Ready:}
The test plan is ready for test case generation. Any `actionability_result.advisory_gaps` remain
visible follow-up items in `TestPlanGaps.md` and do not block this step. Run
`/test-plan-create-cases <feature_dir>` to proceed.

{If verdict = Revise (after max cycles):}
The test plan improved but still has issues. Review `<feature_dir>/TestPlanReview.md` for remaining feedback. Consider providing additional source documents (ADR, API spec) to resolve blocking grounding or operational gaps; advisory actionability gaps alone do not require them.

{If verdict = Rework:}
The test plan needs significant rework. This may indicate the source strategy lacks sufficient detail. Review `<feature_dir>/TestPlanReview.md` for specific issues and provide source documents for blocking grounding or operational gaps; advisory actionability gaps alone do not require them.

{If this plan is already in an open PR and reviewer comments exist:}
Use `/test-plan-resolve-feedback <PR_URL>` to triage and apply PR feedback items.
```

## Anti-hallucination Rules

The score agent MUST follow these constraints when reviewing and suggesting improvements:

**NEVER**:
- Invent resolution paths for TBDs (e.g., "check version in ADR section 3" when no ADR exists or that section doesn't specify versions)
- Add specific requirements, API endpoints, or version constraints not present in source documents
- Fabricate documentation references ("see design doc for details" when no design doc exists)
- Assume information exists in documents without verifying
- Create specificity improvements by inventing details

**ALWAYS**:
- For `actionability == 2`, retain a genuinely unknown required value only as `TBD — Resolution: {concrete action} from/with/by/before/after/using {named source or timing}`. The resolution path must be grounded in an actual source or a known owner/timing; `derive` is valid when the named source grounds the derivation. Apply this rule independently to each TBD in Sections 3.1, 3.2, and 3.3. Missing or vague OpenShift/RHOAI versions and incomplete test-data format/examples may remain as advisory gaps and do not by themselves prevent Actionability 2/2.
- Ground all improvements in actual source document content (strategy, ADR, additional_docs)
- Keep bare/unresolved TBDs, missing or non-substantive Section 3.1 environment/configuration, and unusable or broad-collection RBAC evidence as blocking actionability gaps; they must not support an Actionability score of 2/2. Keep advisory gaps visible in TestPlanGaps.md without requesting source documents solely for those advisories.
- Defer to TestPlanGaps.md for unresolved items
- Only suggest changes that are directly traceable to source material

These rules keep the review grounded in source documents: assess completeness and consistency, and
acknowledge gaps instead of inventing resolution paths or details.

## What This Skill Does NOT Do

- Does NOT generate test plans (use `/test-plan-create`)
- Does NOT generate test cases (use `/test-plan-create-cases`)
- Does NOT modify the source strategy
- Does NOT submit anything to Jira
- Does NOT resolve GitHub PR comments (use `/test-plan-resolve-feedback <PR_URL>`)

$ARGUMENTS
