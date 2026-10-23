---
name: research-to-issues
description: 'Converts research and planning documents into structured tracking issues. Use when turning research into issues, splitting a feature spec into tasks, or creating issues from a PRP plan.'
argument-hint: '[--dry-run] [--source PATH] [--type TYPE] [--skip-anti-scope] [--skip-gaps]'
---

# Source Documents to GitHub Issues

Convert planning and research output into structured GitHub issues with tracking hierarchy, labels, and priority classification. Parse source documents to extract tasks, features, deliverables, and context, then create well-organized GitHub issues via GitHub MCP server (preferred) or `gh` CLI (fallback).

## Supported Source Types

| Source Type   | Produced By                              | Input Path Pattern                  |
| ------------- | ---------------------------------------- | ----------------------------------- |
| deep-research | `ycc:deep-research`                      | Directory with `RESEARCH-REPORT.md` |
| feature-spec  | `ycc:feature-research`                   | `docs/plans/*/feature-spec.md`      |
| parallel-plan | `ycc:parallel-plan`, `ycc:plan-workflow` | `docs/plans/*/parallel-plan.md`     |
| prp-plan      | `ycc:prp-plan`                           | `docs/prps/plans/*.plan.md`         |
| prd           | `ycc:prp-prd`                            | `docs/prps/prds/*.prd.md`           |

## Current Task

**Processing source for**: `$ARGUMENTS`

Parse arguments:

- **--source PATH**: Path to source file or directory (aliases: `--research-dir`)
- **--type TYPE**: Explicit source type (`deep-research`, `feature-spec`, `parallel-plan`, `prp-plan`). Auto-detected if omitted.
- **--dry-run**: Preview all issues that would be created without creating them
- **--skip-anti-scope**: Skip creating issues for anti-scope/deferred items
- **--skip-gaps**: Skip creating issues for research gaps

**Questions:** class `clarify` (source not found): headless (no question tool or chat turn), print the expected paths and stop; class `confirm-publish` (Step 3 source confirmation): headless, behave as `--dry-run`. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

---

## Tool Preference Strategy

### Step 0a: Detect forge provider

Issue creation is provider-aware. Detect the forge provider on `origin` first
(`forge_detect_provider origin`) and route through the matching CLI:
`gh issue create --title --body` for `github`, `tea issues create --title
--description` for `forgejo`/`gitea`. `validate-prerequisites.sh` runs the same
detection and gates the per-provider issue prerequisites. See
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/forge-detection.md`
for the operation-equivalence map. Log the resolved provider + CLI.

**Forgejo/Gitea caveats**: repo-slug resolution (`gh repo view`) and some label
operations (`gh label create`) are `gh`-only and have no `tea` equivalent — skip
them on `forgejo`/`gitea` (create labels via the Forgejo/Gitea UI, and bind
`tea` to the `origin`-bound repo rather than resolving an owner/name slug). The
GitHub MCP path below applies only to `github`.

### Step 0: Detect GitHub MCP Server

Check if GitHub MCP tools are available by looking for tools matching `mcp__github__*`.

| MCP Tools Available?                 | GitHub Operations Strategy                                                   |
| ------------------------------------ | ---------------------------------------------------------------------------- |
| Yes (`mcp__github__*` tools found)   | **Use MCP tools** for issue creation, label creation, and repository queries |
| No (no `mcp__github__*` tools found) | **Use `gh` CLI** via Bash for all GitHub operations                          |

**Always CLI regardless:** git operations, validation script, file reading/analysis.

**Important**: Lack of MCP tools must NEVER block the workflow. If a specific MCP call fails, fall back to the equivalent `gh` CLI command.

---

## Phase 0: Validate Prerequisites

**WARNING: This skill does NOT check for existing issues. Running it twice creates duplicates. Warn the user before proceeding if issues may have already been created from this source.**

### Step 1: Identify Source

Determine the source path:

1. If `--source PATH` or `--research-dir PATH` is specified, use that path
2. Otherwise, search for common locations: `docs/plans/`, `docs/prps/plans/`, `docs/prps/prds/`, `docs/research/`, `research/`
3. If not found, ask the user to specify the path

### Step 2: Run Validation

```bash
${CLAUDE_PLUGIN_ROOT}/skills/research-to-issues/scripts/validate-prerequisites.sh "<source-path>" --type "<type-if-specified>"
```

The script auto-detects the source type and outputs `DETECTED_TYPE: <type>`. Parse this from stdout.

If validation fails, evaluate:

- **If `gh` CLI missing BUT MCP tools available**: Proceed
- **If `gh` CLI fails AND no MCP tools**: Stop
- **If source path or git repo validation fails**: Stop regardless

### Step 3: Confirm Source Type

Display the detected source type and source path to the user for confirmation before proceeding.

---

## Phase 1: Parse Source Document

### Step 4: Load Type-Specific Parser

Read the parsing reference for the detected source type:

| Detected Type | Reference File                                                                      |
| ------------- | ----------------------------------------------------------------------------------- |
| deep-research | `${CLAUDE_PLUGIN_ROOT}/skills/research-to-issues/references/parse-deep-research.md` |
| feature-spec  | `${CLAUDE_PLUGIN_ROOT}/skills/research-to-issues/references/parse-feature-spec.md`  |
| parallel-plan | `${CLAUDE_PLUGIN_ROOT}/skills/research-to-issues/references/parse-parallel-plan.md` |
| prp-plan      | `${CLAUDE_PLUGIN_ROOT}/skills/research-to-issues/references/parse-prp-plan.md`      |
| prd           | `${CLAUDE_PLUGIN_ROOT}/skills/research-to-issues/references/parse-prd.md`           |

Follow the extraction instructions in the reference to produce:

- **tracking_units**: List of `{title, description, metadata, success_criteria}` -- these become tracking issues
- **child_items**: List of `{title, body_fields, labels, parent_tracking_unit}` -- these become child issues
- **extra_items**: List of `{title, body_fields, labels, group}` -- anti-scope, gaps, decisions (optional)

### Step 5: Classify Priority

Read `${CLAUDE_PLUGIN_ROOT}/skills/research-to-issues/references/label-taxonomy.md` for priority assignment rules by source type. Apply priority labels to each item.

---

## Phase 2: Plan Issue Creation

### Step 6: Build Issue Plan

Construct a complete plan:

- **For each tracking unit** -> 1 tracking issue with checkbox list of child items
- **For each child item** -> 1 child issue with full agentic context
- **For each extra item** -> 1 child issue grouped under appropriate tracker

### Step 7: Compute Labels

Collect all unique labels needed. Read `${CLAUDE_PLUGIN_ROOT}/skills/research-to-issues/references/label-taxonomy.md` for the full color scheme. Always include the `source:{type}` provenance label.

### Step 8: Display Plan

Read `${CLAUDE_PLUGIN_ROOT}/skills/research-to-issues/references/plan-display-format.md` and display the plan using the format appropriate for the detected source type.

### Step 9: Check for Dry Run

If `--dry-run` is present in `$ARGUMENTS`: display the plan and **STOP**. Do not create any issues or labels.

Output: "Dry run complete. Remove --dry-run to create these issues."

---

## Phase 3: Create Issues

### Step 10: Create Missing Labels

For each label not already in the repo:

**MCP (preferred):** `mcp__github__create_label` with owner, repo, name, color (no `#` prefix), description.

**CLI fallback:**

```bash
gh label create "<label-name>" --description "<description>" --color "<hex-color>" --force
```

### Step 11: Create Child Issues First

Create all child issues before tracking issues (tracking issues need the child issue numbers for checkbox links).

Select the template based on source type:

| Source Type                      | Template                                                                     |
| -------------------------------- | ---------------------------------------------------------------------------- |
| deep-research, feature-spec, prd | `${CLAUDE_PLUGIN_ROOT}/skills/research-to-issues/templates/feature-issue.md` |
| parallel-plan, prp-plan          | `${CLAUDE_PLUGIN_ROOT}/skills/research-to-issues/templates/task-issue.md`    |

**MCP (preferred):** `mcp__github__create_issue` with owner, repo, title, body, labels array.

**CLI fallback:**

```bash
gh issue create --title "<title>" --body "$(cat <<'EOF'
<composed-body>
EOF
)" --label "<label1>,<label2>,..."
```

Capture the issue number from each created issue. Map item identifiers to issue numbers.

### Step 12: Create Extra Issues

Same process as Step 11 for anti-scope items, research gaps, and decision items using appropriate template variants from `feature-issue.md`.

### Step 13: Create Tracking Issues

Compose tracking issue bodies using `${CLAUDE_PLUGIN_ROOT}/skills/research-to-issues/templates/tracking-issue.md`. Populate checkbox lists with links to child issue numbers (e.g., `- [ ] #42 Set up data models`).

**MCP (preferred):** `mcp__github__create_issue` with title `"Phase {N}: {title}"` or `"Batch {N}: {title}"`, body, labels.

**CLI fallback:**

```bash
gh issue create --title "Phase {N}: {title}" --body "$(cat <<'EOF'
<composed-body>
EOF
)" --label "tracking,phase:{N},priority:high,source:{type}"
```

---

## Phase 4: Summary

### Step 14: Display Results

```markdown
# Issues Created Successfully

**Repository**: {owner/repo}
**Source type**: {detected_type}
**Total issues created**: {count}
**Labels created**: {count}

## Tracking Issues

| Group   | Title         | Issue | Child Issues |
| ------- | ------------- | ----- | ------------ |
| Phase 1 | Foundation    | #XX   | {count}      |
| Phase 2 | Core Platform | #XX   | {count}      |

## All Issues

| #   | Issue | Title              | Labels                            |
| --- | ----- | ------------------ | --------------------------------- |
| 1   | #XX   | Set up data models | type:task, phase:1, priority:high |

## Next Steps

1. Review tracking issues for completeness
2. Assign issues to milestones if desired
3. Prioritize and assign to team members
4. Use `under-review` filter to find items needing decision
```

---

## Important Notes

- **Always show the plan first** -- never create issues without displaying the plan (Step 8)
- **Dry-run is safe** -- encourage using `--dry-run` on first invocation
- **Labels are created with --force** -- safe to run multiple times
- **Issue order matters** -- create child issues before tracking issues (need issue numbers)
- **MCP-first** -- GitHub operations prefer MCP tools with automatic `gh` CLI fallback
- **No implementation** -- this skill creates issues only. It does not write code or create plans.
- **Templates are guides** -- adapt fields to whatever is actually present in the source
- **Agentic-friendly** -- every child issue includes mandatory reading, scope, implementation guidance, and validation criteria to support autonomous engineering workflows

---

## Additional Resources

### Reference Files

Type-specific parsing instructions:

- **`references/parse-deep-research.md`** -- read when parsing a `deep-research` source (document extraction)
- **`references/parse-feature-spec.md`** -- read when parsing a `feature-spec` source (document extraction)
- **`references/parse-parallel-plan.md`** -- read when parsing a `parallel-plan` source (document extraction)
- **`references/parse-prp-plan.md`** -- read when parsing a `prp-plan` source (document extraction)
- **`references/parse-prd.md`** -- read when parsing a `prd` source (document extraction)

Shared references:

- **`references/label-taxonomy.md`** -- read when assigning priority or creating labels (complete scheme with colors and priority rules)
- **`references/plan-display-format.md`** -- read when displaying the parsed plan (format per source type)

### Templates

- **`templates/tracking-issue.md`** -- Tracking issue body structure
- **`templates/feature-issue.md`** -- Feature, anti-scope, and research gap issues
- **`templates/task-issue.md`** -- Implementation task issues (plan-sourced)

### Scripts

- **`scripts/validate-prerequisites.sh`** -- Run in Step 2 for multi-source validation and type detection (`DETECTED_TYPE` on stdout); do not source it
