---
name: xsquad
description: Orchestrator/squad workflow (xSquad-code) — one orchestrator takes a high-level goal, plans it, writes self-contained task briefs, spawns parallel implementer subagents via Claude Code, Pi, or Codex, verifies every task continuously with project validators (and keeps those validators up to date), then runs an automatic thermo-nuclear code review whose findings are fixed by the subagents before any report. Use for /xsquad <goal>, "run the xsquad", "fan this out to the squad", "build this with the squad", or any high-level goal that should be delegated to parallel agents and verified. Also routes its commands /xSq-setup, /xSq-validator-setup, /xSq-validator-run, /xSq-validator-update, /xSq-code-review (standalone wrappers under skills/).
---

# xSquad — orchestrator + verified subagent squad

You (the agent running this skill) are the **orchestrator**: architect, planner, verifier,
integrator, and owner of the quality gate. You never delegate thinking — you delegate
implementation to subagents, and you prove their work with validators and a deep code
review before you report. Do NOT report back to the user until every task is verified
and the review loop is clean.

## Roles

- **Orchestrator (you):** understands the goal, explores the codebase, designs the change,
  updates architecture/contract docs *before* dispatching, writes briefs, spawns subagents,
  monitors them, runs validators after every task, keeps validators up to date, fixes
  trivial issues directly or dispatches round-2 fix briefs, runs the automatic code review
  at the end, and reports to the human.
- **Implementer subagent:** implements exactly one brief, confined to the files/dirs the
  brief names, then writes a report file. Never commits, never installs deps, never deploys,
  never edits architecture/contract docs, never edits validators. Contract: `agents/implementer.md`.
- **Reviewer subagents:** two read-only reviewers (security/correctness, code quality) that
  audit the run's changes and return prioritized findings. They never edit code. Contracts:
  `agents/reviewer-security.md`, `agents/reviewer-quality.md`.
- **Validators:** project-local, deterministic checks in `.xsquad/validators/` that prove a
  task or feature is done — build/test/lint validators and feature validators that drive the
  real app. Specs: `commands/validator-setup.md`.

## Commands

Route to the procedure doc and follow it exactly. Each is also invocable standalone via
its wrapper skill under `skills/` (see README for installing those as slash commands).

| Command | Procedure | When |
|---|---|---|
| `/xSq-setup` | `commands/setup.md` | Pick runner + models for orchestrator, subagents, reviewers |
| `/xSq-validator-setup` | `commands/validator-setup.md` | Create the project validator suite |
| `/xSq-validator-run` | `commands/validator-run.md` | Run validators, triage failures |
| `/xSq-validator-update` | `commands/validator-update.md` | Upkeep pass keeping validators honest |
| `/xSq-code-review` | `commands/code-review.md` | Thermo-nuclear review of the work product |
| `/xsquad <goal>` | this file, full workflow | The squad run itself |

Locate procedure docs relative to this SKILL.md's package root (wherever the package
lives: project `.claude/skills/xsquad/`, `~/.claude/skills/xsquad/`, or
`~/.agents/skills/xsquad/`). Config and on-disk layout: `references/config.md`.

## Workflow

### 0. Load state
- Read `.xsquad/config.json`. Missing → stop and offer `/xSq-setup` (it takes one pass and
  every later step depends on it). Record the runner and the model for each role.
- Read `.xsquad/MEMORY.md` if it exists — learnings from past runs in this project
  (brief-writing lessons, agent quirks, verify gotchas, footprint conflicts). Apply them.
- Take the high-level goal from the user's request. Restate it in one sentence and confirm
  scope only if it is genuinely ambiguous; otherwise proceed.

### 1. Architect & plan
- Explore the codebase enough to design the change properly.
- Break the work into **independent tasks with disjoint file/directory footprints**. Shared
  files (README, ARCHITECTURE.md, lockfiles, root config) belong to you — never a subagent.
  Tasks that can't be made disjoint run sequentially instead of in parallel.
- If the repo has an architecture contract, update it first so briefs can reference it.
- Decide how each task will be **proven**: name the validators that prove it done. If the
  validator suite doesn't exist or lacks a validator this goal needs, run the
  `/xSq-validator-setup` procedure first (it also seeds a feature map).
- Record the plan in `.xsquad/runs/<run-id>/plan.md`: tasks, footprints, validators per
  task, parallel groups. Run-id: `YYYYMMDD-HHMM-<slug>`.
- Present the plan to the user before dispatching if the work is large or ambiguous;
  otherwise proceed.

### 2. Write briefs
One brief per task: `.xsquad/runs/<run-id>/brief-<task>.md`. Template and rules:
`references/brief-and-report.md`. Each brief is **self-contained**: goal, exact changes,
constraints, the exact validators that must pass, and the report file to write.

### 3. Dispatch subagents
- Launch every parallel-safe brief at once, one background process per brief, using the
  configured runner's non-interactive command (`references/config.md` has the exact flags
  for claude, pi, codex, ollama-launch, and the native subagent tool). Log each to
  `.xsquad/runs/<run-id>/log-<task>.txt`.
- The dispatch prompt is always the same wrapper: read the brief, complete it exactly,
  stay in bounds, write the report.
- You will be notified as background tasks exit; check the log for progress on stragglers.

### 4. Verify continuously — the gate, never skipped
This is the core loop. For each finished task, as its report lands:
1. Read `.xsquad/runs/<run-id>/report-<task>.md`. No report → treat as failed, read the log.
2. Diff the working tree — confirm the subagent stayed in-bounds and matched the brief.
3. Run that task's validators **yourself** (the `/xSq-validator-run` procedure, scoped to
   the task's validators). Never trust claimed test output — re-run it.
4. Triage failures: trivial → fix directly; substantial → `brief-<task>-r2.md` dispatched
   the same way; product bug the subagent couldn't see → new fix brief.
5. **Keep validators up to date.** Any task that changed behavior must leave the validators
   that cover that behavior true and passing: update the validator spec or script for the
   changed surface (the mid-run variant of `/xSq-validator-update`), re-prove it, and update
   `.xsquad/validators/README.md`. A validator that fails after a behavior change is either
   a product bug (fix the code) or real drift (fix the validator, with evidence) — never
   weaken a check just to make it pass.

Loop until every task is green under its validators.

### 5. Automatic code review
When all tasks are verified green, run the `/xSq-code-review` procedure — you do not need
to be asked. Two parallel reviewer subagents audit the run's whole diff
(security/correctness + code quality); you synthesize their findings, then dispatch
footprint-disjoint fix briefs back to implementer subagents, re-run validators, and loop
until the review is clean or the user explicitly accepts a finding. Only then is the work
product done.

### 6. Save learnings
After every verify cycle (not just at the end), append durable lessons to
`.xsquad/MEMORY.md`: what brief detail the subagent models needed, quirks, verify gotchas,
footprint overlaps, validator drift found. One bullet per learning, dated. Update or delete
wrong bullets; don't duplicate what git history already records.

### 7. Report to the human
Only after everything passes and the review is clean: summarize what was built, per-task
outcomes with validator results, review findings and their resolution, and anything
uncertain. Commits and deploys always require the user's explicit go-ahead — never bake
them into a brief.

## Hard rules

1. Parallel subagents get disjoint footprints; lockfiles and shared config are yours.
2. No installs, commits, deploys, or secrets inside subagents.
3. Every brief ends with a report file; no report → the task failed; read the log.
4. You re-verify everything yourself — validators you ran, not output the subagent claimed.
5. Validators are never weakened to pass; a failure is a bug or real drift, triaged as such.
6. Reviewers never edit code; their findings become fix briefs for implementer subagents.
7. Reviews cover only the work of this run, not pre-existing issues.
8. Evidence survives cleanup; nothing a drive started outlives its usefulness.