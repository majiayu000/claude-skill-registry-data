---
name: development-plan
description: Break a feature into an implementation plan of small tasks with exact files, tests and commits. Use when the user is about to build a feature and wants the work broken down first. Not for stories, a backlog or project scope or schedule; see /project-management-user-stories, /project-management-backlog-creation, /project-management-project-charter or /project-management-roadmap.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: development
  phase: 1
  artifact: 01-plan.md
  stack-aware: true
---

# Plan

Create a detailed implementation plan for "$ARGUMENTS". Break the work into bite-sized tasks (2-5 minutes each) with exact file paths, test strategy, and commit points.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"development-plan","workflow":"development","phase":1,"project":"<project>","event":"skipped","artifact":"01-plan.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Plan) of the Plan-Build-Test-Ship workflow (`development`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `development` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise, unless the user named this skill, ask one question, since this is the first phase of its workflow: "Just this step, or the whole Plan-Build-Test-Ship workflow?" End your turn and wait; on the whole workflow, hand off the same way; on just this step, continue here.

**Recall.** Before you ask the user anything, look for what this repository already holds about `<project>`: if a tool is available whose description says it searches or maps this repository (a memory or repo-map server such as `repo_map` or `entities`), query it for `<project>` and this phase's subject and read what it returns, keeping only results from this repository; in every case also list `.singularskills/*/<project>/` and read the **Decisions** and **Open questions** of any artifact there, and the lines of `.singularskills/log.jsonl` whose `project` is `<project>`. After the frontmatter and title, add a `## Recalled` section of at most ten lines naming what you found and where (path or tool), or the single line `Nothing recalled: no earlier artifacts, log lines or memory results for <project>.` Ask the user only what this did not answer. The trail's shape is described in `references/memory/trail.md`, bundled with this skill.

**Stack.** Before you build, test, lint, run or generate code, read the `Stack` section of the project's `AGENTS.md`, or of `CLAUDE.md` when `AGENTS.md` has none. Use its commands exactly as written, its `layout` for where files go and its `rules` as requirements. If it names a `profile`, also read the file `<profile>.md` in the `stacks` folder of this skill's bundled references for the full commands, layout and rules; the project's own keys win where both speak. If there is no `Stack` section, run the `singular-detect` skill, state what you inferred in one line, and offer to write the section with `singular-init`. Never assume a package manager, test runner or formatter the project did not declare.

Before you start work, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"development-plan","workflow":"development","phase":1,"project":"<project>","event":"started","artifact":"01-plan.md","note":""}`.

None — this is the first phase of any development effort.

## Process

1. **Understand the feature:**
   - Clarify what "<project>" means — ask the user if ambiguous
   - Identify acceptance criteria and constraints
   - Determine scope boundaries

2. **Explore the codebase:**
   - Read relevant existing code, tests, and configuration
   - Identify files to create and files to modify
   - Understand existing patterns and conventions
   - Note dependencies and potential conflicts

3. **Break into tasks:**
   - Each task should take 2-5 minutes to complete
   - Each task produces a working, committable state
   - Order tasks so each builds on the previous
   - For each task specify: files to touch, steps, expected outcome

4. **Define test strategy:**
   - What tests need to be written?
   - What existing tests might break?
   - How to verify the feature works end-to-end?

5. **Write the plan** using the template from `references/plan-template.md`

6. **Write the artifact** to `.singularskills/development/<project>/01-plan.md`

## References

- `references/stacks/bun-react-ts.md` and `references/stacks/rust-gpui.md`: the shipped stack profiles

## Output

The implementation plan written to `.singularskills/development/<project>/01-plan.md`. Present a summary to the user highlighting:
- Number of tasks
- Key architectural decisions
- Test strategy
- Estimated complexity

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"development-plan","workflow":"development","phase":1,"project":"<project>","event":"finished","artifact":"01-plan.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `none`, as this phase has no gate):

```yaml
---
skill: development-plan
workflow: development
phase: 1
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
