---
name: test-plan-create
description: Generate a test plan from a strategy (RHAISTRAT or RHOAIENG), with optional ADR and/or design-spec companions. Use when starting test planning for a new RHOAI feature with a defined Jira strategy.
argument-hint: <JIRA_KEY> [COMPANION_DOC_PATH...]
user-invocable: true
model: claude-opus-4-6
allowedTools:
  - Read
  - Write
  - Bash
  - Glob
  - Skill
  - AskUserQuestion
---

# Test Plan Generator

Generate a RHOAI test plan from a refined strategy, with optional ADR and/or design-spec companions.

## Usage

```
/test-plan-create <JIRA_KEY> [COMPANION_DOC_PATH...]
```

Examples:
- `/test-plan-create RHAISTRAT-400`
- `/test-plan-create RHAISTRAT-400 /path/to/adr.pdf ./design-spec.md`

## Inputs

Parse `$ARGUMENTS` as:
1. Required Jira key: a `RHAISTRAT-*` strategy or `RHOAIENG-*` issue.
2. Optional companion paths. After setting
   `repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)`, classify each with the CLI
   (do not inspect content yourself):
   `uv run --project "$repo_root" python "$repo_root/scripts/resolve_design_spec.py" --classify "$path"`
   → `kind` is `design_spec` (set `LOCAL_DESIGN_SPEC_PATH`), `adr`, or `other`.

With no arguments, use this session's `/strat.create` or `/strat.refine` strategy at Step 1. If none
exists, ask for a Jira key, companion paths, optional ADR/design-spec URL (metadata only; never
fetch), and optional snake_case feature-directory name.

**Design spec (UI):** Prefer available `SCR-*` HTML, `J-*` journeys, and optional `TU-*`/`DATA-*`.
Local `design_spec` wins; otherwise Step 1.5 finds `{KEY}-design-spec.md` or the newest matching
Jira attachment. Do not invent UI absent from STRAT/spec.

## Process

Use stdout for substitutions and stderr for diagnostics. Stop on nonzero exit.

### Step 0: Pre-flight Checks

#### 0.1 Python dependencies

Install the package so scripts are importable from any directory:
```bash
bash "${CLAUDE_SKILL_DIR}/../../scripts/bootstrap.sh" --layout "${CLAUDE_SKILL_DIR}" || exit 1
repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
(cd "$repo_root" && uv sync --extra dev)
```

If installation fails, inform the user and **STOP**; do not proceed.

#### 0.2 Jira Environment Variables

Verify that `JIRA_URL`, `JIRA_USER`, and `JIRA_TOKEN` are configured:

```bash
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python -c "from scripts.jira_utils import require_env; [require_env(v) for v in ('JIRA_URL','JIRA_USER','JIRA_TOKEN')]")
```

If it exits non-zero, **STOP immediately**. Do not continue or use alternative sources (MCP, cache,
web, or any workaround). Report the error and tell the user to set the missing variables: `JIRA_URL`
(base URL), `JIRA_USER` (username/email), and `JIRA_TOKEN` (API token). Otherwise proceed to Step 0.3.

#### 0.3 Determine Output Directory

Keep artifacts outside the skill repository. `--output-dir` sets the contributor override and
`FORCE_OUTPUT_DIR=true`; otherwise read `.claude/settings.json` and ask via AskUserQuestion (empty uses its
saved value or `~/Code/opendatahub-test-plans/plans/`). Expand `~`.

Resolve relative paths against the caller workspace before running a plugin helper:

```bash
target_dir=$(python3 -c 'import os,sys; print(os.path.abspath(os.path.expanduser(sys.argv[1])))' "$target_dir")
```

Validate every target. Overrides never permit package writes or Fullsend output outside
`FULLSEND_TARGET_REPO_DIR`:
```bash
if [ -n "${FULLSEND_TARGET_REPO_DIR:-}" ]; then
    FULLSEND_TARGET_REPO_DIR=$(cd "$FULLSEND_TARGET_REPO_DIR" && pwd -P) || exit 1
    export FULLSEND_TARGET_REPO_DIR
fi
force_flag=$([ "$FORCE_OUTPUT_DIR" = "true" ] && echo "--force" || echo "")
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/repo.py validate-local-path "$target_dir" $force_flag) || exit 1
```

Unless `--output-dir` was used, ask whether to save the path. On yes, atomically update only
`test-plan.output_dir`; on no, leave settings unchanged. Create it and stay in the caller workspace
through Step 1 so the guarded `.odh-test-gen/` helper link resolves:
```bash
mkdir -p "$target_dir"
echo "✓ Creating test plan artifacts in: $target_dir"
```

Step 1.5 `save-snapshot` stores it in `<feature_dir>/.test-plan-output-dir.json` for discovery
without environment variables.

### Step 1: Gather Information

1. **Strategy**: Fetch a supplied Jira key with `fetch_issue.py`; for auto-detected keys, read
   `artifacts/strat-tasks/` — do NOT fetch.

   **Fetching from Jira:**
   ```bash
   repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
   parse_strat_script="$repo_root/scripts/parse_strat.py"
   if [ "$(pwd -P)" != "$repo_root" ]; then
       parse_strat_script=".odh-test-gen/scripts/parse_strat.py"
   fi
   tmp_result=$(uv run --project "$repo_root" python "$parse_strat_script" new-strat-tmp) || exit 1
   strategy_file=$(printf '%s\n' "$tmp_result" | jq -r '.strategy_file')
   (cd "$repo_root" && \
    uv run python scripts/fetch_issue.py <JIRA_KEY> --output "$strategy_file")
   ```

   The fetcher is read-only. Only when the description says `exceeds Jira's description size limit`
   does it resolve the exact `<JIRA_KEY>-strategy.md` attachment; otherwise the description is
   authoritative and matching attachments are ignored.

   **Auto-detected from `artifacts/strat-tasks/<JIRA_KEY>.md`** (shared cache and Jira-outage
   fallback for other skills):
   ```bash
   resolve_result=$(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/parse_strat.py resolve-local "<JIRA_KEY>") || exit 1
   strategy_file=$(printf '%s\n' "$resolve_result" | jq -r '.strategy_file')
   ```

   - `components` is extracted deterministically in Step 1.5 (`parse_strat.py save-snapshot`).
2. **ADR** (if companion `kind` is `adr`): Read for API/data/implementation detail.
3. **Design spec**: Do not resolve yet; snapshot once in Step 1.5 after `feature_dir` exists.

After acquiring the strategy, enter the output directory before creating feature artifacts:

```bash
cd "$target_dir" || exit 1
```

### Step 1.5: Parse Strategy Sections and Snapshot the Strategy

Parse the strategy before snapshotting it:

```bash
repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
gate_result=$(cd "$repo_root" && uv run python scripts/parse_strat.py workflow-inputs "$strategy_file")
gate_exit=$?

if [ "$gate_exit" -ne 0 ]; then
  echo "workflow-inputs failed to parse the strategy; cannot proceed" >&2
  echo "$gate_result" >&2
  exit 1
fi

gate_status=$(printf '%s\n' "$gate_result" | jq -r '.status')
if [ "$gate_status" = "ok" ]; then
  ac_json=$(printf '%s\n' "$gate_result" | jq -c '.ac_json')
  nfr_json=$(printf '%s\n' "$gate_result" | jq -c 'if .nfr_json.found then .nfr_json else empty end')
  oos_json=$(printf '%s\n' "$gate_result" | jq -c 'if .oos_json.found then .oos_json else empty end')
  ac_count=$(printf '%s\n' "$gate_result" | jq -r '.ac_count')
  nfr_category_flags=()
  while IFS= read -r cat; do [ -n "$cat" ] && nfr_category_flags+=(--nfr-category "$cat"); done < <(printf '%s\n' "$gate_result" | jq -r '.nfr_categories[]? // empty')
fi

feature_name="<user-provided feature directory name from Inputs (Optional) if given, else snake_case derived from the strategy title>"
(cd "$repo_root" && uv run python scripts/validate.py feature-name "$feature_name") || exit 1
feature_dir="$(pwd)/$feature_name"
```

Snapshot to `$feature_dir/.source-strategy.md`; create the feature directory, move temp fetches, and
copy (never delete) the shared cache:

```bash
snapshot_result=$(cd "$repo_root" && uv run python scripts/parse_strat.py save-snapshot "$strategy_file" "$feature_dir") || exit 1
strategy_file=$(printf '%s\n' "$snapshot_result" | jq -r '.strategy_file')
components=$(printf '%s\n' "$snapshot_result" | jq -r '.components | join(",")')
```

Resolve and snapshot the design spec **once** (local wins; else Jira attachment). Continue if
`source: none`:

```bash
design_spec_snap=$(cd "$repo_root" && uv run python scripts/resolve_design_spec.py \
    --issue-key <JIRA_KEY> \
    ${LOCAL_DESIGN_SPEC_PATH:+--local-path "$LOCAL_DESIGN_SPEC_PATH"} \
    --feature-dir "$feature_dir" --snapshot) || exit 1
design_spec_file=$(echo "$design_spec_snap" | jq -r '.snapshot_path // empty')
# If snapshotted, add ".source-design-spec.md" to additional_docs in Step 3.1.
```

If `$gate_status` is `no_acceptance_criteria` (no ACs or count 0), **STOP**:
1. Write a lowest-score review:
   ```bash
   (cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/frontmatter.py set \
       <absolute_path_to_output_dir>/<feature_name>/TestPlanReview.md \
       feature="<feature_name>" source_key=<JIRA_KEY> score=0 pass=false verdict=Rework \
       scores='{"specificity":0,"grounding":0,"scope_fidelity":0,"actionability":0,"consistency":0}' \
       auto_revised=false)
   ```
2. Write review body: `"Strategy has no acceptance criteria. Cannot generate AC-traced test plan."`
3. Stamp `test-plan-rubric-fail` on the Jira issue (non-blocking). Do NOT proceed to Step 2.

### Step 2: Analyze (Parallel Native Skill Calls)

**Scope and traceability**: Section 2.1 permits e2e/system and UI only. Every Section 1.3 objective
needs a grounded AC/NFR citation. In-scope entries in 1.2, 2.3, 7.1–7.5, and 8 end with
`(Objective: #N)`; never guess `N`. Ungrounded 7.1–7.5 categories are **Not Applicable**. Step 3.2
validates these rules.

The endpoint analyzer reports Section 1.2 items omitted from 1.3 for lack of AC. Preserve its output
and collect `## Gaps` in `TestPlanGaps.md` at Step 3.5; do not invent objectives.

Call all three registered analyzer skills in parallel through the native `Skill` tool, one call per
skill, using the names below and passing inputs in `args`. Supply strategy path, original ADR path
(if provided), and `<feature_name>/.source-design-spec.md` (if present); never inline documents.
Pass Step 1.5 JSON as ground truth. Stop if a call fails or returns no result; never substitute a
generic `Agent`, inline analysis, or another model.

- **endpoints** (`test-plan.analyze.endpoints`): strategy, ADR, design spec (if any),
  `ac_json`, `oos_json`, `nfr_json`. Prefer
  `SCR-*`/`J-*` for UI when a design spec exists.
- **risks** (`test-plan.analyze.risks`): strategy, ADR, design spec (if any),
  `ac_json`, `nfr_json` → e2e/UI levels, types, priorities, risks, NFR assessments.
- **infra** (`test-plan.analyze.infra`): strategy, ADR, design spec (if any). Prefer
  `TU-*`/`DATA-*` for Section 3 when present.

Merge all three results and collect `## Gaps` for Step 3.5. Add nothing absent from their outputs.

**Evidence policy:** In Sections 3.1–3.3, bare/unresolved `TBD` blocks. Unknowns need
`TBD — Resolution: {action} from/with/by/before/after/using {source}`; `derive` is valid when a named
overlay grounds it. Count examples only in `Example`/`Sample`/`Fixture` labels or `e.g.`/`for example`
clauses. Advisories may score `actionability == 2`; only `bare_tbd`/`missing_details` block scoring.

### Step 3: Generate Files

1. Ensure `test_cases/` exists: `mkdir -p -- "$feature_dir/test_cases"`.
2. Resolve the strategy URL from `JIRA_URL` (falling back to `JIRA_BASE_URL`); never hardcode or infer a host:
   ```bash
   jira_url="${JIRA_URL:-$JIRA_BASE_URL}"
   strat_url="${jira_url%/}/browse/${JIRA_KEY}"
   ```
   Use this exact `strat_url` in the template and `README.md`.
3. Fill `TestPlan.md` from `${CLAUDE_SKILL_DIR}/test-plan-template.md`, preserving section order and
   headings. Do not write frontmatter manually. Wrap prose/list items to 100 characters and apply
   Step 2 objective markers, excluding out-of-scope Section 1.2 items.
4. In Section 9.2 fill only Interface from Section 4; leave Test Cases and Coverage empty.
5. Include feature name/description, `strat_url`, optional ADR/design-spec refs, TestPlan link, and
   automated-test destination in `README.md`.

### Step 3.1: Set Frontmatter

After generating `TestPlan.md`, use Bash and `frontmatter.py` to validate and set metadata. Set
`SOURCE_TYPE` from the Jira key (`RHAISTRAT-*` → `strat`,
`RHOAIENG-*` → `issue`):
```bash
if [[ <JIRA_KEY> == RHAISTRAT-* ]]; then
    SOURCE_TYPE="strat"
elif [[ <JIRA_KEY> == RHOAIENG-* ]]; then
    SOURCE_TYPE="issue"
fi
```

Run Python from the test-plan repo (with `pyproject.toml`), using absolute paths.

```bash
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/frontmatter.py set <absolute_path_to_output_dir>/<feature_name>/TestPlan.md \
    feature="<feature_name>" \
    source_key=<JIRA_KEY> \
    source_type=$SOURCE_TYPE \
    status=Draft \
    author="<team_name>" \
    components="$components" \
    additional_docs="<comma-separated list of doc links, or []>")
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/version.py set <absolute_path_to_output_dir>/<feature_name>/TestPlan.md 1.0.0)
```

Use Step 1.5 `components` (empty becomes `[]`) and include the ADR, other user links, and snapshotted
`.source-design-spec.md` in `additional_docs` (or `[]`). Scripts set `last_updated` and default
`reviewers` to `[]`. Fix errors and retry; never write frontmatter by hand.

### Step 3.2: Validate Generated Test Plan

Run these deterministic checks after frontmatter; Step 1.5 sets `$ac_count` and
`$nfr_category_flags`:

```bash
testplan="<absolute_path_to_output_dir>/<feature_name>/TestPlan.md"
feature_dir="<absolute_path_to_output_dir>/<feature_name>"
repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)

team_list=$(cd "$repo_root" && uv run python scripts/get_component_test_dir.py --teams-only "$feature_dir") || {
    echo "ERROR: scripts/get_component_test_dir.py --teams-only failed — stopping." >&2
    echo "$team_list" >&2
    exit 1
}

(cd "$repo_root" && \
 scope_result=$(uv run python scripts/validate_test_scope.py "$testplan" \
     --include-teams="$team_list" --checks-dir=scripts/checks) && \
 (printf '%s\n' "$scope_result" | jq -e '.valid' >/dev/null || { echo "$scope_result" >&2; exit 1; }) && \
 uv run python scripts/validate.py ac-citations "$testplan" --ac-count "$ac_count" "${nfr_category_flags[@]}" && \
 uv run python scripts/validate.py ac-coverage "$testplan" --ac-count "$ac_count" && \
 uv run python scripts/validate.py structure "$testplan" && \
 uv run python scripts/validate.py category-prefixes "$testplan" && \
 uv run python scripts/validate.py interface-types "$testplan" && \
 uv run python scripts/validate.py infra-scope "$testplan") || {
    echo "ERROR: test-plan validation failed — stopping." >&2
    exit 1
}

citation_inputs=$(cd "$repo_root" && uv run python scripts/build_citation_inputs.py "$feature_dir" \
    --strategy-file "$strategy_file") || {
    echo "ERROR: scripts/build_citation_inputs.py failed — stopping." >&2
    echo "$citation_inputs" >&2
    exit 1
}
actionability_result=$(printf '%s\n' "$citation_inputs" | jq -c '.actionability_result')
printf '%s\n' "$citation_inputs" | jq -e '.scope_coverage_result.valid' >/dev/null || {
    echo "ERROR: scope coverage is incomplete; add `(Objective: #N)` markers and grounded objectives." >&2
    echo "$citation_inputs" >&2
    exit 1
}
```

If a check fails, fix `TestPlan.md` and retry once; if it fails again, **STOP** and report it.

### Step 3.5: Collect Gaps and Prompt for Additional Documents

Write each Step 2 sub-agent's full analysis verbatim to the three named `.analysis-*.md` files; the
script extracts `## Gaps`, so do not hand-slice it.

Then run:

```bash
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && \
 uv run python scripts/consolidate_gaps_and_stamp.py \
   --feature-name "<feature_name>" \
   --source-key <JIRA_KEY> \
   --source endpoints=<feature_dir>/.analysis-endpoints.md \
   --source risks=<feature_dir>/.analysis-risks.md \
   --source infra=<feature_dir>/.analysis-infra.md \
   --actionability-result "$actionability_result" \
   --last-updated "$(date -u +%F)" \
   --skip-cleanup \
   --out <feature_dir>/TestPlanGaps.md)
```

Success writes `TestPlanGaps.md` and prints `{"gap_count": int, "status": str, "next":
"proceed"|"prompt_user"}`. Never hand-count gaps, edit frontmatter, or run `check-interactive`.
Keep staging files on failure for debugging.

Render payload `advisory_gaps` in an Advisory Actionability Gaps section for visibility; they do not
change `gap_count`, status, or the document menu. Only consolidated analyzer groups drive the menu;
blocking actionability fields still reach review. Reclassify only version/build or test-data
format/example concerns, count unrelated concerns, and keep reclassified findings visible. Never
request documents solely for advisories.

If `next` is `proceed`, go to Step 3.6. If `prompt_user`, ask about consolidated analyzer groups;
show advisories only as informational follow-ups:

1. **Provide documents** — paste file paths to resolve gaps
2. **Proceed to review** — continue as-is
3. **Proceed + generate test cases** — continue and auto-run `/test-plan-create-cases`

**If option 1:** Read documents; rerun only relevant registered Step 2 Skill calls in parallel with
their original strategy/ADR/design-spec paths, Step 1.5 JSON, and new document paths. Stop on failure;
do not substitute a generic Agent or inline analysis. Update the test plan and recompute gate inputs before
collecting gaps, so actionability evidence is current:
```bash
citation_inputs=$(cd "$repo_root" && uv run python scripts/build_citation_inputs.py "$feature_dir" \
  --strategy-file "$strategy_file") || { echo "$citation_inputs"; exit 1; }
actionability_result=$(printf '%s\n' "$citation_inputs" | jq -c '.actionability_result')
```
Rerun `consolidate_gaps_and_stamp.py` with `--skip-cleanup` and fresh `actionability_result`, then
follow `next`. **If option 2:** proceed to Step 3.6. **Option 3:** also run `/test-plan-create-cases`
with the feature directory after Step 4.

### Step 3.6: Stamp Jira label — test plan created

Add `test-plan-auto-created` to the source issue for org-pulse tracking.

Read `source_key` from `<feature_name>/TestPlan.md` frontmatter:
```bash
source_key=$(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/frontmatter.py read <absolute_path_to_output_dir>/<feature_name>/TestPlan.md source_key)
```

Then add the label with `add_jira_labels.py`:
```bash
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && \
 uv run python scripts/add_jira_labels.py "$source_key" test-plan-auto-created)
```

### Step 4: Review, Score, and Improve

After the gaps flow, invoke **`test-plan.review`** for the feature directory. It scores five criteria
(0–2 each), may auto-revise for up to 2 cycles, and writes feedback to
`<feature_name>/TestPlanReview.md`.

**Refresh TestPlanGaps.md** after review, since revisions may resolve blocking gaps or add advisories.
Recompute `actionability_result` from the final `TestPlan.md` and rerun
`consolidate_gaps_and_stamp.py` with Step 3.5's flags:

```bash
repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
citation_inputs=$(cd "$repo_root" && uv run python scripts/build_citation_inputs.py <feature_dir> \
  --strategy-file "$strategy_file") || { echo "$citation_inputs"; exit 1; }
actionability_result=$(printf '%s\n' "$citation_inputs" | jq -c '.actionability_result')

(cd "$repo_root" && \
 uv run python scripts/consolidate_gaps_and_stamp.py \
   --feature-name "<feature_name>" \
   --source-key <JIRA_KEY> \
   --source endpoints=<feature_dir>/.analysis-endpoints.md \
   --source risks=<feature_dir>/.analysis-risks.md \
   --source infra=<feature_dir>/.analysis-infra.md \
   --actionability-result "$actionability_result" \
   --last-updated "$(date -u +%F)" \
   --skip-cleanup \
   --out <feature_dir>/TestPlanGaps.md)
```

**Handle the review output:**

1. Read the verdict from `<feature_name>/TestPlanReview.md` frontmatter.
2. Apply only clearly correct improvements:
   - Consistency fixes, such as Section 4 interfaces missing from Section 9.2.
   - Feature-specific priority definitions when the strategy supplies the language.
   - **TBD/actionability:** apply the Evidence policy per occurrence; never invent resolution paths.
     Repair blocking `bare_tbd`/`missing_details` only when sources provide facts. Missing/vague
     versions and incomplete data format/examples are advisory: keep them in `TestPlanGaps.md` and do
     not revise or request documents solely for them. Missing Section 3.1 and unusable RBAC remain
     blocking; Actionability 2/2 requires no blocking gaps.
   - Add content only when directly traceable to strategy, ADR, design spec, API/design docs, or
   `additional_docs`.

   Use the Edit tool for applied auto-fixes.
3. Show the score/verdict, auto-fixes, and remaining `TestPlanGaps.md` gaps.
4. For **Rework**, request source documents before test cases when the remaining failure is a
   blocking grounding or operational gap; advisory actionability gaps alone do not require them.

### Step 4.5: Stamp rubric verdict label

From the test-plan repo, use `frontmatter.py read` with absolute paths for `verdict` and
`auto_revised` from `TestPlanReview.md` and `source_key` from `TestPlan.md`; do not parse YAML by
hand. Add the matching Jira label:

| Verdict | Label |
|---------|-------|
| `Ready` | `test-plan-rubric-pass` |
| `Revise` | `test-plan-rubric-revise` |
| `Rework` | `test-plan-rubric-fail` |

For any other verdict, warn and skip. If `auto_revised=true`, also add
`test-plan-auto-revised`.

```bash
repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)
source_key=$(cd "$repo_root" && \
    uv run python scripts/frontmatter.py read <absolute_path_to_output_dir>/<feature_name>/TestPlan.md source_key)
verdict=$(cd "$repo_root" && \
    uv run python scripts/frontmatter.py read <absolute_path_to_output_dir>/<feature_name>/TestPlanReview.md verdict)
auto_revised=$(cd "$repo_root" && \
    uv run python scripts/frontmatter.py read <absolute_path_to_output_dir>/<feature_name>/TestPlanReview.md auto_revised)

if [ "$auto_revised" = "true" ]; then
    (cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && \
     uv run python scripts/add_jira_labels.py "$source_key" --verdict "$verdict" test-plan-auto-revised)
else
    (cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && \
     uv run python scripts/add_jira_labels.py "$source_key" --verdict "$verdict")
fi
```

Label stamping is **non-blocking**: warn on failure and continue without retrying.

### What this skill does NOT do

- **Sources/feedback:** Fetch only the requested strategy/issue, never child stories. Read ADRs only
  from supplied paths (URLs are metadata). Resolve design specs from a local path or matching Jira
  attachment via `resolve_design_spec.py`; use `/test-plan-resolve-feedback` for PR comments.
- **Test cases/ownership:** Do not create `TC-*.md` or executable tests. Keep Sections 5.1, 6, and
  9.1 as placeholders; Section 5.2 is the category contract. `/test-plan-create-cases` owns case
  files, Sections 5.1, 6.1–6.2, 9.1, and Section 9.2 Test Cases. This skill owns only Section 9.2
  Interface and Section 9.3's change log; downstream tooling fills Coverage.
- **Scope/analysis:** Section 2.1 permits only e2e/system and UI. Cite every AC and grounded NFR;
  never invent objectives, scope, NFR analysis, risks, or mitigations.

$ARGUMENTS
