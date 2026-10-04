---
name: quality
description: "Generate a code quality report for a pipeline project by reading quality frontmatter from progress.md and optionally running fresh analysis."
argument-hint: "<callsign>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - mcp__wcp__wcp_get_artifact
  - mcp__wcp__wcp_attach
  - mcp__wcp__wcp_comment
---

# Quality

You **generate a code quality report** for a pipeline project by reading the `pipeline_quality_*` frontmatter from `progress.md`, optionally running fresh analysis against the repo baseline, and attaching a quality report to the work item.

## Inputs

- `wcp_get_artifact($ARGUMENTS, "progress.md")` — quality frontmatter from Stage 5 implementation milestones
- The current repository — for running fresh baseline and per-file analysis
- The conventions file — for Complexity Analysis tool configuration

## Before You Start

1. Locate the **conventions file** in the current repo root — look for `CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` (use the first one found). Read it in full. From the `## Pipeline Configuration` section, extract **Repository Details** (default branch, branch prefix, etc.), and look for a **Complexity Analysis** section.
2. Read progress.md: `wcp_get_artifact($ARGUMENTS, "progress.md")`

If progress.md does not exist, **STOP**:

> "No progress artifact found for `$ARGUMENTS`. Run Stage 5 implementation first."

## Step-by-Step Procedure

### 1. Read Quality Frontmatter

`wcp_get_artifact($ARGUMENTS, "progress.md")` — extract YAML frontmatter. Parse all `pipeline_quality_*` fields:

**Per-milestone fields** (pattern: `pipeline_quality_mN_*`):
- `pipeline_quality_mN_flog_avg`
- `pipeline_quality_mN_flog_max`
- `pipeline_quality_mN_flog_max_method`
- `pipeline_quality_mN_files_analyzed`

**Project summary fields** (written by `/create-pr`):
- `pipeline_quality_flog_avg`
- `pipeline_quality_repo_baseline_flog_avg`
- `pipeline_quality_delta`
- `pipeline_quality_verdict`
- `pipeline_quality_files_analyzed`

If **no** `pipeline_quality_*` fields exist in the frontmatter, **STOP** with a helpful message:

> "No quality data found in progress.md for `$ARGUMENTS`. Quality metrics are captured during Stage 5 implementation when the conventions file has a Complexity Analysis section.
>
> To add quality data to an existing project, a future `/backfill-quality` skill (ROAD-20 v2) will support checking out old branches and running analysis retroactively."

### 2. Run Current Repo Baseline

If the conventions file has a Complexity Analysis section, run the repo baseline command for a fresh comparison:

```bash
<repo-baseline-command>
```

Parse the output to extract the current repo-wide flog/method average. Store as `current_baseline`.

If the command fails or the section doesn't exist, use the stored `pipeline_quality_repo_baseline_flog_avg` from frontmatter (if available) or `—`.

### 3. Fresh Per-File Analysis (Optional)

Check if the project branch still exists:

```bash
git branch --list '<branch-prefix>$ARGUMENTS'
```

If the branch exists:
1. Check out the branch: `git checkout <branch-prefix>$ARGUMENTS`
2. Get all pipeline-touched files: `git diff --name-only origin/<default-branch>...<branch-prefix>$ARGUMENTS -- '<file-glob>'` (exclude spec/)
3. Run the score command on each file to get fresh per-file scores
4. Run the per-file command on files with the highest scores to identify current hotspot methods
5. Check out the previous branch: `git checkout -`

If the branch does not exist (already merged/deleted), note this in the report and rely solely on frontmatter data.

**Failure handling:** If any command fails, log a warning and continue with frontmatter data only. Never fail the report because of a stale branch.

### 4. Write Quality Report

Attach the quality report to the work item:

```
wcp_attach(
  id=$ARGUMENTS,
  type="quality",
  title="Quality Report",
  filename="quality.md",
  content="[quality report]"
)
```

Use the following template for the report content:

```markdown
# Code Quality Report — $ARGUMENTS

> Generated: <current date/time>
> Tool: [tool name from Pipeline Configuration, or from frontmatter context]
> Hotspot threshold: [threshold from Pipeline Configuration, or "unknown"]

## Quality Scorecard

| Metric | Value |
|--------|-------|
| **Project flog avg** | [from frontmatter or fresh analysis] |
| **Repo baseline avg** | [current_baseline or stored baseline] |
| **Delta** | [delta] |
| **Verdict** | [verdict] |
| **Total files analyzed** | [files_analyzed] |

## Per-Milestone Breakdown

| Milestone | Flog Avg | Flog Max | Max Method | Files |
|-----------|----------|----------|------------|-------|
| M1 | [m1_flog_avg] | [m1_flog_max] | [m1_flog_max_method] | [m1_files_analyzed] |
| M2 | ... | ... | ... | ... |
[One row per milestone with quality data]

## Hotspots

[Top 5 methods above the hotspot threshold, from fresh analysis if available, otherwise from per-milestone flog_max data]

| Score | Method | Source |
|-------|--------|--------|
| [score] | [ClassName#method_name] | [file path or milestone] |

[If no methods above threshold: "No methods above the hotspot threshold of [threshold]."]

## Baseline Context

| Metric | Value |
|--------|-------|
| **Stored baseline** (at PR time) | [pipeline_quality_repo_baseline_flog_avg] |
| **Current baseline** | [current_baseline or "—"] |
| **Baseline drift** | [current - stored, or "—"] |

> Baseline drift shows how the repo average has changed since the PR was created. A rising baseline means overall repo complexity is increasing.

## Data Quality Notes

- [Note whether data is from frontmatter only or includes fresh analysis]
- [Note if project branch was available for fresh analysis]
- [Note any milestones missing quality data]
- [Note if baseline was live or stored]
```

### 5. Handle Missing Data

- If a per-milestone field is missing, display `—` in the table
- If project summary fields are missing (no `/create-pr` run yet), compute from per-milestone data if possible
- If the branch is gone, note "Fresh analysis unavailable — branch merged/deleted" and use frontmatter only
- Use `—` for any metric that cannot be computed

### 6. Post Completion Comment

Add a comment to the work item summarizing the quality report:

```
wcp_comment(
  id=$ARGUMENTS,
  author="pipeline/quality",
  body="Quality report attached as quality.md — [verdict summary]"
)
```

## What NOT To Do

- **Do not modify any project documents.** Only attach `quality.md` to the WCP work item.
- **Do not modify source code.** This is a read-only analysis tool.
- **Do not fabricate scores.** Use `—` for missing data.
- **Do not run pipeline stages.** This is a standalone reporting tool.
- **Do not leave the repo on a different branch.** Always `git checkout -` after analysis.

## When You're Done

Tell the user:

1. The quality report has been attached to `$ARGUMENTS` as `quality.md`
2. Summarize key metrics: project flog avg, delta from baseline, verdict
3. Highlight any hotspots above threshold
4. Note data quality limitations (frontmatter vs fresh, branch availability)
