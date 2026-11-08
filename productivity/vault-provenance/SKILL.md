---
name: vault-provenance
description: 'Classifies claims in one vault note by epistemic status and back-fills its sources frontmatter. Use when the user wants claims and sources checked ("epistemic status", "provenance", "mark claims"). Not for whole-vault audits (use vault-health).'
argument-hint: <note name or path>
allowed-tools: Agent, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Read, Write, Grep, AskUserQuestion
---

# Vault Provenance

## Overview

Discipline skill that classifies every factual claim in a single vault note against a five-value epistemic vocabulary (`first-hand | cited | inferred | received | unmarked`) and back-fills the note's `epistemic_status:` and `sources: []` frontmatter after explicit user approval. Scope is strictly per-note — never vault-wide. Body content is preserved verbatim unless the user opts into annotation mode.

## When to Use

Classifying the factual claims of a single vault note by epistemic status and back-filling its sources, for example after drafting a research note or before promoting it to `evergreen`.

### When NOT to use

- Vault-wide provenance audits — this skill is per-note by design.
- Whole-vault structure audits (orphans, broken links, stubs, tags) — use `vault-health`.
- Suggesting new links between notes — use `vault-connect`.
- Atomizing a note into smaller notes — use `process-notes`.
- Schema or frontmatter compliance checks — use `vault-schema`.

## Arguments

`$ARGUMENTS` is `<note name or path>`. If the argument is a bare name, resolve it against the vault by exact filename match first, then by case-insensitive basename match. If the argument is missing or matches zero / multiple notes, escalate via AskUserQuestion — never guess.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **MAX_CLAIMS_PER_NOTE**: 25 — hard cap delegated to `provenance-tracer`; if more claims exist, the first 25 are classified and the cap is flagged in the summary.
- **EPISTEMIC_VOCAB**: `[first-hand, cited, inferred, received, unmarked]` — closed set; no other values.

## Core Process

### Phase Overview

| Phase | Goal                            | Details                      |
| ----- | ------------------------------- | ---------------------------- |
| 0     | Setup                           | Inline below                 |
| 1     | Scan claims                     | `phases/scan_claims.md`      |
| 1.5   | User approval — classifications | Inline below                 |
| 2     | Back-fill sources               | `phases/backfill_sources.md` |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS` as `<note name or path>`.
1. Resolve the note: if the argument is an absolute path, use it; if a relative path or bare name, resolve against the vault. If zero or multiple matches, escalate via AskUserQuestion with the candidate list. Never guess.
1. Derive `task_name = <YYYY_MM_DD>_vault-provenance_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<slug>` is the note basename normalised to `[a-z0-9-]`; on same-day collision append `_v2`, `_v3`. Create `TASK_DIR<task_name>/` on disk.
1. Write `state.md` with `schema_version: 2`, `phase_complete: false`, `what_remains: []`, `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `NotePath: <absolute path>`, `TaskName: <task_name>`.
1. Print a visible setup block showing `task_name`, resolved note path, and the output artifact path `<PROJECT_ROOT>/.mz/task/<task_name>/claims_analysis.md`.

### Phase 1 — Scan claims

See `phases/scan_claims.md`.

### Phase 1.5: User approval — classifications

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/claims_analysis.md` and capture its full contents into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: claims gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the artifact verbatim as a normal markdown chat message:

```
## Claims analysis ready for review — vault-provenance

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/claims_analysis.md>

---
**Approve** → proceed to Phase 2 to back-fill frontmatter  ·  **Reject** → abort task, no frontmatter written  ·  reply with feedback to revise
```

Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/claims_analysis.md` — do not substitute a path, summary, or placeholder.

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the artifact in the question body:

- question: `The claims analysis above is ready for review.`
- header: `Claims`
- options: **Approve** — proceed to Phase 2 to back-fill frontmatter · **Reject** — abort task, no frontmatter written

**Response handling**:

- **Approve** → add `- classifications approved: .mz/task/<task_name>/claims_analysis.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry, set `Phase: classifications_approved`, and proceed to Phase 2.
- **Reject** → update state to `aborted_by_user` and stop. No frontmatter write occurs.
- **Any other reply (feedback)** → incorporate edits (e.g., "reclassify claim 3 as received", "swap proposed source on claim 7", "enable annotation mode"), re-dispatch `provenance-tracer` if a full re-scan is needed or edit the artifact in place for targeted changes, overwrite `<PROJECT_ROOT>/.mz/task/<task_name>/claims_analysis.md`, return to Surface 1, re-read the updated artifact, and re-emit the entire plan message from scratch — never diff-only, never summary-only. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: claims gate`, stop. A missing answer is never approval.

### Phase 2 — Back-fill sources

See `phases/backfill_sources.md`.

## Common Rationalizations

| Rationalization                                                     | Rebuttal                                                                                                                                                                                              |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "This note is obviously first-hand — skip the analysis."            | "First-hand classification requires tracing each claim to a direct experiential marker; skipping the analysis produces a false confidence marker across every sentence in the note."                  |
| "Classify all claims at the note level, not per-claim."             | "Note-level classification loses provenance granularity; a single note routinely mixes first-hand observation, cited findings, and inferred conclusions. Every claim must carry its own attribution." |
| "Sources frontmatter is optional — the user probably won't use it." | "Provenance is the whole point of this skill; the frontmatter-only annotation contract is the default output. Treating it as optional silently reduces the skill to an advisory pass."                |
| "Inline annotations are more visible — patch the body by default."  | "Body annotations mutate author-authored prose and can break formatted notes; they require explicit opt-in during the Phase 1.5 feedback loop. Frontmatter-only is the default for a reason."         |

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
