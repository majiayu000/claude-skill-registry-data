---
name: memory-bank
description: Use when CLAUDE.md or CLAUDE-*.md memory-bank files need creating, auditing, updating, or syncing with the codebase — after significant code changes, when documented patterns contradict the implementation, at session end to capture learnings, or when context files have grown stale or bloated.
---

# Memory Bank Maintenance

## Overview

One skill for the whole memory-bank lifecycle (CLAUDE.md plus the
CLAUDE-activeContext / patterns / decisions / troubleshooting /
config-variables files). Replaces the claude-md-management and
codebase-documenter plugins and the update-memory-bank, analyze-codebase,
and cleanup-context commands — if any of those are still visible, use this
skill instead.

## Ground rules

- Every line in these files is prompt cost in every future session: one line
  per concept, no verbose explanations, no information git already records
  (history, past fixes, code structure that is obvious from reading it).
- Verify claims against the actual code before writing them down — a wrong
  memory is worse than no memory.
- Preserve planning, historical, and strategic notes when syncing; drift
  fixes update facts, they don't erase intent.
- Never delete CLAUDE.md or CLAUDE-*.md files; never commit them unless the
  user asks (repo rule: exclude from commits).
- Convert relative dates ("last week") to absolute dates when capturing.

## Modes

**capture** (end of session / "remember this"): reflect on what context was
missing this session — commands discovered, style patterns, config quirks,
gotchas. Add the few that will recur to the right file: shared → CLAUDE.md,
session state → CLAUDE-activeContext.md, conventions → CLAUDE-patterns.md,
rationale → CLAUDE-decisions.md, proven fixes → CLAUDE-troubleshooting.md.
Create a memory-bank file only if a learning belongs there and the file
doesn't exist yet.

**sync** ("docs don't match the code"): for each memory-bank file, check its
claims against the implementation; fix what drifted, flag what you're unsure
about. For a large sweep, spawn one general-purpose subagent per file on
`sonnet` (fact-checking docs against code is execution-heavy — see the
model-routing rule in CLAUDE.md) and have each return a list of stale claims
with file:line evidence.

**audit** ("check/improve our CLAUDE.md files"): find all CLAUDE.md files
(`fd CLAUDE.md`), then per file: commands that no longer exist, wrong paths,
duplicated guidance, bloat (cut it via optimize mode), missing load-bearing
context. Report before editing.

**optimize** ("context files too big"): dedupe across files, collapse
narratives into single-line facts, move project-specific detail out of the
global file. Show the diff of what gets cut.

## Common mistakes

- Writing session narrative ("today we fixed…") instead of reusable facts.
- Recording one-off fixes that will never recur.
- Trimming so aggressively the why behind a decision is lost — keep the
  one-line rationale.
