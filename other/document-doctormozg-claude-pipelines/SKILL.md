---
name: document
description: 'Writes or polishes technical docs: READMEs, API references, tutorials and how-tos. Use when the user says "write docs for", "document this" or "polish the README", or wants a guide new users can follow. Not for marketing copy (use copywrite).'
argument-hint: <what to document or polish>
allowed-tools: Agent, Bash(git rev-parse *), Bash(git symbolic-ref *), Bash(git merge-base *), Bash(git diff *), Bash(git ls-files *), Bash(git status *), Bash(git log *), Bash(mkdir *), Bash(date *), Read, Write, Edit, Glob, Grep, AskUserQuestion, WebFetch, WebSearch
---

# Technical Documentation Pipeline

## Overview

Creates or polishes technical documentation for a project. Researches the codebase first, dispatches `expert-technical-writer` (opus) to write the document, then runs `expert-naturalizer` (sonnet) to remove residual AI patterns. Output lands at `.mz/reports/<YYYY_MM_DD>_document_<slug>.md`.

## When to Use

Technical documentation (README, API reference, guide, tutorial, how-to, explanation), written from scratch or polished from an existing document.

### When NOT to use

- User wants promotional or marketing copy — use `copywrite`
- User wants only an AI-text rewrite of existing prose — use `naturalize`
- User wants code review or audit — use `review-branch` or `audit`
- User wants to brainstorm doc structure — use `brainstorm`

## Input

`$ARGUMENTS` — description of what to document. Inline modifiers:

- `scope:branch|global|working` — constrains codebase research to a subset (default: `global`)
- `type:tutorial|howto|reference|explanation|readme|api|all` — Diátaxis content type target (default: `all` lets the writer choose; explicit type produces a single-type doc)
- `@doc:<path>` — existing document to polish instead of creating from scratch

If `$ARGUMENTS` is empty, ask via `AskUserQuestion`. Never guess.

## Scope Parameter

See `<PLUGIN_ROOT>/shared/scope-parameter.md` for the canonical scope modes (`branch`, `global`, `working`) and their git commands.

- **Default**: `global`
- Scope constrains **research only** — Phase 2 writing and Phase 3 naturalization read whatever the writer needs

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **REPORT_DIR**: `<PROJECT_ROOT>/.mz/reports/`
- **MAX_DOC_TYPES**: 4 (tutorial / how-to / reference / explanation per Diátaxis)
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

| #   | Phase                                | File                 | Loop?             |
| --- | ------------------------------------ | -------------------- | ----------------- |
| 0   | Setup                                | inline below         | —                 |
| 1   | Codebase research                    | `phases/research.md` | —                 |
| 1.5 | Research approval gate               | inline below         | feedback sub-loop |
| 2   | Writing (expert-technical-writer)    | `phases/writing.md`  | —                 |
| 3   | Auto-naturalize (expert-naturalizer) | `phases/writing.md`  | —                 |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS`. Extract: brief, `scope:`, `type:`, `@doc:` references.
1. If brief is empty → `AskUserQuestion` for the topic. Never guess.
1. `task_name` = `<YYYY_MM_DD>_document_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and slug is a snake_case summary (max 20 chars). On same-day collision append `_v2`, `_v3`.
1. Run `mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>"`.
1. Write `state.md`: schema_version: 2, Status, Phase, Started, phase_complete: false, what_remains: [], FilesWritten.
1. Emit a visible setup block: `task_name`, working dir, report path, detected modifiers.

### Phase 1.5: Research Approval Gate

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/research.md` with the Read tool. Capture the full file contents (stack detection, public APIs, conventions, prior art, constraints, proposed doc structure) into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: research gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the research verbatim as a normal markdown chat message. Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/research.md` — do not substitute a path, summary, or placeholder. Structure:

```
## Research ready for review — document

<verbatim research.md contents>

---
**Approve** → proceed to Phase 2 (writing)  ·  **Reject** → task marked aborted, no docs written  ·  reply with feedback to revise
```

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the research contents in the question body, they live in the plan message above:

- question: `The research above is ready for review.`
- header: `Research`
- options: **Approve** — proceed to Phase 2 (writing) · **Reject** — abort the task, no docs written

**Response handling**:

- **Approve** → add `- research approved: .mz/task/<task_name>/research.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry from `what_remains`, set `Phase: research_approved`, and proceed to Phase 2.
- **Reject** → update state to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → re-run Phase 1 with feedback, overwrite `research.md`, return to Surface 1, re-read `research.md`, and re-emit the entire plan message from scratch with the full new contents — never diff-only, never summary-only. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: research gate`, stop. A missing answer is never approval.

## Common Rationalizations

| Rationalization                      | Rebuttal                                            |
| ------------------------------------ | --------------------------------------------------- |
| "skip research, just write the docs" | docs without grounding hallucinate API signatures   |
| "skip the approval gate"             | wrong doc structure costs 3× to fix after writing   |
| "skip the naturalize pass"           | tech-writer output still carries AI-pattern residue |

## Red Flags

- You wrote the document inline instead of dispatching `expert-technical-writer`.
- You skipped the research approval gate.
- You skipped the naturalize pass — Phase 3 is mandatory.
- The final document mixes Diátaxis types without explicit section labels.
- You fabricated API signatures the codebase does not contain.

## Verification

Output a visible final block:

```
Documentation pipeline complete.
Task dir:   .mz/task/<task_name>/
Report:     .mz/reports/<YYYY_MM_DD>_document_<slug>.md
Diátaxis:   <types written, e.g., tutorial+reference>
Naturalize: applied (<words removed>, <patterns broken>)
Files:
  - research.md
  - <output>.md (post-naturalize)
```

If any phase is incomplete, print the blocker explicitly.

## Error Handling

- Empty brief → `AskUserQuestion`. Never guess.
- `@doc:` path does not exist → ask the user whether to proceed without it.
- `scope:` resolves to zero files → escalate via AskUserQuestion; offer to widen scope.
- `expert-technical-writer` returns `BLOCKED` or `NEEDS_CONTEXT` → re-dispatch once with the missing context filled; if still blocked, escalate.
- `expert-naturalizer` returns `BLOCKED` → keep the technical-writer output as the final artifact and warn the user that naturalization did not run.
- Update `state.md` before and after every agent dispatch.

## State Management

Update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` after each phase:

- `Status:` `pending` | `running` | `blocked` | `complete` | `aborted_by_user` | `failed`
- `Phase:` `0` | `1` | `1.5` | `2` | `3`
- `FilesWritten:` cumulative list

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

Never rely on conversation memory for cross-phase state.
