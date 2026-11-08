---
name: brainstorm
description: 'Generates ideas for an open problem from a panel of differing viewpoints. Use when the user says "brainstorm", "creative ideas for" or "think about this from different angles", or wants options. Not for critiquing a proposal (use expert).'
argument-hint: <topic or problem to brainstorm>
allowed-tools: Agent, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Read, Write, Glob, Grep, AskUserQuestion, WebFetch, WebSearch
---

# Creative Brainstorming Pipeline

## Overview

You orchestrate a multi-lens brainstorming session. A curated panel of 5 thinkers from 16 available lenses generates ideas from diverse perspectives, a synthesizer merges them, and the panel votes iteratively until consensus or max rounds.

## When to Use

Creative ideation on an open problem, with ideas drawn from a panel of differing viewpoints.

### When NOT to use

- The user wants a single concrete decision or implementation — use `build` or `explain` instead.
- The user wants verification of an existing idea — use `debug certainty:low` instead.
- The problem has one objectively correct answer knowable from docs — look it up instead of ideating.

## Input

`$ARGUMENTS` — The topic, problem, or question to brainstorm. If empty, ask the user.

## Constants

- **MAX_ITERATIONS**: 5
- **PANEL_SIZE**: 5
- **TOTAL_LENSES**: 16
- **MAJORITY_THRESHOLD**: 3
- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`. Phase files write `<SKILL_DIR>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Available Lenses

| Agent              | Lens                                                  | Best for                                                 |
| ------------------ | ----------------------------------------------------- | -------------------------------------------------------- |
| lens-engineer      | Systems thinking, technical feasibility, scalability  | Technical problems, product design, architecture         |
| lens-artist        | Aesthetics, form, visual communication, experience    | Design, branding, UX, presentation, media                |
| lens-philosopher   | Meaning, ethics, cultural impact, narrative framing   | Ethics, purpose, messaging, social impact                |
| lens-mathematician | Patterns, optimization, formal logic, structure       | Algorithms, processes, strategy, quantitative            |
| lens-scientist     | Hypotheses, experiments, evidence, natural systems    | Research, validation, methodology, bio-inspired          |
| lens-economist     | Incentives, markets, game theory, resource allocation | Business models, pricing, strategy, growth               |
| lens-storyteller   | Narrative, metaphor, emotional arcs, audience         | Marketing, pitching, content, communication              |
| lens-futurist      | Emerging trends, disruption, long-term trajectories   | Innovation, strategy, roadmaps, future-proofing          |
| lens-psychologist  | Cognition, bias, motivation, behavior, UX             | User research, adoption, persuasion, habits              |
| lens-historian     | Precedent, patterns of change, cultural context       | Risk, lessons learned, positioning, analogies            |
| lens-cto           | Architecture, build-vs-buy, tech-debt, org impact     | Technology strategy, platform leverage, delivery risk    |
| lens-data          | Measurement, experimentation, instrumentation, growth | Metrics design, A/B tests, analytics, growth loops       |
| lens-devops        | Reliability, SLOs, observability, capacity, cost      | Production systems, on-call, rollout, operational burden |
| lens-product       | PMF, jobs-to-be-done, prioritization, kill criteria   | Roadmap, MVP scoping, user value, backlog tradeoffs      |
| lens-security      | Threat modeling, attack surface, authZ, compliance    | Appsec review, data handling, trust boundaries           |
| lens-seo           | Search intent, content strategy, technical SEO        | Organic growth, content planning, indexing decisions     |

## Core Process

### Phase Overview

| #   | Phase              | Details                       | Loop?            |
| --- | ------------------ | ----------------------------- | ---------------- |
| 0   | Setup              | Inline below                  | --               |
| 1   | Panel Selection    | Inline below                  | --               |
| 1.5 | User Approval      | Inline gate                   | --               |
| 2   | Ideation           | `phases/ideation.md`          | --               |
| 3   | Synthesis + Voting | `phases/voting_and_report.md` | max 5 iterations |
| 4   | Report             | `phases/voting_and_report.md` | --               |

## Red Flags

- You collapsed into one-voice output instead of running multiple personas.
- You skipped the critique/voting phase and jumped straight to a report.
- Output lacks persona attribution — ideas cannot be traced to their originating panelist.

## Verification

Before completing, output a visible block showing: selected panel (5 names), iteration count, voting rounds, majority verdict or tie status, and the absolute path of the written report. Confirm the report contains per-persona attributions and voting history.

## Phase 0: Setup

Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below. Derive task name as `<YYYY_MM_DD>_brainstorm_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and slug is a snake_case summary (max 20 chars) of the topic; on same-day collision append `_v2`, `_v3`. Run `mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>"`. Write `state.md` with schema_version: 2, Status: running, Phase: setup, Started: timestamp, phase_complete: false, what_remains: [], Iteration: 0.

## Phase 1: Panel Selection

Analyze the topic and select the **PANEL_SIZE** (5) best-suited lenses from the table above. Consider:

- What lenses are most relevant to this topic?
- What complementary perspectives would create productive tension?
- Favor diversity of approach over obvious relevance — a historian on a tech problem or an artist on a business problem often produces the most surprising ideas.

Write `<PROJECT_ROOT>/.mz/task/<task_name>/panel.md` with the 5 selected agents and a one-sentence justification for each.

Update state phase to `panel_selected`.

## Phase 1.5: User Approval Gate

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated.

**Pre-read**: Read `<PROJECT_ROOT>/.mz/task/<task_name>/panel.md` with the Read tool. Capture the full file contents (5 selected panelist agents with one-sentence justifications) into context. Also derive the 11 not-selected lenses from the 16-lens table minus the 5 in `panel.md`.

**State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: panel gate]`; `Status` stays `running`.

**Surface 1 — emit the plan message.** Output the panel verbatim as a normal markdown chat message. Emit the full verbatim contents of `<PROJECT_ROOT>/.mz/task/<task_name>/panel.md` plus the inline list of not-selected lenses — do not substitute a path, summary, or placeholder. Structure:

```
## Panel ready for review — brainstorm

Panel assembled for "<topic>".

Selected (with justifications):
<verbatim panel.md contents>

Not selected: <comma-separated list of 11 remaining lens names>

---
**Approve** → proceed to Phase 2 (Ideation), dispatch panel in parallel  ·  **Reject** → mark task aborted, stop processing  ·  reply with feedback to revise
```

**Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the panel contents in the question body, they live in the plan message above:

- question: `The panel above is ready for review.`
- header: `Panel`
- options: **Approve** — proceed to Phase 2 (Ideation) · **Reject** — abort the task, nothing dispatched

**Response handling**:

- **Approve** → add `- panel approved: .mz/task/<task_name>/panel.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry from `what_remains`, set `Phase: panel_approved`, and proceed to Phase 2.
- **Reject** → update state to `aborted_by_user` and stop. Do not proceed.
- **Any other reply (feedback)** → adjust panel per feedback, overwrite `panel.md`, return to Surface 1, re-read `panel.md`, and re-emit the entire plan message from scratch with the full new contents — never diff-only, never summary-only, since context compaction may have destroyed the user's memory of earlier iterations. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.
- **No answer** → set `Status: blocked`, keep `awaiting approval: panel gate`, stop. A missing answer is never approval.

## Phase 2: Ideation

Dispatch the 5 selected personality agents in parallel. **See `phases/ideation.md`** for dispatch prompt template and idea collection. Update state phase to `ideation_complete`, increment iteration.

## Phase 3: Synthesis + Voting

A randomly-selected panelist synthesizes all ideas, then all 5 vote.

**See `phases/voting_and_report.md` → Phase 3** for synthesis, voting, and convergence check.

If majority reached → proceed to Phase 4. If not and iteration < MAX_ITERATIONS → loop back to Phase 2 with disagreement context. If MAX_ITERATIONS hit → proceed to Phase 4 with best available.

## Phase 4: Report

Compile final report with winning ideas, all perspectives, and voting history. **See `phases/voting_and_report.md` → Phase 4** for report template. Write to `<PROJECT_ROOT>/.mz/reports/<YYYY_MM_DD>_brainstorm_<topic_slug>.md` (append `_v2`, `_v3` if exists). Present summary to user.

## Error Handling

- **Empty topic**: ask via AskUserQuestion. Never guess.
- **Agent returns empty/off-topic**: retry once with clarified prompt. If still empty, exclude from voting and note in report.
- **All iterations exhausted without majority**: report the top 2-3 ideas with vote distribution and all personality feedback. Let the user decide.
- **Tie in votes**: report both tied ideas equally, include all justifications.

## State Management

After each phase, update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md`. Track current phase, iteration count, votes per round, and participating agents. Persist all ideas and votes in `<PROJECT_ROOT>/.mz/task/<task_name>/history.md` for later rounds.

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

Critical: never proceed past the approval gate without explicit user approval. Never skip voting. Never fabricate votes.
