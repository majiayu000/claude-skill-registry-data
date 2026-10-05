---
name: session-start
description: "Run the mandatory session startup checklist. Reads context docs, checks git status, checks active OpenSpec changes, reports current milestone and branch. TRIGGER when the user says \"start session\", \"begin session\", \"let's get started\", \"starting work\", \"resume session\", \"pick up where I left off\", \"what should I work on\", or at the start of every Claude Code session."
---

# Session Startup Checklist

Run this checklist at the start of every session. No exceptions.

## Step 1: Check Setup

Read `CLAUDE.md` and check if the Setup Checklist has uncompleted items. If so, remind the user.

## Step 2: Load Context Documents

Read these files in order:
1. `docs/openspec-workflow-reference.md` — canonical naming + workflow reference (if present; graceful skip with "workflow ref: not found" notice if missing)
2. `docs/project-brief.md` — living summary: capability map, service registry, skill inventory, ADR index, active work pointer, known debt (if present; graceful skip with "project-brief: not found" notice if missing)
3. `docs/session-startup-checklist.md`
4. `docs/project-naming-standards.md`
5. `docs/current-story.md`
6. `docs/next-prompt.md` (the hub/index)

Then check for branch-specific next-prompt files:
- Get current branch: !`git branch --show-current`
- Detect identifier format via shared utility: `bash .claude/skills/_shared/milestone-format.sh "<id-from-branch>"` outputs `format=M|kebab` and normalizes the id
  - Branch `feature/M1.2.3-description` → identifier `M1.2.3`, format `M`
  - Branch `feature/architecture-compliance-sweep` → identifier `architecture-compliance-sweep`, format `kebab`
- If `docs/next-prompt-[identifier].md` exists, read it too
- If on `main`, check `docs/next-prompt.md` for active milestone pointers and read the relevant files

## Step 3: Check Git State

Current branch and status:
- Branch: !`git branch --show-current`
- Status: !`git status --short`
- Recent commits: !`git log --oneline -5`

## Step 4: Set Status Line

Write the active identifier and step to a **branch-keyed** status file so the status line displays it for the entire session. This prevents multiple sessions from overwriting each other.

Parse the active identifier and current step from `current-story.md`. Determine the branch slug by replacing `/` with `-` in the branch name. Detect format via `.claude/skills/_shared/milestone-format.sh`.

Format by identifier type:
- **Legacy M-format**: `[M#.#] feature-name .# step-name`
  - `[M16.9] ml-model-retraining .3 full-retrain`
  - `[M7.7] app-store-submission`
- **OpenSpec change-id format**: `[<change-id>] <optional-phase>`
  - `[architecture-compliance-sweep] phase 1`
  - `[expand-claude-context-infrastructure]`

Use a single line. The step/phase is optional — include it when a sub-milestone or phase is active.

```bash
# Identifier detected from branch via milestone-format.sh (e.g., M7.7 or architecture-compliance-sweep)
bash .claude/skills/_shared/status-line.sh write "[<identifier>] <phase-or-feature-name>"
```

The helper derives the branch-slug automatically from `git branch --show-current` and writes to `~/.claude/forager-status-<slug>.txt`. All workflow skills that represent a focus transition use this same helper — see [`CLAUDE.md § Status Line (Focus Sync)`](../../../CLAUDE.md).

## Step 5: Check Active OpenSpec Changes

Check if there are any active (non-archived) changes:
```bash
ls openspec/changes/ 2>/dev/null | grep -v archive
```

If active changes exist, read their `tasks.md` to understand what's in progress.

## Step 6: Report

After reading all documents, provide a concise status report:

1. **Current milestone**: What M#.#.# is active, what status
2. **Branch check**: Are we on the correct feature branch? Flag if on `main`
3. **Uncommitted work**: Any staged/unstaged changes?
4. **Setup status**: Any unconfigured items in CLAUDE.md Setup Checklist?
5. **Next action**: What should we work on based on current-story.md and the branch-specific next-prompt

## Step 7: Red Flag Check

Verify:
- [ ] Not on `main` (should be on feature branch for any code work)
- [ ] Branch identifier matches a valid format (M#.#.# legacy OR kebab change-id) — `bash .claude/skills/_shared/milestone-format.sh` exits non-zero on malformed names
- [ ] Current work is documented in current-story.md
- [ ] OpenSpec change exists for active work (or next-prompt file as legacy fallback)
- [ ] No duplicate services being created

If any red flags are found, report them before proceeding.
