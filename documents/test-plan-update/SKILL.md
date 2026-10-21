---
name: test-plan-update
description: Update an existing test plan with new documentation (ADR, API specs, design specs, design docs). Re-analyzes, updates artifacts, bumps version, and optionally regenerates test cases. Use when requirements evolve or new technical documentation becomes available after initial test plan creation.
argument-hint: "<SOURCE> [<NEW_DOC_PATH>...]"
user-invocable: true
model: claude-opus-4-6
allowedTools:
  - Read
  - Write
  - Edit
  - Bash
  - Skill
  - AskUserQuestion
---

# Test Plan Updater

Update an existing test plan when new information becomes available (ADRs, API specs, design specs,
design documents, requirement changes).

## Usage

```
/test-plan-update <SOURCE> [<NEW_DOC_PATH>...]
```

Examples:
- `/test-plan-update ~/Code/opendatahub-test-plans/plans/ai-hub/mcp_catalog adr.pdf`
- `/test-plan-update ~/Code/opendatahub-test-plans/plans/ai-hub/mcp_catalog ./design-spec.md`
- `/test-plan-update ~/Code/opendatahub-test-plans/plans/ai-hub/mcp_catalog` (pull latest design-spec
  attachment from Jira using TestPlan `source_key`)
- `/test-plan-update https://github.com/org/repo/pull/42 api-spec.md design.md`
- `/test-plan-update https://github.com/org/repo/tree/test-plan/RHAISTRAT-400 requirements-v2.md`

## Inputs

### From arguments
Parse `$ARGUMENTS` to extract:
1. **First argument** (required): Test plan source - can be:
   - Local directory path: `mcp_catalog` or `/path/to/mcp_catalog`
   - GitHub branch: `https://github.com/org/repo/tree/test-plan/RHAISTRAT-400`
   - GitHub PR: `https://github.com/org/repo/pull/5`
2. **Remaining arguments** (optional): Paths to new documentation files (ADR, API
   spec, design spec, design doc, etc.). After setting
   `repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)`, classify each path with the
   deterministic CLI
   (`uv run --project "$repo_root" python "$repo_root/scripts/resolve_design_spec.py" --classify <path>`);
   use `kind` to decide labeling and whether to snapshot as a design spec. If no paths are
   given, set `PULL_JIRA_DESIGN_SPEC=true` to fetch the newest design-spec attachment via
   `source_key` into a temp file in Step 2 (analyzers see it; feature-dir snapshot waits for
   Step 4).

When a new design-spec path is provided:
1. Classify/read it in Step 2, but **do not** snapshot or edit frontmatter yet
2. After the user approves the merge in Step 4, snapshot from `$repo_root` and add it to
   `additional_docs`
3. Pass the staged design-spec content to analyzers / merge / resolve-gaps as **Design Spec**

When `PULL_JIRA_DESIGN_SPEC=true`, fetch into a temp dir in Step 2 (not the feature dir), pass
that path to analyzers/merge as **Design Spec**, then snapshot into `$feature_dir` only after
Step 4 approval via `--local-path "$STAGED_DESIGN_SPEC_PATH"`.

### Interactive fallback
If insufficient arguments are provided, ask the user via AskUserQuestion:
> **Where is the test plan to update?**
>
> You can provide:
> - Local directory path (e.g., `~/Code/opendatahub-test-plans/plans/ai-hub/mcp_catalog`)
> - GitHub branch URL (e.g., `https://github.com/org/repo/tree/test-plan/RHAISTRAT-400`)
> - GitHub PR URL (e.g., `https://github.com/org/repo/pull/5`)

Then ask:
> **What new documentation should be incorporated?**
>
> Provide file paths (ADR, API spec, design spec, etc.), or leave empty to pull the newest
> design-spec attachment from Jira using the plan's `source_key`.

## Process

### Step 0: Pre-flight Checks

#### 0.1 Python dependencies

Install the test-plan package (makes all scripts importable):
```bash
bash "${CLAUDE_SKILL_DIR}/../../scripts/bootstrap.sh" --layout "${CLAUDE_SKILL_DIR}" || exit 1
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv sync --extra dev)
```

If installation fails, inform the user and do NOT proceed. Once installed, all Python scripts will work from any directory.

#### 0.2 Locate Test Plan

1. **Use the shared locate-feature-dir utility**:
   ```bash
   result=$(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/repo.py locate-feature-dir "<source>")
   if [ $? -ne 0 ]; then
       echo "$result"
       exit 1
   fi

   # Parse JSON output
   feature_dir=$(printf '%s\n' "$result" | jq -r '.feature_dir')
   source_type=$(printf '%s\n' "$result" | jq -r '.source_type')
   ```

2. **Validate local paths against skill repository**:
   ```bash
   if [ "$source_type" = "local" ]; then
       # Validate against skill repository (no force flag for updates)
       if [ -n "${FULLSEND_TARGET_REPO_DIR:-}" ]; then
           FULLSEND_TARGET_REPO_DIR=$(cd "$FULLSEND_TARGET_REPO_DIR" && pwd -P) || exit 1
           export FULLSEND_TARGET_REPO_DIR
       fi
       (cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/repo.py validate-local-path "$feature_dir") || exit 1
   fi
   ```

**Note**: GitHub sources are always external repos, so no skill repo validation needed.

#### 0.3 Verify new documents exist

Set `repo_root=$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)`.

If no document paths were provided, set `PULL_JIRA_DESIGN_SPEC=true` (fetch in Step 2 via
`source_key`; feature-dir snapshot waits for Step 4). Otherwise, for each new document path:
```bash
if [ ! -f "$doc_path" ]; then
    echo "❌ ERROR: Document not found: $doc_path"
    exit 1
fi
```

### Step 1: Read Existing Artifacts

1. **Read `<feature_dir>/TestPlan.md`** using Read tool
   - Extract frontmatter: `source_key`, `version`, `feature`, `components`, `additional_docs`
   - Extract original strategy reference (JIRA key)
   - Store current test plan content for comparison

2. **Read `<feature_dir>/TestPlanGaps.md`** (if exists)
   - Extract existing gaps organized by section
   - Store for comparison with new gaps

3. **Read `<feature_dir>/TestPlanReview.md`** (if exists)
   - Note current score and verdict (will be re-evaluated after update)

4. **Read `<feature_dir>/README.md`**
   - Store for updating version and changelog

5. **Check for test cases**: `<feature_dir>/test_cases/INDEX.md`
   - If exists, count test cases for summary
   - Store flag `has_test_cases=true`

### Step 2: Read New Documents

For each new document path:
1. Classify with
   `uv run --project "$repo_root" python "$repo_root/scripts/resolve_design_spec.py" --classify "$doc_path"`
   and use `kind` (`design_spec` | `adr` | `other`) for labeling — do not inspect content yourself.
2. Read the document using Read tool (for binary ADR PDFs, rely on classify + path metadata).
3. Store content with label mapped from kind (`Design Spec`, `ADR`, or inferred other label).
4. If `kind` is `design_spec`, **stage** the path for later snapshot — do **not** write
   `.source-design-spec.md` or edit `additional_docs` yet (wait for Step 4 approval).

If `PULL_JIRA_DESIGN_SPEC=true`, fetch the attachment into a **temp** dir before analysis (do not
write `$feature_dir/.source-design-spec.md` yet):

```bash
tmp_ds_dir=$(mktemp -d)
jira_ds=$(cd "$repo_root" && uv run python scripts/resolve_design_spec.py \
  --issue-key "$source_key" --feature-dir "$tmp_ds_dir" --snapshot) || exit 1
if [ "$(echo "$jira_ds" | jq -r '.has_content')" = "true" ]; then
  STAGED_DESIGN_SPEC_PATH="$tmp_ds_dir/.source-design-spec.md"
fi
```

Read `$STAGED_DESIGN_SPEC_PATH` when set and label it **Design Spec** for Steps 3–5.

### Step 3: Re-analyze with New Material

Invoke the three analyzer skills **in parallel** using the Skill tool, passing:
- Original strategy content (from Jira via source_key, or from local cache)
- Existing additional docs (from frontmatter `additional_docs`)
- New documents (just read in Step 2), including a Jira-fetched design spec at
  `$STAGED_DESIGN_SPEC_PATH` when `PULL_JIRA_DESIGN_SPEC=true`

- **`test-plan.analyze.endpoints`**: Re-extract feature scope and API endpoints
- **`test-plan.analyze.risks`**: Re-determine test levels, types, priorities, risks
- **`test-plan.analyze.infra`**: Re-identify environment, test data, infrastructure needs

Each analyzer returns:
- Updated findings for their sections
- New gaps (if any)
- Resolved gaps (if any were addressed by new docs)

### Step 4: Merge New Findings into TestPlan.md

Invoke the **`test-plan-merge`** forked sub-agent using the Skill tool to intelligently merge new analyzer findings into the existing test plan:

```
Skill: test-plan-merge
Arguments:
  Old TestPlan.md: <full content from Step 1>
  New Findings from Analyzers:
    - Endpoints: <findings from Step 3>
    - Risks: <findings from Step 3>
    - Infrastructure: <findings from Step 3>
  New Documents: <full content from Step 2 with labels>
    Example:
      ADR (adr-v2.pdf):
      <full text content of the ADR>

      API Spec (api-spec.md):
      <full text content of the API spec>
```

**Rationale**: The merge agent needs access to actual document content (not just filenames) to:
- Verify analyzer claims (e.g., "Gap resolved by ADR section 3.2" - agent can check if true)
- Detect contradictions between new docs and existing content
- Make informed decisions about what to merge vs. what to flag for manual review
- Ground merge decisions in source material rather than trusting analyzer summaries

The sub-agent has `context: fork` so it runs in isolation and returns cleanly.

The merge sub-agent returns:
- Updated section content for Sections 1-4, 7-9
- Change summary (what was added/updated/deprecated)
- Statistics (sections updated, items added, user edits preserved)

**Validate merge (manual review)**:
1. Present the change summary to the user:
   ```
   Merge completed. Changes proposed:

   Sections modified: <list from statistics>
   User edits preserved in: <list from statistics>
   Items added: <count>
   Items updated: <count>
   Items deprecated: <count>

   <full change summary from agent>
   ```

2. Ask user via AskUserQuestion:
   > **Review merge changes before applying**
   >
   > The merge agent updated <N> sections. Review the changes above.
   >
   > Proceed with these updates? [yes/no]

3. If **no**: Stop without applying updates (TestPlan.md unchanged; discard staged design-spec
   snapshot/frontmatter changes — nothing was written to `$feature_dir` yet)
4. If **yes**: Continue to apply updates. If `$STAGED_DESIGN_SPEC_PATH` is set, snapshot it now:
   ```bash
   (cd "$repo_root" && uv run python scripts/resolve_design_spec.py \
     --local-path "$STAGED_DESIGN_SPEC_PATH" \
     --feature-dir "$feature_dir" --snapshot) || exit 1
   ```
   Then add `.source-design-spec.md` to `additional_docs` when bumping frontmatter in Step 9.

**Rationale**: Provides manual validation that merge preserved user edits and made sensible decisions. User can review the change summary before committing to the updates.

**Apply the updates**:
1. Use Edit tool to update each modified section in TestPlan.md
2. Store the change summary for use in Step 10
3. Sections 5, 6, 10 (test cases, E2E, traceability) remain unchanged unless test cases are regenerated in Step 7

### Step 5: Resolve Gaps

Invoke the **`test-plan-resolve-gaps`** forked sub-agent using the Skill tool to cross-reference old gaps with new findings:

```
Skill: test-plan-resolve-gaps
Arguments:
  Old Gaps from TestPlanGaps.md: <content from Step 1>
  New Findings from Analyzers:
    - Endpoints: <findings from Step 3>
    - Risks: <findings from Step 3>
    - Infrastructure: <findings from Step 3>
  New Documents: <full content from Step 2 with labels>
    Example:
      ADR (adr-v2.pdf):
      <full text content>
```

**Rationale**: Same as Step 4 - the agent needs actual document content to verify gap resolution claims (e.g., "API versioning now specified in ADR section 2.3" - agent can check if true).

The sub-agent has `context: fork` so it runs in isolation and returns cleanly.

The sub-agent returns:
- Resolved gaps (with which doc/finding resolved them)
- Unresolved gaps (still open)
- New gaps identified by analyzers
- Statistics (total before/after, resolved count)

**Validate gap count arithmetic**:
```bash
# Extract counts from sub-agent statistics
resolved_count=<from_statistics>
unresolved_count=<from_statistics>
new_count=<from_statistics>

# Validate arithmetic (original - resolved + new = unresolved)
(cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/validate.py gap-counts \
    "$feature_dir" $resolved_count $unresolved_count $new_count)

if [ $? -ne 0 ]; then
    echo "⚠️  Gap count mismatch detected. Please review resolve-gaps output manually."
    # Ask user via AskUserQuestion: Continue anyway? [yes/no]
    # If no: exit 1
fi
```

**Update TestPlanGaps.md**:
1. Write the "## Resolved Gaps" section with resolved gaps
2. Write the "## Unresolved Gaps" section (or use original section names)
3. Add "## New Gaps Identified" section if any new gaps
4. Update frontmatter:
   ```bash
   # Get gap count from sub-agent statistics
   new_gap_count=<count_of_unresolved_gaps>

   # Update status: Open if gaps remain, Resolved if all resolved
   new_status=$([ $new_gap_count -eq 0 ] && echo "Resolved" || echo "Open")

   (cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/frontmatter.py set <feature_dir>/TestPlanGaps.md \
       gap_count=$new_gap_count \
       status=$new_status)
   ```

### Step 6: Re-run Quality Review

Invoke **`test-plan.review`** skill with the updated feature directory:
```
/test-plan-review <feature_dir>
```

This generates a new `TestPlanReview.md` with updated score and verdict.

**Handle review output**:
1. Read the new verdict from frontmatter
2. Apply any auto-fix suggestions from the reviewer
3. Store scores for summary (will show in Step 10)

### Step 7: Ask About Test Cases

If `has_test_cases=true` (test cases exist), ask the user via AskUserQuestion:

> **New information has been incorporated into the test plan.**
>
> Changes detected:
> - <summary of what changed: new endpoints, updated risks, etc.>
>
> **Do you want to update the existing test cases?**
>
> 1. **Yes, update test cases** — regenerate affected test cases and add new ones for new coverage
> 2. **No, keep test cases as-is** — only TestPlan.md has been updated
> 3. **Review changes first** — show me the diff before deciding

If user selects option 1:
- Invoke `/test-plan-create-cases <feature_dir>` to regenerate test cases
- The skill will update existing TCs and generate new ones for changed requirements

If user selects option 3:
- Show summary of TestPlan.md changes (what sections were updated)
- Ask again: "Update test cases now? [yes/no]"

### Step 8: Update README.md

Update the README with:
1. New version number (from Step 9 frontmatter update)
2. Updated "Last modified" date
3. Changelog entry:
   ```markdown
   ## Changelog

   ### v1.1.0 (2026-04-23)
   - Updated with new API specification
   - Resolved 3 gaps from TestPlanGaps.md
   - Added 2 new endpoints to Section 4
   ```

### Step 9: Version Bump and Frontmatter Update

1. **Bump version** (minor; if test cases were regenerated, bump twice):
   ```bash
   (cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/version.py bump <feature_dir>/TestPlan.md minor)
   ```
   If test cases were regenerated, run a second minor bump.
   The script outputs JSON with `old_version` and `new_version`.

2. **Update TestPlan.md frontmatter** (additional_docs and other fields):
   ```bash
   (cd "$(cd -P "${CLAUDE_SKILL_DIR}/../.." && pwd -P)" && uv run python scripts/frontmatter.py set <feature_dir>/TestPlan.md \
       additional_docs="<updated_comma_separated_list>")
   ```

3. **Update status** if needed:
   - If was "Draft" and review verdict is "Ready" → set to "Ready for Review"
   - If was "In Review" → keep as "In Review" (PR reviewers will re-review)

### Step 10: Summary

Present final summary to user:
> **Test plan updated successfully**
>
> - **Location**: `<feature_dir>`
> - **Version**: <old_version> → <new_version>
> - **Quality score**: <old_score>/10 → <new_score>/10
> - **Verdict**: <verdict>
> - **Gaps resolved**: <N>
> - **Gaps remaining**: <M>
> - **Test cases**: <updated|unchanged>
>
> Updated artifacts:
> - TestPlan.md
> - TestPlanGaps.md
> - TestPlanReview.md
> - README.md
> - test_cases/ (if regenerated)
>
> **Next steps**:
> - Review changes: `git diff` (if in git repo)
> - Publish updates: `/test-plan-publish <feature_name>`

## What this skill does NOT do

- Does NOT create a new test plan from scratch — use `/test-plan-create` for that
- Does NOT resolve PR review feedback — use `/test-plan-resolve-feedback` for that
- Does NOT commit or push changes to GitHub — use `/test-plan-publish` after updating
- Does NOT modify the original strategy (JIRA issue) — only the test plan
- Does NOT auto-regenerate test cases without asking — always prompts user first

$ARGUMENTS
