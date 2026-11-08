---
name: copywrite
description: 'Writes promotional copy: landing pages, emails, announcements, social posts, release notes and pitch one-pagers. Use when the user says "write a landing page", "draft a launch email" or "sell this feature". Not for technical docs (use document).'
argument-hint: <what to promote, plus format:landing|email|announcement|social|changelog|pitch>
allowed-tools: Agent, Bash(git rev-parse *), Bash(git symbolic-ref *), Bash(git merge-base *), Bash(git diff *), Bash(git ls-files *), Bash(git status *), Bash(git log *), Bash(mkdir *), Bash(date *), Read, Write, Edit, Glob, Grep, AskUserQuestion, WebFetch, WebSearch
---

# Copywriting Pipeline

## Overview

Produces promotional and persuasive copy — landing pages, launch emails, announcements, social posts, changelog entries, and pitch one-pagers. Researches the product and competitive positioning first, dispatches `expert-copywriter` (opus) to write the copy, then runs `expert-naturalizer` (sonnet) to remove residual AI patterns. Output lands at `.mz/reports/<YYYY_MM_DD>_copywrite_<slug>.md`.

## When to Use

Promotional copy (landing page, email, announcement, social post, changelog entry, pitch), written fresh or as a rewrite of existing marketing copy with sharper positioning.

### When NOT to use

- User wants technical documentation — use `document` (which also runs naturalize as Phase 3)
- User wants only an AI-text rewrite of existing prose — use `naturalize`
- User wants an internal report or review — use `audit`, `review-branch`, etc.
- User wants to brainstorm positioning before writing — use `brainstorm` first, then `copywrite`

## Input

`$ARGUMENTS` — description of what to promote. Inline modifiers:

- `format:landing|email|announcement|social|changelog|pitch` — the output format. **Required**. If absent, the orchestrator asks via `AskUserQuestion`.
- `scope:branch|global|working` — constrains codebase scan to a subset (default: `global`). Used for tone-matching against existing copy in the repo.
- `@brief:<path>` — existing brief, product spec, or feature doc to ground the copy in. Strongly recommended.

If `$ARGUMENTS` is empty, ask via `AskUserQuestion` for the product, audience, and format. Never guess.

## Scope Parameter

See `<PLUGIN_ROOT>/shared/scope-parameter.md` for the canonical scope modes (`branch`, `global`, `working`) and their git commands.

- **Default**: `global`
- Scope constrains **codebase research only** — Phase 2 writing and Phase 3 naturalization read whatever the writer needs

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **REPORT_DIR**: `<PROJECT_ROOT>/.mz/reports/`
- **SUPPORTED_FORMATS**: `landing`, `email`, `announcement`, `social`, `changelog`, `pitch`
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

| #   | Phase                                  | File                 | Loop?             |
| --- | -------------------------------------- | -------------------- | ----------------- |
| 0   | Setup                                  | inline below         | —                 |
| 1   | Research (positioning + codebase tone) | `phases/research.md` | —                 |
| 1.5 | Brief approval gate                    | inline below         | feedback sub-loop |
| 2   | Writing (expert-copywriter)            | `phases/writing.md`  | —                 |
| 3   | Auto-naturalize (expert-naturalizer)   | `phases/writing.md`  | —                 |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS`. Extract: topic, `format:`, `scope:`, `@brief:` references.
1. If `format:` is missing → `AskUserQuestion` with `landing`, `email`, `announcement` and `social` as options, and a question text that names `changelog` and `pitch` as typed replies (AskUserQuestion takes at most four options). Never guess.
1. If topic/brief is empty → `AskUserQuestion` for what to promote and to whom. Never guess.
1. If `@brief:<path>` is referenced, read the file and verify it exists and is readable text.
1. `task_name` = `<YYYY_MM_DD>_copywrite_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and slug is a snake_case summary derived from the topic + format (max 20 chars). On same-day collision append `_v2`, `_v3`.
1. Run `mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>"`.
1. Write `state.md`: schema_version: 2, Status, Phase, Started, phase_complete: false, what_remains: [], Format, BriefSource, FilesWritten.
1. Emit a visible setup block: `task_name`, format, brief source, scope, report path.

### Phase 1.5: Brief Approval Gate

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/brief.md` with the Read tool. Capture the full file contents (positioning, audience, value claim, named customers/numbers, tone decisions, format-specific constraints) into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: brief gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the brief verbatim as a normal markdown chat message. Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/brief.md` — do not substitute a path, summary, or placeholder. Structure:

```
## Brief ready for review — copywrite

<verbatim brief.md contents>

---
**Approve** → proceed to Phase 2 (writing)  ·  **Reject** → task marked aborted, no copy written  ·  reply with feedback to revise
```

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the brief contents in the question body, they live in the plan message above:

- question: `The brief above is ready for review.`
- header: `Brief`
- options: **Approve** — proceed to Phase 2 (writing) · **Reject** — abort the task, no copy written

**Response handling**:

- **Approve** → add `- brief approved: .mz/task/<task_name>/brief.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry from `what_remains`, set `Phase: brief_approved`, and proceed to Phase 2.
- **Reject** → update state to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → re-run Phase 1 with feedback, overwrite `brief.md`, return to Surface 1, re-read `brief.md`, and re-emit the entire plan message from scratch with the full new contents — never diff-only, never summary-only. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: brief gate`, stop. A missing answer is never approval.

## Common Rationalizations

| Rationalization                             | Rebuttal                                                                                     |
| ------------------------------------------- | -------------------------------------------------------------------------------------------- |
| "skip research, the brief is enough"        | the brief lacks competitive context and tone-matching against the project's voice            |
| "skip the approval gate to save time"       | bad positioning costs 3× to fix after the copy is written and shared                         |
| "skip the naturalize pass"                  | copywriter output still carries AI-pattern residue (adjective stacks, mechanical antithesis) |
| "format doesn't matter, write generic copy" | a landing page and a changelog are different shapes; generic copy fits neither               |

## Red Flags

- You wrote the copy inline instead of dispatching `expert-copywriter`.
- You skipped the brief approval gate.
- You skipped the naturalize pass — Phase 3 is mandatory.
- You invented metrics, customer names, or capabilities not in the brief.
- The final copy uses the wrong format (e.g., five-paragraph essay structure on a social post).

## Verification

Output a visible final block:

```
Copywriting pipeline complete.
Task dir:   .mz/task/<task_name>/
Report:     .mz/reports/<YYYY_MM_DD>_copywrite_<slug>.md
Format:     <landing|email|announcement|social|changelog|pitch>
Naturalize: applied (<words removed>, <patterns broken>)
Files:
  - brief.md
  - <output>.md (post-naturalize)
```

If any phase is incomplete, print the blocker explicitly.

## Error Handling

- Empty topic → `AskUserQuestion`. Never guess.
- Missing `format:` → the Phase 0 format question: four options, with `changelog` and `pitch` as typed replies. Never guess.
- `@brief:` path does not exist → ask the user whether to proceed without it; warn that copy quality drops sharply without a grounded brief.
- `scope:` resolves to zero files → continue with empty codebase tone-match; warn the user that voice-matching is unavailable.
- `expert-copywriter` returns `BLOCKED` or `NEEDS_CONTEXT` → re-dispatch once with the missing context filled; if still blocked, escalate via AskUserQuestion.
- `expert-naturalizer` returns `BLOCKED` → keep the copywriter output as the final artifact and warn the user that naturalization did not run.
- Update `state.md` before and after every agent dispatch.

## State Management

Update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` after each phase:

- `Status:` `pending` | `running` | `blocked` | `complete` | `aborted_by_user` | `failed`
- `Phase:` `0` | `1` | `1.5` | `2` | `3`
- `Format:` `landing` | `email` | `announcement` | `social` | `changelog` | `pitch`
- `BriefSource:` `inline` | `file:<path>` | `none`
- `FilesWritten:` cumulative list

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

Never rely on conversation memory for cross-phase state.
