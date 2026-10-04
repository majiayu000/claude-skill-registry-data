---
name: workflow-runs-analysis
description: Read-only analysis of workflow runs from the durable ledger. Produces validated process-quality findings. Default window last 24h. Report mivia-report/v1.
triggers:
  - analyze workflow runs
  - workflow run analysis
  - analyze the ledger
  - process quality report
tools:
  - workflow_list_runs
  - workflow_status
  - workflow_events
  - workflow_inspect
argument-hint: "Time frame (optional): 24h|7d|ISO range; default last 24h"
short-description: Analyze workflow-run ledger for process-quality findings
user-invocable: true
---

This skill is defined in `.agents/skills/workflow-runs-analysis/SKILL.md`.

Read that file now and follow it exactly. It is the only definition. This file
is an alias so Claude Code can find the skill. Bundled resources live beside
the canonical file.
