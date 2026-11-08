---
name: vault-research
description: 'Atomizes a research or brainstorm report from .mz/ into permanent vault notes. Use when the user wants a report imported ("ingest research", "import report", "atomize report", "research to notes"). Not for the user''s own captures (use process-notes).'
argument-hint: <report path>
allowed-tools: Agent, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Read, Write, Grep, AskUserQuestion
---

# Vault Research

## Overview

Discipline skill that atomizes a long research report into permanent notes, pre-filtering known noise sections before atomization. Reuses `atomization-proposer` (dispatched once per 450-word window, below the agent's 2000-word input cap) and `link-suggester`. Produces claim-style atomic notes under the vault's permanent folder inside a `research/` subfolder, each carrying `type: research`, `source_type: research-report`, and full provenance.

## When to Use

Turning a generated research, brainstorm or deep-research report from `.mz/research/` or `.mz/reports/` into separately linkable permanent notes, discarding known noise sections (panel deliberations, methodology, cut ideas).

### When NOT to use

- Capturing raw multimodal input (voice memos, images, PDFs, YouTube) — use `vault-ingest`.
- Processing existing fleeting notes already in the vault — use `process-notes`.
- Proposing `[[wikilinks]]` between notes that already exist — use `vault-connect`.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **MAX_NOTES**: 15 (hard cap across all atomization windows; excess proposals are deduped and truncated)
- **LONG_REPORT_THRESHOLD_WORDS**: 2000 (warn the user before proceeding on reports above this size)
- **ATOMIZATION_WAVE_WORD_CAP**: 450 (per-window word budget, below `atomization-proposer`'s 2000-word input cap)
- **NOISE_SECTIONS**: `["Vote Tally", "Voting History", "Panel Perspectives", "Methodology", "Deliberately Cut", "All Ideas by Round"]`

## Core Process

| #   | Phase                      | Reference                              | Loop?          |
| --- | -------------------------- | -------------------------------------- | -------------- |
| 0   | Setup                      | inline                                 | —              |
| 1   | Parse + noise filter       | `phases/parse_report.md`               | —              |
| 1.5 | Approval — noise exclusion | inline                                 | until approved |
| 2   | Atomize + write            | `phases/atomize_and_write.md`          | —              |
| 2.5 | Approval — proposals       | inline                                 | until approved |
| 3   | Link suggestions           | `phases/atomize_and_write.md` (Step 5) | —              |
| 3.5 | Approval — links           | inline                                 | until approved |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Resolve `$ARGUMENTS` as an absolute report path. The path must exist — if it does not, ask the user via AskUserQuestion for a corrected path.
1. If the resolved path is not under `.mz/research/` or `.mz/reports/`, warn the user but do not block — record `NonStandardLocation: true` in `state.md`.
1. Read the report and compute word count. If it exceeds `LONG_REPORT_THRESHOLD_WORDS` (2000), record `LongReport: true` and warn the user before proceeding.
1. Resolve the vault path and read vault CLAUDE.md. Extract the permanent folder convention (e.g., `04 - Permanent/`, `permanent/`, `notes/permanent/`). If no permanent folder convention is found, ask via AskUserQuestion — never guess.
1. Derive `task_name = <YYYY_MM_DD>_vault-research_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<slug>` is a filename-sanitized form of the report basename; on same-day collision append `_v2`, `_v3`. Create `TASK_DIR<task_name>/` on disk.
1. Write `state.md` with `schema_version: 2`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `phase_complete: false`, `what_remains: []`, `ReportPath: <absolute path>`, `ReportWordCount: <N>`, `Vault: <absolute vault path>`, `PermanentFolder: <extracted folder>`.

### Phase 1.5: User Approval — Noise Exclusion

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/parsed_report.md` in full and capture its contents into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: noise gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the artifact verbatim as a normal markdown chat message:

```
## Noise filter results ready for review — vault-research

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/parsed_report.md>

---
**Approve** → proceed to Phase 2 atomization  ·  **Reject** → abort the task  ·  reply with feedback to revise
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/parsed_report.md` — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the artifact in the question body:

- question: `The noise filter results above are ready for review.`
- header: `Noise`
- options: **Approve** — proceed to Phase 2 atomization · **Reject** — abort the task

**Response handling**:

- **Approve** → add `- noise filter approved: .mz/task/<task_name>/parsed_report.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: noise_filter_approved`, and proceed to Phase 2.
- **Reject** → update `state.md` Status to `aborted_by_user` and stop.
- **Any other reply (feedback)** → typical feedback adds or removes sections from the noise list. Apply the edits to the effective noise list, re-run Phase 1 (`phases/parse_report.md`), overwrite `parsed_report.md`, return to Surface 1, re-read the updated artifact, and re-emit the entire plan message from scratch. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: noise gate`, stop. A missing answer is never approval.

### Phase 2.5: User Approval — Atomization Proposals

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/proposals.md` in full and capture its contents into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: proposals gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the artifact verbatim as a normal markdown chat message:

```
## Atomization proposals ready for review — vault-research

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/proposals.md>

---
**Approve** → write notes to vault and proceed to Phase 3 link suggestions  ·  **Reject** → abort the task, no vault writes have occurred  ·  reply with feedback to revise
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/proposals.md` — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the artifact in the question body:

- question: `The atomization proposals above are ready for review.`
- header: `Proposals`
- options: **Approve** — write notes to vault and proceed to Phase 3 link suggestions · **Reject** — abort the task, no vault writes have occurred

**Response handling**:

- **Approve** → add `- proposals approved: .mz/task/<task_name>/proposals.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: proposals_approved`, and continue Phase 2 (post-approval write).
- **Reject** → update `state.md` Status to `aborted_by_user` and stop. No vault writes have occurred yet.
- **Any other reply (feedback)** → apply feedback (skip numbered proposals, merge, split, retitle), re-run the affected window(s), regenerate `proposals.md`, return to Surface 1, re-read the updated artifact, and re-emit the entire plan message from scratch. This is a loop — repeat until explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: proposals gate`, stop. A missing answer is never approval.

### Phase 3.5: User Approval — Link Suggestions

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/link_suggestions.md` in full and capture its contents into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: links gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the artifact verbatim as a normal markdown chat message:

```
## Link suggestions ready for review — vault-research

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/link_suggestions.md>

---
**Approve** → apply all links and complete the task  ·  **Reject** → skip all links, mark task complete with no Related sections added  ·  reply with feedback to revise
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/link_suggestions.md` — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the artifact in the question body:

- question: `The link suggestions above are ready for review.`
- header: `Links`
- options: **Approve** — apply all links and complete the task · **Reject** — skip all links, mark task complete with no Related sections added

**Response handling**:

- **Approve** → add `- links approved: .mz/task/<task_name>/link_suggestions.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: links_approved`, apply all links, and proceed to completion.
- **Reject** → set `Status: complete`, `phase_complete: true`, `what_remains: []`, `LinksAdded: 0`, `LinksSkipped: true`. Written notes stay on disk without a Related section.
- **Any other reply (feedback)** → skip specified links, accept the rest, overwrite `link_suggestions.md`, return to Surface 1, re-read the updated artifact, and re-emit the entire plan message from scratch. This is a loop — repeat until the user explicitly approves. Never proceed without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: links gate`, stop. A missing answer is never approval.

## Common Rationalizations

| Rationalization                                                  | Rebuttal                                                                                                                                                                                                |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Send the whole report to atomization-proposer in one dispatch." | "atomization-proposer has a 2000-word input cap; oversized input returns DONE_WITH_CONCERNS with only partial processing. The 450-word windowing scheme exists to keep every dispatch fully processed." |
| "Noise sections are obvious — skip the user approval gate."      | "The user may want to include methodology or panel-perspectives sections; every exclusion needs explicit approval. Silent drops destroy information the user intended to capture."                      |
| "Run all atomization windows in parallel for speed."             | "Sequential windows are required because each dispatch writes to a numbered output file and shares agent context; parallel writes would collide and produce interleaved output."                        |

## Red Flags

- Dispatching `atomization-proposer` with more than `ATOMIZATION_WAVE_WORD_CAP` words.
- Running atomization windows in parallel instead of sequentially.
- Presenting any approval gate as a path or summary instead of the verbatim artifact contents.
- Writing to the vault root or to `<vault>/<INBOX_FOLDER>/` instead of `<vault>/<permanent_folder>/research/`.
- Omitting `type: research`, `source_type: research-report`, or `report_path` from any note's frontmatter.
- Proceeding past any `.5` approval gate without explicit "approve" from the user.

## Verification

Print this block before concluding — silent checks get skipped:

```
vault-research verification:
  [ ] parsed_report.md emitted verbatim as a chat message (Surface 1) and AskUserQuestion selector presented before any atomization
  [ ] proposals.md emitted verbatim as a chat message (Surface 1) and AskUserQuestion selector presented before any vault write
  [ ] link_suggestions.md emitted verbatim as a chat message (Surface 1) and AskUserQuestion selector presented before any link was written
  [ ] All written notes carry type: research, source_type: research-report, report_path, status: draft
  [ ] state.md Status is `complete` with Completed timestamp
```

If any box is unchecked, the skill did not run correctly — report the failure explicitly rather than claiming success.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
