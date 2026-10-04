---
name: roadmap
description: >
  Strategic roadmap management for GitHub repositories. Syncs
  ROADMAP.md with GitHub Issues and labels, bootstraps roadmap
  files from scratch, runs brainstorming sessions with boundary
  checking, and provides quick status summaries. Use when managing
  project planning, syncing roadmap state, or exploring feature
  ideas.
compatibility: >
  Requires GitHub CLI (gh) authenticated. Works with any GitHub
  repository that uses Issues and milestones for project planning.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Strategic Roadmap Management

Manage project roadmaps through five modes: sync ROADMAP.md with
GitHub reality, bootstrap planning files from scratch, brainstorm
new features collaboratively, get a quick status summary, or show
help.

## Prerequisite check

```bash
gh --version 2>/dev/null && gh auth status 2>/dev/null
```

If `gh` is not installed, direct the user to
<https://cli.github.com>. If not authenticated, direct them to run
`gh auth login`. Do **not** proceed without a working, authenticated
GitHub CLI.

## Constitutional principle

**CONTEXT.md is the project constitution.** All modes must read and
respect the boundaries defined in CONTEXT.md. If CONTEXT.md exists,
read it first and constrain all analysis and recommendations.

When any recommendation would violate CONTEXT.md boundaries:

1. Explicitly flag the violation
2. Explain which boundary would be crossed
3. Suggest an alternative that respects the boundaries

## Mode dispatch

Determine the mode from the user's input. If no mode is specified,
default to sync.

| Argument | Mode | Purpose |
| -------- | ---- | ------- |
| *(none)* | sync | Sync ROADMAP.md with GitHub, recommend priorities |
| `sync` | sync | Same as default |
| `generate` | generate | Bootstrap CONTEXT.md + ROADMAP.md from scratch |
| `brainstorm` | brainstorm | Creative ideation session (read-only) |
| `status` | status | Quick read-only summary |
| `help` | help | Show available modes |

## Mode: sync

Synchronize ROADMAP.md with GitHub and provide prioritized
recommendations. This is the primary mode.

1. Fetch open issues, recently closed issues, and milestones via
   `gh` CLI
2. Read ROADMAP.md and CONTEXT.md
3. Check for legacy section layout — if found, ask the user whether
   to migrate to canonical structure (Vision → Immediate Focus →
   Near-Term → Future → Completed → Boundaries)
4. Detect discrepancies between ROADMAP.md and GitHub (issues marked
   done but still open, open but closed, missing entirely)
5. Update ROADMAP.md — fix discrepancies, move closed issues to
   "Completed Milestones" under quarterly sub-headings
6. Estimate LOE for open issues without `effort/*` labels using the
   heuristics in `references/label-config.md`
7. Sync GitHub labels — create missing labels, add/remove
   `roadmap/*` labels to match ROADMAP.md sections
8. Append LOE indicators (`[S]`, `[M]`, `[L]`) to issue lines in
   ROADMAP.md
9. Generate 3-5 prioritized recommendations based on dependencies,
   impact vs effort, theme coherence, and LOE balance
10. Present summary of all changes and recommendations

For detailed workflow steps, see `references/sync.md`. For label
definitions and LOE heuristics, see `references/label-config.md`.

## Mode: generate

Bootstrap CONTEXT.md and ROADMAP.md for a new or undocumented
project.

1. If either file exists, ask the user: regenerate, merge, or abort
2. Investigate the codebase — structure, dependencies, entry points,
   capabilities
3. Infer project boundaries ("hard no's") — what the project does
   NOT do
4. Research externally for similar tools and industry context
5. Draft CONTEXT.md with: core identity, technical boundaries, data
   source of truth, interaction model, verification criteria
6. Fetch all GitHub issues and milestones
7. Categorize issues into Immediate Focus, Near-Term, Future, and
   Completed (grouped by quarter)
8. Estimate LOE per open issue and apply `effort/*` labels
9. Draft ROADMAP.md with canonical structure and LOE indicators
10. Write CONTEXT.md first, then ROADMAP.md. Run markdownlint on
    both.

For detailed workflow steps and templates, see
`references/generate.md`. For LOE heuristics, see
`references/label-config.md`.

## Mode: brainstorm

Explore new possibilities through collaborative ideation. This mode
is **read-only by default** — do not create issues or modify
ROADMAP.md until the user explicitly approves.

1. Read CONTEXT.md and ROADMAP.md for current state and boundaries
2. Investigate the codebase for extension points, underutilized
   capabilities, and seams for new features
3. Research externally for similar tools, user requests, and trends
4. Use ideation techniques with the user: "What if...",
   "Who else...", "Why not...", "What's missing...", "What annoys..."
5. Evaluate each idea: boundary check against CONTEXT.md, effort,
   impact, dependencies
6. Present ideas in structured format (description, rationale,
   boundary check, effort, impact, next step)
7. Ask the user which ideas to formalize — only then create issues
   or update ROADMAP.md

For detailed workflow steps and idea template, see
`references/brainstorm.md`.

## Mode: status

Quick read-only summary of current roadmap state. No modifications.

1. Fetch issue counts and milestone progress via `gh` CLI
2. Read ROADMAP.md
3. Present summary tables: overall metrics, by category
   (enhancement/bug/docs), by LOE (small/medium/large)
4. Flag obvious discrepancies without deep analysis

For detailed workflow steps and table templates, see
`references/status.md`.

## Mode: help

Display available modes and usage:

```text
roadmap — Strategic Roadmap Management

MODES:
  (default)    Sync ROADMAP.md + labels with GitHub, recommend priorities
  sync         Same as default
  generate     Bootstrap CONTEXT.md + ROADMAP.md from scratch
  brainstorm   Creative ideation session (collaborative, read-only)
  status       Quick read-only summary of current state
  help         Show this help message

LABELS (synced automatically):
  roadmap/current  → "Immediate Focus" section
  roadmap/next     → "Near-Term Vision" section
  roadmap/future   → "Future Vision" section
  effort/small     → 1-2 hours
  effort/medium    → half day to 1 day
  effort/large     → multi-day

KEY PRINCIPLES:
  CONTEXT.md is the project constitution (all modes respect it)
  Brainstorm mode is read-only until user approves ideas
  Generate mode asks before overwriting existing files
  Labels are synced to match ROADMAP.md sections
  LOE is auto-estimated for issues missing effort/* labels
```

## Output guidelines

- Use tables for structured comparisons
- Use emoji sparingly and only for status indicators
- Always include issue numbers when referencing GitHub issues
- Run markdownlint after any file modifications
