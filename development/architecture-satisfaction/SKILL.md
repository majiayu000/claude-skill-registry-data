---
name: architecture-satisfaction
description: Run a bounded architectural refactor loop toward a stated design.
disable-model-invocation: true
argument-hint: "The architectural target to refactor toward"
---

# Architecture Satisfaction

## Goal

Refactor toward a concrete architectural target while keeping the system working after each meaningful step.

## Loop Prompt

```text
Refactor until you are happy with the architecture. After each significant step, live-test the system, run an independent review, and commit. Track progress in /tmp/refactor-{projectname}.md.
```

Stop when the architecture is satisfactory and checks pass.

## When To Use

Use this for a deliberate architectural refactor where the desired destination can be stated in concrete terms and the current system can be tested after each meaningful change.

This is not a general cleanup pass. Use `housekeeper` for low-risk code hygiene, and `repository-cleanup` for Git branch/PR/worktree/stash cleanup.

## Define Satisfactory First

Before editing code, write down the target in concrete terms. Include the parts that make the architecture satisfactory, such as:

- Module boundaries and ownership.
- Dependency direction.
- Public interfaces that should stay stable.
- Behavior that must keep working.
- Performance constraints.
- Tests, smoke checks, or live flows that prove safety.
- Known risks and rollback points.

If the target is vague, pause and clarify it: ask the open points as choices (`AskUserQuestion` where available, for example which public interfaces must stay stable; otherwise in chat). A subjective stop condition can otherwise run indefinitely.

Get the target approved before the first edit. Where the harness has plan mode, enter it (`EnterPlanMode`), write the target and verification plan as the plan, present it with `ExitPlanMode` for approval, and copy the approved plan into the progress file; otherwise show the target and plan in chat and wait for an explicit yes.

## Progress File

Create or update a progress file in `/tmp` named for the project, for example:

```bash
/tmp/refactor-my-project.md
```

Track:

- Architectural target and constraints.
- Current risks.
- Checkpoint history.
- Decisions made.
- Commands run and their results.
- Independent review findings.
- Blockers.
- Next action.

The progress file is scratch state for long refactors and handoffs. Do not use it as a substitute for project documentation unless the user asks.

## Workflow

1. Inspect the current repository state: branch, uncommitted work, recent commits, test commands, app startup commands, and relevant architecture docs.
2. Define the architectural target, constraints, current risks, and verification plan in the progress file, and get them approved (Define Satisfactory First) before any code edit.
3. Make one significant, reviewable change at a time.
4. Live-test the affected behavior after each significant change. Prefer the project's real app/runtime checks when available, not only static checks.
5. Run the relevant automated checks: tests, type checks, linters, formatters, build, migrations, or focused smoke scripts.
6. Run an independent review after each significant change. Run the `code-review` skill against the checkpoint's starting commit (its Correctness axis runs as the `leek-skills:pr-reviewer` subagent where the harness has subagents, and inline otherwise), and brief it with the Independent Review Focus below. Where that skill is not installed, use an existing autoreview command or a separate review pass that looks for behavior regressions, missed callers, leaky abstractions, and test gaps.
7. Fix issues found by live testing, checks, or review before moving to the next architectural step.
8. Commit each verified checkpoint when the user has asked for commits or the repository workflow expects checkpoint commits. Keep commits small and named after the architectural move.
9. Update the progress file with the checkpoint, evidence, decisions, and next action.
10. Repeat until the stated architecture target is met, checks pass, and review finds no blocking issue.

## Checkpoint Discipline

Each checkpoint should have:

- One coherent architectural change.
- Passing or explicitly explained verification.
- A reviewed diff.
- A short commit message if committing.
- A progress-file entry explaining what changed and why.

Do not let several unrelated refactors accumulate before verification. Small verified checkpoints reduce risk and preserve rollback points.

## Independent Review Focus

Ask the review pass to look for:

- Broken dependency direction or circular dependencies.
- Interfaces that became broader or leak implementation details.
- Call sites missed during the refactor.
- Behavior changes not covered by tests.
- Migration or data compatibility risks.
- Performance regressions.
- Over-abstracted code that is harder to understand than the original.
- Documentation or comments that now describe old architecture.

## Report

End with:

- Architectural target.
- Checkpoints completed.
- Live tests and automated checks run.
- Independent review findings and fixes.
- Commits created, if any.
- Remaining risks or deferred work.
- Current progress-file path.

Start each item that needs the user (a risk, a deferral, an approval) with ⚠️, and each failed check with ❌. No other marks.

## Guardrails

- Do not begin a broad refactor without a concrete target and verification plan.
- Do not combine unrelated architecture moves in one checkpoint.
- Do not commit failing checkpoints unless the user explicitly wants a work-in-progress checkpoint.
- Do not rewrite public interfaces, data shapes, or migration behavior without checking callers and compatibility.
- Do not discard user changes or unrelated work.
