---
name: batch-fix
description: 'Applies one mechanical fix or compliance check across many skill, agent and phase files, with approval before any edit. Use when the user wants a "batch fix", "mass edit" or "bulk compliance fix" to "apply across plugins". Not for one file.'
argument-hint: <free-form task brief describing what to check and what to change>
allowed-tools: Agent, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

## Overview

Repo-local discipline skill that mass-applies a single check-and-fix across skill, phase, and agent files under `plugins/`. A free-form task brief is expanded into numbered criteria; haiku proposer agents run in parallel waves and emit targeted before/after edits per file; the orchestrator aggregates the edits into a unified diff and applies them only after two explicit user approvals. Never commits.

## When to Use

- Enforcing a newly-codified guideline retroactively across every plugin file.
- Replacing a boilerplate phrase, header, or frontmatter shape that is duplicated in many files.
- Sweeping in a consistent fix the audit skill already identified as systemic.
- Trigger phrases: "batch fix", "apply across all plugins", "mass edit", "bulk compliance fix".

### When NOT to use

- Fixing a single known file — just `Edit` it directly.
- Refactoring internal logic, restructuring content, or rewriting prose — this skill is for deterministic mechanical rewrites only.
- Version bumps across `plugin.json` / `marketplace.json` — use `./set_versions.sh`.
- Changing source code inside `plugins/<name>/scripts/` or any non-markdown asset — scan globs target skills, phases, and agents only.

## Constants

- **MAX_PARALLEL**: 6
- **TASK_DIR**: `.mz/task/`
- **SCAN_GLOBS**:
  - `plugins/*/skills/**/SKILL.md`
  - `plugins/*/skills/**/phases/*.md`
  - `plugins/*/agents/*.md`

## Arguments

`$ARGUMENTS` is the free-form task brief. It must describe both what to check for and what to change. Examples:

- "Every skill's Phase 1.5 gate must end with the canonical approve/reject/feedback string."
- "Every haiku agent description must start with 'Pipeline-only.' and include 'When NOT to use:' in the body."
- "Remove every `Co-Authored-By` line from agent files."

If `$ARGUMENTS` is empty, escalate via AskUserQuestion — never guess the brief.

## Core Process

### Phase Overview

| Phase | Goal                    | Details                 |
| ----- | ----------------------- | ----------------------- |
| 0     | Setup                   | Inline below            |
| 1     | Scan + expand brief     | `phases/scan.md`        |
| 1.5   | Gate 1: brief + files   | Inline below            |
| 2     | Propose (parallel)      | `phases/dispatch.md`    |
| 3     | Consolidate             | `phases/consolidate.md` |
| 3.5   | Gate 2: aggregated diff | Inline below            |
| 4     | Apply                   | `phases/apply.md`       |

### Phase 0: Setup

1. If `$ARGUMENTS` is empty, escalate via AskUserQuestion with a prompt requesting the free-form brief. Never fabricate one.
1. `task_name` = `<YYYY_MM_DD>_batch-fix_<slug>` where `<YYYY_MM_DD>` is today's date (underscores, not dashes) and `<slug>` is a snake_case summary of the brief (max 20 chars). On same-day collision append `_v2`, `_v3`.
1. Create `.mz/task/<task_name>/` and the subdirectory `.mz/task/<task_name>/proposals/`.
1. Write `state.md` with `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `Brief: <original $ARGUMENTS>`, `Scan globs: <list>`.
1. Emit a visible setup block showing `task_name`, working dir, and scan globs.

### Phase 1 — Scan + expand brief

See `phases/scan.md`.

### Phase 1.5: Gate 1 — brief + scoped file list

**This orchestrator** (not a subagent) must present to the user via AskUserQuestion. This step is interactive and must not be delegated.

Before invoking AskUserQuestion, Read `.mz/task/<task_name>/criteria.md` and `.mz/task/<task_name>/candidates.md` in full. The question body must contain the **verbatim contents** of both artifacts. Do not substitute a path, summary, or placeholder — present the full text.

Use AskUserQuestion with:

```
Batch-fix scope ready. Please review:

=== criteria.md ===
<verbatim contents of criteria.md>

=== candidates.md ===
<verbatim contents of candidates.md>

Reply 'approve' to proceed, 'reject' to abort, or provide feedback for changes.
```

**Response handling**:

- **"approve"** → update `state.md` to `scope_approved`, proceed to Phase 2.
- **"reject"** → update `state.md` to `aborted_by_user` and stop. Do not proceed.
- **Feedback** → adjust the brief, criteria, or candidate list per the feedback, re-run Phase 1 if the criteria or globs changed, then return to this gate and re-present **via AskUserQuestion** using the same format. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.

### Phase 2 — Propose (parallel)

See `phases/dispatch.md`.

### Phase 3 — Consolidate

See `phases/consolidate.md`.

### Phase 3.5: Gate 2 — aggregated diff

**This orchestrator** (not a subagent) must present to the user via AskUserQuestion. This step is interactive and must not be delegated.

Before invoking AskUserQuestion, Read `.mz/task/<task_name>/diff.md` in full. The question body must contain the **verbatim contents** of `diff.md`. Do not substitute a path, summary, or placeholder — present the full text.

Use AskUserQuestion with:

```
Proposed edits ready for review. Please inspect:

=== diff.md ===
<verbatim contents of diff.md>

Reply 'approve' to proceed, 'reject' to abort, or provide feedback for changes.
(feedback examples: "skip edit e3 in vault-review", "skip all edits in file X", "re-run with narrower criterion 2")
```

**Response handling**:

- **"approve"** → update `state.md` to `diff_approved`, proceed to Phase 4 applying every edit in `edits.json`.
- **"reject"** → update `state.md` to `aborted_by_user` and stop. Do not write any file.
- **Feedback** → parse skip directives into an exclusion list (edit ids and/or file paths) and regenerate `diff.md` / `edits.json` without those edits. If the feedback requires re-running proposers with tighter criteria, update `criteria.md` and re-run Phase 2 for the affected files. Return to this gate and re-present **via AskUserQuestion** using the same format. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 4 without explicit approval.

### Phase 4 — Apply

See `phases/apply.md`.

## Techniques

Techniques: delegated to phase files — see Phase Overview table above.

## Common Rationalizations

| Rationalization                                                        | Rebuttal                                                                                                                                                                    |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "The fix is trivial — skip Gate 1 and go straight to proposals."       | "The per-file candidate list is where scope mistakes get caught. Skipping Gate 1 is how an unintended `plugin.json` edit slips into a mass rewrite and corrupts manifests." |
| "Proposals look fine in the summary, skip Gate 2."                     | "Gate 2 is the only place the user sees every old/new pair together. A haiku agent hallucinating a near-miss Edit is caught here or nowhere."                               |
| "Let the proposer use Write instead of emitting edits — it's simpler." | "Proposer writing directly removes the aggregate review surface and breaks the propose-only contract. Orchestrator applies, proposer proposes — never cross the line."      |

## Red Flags

- Dispatching proposers before Gate 1 approval.
- Applying any edit without Gate 2 approval.
- Proposer agents writing to plugin files directly instead of to `.mz/task/<task_name>/proposals/`.
- Treating `DONE_NO_CHANGE` as an error — a file being already compliant is the expected outcome for most batches.
- Committing after apply — this skill never commits; the user commits when ready.

## Verification

Print this block before concluding — silent checks get skipped:

```
batch-fix verification:
  [ ] Gate 1 was presented via AskUserQuestion with verbatim criteria.md + candidates.md
  [ ] Gate 2 was presented via AskUserQuestion with verbatim diff.md
  [ ] Every applied edit came from edits.json; no ad-hoc orchestrator rewrites
  [ ] summary.md lists files changed, files skipped, and apply failures
  [ ] state.md Status is `completed` with Completed timestamp
  [ ] No commit was created
```

If any box is unchecked, the skill did not run correctly — report the failure explicitly rather than claiming success.

## Error Handling

- **Empty `$ARGUMENTS`** → escalate via AskUserQuestion for the brief; never guess.
- **Scan produced zero candidates** → report the empty result and exit (no gate, no proposers) — nothing to do.
- **Proposer returns `NEEDS_CONTEXT`** → re-dispatch once with expanded criteria citing the specific ambiguity; if still `NEEDS_CONTEXT`, record in `skipped.md` and continue.
- **Proposer returns `BLOCKED`** → record in `skipped.md` with the block reason, surface at Gate 2, do not auto-retry.
- **Edit apply fails** (old_string non-unique or not found) → record in `apply_failures.md`, surface in the final summary, and do not abort — other edits still apply.
- **More than 6 proposers requested for one wave** → split into sequential waves of 6; never dispatch a wave larger than `MAX_PARALLEL`.

## State Management

After each phase, update `.mz/task/<task_name>/state.md` with current phase, iteration counts, number of proposals, and apply results. Allows resumption if interrupted.
