---
name: outreach-research
description: 'Ranks target companies for what the user sells, as a lead list. Use when the user wants to know who to target ("find companies", "find potential clients", "lead generation"). Not for deepening a card or writing letters (use outreach-enrich-company).'
argument-hint: <target description> [sector:filter] [region:market] [limit:N] [brief:run_name]
allowed-tools: Agent, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(rm *), Read, Write, Glob, Grep, WebFetch, WebSearch, AskUserQuestion
---

# Outreach Research Pipeline

## Overview

You are an orchestrator that drives a full business outreach intelligence pipeline. You receive an outreach goal and autonomously define strategy, research sources, discover companies, scan reputations, enrich with deep intelligence, score leads, write per-company dossier cards, and produce an executive summary report. Every company gets exactly two permanent files: a `.json` (machine-readable, progressively enriched) and a `.md` (human-readable dossier card). No bulk JSON arrays.

## When to Use

Discovers prospective companies for an outreach goal and produces a scored lead list with a dossier card per company.

### When NOT to use

- The user wants to draft outreach letters or messages, or deepen an existing company card — use `outreach-enrich-company`; this skill researches targets, not content.
- The user wants competitive analysis of a single named company — use `explain` or `debug certainty:low` on public sources instead.
- The user has not defined an outreach goal or target profile — ask before invoking, or scope it first with `outreach-brief`.

## Input

- `$ARGUMENTS` — The outreach goal. Examples:
  - `"find potential clients for our DevOps consulting in DACH region"`
  - `"SaaS companies in Latin America sector:HR-tech limit:30"`
  - `"find AI startups in Singapore for partnership opportunities"`

If empty, ask the user what kind of companies they want to find and why.

## Scope Parameter

Extract scope modifiers from `$ARGUMENTS`, case-insensitive. `outreach-research` is outbound (company discovery), so scope controls **which prospective companies enter the funnel**, not which files to scan. Remaining text controls the outreach goal (orthogonal).

- **`sector:<value>`** — restrict discovery to a specific industry/vertical (e.g. `sector:HR-tech`, `sector:fintech`). Default: inferred by `outreach-strategist` from the goal text.
- **`region:<value>`** — restrict discovery to a geographic market (e.g. `region:DACH`, `region:LATAM`). It overrides any geography in the goal text or the brief and is a hard filter: the strategist targets it, the source researcher searches it, and scouts drop companies outside it. Default: inferred by `outreach-strategist` from the goal text; global if no signal.
- **`limit:<N>`** — maximum companies to carry through the pipeline. Default: 20.
- **`brief:<run_name>`** — seed discovery from an `outreach-brief` run. The strategist is given that run's `brief.json` and `climate.json`, so the target profile, outreach angles, and scoring weights reflect the captured brief and the local business climate, and the sender voice comes from the brief's voice and goal. Default: none (goal text only).
- **Default** — full-scope strategist-driven discovery using only the goal text when no modifiers are present.

## Argument Parsing

Extract from `$ARGUMENTS`:

- **goal** — the full description (everything not matching a parameter pattern)
- **sector** — optional, from `sector:<value>` (default: inferred by strategist)
- **region** — optional, from `region:<value>`; overrides any geography in the goal text or the brief (default: null, so the strategist infers geography from the goal)
- **limit** — optional, from `limit:<N>` (default: 20)
- **brief** — optional, from `brief:<run_name>`; resolves to `<PROJECT_ROOT>/.mz/outreach/<brief_run>/brief.json` + `climate.json` (default: none)

## Directory Structure

Two separate directories are used:

- **State** — `<PROJECT_ROOT>/.mz/task/<task_name>/state.md`. This is the source of truth across phases; never rely on conversation memory.
- **Outreach data** — `<PROJECT_ROOT>/.mz/outreach/<run_name>/` (called `<RUN_DIR>` in phase files) holds `strategy.json`, `sources.json`, temp `_scout/` and `_enrichment/` folders, permanent `companies/<slug>.json` + `companies/<slug>.md` pairs, `scout_summary.md`, and `<YYYY_MM_DD>_outreach_<goal_slug>.md`.

`task_name` follows the pattern `<YYYY_MM_DD>_outreach_research_<slug>`; `run_name` is `<YYYY_MM_DD>_outreach_research_<goal_slug>` (same leading-date convention). They are independent: `task_name` identifies the pipeline invocation, `run_name` identifies the outreach output bundle.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.

## Core Process

### Phase Overview

| #   | Phase                     | Agent(s)                              | Details                                                       |
| --- | ------------------------- | ------------------------------------- | ------------------------------------------------------------- |
| 0   | Setup                     | —                                     | Inline below                                                  |
| 1   | Strategy                  | `outreach-strategist`                 | `phases/discovery.md`                                         |
| 1.5 | User approval of strategy | — (orchestrator, AskUserQuestion)     | Inline below (+ `phases/discovery.md` §Phase 1.5 for details) |
| 2   | Source Research           | `outreach-source-researcher`          | `phases/discovery.md`                                         |
| 3   | Scout + Dedup             | N x `outreach-scout` (parallel)       | `phases/discovery.md`                                         |
| 4   | Scan                      | N x `outreach-scanner` (parallel)     | `phases/enrichment_and_report.md`                             |
| 5   | Enrich                    | `outreach-enrichment-orchestrator`    | `phases/enrichment_and_report.md`                             |
| 6   | Score                     | inline (orchestrator)                 | `phases/enrichment_and_report.md`                             |
| 7   | Write Cards               | N x `outreach-card-writer` (parallel) | `phases/enrichment_and_report.md`                             |
| 8   | Report                    | `outreach-reporter`                   | `phases/enrichment_and_report.md`                             |

Read the relevant phase file when you reach that phase. Do not read both phase files upfront.

### Phase 1.5: User Approval of Strategy

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/outreach/<run_name>/strategy.json` with the Read tool. Capture the full file contents (target profile, sector/geo scope, candidate-source plan, estimated fan-out cost) into context.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: strategy gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the strategy verbatim as a normal markdown chat message. Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/outreach/<run_name>/strategy.json` — do not substitute a path, summary, or placeholder. Structure:

````
## Strategy ready for review — outreach-research

```json
<verbatim contents of <PROJECT_ROOT>/.mz/outreach/<run_name>/strategy.json>
```

---
**Approve** → proceed to Phase 2 (source research and company discovery)  ·  **Reject** → mark task aborted, no outreach data generated  ·  reply with feedback to revise
````

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the strategy in the question body, it lives in the plan message above:

- question: `The strategy above is ready for review.`
- header: `Strategy`
- options: **Approve** — proceed to Phase 2 (source research and company discovery) · **Reject** — abort the task, no outreach data generated

**Response handling**:

- **Approve** → add `- strategy approved: .mz/outreach/<run_name>/strategy.json` under `## Decisions` in `state.md`, remove the `awaiting approval` entry from `what_remains`, set `Phase: strategy_approved`, and proceed to Phase 2.
- **Reject** → update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` Status to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → re-dispatch `outreach-strategist` with the feedback appended, overwrite `strategy.json`, return to Surface 1, re-read `strategy.json`, and re-emit the entire plan message from scratch with the full new contents — never diff-only, never summary-only, since context compaction may have destroyed the user's memory of earlier iterations. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: strategy gate`, stop. A missing answer is never approval.

## Red Flags

- You dispatched enrichment before the user approved the target profile.
- You used a banned data source (scraped LinkedIn, unverified aggregators, AI-summarized listings).
- Report lives in chat instead of `.mz/reports/` or the run's executive summary file.

## Verification

Before completing, output a visible block showing: run name, company count after dedup, scored leads count, and the absolute path of the executive summary report. Confirm the report file and per-company card pairs exist on disk.

______________________________________________________________________

## Phase 0: Setup

Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.

Parse arguments. Derive two names:

- `task_name` (state dir) = `<YYYY_MM_DD>_outreach_research_<slug>` where `<slug>` is a snake_case summary of the goal (max 20 chars) and `<YYYY_MM_DD>` is today's date with underscores.
- `run_name` (outreach output dir) = `<YYYY_MM_DD>_outreach_research_<goal_slug>`, max 40 chars total (keep `<goal_slug>` short to fit). Example: `"find DevOps clients in DACH"` → `2026_05_11_outreach_research_devops_dach`.

```bash
mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>"
mkdir -p "<PROJECT_ROOT>/.mz/outreach/<run_name>/companies"
```

Write `<PROJECT_ROOT>/.mz/task/<task_name>/state.md`:

```yaml
schema_version: 2
Status: running
Phase: 0
Started: <ISO timestamp>
phase_complete: false
what_remains: []
Goal: <goal>
Sector: <parsed or null>
Region: <parsed or null>
Limit: <limit>
RunName: <run_name> (outreach output dir)
BriefRun: <brief_run or null>
```

If `brief:<run_name>` was supplied, read `<PROJECT_ROOT>/.mz/outreach/<brief_run>/brief.json` and `<PROJECT_ROOT>/.mz/outreach/<brief_run>/climate.json` and carry their contents into Phase 1. If either file is missing, warn and continue without it — the brief is an enhancement, never a hard dependency. When the goal text is empty but a brief is present, derive the goal from the brief's `offering` and `goal_channels_voice.goal`.

After setup completes, read `phases/discovery.md` and proceed to Phase 1.

______________________________________________________________________

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

## Resume Support

Before creating anything in Phase 0, check if `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` exists for the resolved `task_name`. If it does, read the `Phase` field and resume from the next incomplete phase. All phases are idempotent — re-running overwrites output files.

## Error Handling

- Agent fails or returns empty: append an `Errors:` bullet in `<PROJECT_ROOT>/.mz/task/<task_name>/state.md`, continue with available data.
- All agents in a phase fail (zero results): stop the pipeline and report the failure.
- Never fabricate data — incomplete results are better than false results.
- Corrupted company JSON during any phase: log the error in state.md, skip that company, continue.
