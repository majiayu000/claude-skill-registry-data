---
name: vault-ingest
description: 'Turns a voice memo, screenshot, PDF or YouTube video into a transcribed fleeting note. Use when the user wants media captured into the vault ("ingest audio", "transcribe voice", "ingest PDF"). Not for existing captures (use process-notes).'
argument-hint: '<path or URL> [modality hint: voice|image|pdf|youtube]'
allowed-tools: Agent, Read, Write, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(which *), Bash(ffprobe *), Bash(pdfinfo *), Bash(awk *), Bash(true *), Grep, Glob, AskUserQuestion
---

# Vault Ingest

## Overview

Discipline skill for multimodal capture into the vault as fleeting notes. Detects input modality (voice, image, PDF, YouTube, screenshot), verifies the required transcription or OCR tool is installed, dispatches `capture-normalizer` to produce a clean transcript, presents the transcript for user approval, and writes a frontmatter-annotated fleeting note to the vault inbox. Every capture produces a note with `status: draft`, `type: fleeting`, and full provenance fields so downstream skills (`process-notes`, `vault-schema`) can reason about it.

## When to Use

Capturing raw media (voice memos, screenshots and images, PDFs, YouTube videos) into the vault as a single transcribed fleeting note.

### When NOT to use

- Processing fleeting notes that are already in the vault — use `process-notes`.
- Atomizing long captured notes into permanent atomic notes — use `process-notes` as a follow-up after capture.
- Proposing `[[wikilinks]]` between notes — use `vault-connect`.
- Importing research reports or brainstorm outputs — use `vault-research`.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **INBOX_FOLDER**: `inbox/`
- **MAX_TRANSCRIPT_PREVIEW**: 500 (words shown in the approval gate; longer transcripts are truncated with `...`)
- **VOICE_MAX_DURATION_SEC**: 3600 (warn before transcribing audio longer than 1 hour)
- **PDF_MAX_PAGES**: 50 (warn before extracting from PDFs longer than this)

## Core Process

### Phase Overview

| Phase | Goal                         | Details                           |
| ----- | ---------------------------- | --------------------------------- |
| 0     | Setup                        | Inline below                      |
| 1     | Detect tooling + transcribe  | `phases/detect_and_transcribe.md` |
| 1.5   | User approval — transcript   | Inline below                      |
| 2     | Write fleeting note to vault | `phases/approve_and_write.md`     |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS`. First argument is the input path or URL. Second argument (optional) is an explicit modality hint: `voice`, `image`, `pdf`, or `youtube`.
1. If the first argument is empty, ask the user via AskUserQuestion what to ingest. Never guess.
1. Detect modality from the input:
   - Extension `.m4a`, `.wav`, `.mp3` → `voice`.
   - Extension `.png`, `.jpg`, `.jpeg`, `.heic` → `image` (record `source_type: screenshot` if user confirmed it is a screenshot, else `image`).
   - Extension `.pdf` → `pdf`.
   - URL containing `youtube.com` or `youtu.be` → `youtube`.
   - If the second argument is present, it overrides the detected modality.
   - If modality cannot be inferred and no hint was given, ask via AskUserQuestion.
1. Resolve the vault path with precedence: `$OBSIDIAN_VAULT_PATH` → `$MZ_VAULT_PATH` → walk up from cwd to the nearest `.obsidian/` directory. If none found, ask via AskUserQuestion.
1. Derive `task_name = <YYYY_MM_DD>_vault-ingest_<modality>` where `<YYYY_MM_DD>` is today's date (underscores); on same-day collision append `_v2`, `_v3`. Create `TASK_DIR<task_name>/` on disk.
1. Write `state.md` with `schema_version: 2`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `Input: <path or URL>`, `Modality: <voice|image|pdf|youtube>`, `Vault: <absolute path>`, `phase_complete: false`, `what_remains: []`.

### Phase 1.5: User Approval — Transcript

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/transcript.md` and capture the full contents into context. Note the modality, tool, and duration/pages from the frontmatter.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: transcript gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the transcript verbatim as a normal markdown chat message (truncated at `MAX_TRANSCRIPT_PREVIEW` words with a trailing `...` when longer):

```
## Transcript ready for review — vault-ingest

Transcript produced from <input>. Modality: <modality>, transcription tool: <tool>, duration/pages: <detail>.

<verbatim transcript body, truncated at MAX_TRANSCRIPT_PREVIEW words with "..." when longer>

---
**Approve** → proceed to Phase 2, write the fleeting note to the vault  ·  **Reject** → task marked aborted, no fleeting note written  ·  reply with feedback to revise
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/transcript.md` (transcript body, up to `MAX_TRANSCRIPT_PREVIEW` words) — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the transcript in the question body, it lives in the plan message above:

- question: `The transcript above is ready for review.`
- header: `Transcript`
- options:
  - **Approve** — proceed to Phase 2, write the fleeting note to the vault
  - **Reject** — abort, no fleeting note written

Response handling:

- **Approve** → add `- transcript approved: .mz/task/<task_name>/transcript.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: transcript_approved`, and proceed to Phase 2.
- **Reject** → update state to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → common feedback is "try a different tool" (switch `whisper-cpp` → `whisper`, `ocrit` → `tesseract`) or "the transcript is truncated, rerun". Incorporate the feedback, re-run Phase 1 with the adjusted tool choice, return to this gate, re-read `<PROJECT_ROOT>/.mz/task/<task_name>/transcript.md`, and re-emit the entire plan message from scratch (never diff-only). This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: transcript gate`, stop. A missing answer is never approval.

## Common Rationalizations

| Rationalization                                                               | Rebuttal                                                                                                                                                                                         |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "The tool is missing — just write an empty fleeting note with a source link." | "An empty note with provenance metadata masquerading as captured content is worse than no note at all — it pollutes future search and appears 'processed' when it is not. Escalate via BLOCKED." |
| "Skip the approval gate — the user already chose to capture this."            | "Tool output is noisy: VTT timestamps survive, whisper inserts `[inaudible]`, OCR mangles layout. The approval gate exists so the user sees what the vault will actually contain."               |
| "Transcript has garbage — ship it anyway, the user can fix it in Obsidian."   | "Captured notes are the raw intake layer for the entire pipeline. Bad captures propagate into atomization, linking, and Q&A. Either a fallback tool recovers quality or the user says BLOCKED."  |

## Red Flags

- Dispatching `capture-normalizer` before running `which <tool>` detection.
- Writing a fleeting note with an empty body because the transcription tool failed.
- Presenting the approval gate as a path or one-line status instead of the verbatim transcript.
- Skipping the modality detection step and guessing from filename alone when `$ARGUMENTS[2]` was provided.
- Writing to the vault root or to `<vault>/permanent/` instead of `<vault>/<INBOX_FOLDER>/`.
- Omitting `source_type`, `captured_at`, or `status: draft` from the frontmatter.

## Verification

Print this block before concluding — silent checks get skipped:

```
vault-ingest verification:
  [ ] Tool detection logged to tooling.md before capture-normalizer dispatch
  [ ] Transcript shown verbatim via AskUserQuestion before any vault write
  [ ] Fleeting note written under <vault>/<INBOX_FOLDER>/ with source_type + captured_at + status: draft
  [ ] state.md Status is `complete` with Completed timestamp
```

If any box is unchecked, the skill did not run correctly — report the failure explicitly rather than claiming success.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
