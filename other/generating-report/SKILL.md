---
name: generating-report
description: Generates structured reports including status updates, assessments, post-mortems, and executive summaries. Use when writing a report, creating a project status update, or documenting an incident post-mortem.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch
  argument-hint: "[report-type] [topic]"
  stability: stable
  content-hash: sha256:ed0c11638e37e07dcd465265198d17598dbfc1e9fd6c0d764cc28801733949ec
  last-verified-cc-version: 1.0.34
---

# Report Generation

**Target**: $ARGUMENTS

Generate a structured report based on the requested type and topic.

## References (MUST READ)

Read these before proceeding:

- `references/report-structure.md` — Status, assessment, post-mortem, and executive report formats

## Report Types

| Type | Trigger phrases | Output path |
|------|----------------|-------------|
| **Status** | "status report", "project status", "weekly update" | `docs/reports/<date>-status-<slug>.md` |
| **Assessment** | "assessment", "evaluation", "review" | `docs/reports/<date>-assessment-<slug>.md` |
| **Post-mortem** | "post-mortem", "incident report", "retrospective" | `docs/reports/<date>-postmortem-<slug>.md` |
| **Executive** | "executive summary", "exec summary", "briefing" | `docs/reports/<date>-executive-<slug>.md` |

## Workflow

1. **Detect report type** from arguments — default to Status if ambiguous
2. **Read reference** for the matching report structure
3. **Glob for existing reports** in `docs/reports/` to maintain consistency
4. **Gather context:**
   - Grep for recent changes, TODOs, or relevant code patterns
   - Read project README or CHANGELOG if available
   - WebSearch for external context if needed
5. **Generate the report** using the appropriate structure
6. **Output location** and suggest distribution/follow-up

## Rules

- Always use ISO date format (YYYY-MM-DD) in filenames and content
- Include YAML frontmatter with title, date, type, and author fields
- Post-mortems must be blameless — focus on systems, not individuals
- Status reports must include blockers and next steps
- Executive summaries must fit on one page (roughly 500 words)
- Never fabricate metrics or data — mark unknown values as "TBD"
