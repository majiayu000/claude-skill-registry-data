---
name: backfill-timing
description: "Retrofit YAML frontmatter with pipeline timing metadata onto existing project documents that were created before timing was implemented."
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

# Backfill Timing

You **retrofit YAML frontmatter** with pipeline timing metadata onto existing project artifacts on a WCP work item. This is for projects that completed stages before the timing system was added.

## Inputs

- All artifacts on WCP work item `$ARGUMENTS`
- The current repository — for git commit timestamps

## Before You Start

1. Locate the **conventions file** in the current repo root — look for `CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` (use the first one found). Read it in full.
2. Verify the work item exists by attempting to read artifacts (e.g., `wcp_get_artifact($ARGUMENTS, "prd.md")`).

## Document-to-Stage Mapping

| Document | Stage | Stage Name |
|----------|-------|------------|
| `prd.md` | 0 | prd |
| `discovery-report.md` | 1 | discovery |
| `architecture-proposal.md` | 2 | architecture |
| `gameplan.md` | 3 | gameplan |
| `test-coverage-matrix.md` | 4 | test-generation |
| `progress.md` | 5 | implementation |
| `qa-plan.md` | 7 | qa-plan |

## Step-by-Step Procedure

### 1. Inventory Documents

Read each known artifact by filename via `wcp_get_artifact($ARGUMENTS, filename)`:

- `prd.md`
- `discovery-report.md`
- `architecture-proposal.md`
- `gameplan.md`
- `test-coverage-matrix.md`
- `progress.md`
- `qa-plan.md`

For each that returns content, check if it already has YAML frontmatter with `pipeline_stage` set. If so, **skip it** — it was created with live timing.

### 2. Determine Timestamps per Document

For each document that needs backfilling, try these data sources in priority order:

#### Source A: Git Commit Timestamps (best precision)

For `progress.md`, read its milestone sections. Each milestone section has a `**Commit:** \`SHORT_SHA\`` field. For each commit SHA found:

```bash
git log -1 --format='%aI' <sha>
```

This gives the commit's author date in ISO 8601 format. Use this as `pipeline_mN_completed_at` for the corresponding milestone.

#### Source B: Document Header Dates (day-level precision)

Most documents have a header like `> **Date:** February 5, 2026`. Parse the header from the artifact content and format as `YYYY-MM-DDT00:00:00-0600` (use local timezone offset from `date +%z`).

Use this as `pipeline_completed_at`.

#### Source C: Approval Checklist Dates

For `architecture-proposal.md` and `gameplan.md`, parse the Approval Checklist section from the artifact content. The `### Date:` field contains the approval date. Parse and format as ISO 8601.

Use this as `pipeline_approved_at`.

> **Note:** WCP artifacts don't have filesystem timestamps. If no other source is available (git commits, document header dates, or approval checklist dates), omit the timestamp.

### 3. Write Frontmatter

For each document that needs backfilling:

1. The content was already read in Step 1
2. Prepend the YAML frontmatter block to the content
3. Reattach the modified content using the type mapping below:

```
wcp_attach(
  id=$ARGUMENTS,
  type="<type>",
  title="<title>",
  filename="<filename>",
  content="<modified content with frontmatter>"
)
```

**Type mapping:**

| Filename | type | title |
|----------|------|-------|
| `prd.md` | `prd` | `PRD: [title from content]` |
| `discovery-report.md` | `discovery` | `Discovery Report` |
| `architecture-proposal.md` | `architecture` | `Architecture Proposal` |
| `gameplan.md` | `gameplan` | `Gameplan` |
| `test-coverage-matrix.md` | `test-matrix` | `Test Coverage Matrix` |
| `progress.md` | `progress` | `Implementation Progress` |
| `qa-plan.md` | `qa-plan` | `QA Plan` |

**Standard documents** (prd.md, discovery-report.md, test-coverage-matrix.md, qa-plan.md):

```yaml
---
pipeline_stage: <N>
pipeline_stage_name: "<name>"
pipeline_project: "$ARGUMENTS"
pipeline_completed_at: "<timestamp>"
pipeline_backfilled: true
pipeline_backfill_source: "<source description>"
---
```

Note: `pipeline_started_at` is **omitted** — it cannot be recovered from backfill sources.

**Documents with approval** (architecture-proposal.md, gameplan.md):

```yaml
---
pipeline_stage: <N>
pipeline_stage_name: "<name>"
pipeline_project: "$ARGUMENTS"
pipeline_completed_at: "<timestamp>"
pipeline_approved_at: "<approval timestamp>"
pipeline_backfilled: true
pipeline_backfill_source: "<source description>"
---
```

**progress.md** (per-milestone timing):

```yaml
---
pipeline_stage: 5
pipeline_stage_name: implementation
pipeline_project: "$ARGUMENTS"
pipeline_m1_completed_at: "<timestamp from commit>"
pipeline_m2_completed_at: "<timestamp from commit>"
pipeline_backfilled: true
pipeline_backfill_source: "git commit timestamps"
---
```

### 4. Backfill Source Descriptions

Use these descriptions for the `pipeline_backfill_source` field:

| Source | Description |
|--------|-------------|
| Git commit | `"git commit <short-sha>"` |
| Document header date | `"document header date"` |
| Approval checklist date | `"approval checklist date"` |

If multiple sources were used for different fields, use the primary source.

## What NOT To Do

- **Do not fabricate timestamps.** If no source exists, omit the field.
- **Do not overwrite existing frontmatter.** Skip documents that already have `pipeline_stage` in their frontmatter.
- **Do not modify document content below the frontmatter.** Only prepend/update the YAML block.
- **Do not set `pipeline_started_at` on backfilled documents.** Start times are unrecoverable.

## When You're Done

Post a completion comment:

```
wcp_comment(
  id=$ARGUMENTS,
  author="pipeline/backfill-timing",
  body="Timing frontmatter backfilled for [N] artifacts"
)
```

Tell the user:
1. Which documents were backfilled (and which were skipped)
2. What data sources were used for each document
3. Any documents where no timestamp could be determined
4. **Remind them:** "Backfilled documents have `pipeline_backfilled: true` to distinguish them from live-captured timestamps. Run `/metrics $ARGUMENTS` to see the computed timing data."
