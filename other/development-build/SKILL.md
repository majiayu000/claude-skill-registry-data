---
name: development-build
description: Execute a written implementation plan task by task with test-driven development, committing after each task and logging progress. Use when a feature plan already exists and the user says to start building, implement it or work through the tasks. Not for writing the plan; see /development-plan.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: development
  phase: 2
  artifact: 02-build.md
  stack-aware: true
---

# Build

Execute the implementation plan for "$ARGUMENTS" task-by-task, following test-driven development discipline.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"development-build","workflow":"development","phase":2,"project":"<project>","event":"skipped","artifact":"02-build.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 2 (Build) of the Plan-Build-Test-Ship workflow (`development`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `development` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

**Stack.** Before you build, test, lint, run or generate code, read the `Stack` section of the project's `AGENTS.md`, or of `CLAUDE.md` when `AGENTS.md` has none. Use its commands exactly as written, its `layout` for where files go and its `rules` as requirements. If it names a `profile`, also read the file `<profile>.md` in the `stacks` folder of this skill's bundled references for the full commands, layout and rules; the project's own keys win where both speak. If there is no `Stack` section, run the `singular-detect` skill, state what you inferred in one line, and offer to write the section with `singular-init`. Never assume a package manager, test runner or formatter the project did not declare.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"development-build","workflow":"development","phase":2,"project":"<project>","event":"refused","artifact":"02-build.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"development-build","workflow":"development","phase":2,"project":"<project>","event":"started","artifact":"02-build.md","note":""}`.

Read `.singularskills/development/<project>/01-plan.md`. If this file does not exist, tell the user:

> No plan exists for "<project>". Run `/development-plan <project>` first, or use `--skip-checks` to bypass.

## Process

For each task in the plan:

1. **Write the failing test first:**
   - Write the test that verifies the task's expected behavior
   - Run the test suite — confirm the new test fails
   - If it passes without implementation, the test isn't testing anything — rewrite it

2. **Implement the minimal code to pass:**
   - Write only what's needed to make the failing test pass
   - Don't add features, refactor, or "improve" beyond the task scope
   - Follow existing codebase patterns and conventions

3. **Verify:**
   - Run the full test suite — all tests must pass
   - If other tests broke, fix them before moving on

4. **Commit:**
   - Stage the relevant files
   - Write a clear commit message following the project's convention

5. **Log progress** — after each task, append to the execution log:
   - Task name and status (completed/skipped/blocked)
   - Commit hash
   - Any issues encountered

6. **Write the artifact** to `.singularskills/development/<project>/02-build.md`

## References

- `references/stacks/bun-react-ts.md` and `references/stacks/rust-gpui.md`: the shipped stack profiles

## Output

The execution log written to `.singularskills/development/<project>/02-build.md`. Present a summary to the user highlighting:
- Tasks completed vs. total
- All commits made
- Any issues or deviations from the plan

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"development-build","workflow":"development","phase":2,"project":"<project>","event":"finished","artifact":"02-build.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: development-build
workflow: development
phase: 2
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
