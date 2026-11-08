---
name: freelance-pitch
description: 'Drafts a grounded freelance proposal for one gig. Use when the user wants to pitch a specific gig, by rank, URL or pick ("freelance pitch", "draft proposal", "pitch this gig", "proposal for gig 3"). Not for finding gigs (use freelance-search).'
argument-hint: "[<rank-N> | <gig-URL>] [personality:off]"
allowed-tools: Agent, AskUserQuestion, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(test *), Bash(tr *), Bash(sed *), Bash(cut *), Bash(cp *), Bash(rm *), Bash(sha1sum *), Bash(shasum *), Read, Write, Edit, Glob, Grep, WebFetch, WebSearch
---

# Freelance Pitch

## Overview

You generate a single grounded freelance proposal for a selected gig. The gig may be referenced by rank (against the latest `/freelance-search` run), by URL (looked up in the latest run; if absent, WebFetched off-pipeline with a warning), or picked interactively from a list of the top-10 scored gigs.

The proposal is a markdown file at `.mz/outreach/<run_dir>/proposals/<gig_slug>.md`. Word cap: 350. Hard. Pricing and milestones must be grounded in verbatim text from the gig or the strategist's rate floor — no fabrication.

## When to Use

Drafting a proposal for one specific freelance gig, picked from the latest search run or given by URL.

### When NOT to use

- The user wants to find gigs — use `/freelance-search` instead.
- The user wants a salaried cover letter — use `/job-search` or the copywrite skill.
- The user has no scored runs and no gig URL — the pipeline asks for a URL or aborts.

## Input

- `$ARGUMENTS` — optional, one of:
  - An integer rank (e.g. `3`) → resolve against `<search_run_dir>/scored.json` of the newest freelance-search run.
  - A URL → look up in that `scored.json`; if not found, WebFetch with a warning.
  - Empty → interactive picker.

## Directory Structure

- **State** — `<PROJECT_ROOT>/.mz/task/<task_name>/state.md`.
- **Output** — when resolving against an existing freelance-search run: `<search_run_dir>/proposals/<gig_slug>.md`. When operating off-pipeline (URL with no prior run): `<PROJECT_ROOT>/.mz/outreach/<YYYY_MM_DD>_freelance_pitch_<slug>/proposals/<gig_slug>.md`.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.

## Core Process

### Phase Overview

| #   | Phase                         | Agent(s)                          | Details                       |
| --- | ----------------------------- | --------------------------------- | ----------------------------- |
| 0   | Resolve gig (rank/URL/picker) | — (orchestrator, AskUserQuestion) | `phases/resolve_and_pitch.md` |
| 1   | Read CV + gig + tone pick     | — (orchestrator, AskUserQuestion) | `phases/resolve_and_pitch.md` |
| 1.5 | Tone preference approval      | — (orchestrator)                  | `phases/resolve_and_pitch.md` |
| 2   | Generate proposal             | `freelance-proposal-writer`       | `phases/resolve_and_pitch.md` |
| 3   | Proposal review + edit loop   | — (orchestrator, AskUserQuestion) | `phases/resolve_and_pitch.md` |
| 4   | Write final proposal file     | — (orchestrator)                  | `phases/resolve_and_pitch.md` |

Read the phase file when reaching Phase 0.

## Red Flags

- You generated a proposal without a CV — proposal-writer cannot ground the credibility hook.
- You allowed a milestone with no verbatim grounding from `gig.project_scope_raw`.
- You let a pricing figure stand that does not trace to `gig.budget_range_raw` or `strategy.rate_floor`.
- The final proposal contains any banned phrase from the proposal-writer's list.
- The proposal exceeds 350 words.
- You skipped the user approval gate at Phase 3.

## Verification

Before completing, output a visible block showing: gig title, gig URL, source, output file path, word count, engagement type assumed, and a one-line excerpt of the opener. Confirm the proposal file exists on disk.

______________________________________________________________________

## Phase 0 entry

Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.

Parse `$ARGUMENTS`:

- Integer (e.g. `3`) → `rank_arg`.
- URL (starts with `http://` or `https://`) → `url_arg`.
- `personality:off` token (anywhere in `$ARGUMENTS`) → `personality_mode = off` (default `on`); disables the Phase 1.6 reader-style read so proposals use neutral structure.
- Empty (no rank or URL) → interactive picker.

Find the newest freelance-search run. That skill keeps its state at `<PROJECT_ROOT>/.mz/task/<YYYY_MM_DD>_freelance_search_<slug>/state.md` and its data in the outreach folder that state names under `RunName`.

1. Glob `<PROJECT_ROOT>/.mz/task/*_freelance_search_*/state.md` and sort the matches by the `<YYYY_MM_DD>` prefix of their task folder, newest first, breaking a same-day tie by the later `Started` value. Don't keep Glob's own order or sort by modification time: writing `proposals/` into an older run would make it look newest.
1. Walk that list and stop at the first state whose run folder holds a `scored.json`; a run without one never finished scoring. Set `search_state` to that file and `search_run_dir` to `<PROJECT_ROOT>/.mz/outreach/<RunName>`, with `RunName` read from it. If no state qualifies, there is no prior run.

Branching:

- **`rank_arg` set** → require a prior run. If there is none, AskUserQuestion: "No prior /freelance-search run found. Provide a gig URL, or **Cancel**."
- **`url_arg` set** → if a prior run exists, look up the URL in `<search_run_dir>/scored.json`. If found, use the scored record. If not found, WebFetch the URL and treat as off-pipeline (warn: no prior scoring).
- **Empty** → if a prior run exists, AskUserQuestion with a single-select menu of the top-10 scored gigs (label = `#<rank> <title> — <client> (score <score>)`) plus an "Other URL" option. If there is none, AskUserQuestion demands a URL or aborts.

Set `task_name = <YYYY_MM_DD>_freelance_pitch_<gig_slug>`. Set `run_dir`:

- If gig came from `<search_run_dir>/scored.json`: `run_dir = search_run_dir` (proposals nested under existing run).
- If gig is off-pipeline (URL with no prior scoring): `run_dir = <PROJECT_ROOT>/.mz/outreach/<task_name>` (new sibling directory).

```bash
mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>"
mkdir -p "<run_dir>/proposals"
```

Read `phases/resolve_and_pitch.md` for the rest.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

## Error Handling

- Off-pipeline WebFetch fails: AskUserQuestion to retry the URL or Cancel.
- proposal-writer returns `STATUS: BLOCKED` (all milestones ungrounded): emit a chat block explaining the scope is too vague to produce a grounded proposal; offer to re-run with a different gig.
- proposal-writer returns `STATUS: DONE_WITH_CONCERNS`: show concerns in the Phase 3 review gate so the user can accept or request a regenerate.

## Resume Support

Phase 0 always re-resolves the gig (cheap). Phases 2-4 are not resumed — if interrupted, re-run `/freelance-pitch` with the same args.
