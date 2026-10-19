---
name: implementation-planning
description: >
  Turn a feature request or bug report into a verified, ordered implementation plan
  of small steps, each with files touched, a verification command, and a rollback
  point. Use when a task spans multiple files or steps, requirements are ambiguous,
  work will be handed to another agent or person, or before starting a refactor or
  migration. Covers scoping, open questions, risk ordering, and plan review. Not for
  one-line fixes, for high-level system design (see system-architecture-design), or
  for recording a single decision (see architecture-decision-records).
compatibility: >
  Any Agent Skills-compatible coding agent. Needs read access to the repository;
  git is useful for confirming current state.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "planning, task-breakdown, scoping, workflow, ai-agents, engineering-process"
  topics: "ai-agents, software-development, devtools"
---

# Implementation Planning

A plan is a short, checkable path from the repository's *current, observed* state to a defined *done*. Its job is to expose wrong assumptions cheaply, before code is written. A good plan is small enough to read in two minutes and specific enough that someone else could execute step 1 without asking you anything.

Related skills: [system-architecture-design](../system-architecture-design/SKILL.md) (system-level structure), [architecture-decision-records](../architecture-decision-records/SKILL.md) (record choices made while planning), [test-driven-development](../test-driven-development/SKILL.md) (red-green steps inside each plan step), [git-branching-worktrees](../git-branching-worktrees/SKILL.md) (isolating the work), [refactoring](../refactoring/SKILL.md), [verification-before-completion](../verification-before-completion/SKILL.md) (closing the plan). Depth: [plan template](references/plan-template.md), [scenarios](references/scenarios.md), [sources](references/sources.md).

## When to use

- The change touches more than ~3 files or more than one module.
- Requirements are ambiguous or the request has several plausible readings.
- You will delegate parts to other agents or hand the task to a person.
- The change is hard to reverse: data migrations, public API changes, dependency upgrades.

## When not to use

- Typos, one-line fixes, renames inside one file: just do it and verify.
- Choosing between architectures: use system-architecture-design, then record the outcome as an ADR.
- The user asked only for an explanation or exploration.

## Non-negotiable rules

1. **Plan from observed state.** Read the code, tests, and docs involved before writing steps. Never plan against files you have not opened or APIs you have not confirmed exist.
2. **Surface ambiguity; do not guess silently.** List open questions. Ask the user when an answer would change the plan materially; otherwise state your assumption explicitly and proceed.
3. **Every step has a verification.** A step with no way to check it is not finished planning.
4. **Scope is part of the plan.** State what is out of scope. Do not add refactors, features, or cleanup nobody requested.
5. **No irreversible or shared-system actions without explicit user authorization**: pushing, deploying, deleting data, force operations, schema changes on shared databases. Mark such steps as "needs approval".
6. **Plans are not secrets stores.** Never copy credentials, tokens, or private data into a plan file.
7. **A plan is revisable.** When reality contradicts it, update the plan and say so; do not push through.

## Workflow

### 1. Restate the goal and "done"

Write one sentence of intent and a short list of observable acceptance criteria. If you cannot write criteria, you have an open question, not a plan.

### 2. Survey the current state

Read before planning: the entry points involved, existing tests, similar prior changes (`git log -- <path>`), and project conventions (contribution docs, CI config). Note what you confirmed versus assumed.

### 3. List open questions and assumptions

Split them:
- **Blocking** (answer changes the design): ask now.
- **Non-blocking** (cheap to change later): record as assumption and continue.

### 4. Decompose into steps

Rules of thumb for a good step:
- One reason to change; reviewable as its own commit.
- Leaves the project buildable and tests passing.
- Names the files it touches and the check that proves it.
- Small enough that failure is easy to localize.

Order by risk and dependency: do the riskiest unknown first (a spike or failing test), put pure refactors before behavior changes, and put cleanup last.

### 5. Define the verification and rollback of each step

For each step: command or observation, and how to undo it (`git revert` of that commit, feature flag off, etc.). For data or schema steps, require a tested rollback or a stated reason none exists.

### 6. Review the plan before executing

Check: Does every acceptance criterion map to a step? Is any step more than a few hours of work (split it)? Are independent steps identified (candidates for [parallel-agent-coordination](../parallel-agent-coordination/SKILL.md))? Does any step need user approval?

### 7. Execute and update

Mark steps done only with evidence (see verification-before-completion). Revise the plan visibly when discoveries change it.

## Worked example

Request: "Add a `--json` flag to the `report` CLI command."

Survey finds: `cli/report.py` formats text via `render_text()`; tests in `tests/test_report.py`; the arg parser lives in `cli/main.py`; a docs page lists flags.

```text
Goal: `report --json` prints the same data as valid JSON on stdout.
Done when: JSON output parses; text output unchanged; docs list the flag.
Out of scope: changing text format, other commands.
Assumption: output is a single JSON object (not JSON Lines). Non-blocking; confirm in PR.

1. Extract data assembly from render_text() into build_report() (pure refactor).
   Files: cli/report.py. Verify: existing tests unchanged and passing. Rollback: revert commit.
2. Add failing test: --json output parses and has keys X, Y.
   Files: tests/test_report.py. Verify: test fails for the right reason (flag unknown).
3. Add flag in cli/main.py; emit json.dumps(build_report()).
   Verify: new test passes; full suite passes.
4. Document the flag. Verify: docs build or link check passes.
```

Step 1 is separate so a behavior bug in step 3 cannot hide inside the refactor.

## Anti-patterns

- **Plan as essay.** Pages of prose with no verification per step.
- **Plan from imagination.** Naming functions or flags never confirmed in the code.
- **Big-bang step.** "Implement the feature" as one step.
- **Hidden scope growth.** Quietly adding unrelated cleanup.
- **Checklist without checks.** Steps like "make sure it works".
- **Frozen plan.** Continuing a plan that discovery has invalidated.
- **Over-planning trivia.** A ten-step plan for a rename.

## Verification checklist

- [ ] Goal and acceptance criteria are stated and observable.
- [ ] Files and APIs named in the plan were confirmed to exist.
- [ ] Open questions are separated into blocking and non-blocking.
- [ ] Each step has files, a verification, and a rollback.
- [ ] Out-of-scope items are listed.
- [ ] Steps needing approval (shared state, irreversible) are marked.
- [ ] Riskiest unknown is scheduled early.
- [ ] Plan contains no secrets.
