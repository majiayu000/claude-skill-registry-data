---
name: deep-research
description: 'Researches a topic across many web sources and writes a sourced report. Use when the user says "research X", "deep dive into" or "what is the state of", or needs a thorough briefing. Not for consolidating work already on disk (use combine).'
argument-hint: <research topic>
allowed-tools: Agent, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Read, Write, AskUserQuestion
---

# Deep Research

## Overview

Conduct exhaustive, multi-agent research on a topic by decomposing it into independent domains, dispatching parallel pipeline-web-researcher agents, and synthesizing findings into a single report under `.mz/research/`.

## When to Use

Exhaustive multi-source web research on a topic, synthesized into a single sourced report.

### When NOT to use

- Research that already exists on disk and only needs consolidating — use `combine`.
- The user wants a one-line factual answer — use plain web search.
- The topic is narrow enough for a single pipeline-web-researcher agent — dispatch directly.
- The user wants a code review or audit — use `review-branch` or `audit`.

## Arguments

`$ARGUMENTS` is the research topic or question. If empty, ask the user.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.

## Core Process

### Phase Overview

| #   | Phase                         | Details                         |
| --- | ----------------------------- | ------------------------------- |
| 0   | Setup                         | inline below                    |
| 1   | Decomposition + approval gate | inline below                    |
| 2-5 | Research, synthesis, report   | `phases/research_and_report.md` |

### Phase 0: Setup

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS`. If the research topic is empty, escalate via AskUserQuestion — never guess.
1. `task_name` = `<YYYY_MM_DD>_deep_research_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<slug>` is a snake_case summary of the topic (max 20 chars); on same-day collision append `_v2`, `_v3`.
1. Run `mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>/"`.
1. Write `state.md` with, in order: `schema_version: 2` (first line), `Status: running`, `Phase: 0`, `Started: <ISO timestamp>`, `phase_complete: false`, `what_remains: []`, `Topic: <original argument>`, `Subtopics: []`.
1. Emit a visible setup block: `task_name`, topic, working dir, report dir (`<PROJECT_ROOT>/.mz/research/`).

### 1. Analyze and decompose the topic

Break `$ARGUMENTS` into 3-7 independent research domains/subtopics. Each subtopic should be:

- Researchable independently (no dependency on other subtopics' results)
- Specific enough to yield focused search results
- Broad enough to warrant 20+ pages of research

Example for "State of WebAssembly in 2026":

- **Runtime performance** — benchmarks, comparison with native code, recent improvements
- **Language support** — which languages compile to WASM, toolchain maturity
- **Browser adoption** — browser support, feature parity, market share
- **Server-side WASM** — WASI, edge computing, cloud runtimes
- **Ecosystem** — package managers, frameworks, developer tools
- **Production usage** — companies using WASM in production, case studies

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-write + capture**: Write the decomposition to `<PROJECT_ROOT>/.mz/task/<task_name>/decomposition.md` as a numbered list of 3-7 subtopics, each with a 1-3 sentence description and rationale. Then Read that file with the Read tool to capture its full contents into context for the gate.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: decomposition gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the artifact verbatim as a normal markdown chat message. Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/decomposition.md` — do not substitute a path, summary, or placeholder:

```
## Research decomposition ready for review — deep-research

<verbatim contents of <PROJECT_ROOT>/.mz/task/<task_name>/decomposition.md>

---
**Approve** → proceed to parallel dispatch of pipeline-web-researcher agents across all subtopics  ·  **Reject** → abort the task, mark state aborted_by_user  ·  reply with feedback to revise
```

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the decomposition in the question body:

- question: `The research decomposition above is ready for review.`
- header: `Subtopics`
- options: **Approve** — proceed to parallel dispatch of pipeline-web-researcher agents · **Reject** — abort the task, mark state aborted_by_user

**Response handling**:

- **Approve** → add `- decomposition approved: .mz/task/<task_name>/decomposition.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry from `what_remains`, set `Phase: decomposition_approved`, and proceed to Step 2 (dispatch researchers).
- **Reject** → update state to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → adjust the decomposition accordingly, overwrite `decomposition.md`, return to this gate, re-read `decomposition.md`, and re-emit the entire plan message from scratch with the full new contents — never diff-only, never summary-only, since context compaction may have destroyed the user's memory of earlier iterations. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval; never dispatch researchers without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: decomposition gate`, stop. A missing answer is never approval.

### 2. Dispatch parallel pipeline-web-researcher agents

Launch a `pipeline-web-researcher` agent per subtopic in parallel. **See `phases/research_and_report.md` → Step 2** for the dispatch prompt template.

### 3. Collect and synthesize

After all agents complete, cross-reference findings, identify emergent patterns, and assess coverage. **See `phases/research_and_report.md` → Step 3**.

### 4. Write the report

Write the final report to `<PROJECT_ROOT>/.mz/research/` using the naming convention `<YYYY_MM_DD>_research_<slugified_topic>.md`. **See `phases/research_and_report.md` → Step 4** for the template.

### 5. Report to user

Display path, source count, subtopic count, and top 3-5 findings. Then set `Status: complete`, `Phase: 5`, `phase_complete: true` and `what_remains: []` in `state.md`, and add the report path, relative to the project root, to `FilesWritten`.

## Red Flags

- You dispatched a single researcher instead of a parallel fan-out across subtopics.
- You skipped the decomposition approval gate and jumped straight to research.
- The report lives in chat output instead of `.mz/research/<file>.md`.

## Verification

Output the final report path (`<PROJECT_ROOT>/.mz/research/<YYYY_MM_DD>_research_<slug>.md`), confirm the file exists on disk, and print the number of subtopics researched alongside the top 3-5 findings.

## Error Handling

- **Empty topic argument** → escalate via AskUserQuestion; never guess.
- **Missing tooling** (`WebSearch`/`WebFetch` unavailable, `Agent` tool absent) → escalate via AskUserQuestion rather than degrade silently.
- **Empty researcher result** (agent returns nothing or malformed output) → retry that subtopic once with a clarified prompt; if still empty, note the gap in `state.md` and escalate via AskUserQuestion before writing the final report.
- Never guess — on any ambiguity (unclear scope, conflicting subtopics, source availability) escalate via AskUserQuestion rather than fabricate.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
