---
name: do-roast
description: 'Roasts code in a character voice, each joke tied to a real finding. Use when the user wants a funny review of code ("roast this code", "do-roast", "make fun of", "character roast of"). Not for a serious code review (use review-branch).'
argument-hint: <persona> <freeform target — path, branch, text, or natural-language scope>
allowed-tools: Agent, Bash(git rev-parse *), Bash(git diff *), Bash(mkdir *), Bash(date *), Bash(printf *), Bash(sha256sum *), Bash(shasum *), Read, Write, Glob, Grep, AskUserQuestion, WebFetch, WebSearch
---

# Evidence-Anchored Character Roasting Pipeline

## Overview

You orchestrate a character-voice code roast. Static analysis, docs coherence, and web best-practice research produce a structured dossier of numbered findings; the user's chosen persona agent renders a roast that may embellish tone but may not invent substance. Every roast line must cite a real finding.

## When to Use

A funny roast, in a chosen persona's voice, of code, a branch, a PR or text, where every roast line cites a real finding.

### When NOT to use

- Actual code review — use `/review-branch` or `/audit`.
- Actual planning — use `/build`.
- Serious architecture critique — use `/explain`.
- The target does not exist or cannot be resolved to concrete files or text.

## Input

`$ARGUMENTS` is split on first whitespace. Token 1 = persona (validated against `PERSONA_ALLOWLIST`, case-insensitive). Remainder = free-form target prompt. Empty `$ARGUMENTS` → ask. Unknown persona → ask with allowlist. Empty remainder → ask.

## Constants

- **PERSONA_ALLOWLIST**: `["caveman", "wh40k-ork", "pirate", "viking", "dwarf", "drill-sergeant", "yoda"]` (lowercase canonical)
- **MAX_PERSONAS**: 7 (allowlist bound; single-persona dispatch per invocation)
- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **REPORT_DIR**: `<PROJECT_ROOT>/.mz/reports/`
- **RESEARCH_CACHE_DIR**: `<PROJECT_ROOT>/.mz/research/` (stack-wide web cache, 7-day staleness)
- **MAX_FINDINGS**: 30 (upper bound on dossier entries per invocation)
  - Note: `MAX_FINDINGS=30` is the upper bound. Analysis should prefer 10-15 high-quality Critical/Nit findings over 30 weak Optional/FYI — reduces dispatch token cost and improves voice focus.
- **DOSSIER_SEVERITY_LABELS**: `["Critical", "Nit", "Optional", "FYI"]`

## Available Personas

<!-- verify: every value in PERSONA_ALLOWLIST must appear in this table -->

| Persona        | Voice                         | Best for roasting                                           |
| -------------- | ----------------------------- | ----------------------------------------------------------- |
| caveman        | Hulk-speak, pre-linguistic    | Over-engineered abstractions — "me no understand, me smash" |
| wh40k-ork      | Greenskin dakka warrior       | Weedy/overclever code ("dat code iz weedy")                 |
| pirate         | Robert-Newton West-Country    | Ships that won't sail — bloated files, leaks, "Davy Jones"  |
| viking         | Skald with kennings           | Forgettable code, no sagas, "argr" / ignoble logic          |
| dwarf          | Scottish brogue + Dammaz Kron | Shoddy craftsmanship — "umgak", grudge book additions       |
| drill-sergeant | FMJ Gunnery-Sergeant cadence  | Discipline failures, fitness metaphors, profanity allowed   |
| yoda           | OSV-inverted disappointment   | Clouded logic, "much to learn" disappointment register      |

## Core Process

### Phase Overview

| #   | Phase                      | Details             |
| --- | -------------------------- | ------------------- |
| 0   | Setup + arg parse          | Inline below        |
| 0.5 | Target resolution          | Inline below        |
| 1   | Structural/smell analysis  | `phases/analyze.md` |
| 2   | Docs coherence analysis    | `phases/analyze.md` |
| 3   | Web best-practice research | `phases/analyze.md` |
| 4   | Dossier writer             | `phases/analyze.md` |
| 5   | Persona dispatch           | `phases/render.md`  |
| 6   | Report assembly + teaser   | `phases/render.md`  |

## Common Rationalizations

| Rationalization                                                                                | Rebuttal                                                                                                                |
| ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| "Just this once, the persona can riff on something not in the dossier — it's funnier."         | The whole plugin's value is evidence anchoring. One fabricated line poisons every future roast's credibility. Cut it.   |
| "The code probably has this bug even though analysis didn't find it — persona can mention it." | If analysis missed it, analysis gets re-run. The persona may not invent findings. Re-run Phase 1-4, do not extrapolate. |
| "The user will never notice a made-up line if the rest is grounded."                           | The user will grep the roast for `Finding N` citations. Fabrication is detectable and contractually forbidden.          |

## Red Flags

- Dossier contains fewer than 3 findings but persona roast is >200 lines — embellishment exceeded substance.
- Roast mentions a file path that does not appear in the dossier — fabrication.
- Persona agent was dispatched without the dossier inlined in the prompt.
- Any author name, git blame output, or real-person reference in the dossier or report.
- A natural-language target with several candidates was roasted without asking which ones.

## Verification

Output a visible block showing: task name, resolved target, persona chosen, finding count by severity, report path, and the rendered teaser paragraph. Confirm the report file exists and is non-empty. Confirm every `Finding N` in the dossier has at least one reference in the rendered roast (soft check).

## Phase 0: Setup

Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below. Parse `$ARGUMENTS`: split on first whitespace; validate token 1 against `PERSONA_ALLOWLIST` (lowercase compare). Unknown → AskUserQuestion listing allowed personas. Empty remainder → AskUserQuestion asking what to roast. Skill name `do-roast` → task dir prefix `do_roast` (snake_case). Derive task name: `<YYYY_MM_DD>_do_roast_<slug>` where slug is a snake_case summary (max 20 chars) of the resolved target or first 3 words of the remainder, and `<YYYY_MM_DD>` is today's date with underscores. Create `TASK_DIR<task_name>/`. Write `state.md` with `schema_version: 2` as the first line, then `Status: running`, `Phase: setup`, `Started: <ISO8601>`, `phase_complete: false`, `what_remains: []`, `Persona: <chosen>`, `Target_raw: <remainder>`.

## Phase 0.5: Target Resolution

Read `phases/analyze.md` ("Phase 0.5: Target resolution detail"), run its ladder on `Target_raw`, and record the result in `state.md` as that section describes. Explicit paths, a branch diff and raw text name their target directly, so the roast goes on to Phase 1 without asking.

Only a natural-language target (rung 4) that leaves more than one candidate needs the user. Ask with an input collector, not an approval gate: no plan message and no Approve/Reject.

- Set `what_remains: [awaiting answer: target]`, keep `Status: running`, and call AskUserQuestion once: question `Which files should the <persona> roast for "<Target_raw>"?`, header `Target`, `multiSelect: true`, one option per candidate with the path as the label and why it matched as the description.
- Record the chosen paths as `resolved_target_list`, set `what_remains: []`, and go on to Phase 1. Run a typed `Other` answer through the ladder again.
- If nobody can answer, set `Status: blocked` and stop.

## Error Handling

- Empty `$ARGUMENTS` → AskUserQuestion (never guess).
- Unknown persona → AskUserQuestion with `PERSONA_ALLOWLIST`.
- Target resolves to 0 files AND is not raw text → escalate with `STATUS: BLOCKED` and prompt user.
- Persona agent returns empty → retry once with clarified prompt; still empty → set `Status: complete` with the concern under `## Notes` in `state.md`, and include the raw dossier in the report.

## State Management

Update `TASK_DIR<task_name>/state.md` after every phase transition. Track: current phase, persona, resolved target list, finding counts by `DOSSIER_SEVERITY_LABELS`, report path.

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

Critical: every line of the rendered roast must trace to a numbered Finding in the dossier. No invention. No real-person attacks. No git blame. If the persona cannot find something to roast within the evidence, it says so — it does not fabricate.
