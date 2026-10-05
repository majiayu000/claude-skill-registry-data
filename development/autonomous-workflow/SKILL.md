---
name: autonomous-workflow
description: "Execute development workflows through Explore-Plan-Code-Verify phases with task-driven tracking, Tier 1/2/3 action classification, decision journaling, and bounded debug loops. Use when executing any development workflow autonomously or orchestrating multi-step implementation tasks. This skill MUST be consulted because skipping phases causes rework, and unbounded verification loops cause agents to loop forever on unsolvable problems."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent, TaskCreate, TaskList, TaskUpdate, TaskGet, AskUserQuestion
---

# Autonomous Workflow

## Iron Law

**NO SKIPPING PHASES. Explore, then Plan, then Code, then Verify. Every phase produces an artifact.**

## Explore > Plan > Code > Verify

1. **EXPLORE**: Agent(Explore) for unfamiliar code; independent Bash queries in one message; read referenced files. LSP: `goToDefinition` from issue keywords, `findReferences` for impact.
2. **PLAN**: TaskCreate per deliverable, dependencies via addBlockedBy, display the plan.
3. **CODE**: TaskUpdate(in_progress); implement; commit incrementally (Tier 1); TaskUpdate(completed) only after the per-task gate. LSP: `hover` before modifying.
4. **VERIFY**, four mandatory layers:
   a. **Static**: lint/test/typecheck in parallel. With `lsp.diagnosticsAsQuality`, LSP diagnostics add a signal (errors P1, warnings P2), never replace CLI checks.
   b. **Runtime**: build, start, verify; on failure enter the debug-fix-retest loop (bounded by `closedLoop.maxDebugIterations`).
   c. **Review**: self-review with fix-forward; fix P1/P2 immediately.
   d. **Verdict**: when `verdict.enabled`, dispatch verdict-judge with acceptance criteria + evidence bundle only (no diff, rationale, journal). Per criterion PASS/FAIL/NEEDS-HUMAN-REVIEW; FAIL enters a fix loop, NEEDS-HUMAN-REVIEW escalates.

## Task-Tool Contract

TaskCreate in PLAN (one per deliverable, imperative subject, acceptance criteria in description); TaskGet before working a task; TaskUpdate(in_progress) before starting; TaskUpdate(completed) only after the per-task gate; TaskList at checkpoints.

## Per-Task Verification Gate

`TaskUpdate(taskId, status: "completed")` is blocked until ALL hold:

1. All tests pass (existing and new); otherwise the task stays `in_progress` in the debug-fix-retest loop.
2. The task's verification command was run and its output recorded as evidence now, not at VERIFY.
3. Every modified file is classified; out-of-context files resolved (separate commit, removed, or user-approved).
4. When `settings.json` `testing.tddMode` is `enforce` (default), RED-GREEN-REFACTOR was observed: failing test before implementation.

## Three-Tier Safety

| Tier | Actions | Behavior |
|------|---------|----------|
| **1** Autonomous | Commits, branches, file edits, staging | Execute |
| **2** Journal | Push, PR creation, issue assignment | Execute, log to journal |
| **3** Confirm | Merge, release, force operations | Human confirmation, always |

`settings.json` `tiers`; promotable (journal→confirm), never demotable. Full tables: `references/three-tier-safety.md`.

## AskUserQuestion Enforcement

"Use the AskUserQuestion tool" means invoke the tool with contextual options, never plain text.

## Decision Journal

- **Init**: `{journal-dir}/issue-{N}.md` at branch creation (default `.decisions/`).
- **Log**: hooks auto-log edits and commits to a gitignored trail; skills add timestamped entries (category, decision, rationale, risk).
- **Summarize** for the PR body: `public` entries only; `internal` (security rationale, credentials, vulnerabilities) never reaches PR bodies, comments, or logs.
- **Anti-estimation guard**: no calendar-time estimates in entries; t-shirt sizing (S/M/L) only when asked.

## Bounded Verification

Ceilings (`qualityCheckMaxIterations`, `closedLoop.maxDebugIterations` default 5, `fixForwardMaxIterations`) are safety nets, not budgets. Run, fix, re-run until convergence. Halt only for **genuine non-convergence** (same failure across the last 3 iterations with no progress AND ceiling reached), then file a six-field escalation per `skills/llm-operator-principles/SKILL.md` § Genuine non-convergence. Never silently loop past the ceiling.

## Stop Conditions

Plan >10 tasks for one issue: decompose first. Contradictory EXPLORE signals: ask before planning. >5 files modified without a commit: stop; tasks too large.

## Closed-Loop Mandate

Fix failures yourself; never report and move on. Minimum runtime verification per project type: `runtime-verification`. Only `markdown-only`, `config-only`, `dependency-bump-only` may skip runtime checks (with the evidence that skill requires); any other skip requires a six-field escalation.

## Graceful Degradation

No agent teams: sequential. No quality commands: `Skill(capability-discovery)`, then runtime-only. No LSP: grep. No gh: git-only.

## Proactive Autonomy

Try first; present 2-3 options with a recommendation, never open questions; use the six fields in `references/escalation-format.md`. Escalate only for: irreversible actions (Tier 3); genuinely ambiguous product/architecture decisions; out-of-whitelist runtime skips; genuine non-convergence. Never for: Tier 1/2 actions; decisions with clear policy; any P1/P2/P3 disposition (fix it — no follow-up issues in default mode); approaching a ceiling.
