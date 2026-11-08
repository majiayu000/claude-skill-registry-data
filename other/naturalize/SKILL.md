---
name: naturalize
description: 'Rewrites machine-sounding or overly polished text so a real person seems to have written it. Use when the user wants existing text to sound human ("humanize this text", "make this sound less like AI"). Not for new promotional copy (use copywrite).'
argument-hint: <text or @file:path to rewrite> [preserve:<terms>] [voice:@file:<profile>] [allow:<punctuation>] [research:yes]
allowed-tools: Agent, Bash(${CLAUDE_PLUGIN_ROOT}/scripts/forbidden-punctuation.sh *), Bash(diff -u *), Bash(git rev-parse *), Bash(date *), Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Text Naturalization Pipeline

## Overview

Rewrites AI-generated text to read as if a human wrote it, in one pass with no approval gates. `expert-naturalizer` (sonnet) detects the AI patterns (vocabulary spikes, structural templates, sentence-rhythm uniformity) and rewrites them, removing banned punctuation such as em dashes and semicolons. With `research:yes`, `pipeline-web-researcher` (mz-base) first gathers patterns newer than the embedded list. With `voice:`, it rewrites toward one writer's measured habits for the register instead of a generic human target. A script then checks the rewrite for banned punctuation, minus what `allow:` lifts. File input is overwritten in place, with the original kept in the task folder and a diff shown at the end.

## When to Use

Rewrites existing AI-generated prose so it reads as human-written.

### When NOT to use

- User wants original technical documentation written from scratch — use `document` (which already runs naturalize as Phase 3)
- User wants new promotional copy written rather than existing text rewritten — use `copywrite` (which also naturalizes)
- User wants to fix grammar in human-written text — this skill assumes AI patterns are present and may damage natural prose
- User wants to translate text — use `translate`

## Input

`$ARGUMENTS` — the text to rewrite or a file reference. Forms accepted:

- Inline text following the skill invocation (the entire arg block becomes the input)
- `@file:<path>` — read text from the specified file; the rewrite overwrites it in place
- `preserve:<term>[,<term>...]` — terms the rewrite keeps verbatim, such as a domain word that sits on the avoid list ("leverage" in a finance text)
- `voice:@file:<path>` — a voice profile: free-form notes on how one writer writes, per register (sentence length, final periods, commas, tone markers, stock phrases, what not to copy). The agent rewrites toward the register it matches
- `allow:<name>[,<name>...]` — punctuation the ban lets through, from `em-dash`, `en-dash`, `semicolon`, `ellipsis` and `arrow`, for a writer whose formal register uses them
- `research:yes` — `pipeline-web-researcher` pulls current AI pattern data from authoritative web sources before the rewrite (use when the embedded vocabulary may be 18+ months old)

If `$ARGUMENTS` is empty, ask via `AskUserQuestion` for either inline text or a file path. Never guess.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **REPORT_DIR**: `<PROJECT_ROOT>/.mz/reports/`
- **CHUNK_THRESHOLD**: 2000 (words above this trigger section-by-section rewriting)
- **PUNCTUATION_CHECK**: `${CLAUDE_PLUGIN_ROOT}/scripts/forbidden-punctuation.sh` (each `--preserve <term>` exempts a preserved term and each `--allow <name>` an allowed character; exit 0 when clean, 1 with one `file:line: <name> <char>` line per hit, 2 on a usage error or a file it can't read)

## Core Process

### Phase Overview

| #   | Phase                                                     | File                  | Loop?                    |
| --- | --------------------------------------------------------- | --------------------- | ------------------------ |
| 0   | Setup                                                     | inline below          | —                        |
| 1   | Rewrite (expert-naturalizer, optional web research first) | `phases/rewriting.md` | —                        |
| 2   | Punctuation check and apply                               | `phases/rewriting.md` | one fix-only re-dispatch |

No phase asks for approval. File input is safe to overwrite because `input.md` keeps the original and the run ends with a diff.

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS`. Detect inline text vs `@file:` reference, `preserve:` terms, `voice:`, `allow:` names and `research:yes`.
1. If empty → `AskUserQuestion` for input source. Never guess.
1. If `@file:` referenced, read the file and verify it is text (not binary, not too large to fit in context — if >50KB, warn the user).
1. If `voice:` is given, read the profile and verify it is text. A missing or binary profile → `AskUserQuestion` to fix the path or run without one.
1. Every `allow:` name must be one of `em-dash`, `en-dash`, `semicolon`, `ellipsis`, `arrow`. An unknown name → `AskUserQuestion`, listing the valid names.
1. `task_name` = `<YYYY_MM_DD>_naturalize_<slug>` where slug derives from the input (file basename or first 5 words of inline text). On collision append `_v2`, `_v3`.
1. Write the input text verbatim to `<PROJECT_ROOT>/.mz/task/<task_name>/input.md` with the Write tool, which creates the folder. Don't copy it with Bash, which a sandbox may mount read-only. For `@file:` input this copy is the original that the diff compares against and the user can restore from.
1. With `voice:`, write the profile verbatim to `<PROJECT_ROOT>/.mz/task/<task_name>/voice.md` the same way, so the agent reads it inside the project.
1. Write `state.md`: schema_version: 2, Status, Phase, Started, phase_complete: false, what_remains: [], InputSource, PreserveTerms, VoiceProfile, AllowedPunctuation, ResearchRequested, FilesWritten.
1. Emit a visible setup block: `task_name`, input source, length in words, preserve terms, voice profile, allowed punctuation, research flag.

Then run Phases 1 and 2 from `phases/rewriting.md`.

## Common Rationalizations

| Rationalization                                              | Rebuttal                                                                                                                    |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| "the text looks fine, skip the rewrite"                      | structural AI patterns are invisible without the agent's detection pass; vocabulary alone is not enough                     |
| "ask before overwriting the file, to be safe"                | `input.md` keeps the original and the diff shows every change, so a question only adds a wait                               |
| "swap the flagged em dash for a hyphen so the check passes"  | outside chat a spaced hyphen reads the same, so the sentence has to be restructured; in chat `-` is a real aside mark       |
| "the check failed twice, leave its lines out of the summary" | the rewrite was applied anyway, so the lines are the only sign of what's left; a concern that isn't listed is a silent pass |
| "the profile uses em dashes, so keep them"                   | only `allow:` lifts the ban; the script would flag a kept dash and the fix pass would strip it anyway                       |
| "skip web research, the embedded list is good enough"        | AI vocabulary shifts every 18 months; `research:yes` exists for a reason                                                    |

## Red Flags

- You rewrote the text inline without dispatching `expert-naturalizer`.
- You asked the user to approve an analysis or the overwrite.
- You overwrote the file before `input.md` held the original.
- You ran the punctuation check on the change report instead of the rewrite.
- You over-edited a code block, table, or proper name.
- You left a `[SPECIFICITY NEEDED]` marker in the text that replaces the user's file.
- You added a citation, statistic, or named source that wasn't in the input.
- You passed the agent the profile's path outside the project instead of `voice.md` in the task folder.
- You "improved" text that was already human-written.

## Verification

Output a visible final block:

```
Naturalization complete.
Task dir:    .mz/task/<task_name>/
Report:      .mz/reports/<task_name>.md
Input:       <source> (<words>)
Output:      <words> (delta: <±N>%)
Patterns:    <count broken>
Rhythm:      burstiness <before> to <after> | length spread <before> to <after> (chat)
Voice:       <register> from <profile> | none
Punctuation: clean | <N> lines left: <file:line list> | not run: <reason>
File update: yes (original at .mz/task/<task_name>/input.md) | no | n/a
```

If any phase is incomplete, print the blocker explicitly.

## Error Handling

- Empty input → `AskUserQuestion`. Never guess.
- `@file:` path does not exist → escalate via AskUserQuestion; offer alternatives.
- `voice:` profile missing or unreadable, or an unknown `allow:` name → AskUserQuestion before anything is written.
- Input is binary or non-text → reject with explanation.
- Input >50KB → warn user and ask whether to proceed (long inputs may exceed context).
- `expert-naturalizer` returns `BLOCKED` → leave the user's file untouched, escalate.
- `expert-naturalizer` returns `NEEDS_CONTEXT` → fill the missing context (e.g., preserve list), re-dispatch once.
- `PUNCTUATION_CHECK` exits 2 → record `PunctuationCheck: not run` with its stderr; the final block reports it.
- Update `state.md` before and after every agent dispatch.

## State Management

Update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` after each phase:

- `Status:` `pending` | `running` | `blocked` | `complete` | `aborted_by_user` | `failed`
- `Phase:` `0` | `1` | `2` | `complete`
- `InputSource:` `inline` | `file:<path>`
- `PreserveTerms:` list of terms, `[]` when none
- `VoiceProfile:` `.mz/task/<task_name>/voice.md` | `none`
- `AllowedPunctuation:` list of `allow:` names, `[]` when none
- `ResearchRequested:` `yes` | `no`
- `FilesWritten:` cumulative list
- `PunctuationCheck:` `clean` | `concerns` | `not run`
- `FileUpdateApplied:` `yes` | `no` | `n/a` (`n/a` for inline input)

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

Never rely on conversation memory for cross-phase state.
