---
name: metrics
description: "Compute and display pipeline timing metrics for a project by reading YAML frontmatter from all project documents."
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

# Metrics

You **compute pipeline timing metrics** for a project by reading the YAML frontmatter from all project artifacts on a WCP work item, enriching with git/PR data, and producing a metrics report.

## Inputs

- All artifacts on WCP work item `$ARGUMENTS`
- The current repository — for git and PR data

## Before You Start

1. Locate the **conventions file** in the current repo root — look for `CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` (use the first one found). Read it in full. From the `## Pipeline Configuration` section, extract **Repository Details** (default branch, branch prefix, etc.).
2. Verify the work item exists: `wcp_get($ARGUMENTS)` or attempt to read any artifact.

## Step-by-Step Procedure

### 1. Read All Frontmatter

Read each of these artifacts via `wcp_get_artifact($ARGUMENTS, filename)`:
- `prd.md`
- `discovery-report.md`
- `architecture-proposal.md`
- `gameplan.md`
- `test-coverage-matrix.md`
- `progress.md`
- `review-report.md`
- `qa-plan.md`

For each that returns content, extract the YAML frontmatter (lines between the opening and closing `---` markers). Skip any that don't exist.

Parse these fields from each document:
- `pipeline_stage`
- `pipeline_stage_name`
- `pipeline_started_at`
- `pipeline_completed_at`
- `pipeline_approved_at` (architecture-proposal.md, gameplan.md)
- `pipeline_backfilled` (boolean)
- `pipeline_m*_started_at` / `pipeline_m*_completed_at` (progress.md)
- `pipeline_pr_created_at` / `pipeline_pr_url` (progress.md)

### 2. Enrich with Git/PR Data

Check for PR merge data:

```bash
gh pr list --head '<branch-prefix>$ARGUMENTS' --state merged --json mergedAt,createdAt,url --limit 1
```

If a merged PR is found, extract `mergedAt` and `createdAt`. If no merged PR, try open PRs:

```bash
gh pr list --head '<branch-prefix>$ARGUMENTS' --state open --json createdAt,url --limit 1
```

### 3. Compute Metrics

For each stage, compute:
- **Duration**: `completed_at - started_at` (if both exist)
- **Wait → Next**: time between this stage's `completed_at` and the next stage's `started_at`

For stages with approval checkpoints:
- **Stage Duration**: `completed_at - started_at` (agent work time)
- **Human Review Time**: `approved_at - completed_at` (time waiting for human approval)

For implementation milestones:
- **Per-milestone duration**: `mN_completed_at - mN_started_at`
- **Total implementation time**: sum of all milestone durations

Compute summary metrics:
- **Total Lead Time**: First stage `started_at` (or `completed_at` if backfilled) → PR merge time (or latest `completed_at`)
- **Active Agent Time**: Sum of all stage durations (where both started_at and completed_at exist)
- **Human Review Time**: Sum of approval wait times (architecture + gameplan)
- **Idle/Queue Time**: Total Lead Time - Active Agent Time - Human Review Time
- **Agent Efficiency**: Active Agent Time / (Active Agent Time + Idle/Queue Time)

### 4. Format Durations

Format all durations in human-readable form:
- Under 1 hour: `Xm` (e.g., `25m`)
- 1-24 hours: `Xh Ym` (e.g., `2h 15m`)
- Over 24 hours: `Xd Yh` (e.g., `3d 2h`)

### 5. Write Metrics Report

Attach the metrics report to the work item:

```
wcp_attach(
  id=$ARGUMENTS,
  type="metrics",
  title="Pipeline Metrics",
  filename="metrics.md",
  content="[metrics report]"
)
```

Use this template for the report content:

```markdown
# Pipeline Metrics — $ARGUMENTS

> Generated: <current date/time>
> Data quality: [live / partially backfilled / fully backfilled]

## Stage Timeline

| Stage | Document | Started | Completed | Duration | Wait → Next |
|-------|----------|---------|-----------|----------|-------------|
| 0: PRD | prd.md | ... | ... | ... | ... |
| 1: Discovery | discovery-report.md | ... | ... | ... | ... |
| 2: Architecture | architecture-proposal.md | ... | ... | ... | — |
| 2→3: Human Review | — | ... | approved ... | ... | — |
| 3: Gameplan | gameplan.md | ... | ... | ... | — |
| 3→4: Human Review | — | ... | approved ... | ... | — |
| 4: Test Generation | test-coverage-matrix.md | ... | ... | ... | ... |
| 5: Implementation | progress.md | — | — | — | — |
| 5/M1 | — | ... | ... | ... | ... |
| 5/M2 | — | ... | ... | ... | ... |
| [continue for each milestone] | | | | | |
| 7: QA Plan | qa-plan.md | ... | ... | ... | ... |
| PR Created | — | — | ... | — | ... |
| PR Merged | — | — | ... | — | — |

Use `—` for fields where data is unavailable.

## Summary

| Metric | Value |
|--------|-------|
| **Total Lead Time** (PRD start → PR merge) | ... |
| **Active Agent Time** | ... |
| **Human Review Time** | ... |
| **Idle/Queue Time** | ... |
| **Agent Efficiency** | ...% |

## Implementation Breakdown

| Milestone | Duration | Files | Tests |
|-----------|----------|-------|-------|
| M1 | ... | ... | ... |
| M2 | ... | ... | ... |
| **Total** | ... | ... | ... |

[If milestone-level data is available from progress.md]

## Data Quality Notes

- [Note which stages have live vs backfilled timestamps]
- [Note any stages with missing data]
- [Note if started_at is missing (backfilled documents)]
```

### 6. Handle Missing Data

- If a field is missing, display `—` in the table
- If `started_at` is missing (backfilled), duration cannot be computed — show `—` for duration
- If only `completed_at` exists, still show it in the timeline for ordering
- Note data quality issues in the "Data Quality Notes" section

### 7. Post Summary Comment

Add a comment to the work item summarizing the metrics:

```
wcp_comment(
  id=$ARGUMENTS,
  author="pipeline/metrics",
  body="Metrics report attached as metrics.md — [brief summary of key metrics]"
)
```

## What NOT To Do

- **Do not modify any project artifacts.** Only produce `metrics.md`.
- **Do not fabricate timestamps.** Use `—` for missing data.
- **Do not run pipeline stages.** This is a read-only analysis tool.

## When You're Done

Tell the user:
1. The metrics report has been attached to `$ARGUMENTS` as `metrics.md`
2. Summarize key metrics: total lead time, active agent time, agent efficiency
3. Note any data quality limitations (backfilled vs live data)
