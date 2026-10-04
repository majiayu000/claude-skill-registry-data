---
name: build-workflow
description: Runs a plan or the delivery stages as one multi-agent run ("run this plan with agents", "run the pipeline end to end", "build a workflow for this"), across pre-flight and orientation, test design, implement, verify live, review, and describe, or any multi-step job the user describes, cheaply and honestly. It first decides whether one agent is enough, then runs the stages as a workflow script, as subagents, or as agents the session spawns directly, depending on what the platform supports, with capped fix loops, a separate skeptical verifier, and an honest blocked exit. Use when asked to build, design, or run a workflow, orchestrate subagents, run the delivery pipeline end to end, implement a plan with agents, or make a multi-agent run cheaper or more reliable.
argument-hint: "[goal | plan file] [stages to run] [go]"
disable-model-invocation: true
---

# Build workflow

Plan and run a multi-agent job so every agent does work one agent couldn't do as well, every result is something the run branches on, and "stuck" is reported as stuck. Multi-agent runs cost many times the tokens of one agent and hurt tightly coupled, sequential work, so the first decision is whether to run one at all.

This skill launches many agents, so it runs only when the user invokes it; that invocation, plus a go on the run plan, is the opt-in for the run and its cost.

## Inputs

- **The goal**: a plan file, a spec, or the job as the user describes it. Which stages to run, if the user names them. `go` skips the plan approval, for headless runs that can't answer a stop.
- **Project settings**: on every invocation, read `.claude/shipyard/build-workflow.md` in the project root if it exists; its settings win over the defaults here. It can set stage commands, default stages, caps, a status file path, invariants, and isolation rules. Its shape is in [references/overlay-example.md](references/overlay-example.md).

## Stages

| Stage | Who runs it | Shape |
|---|---|---|
| Pre-flight | one read-only agent checks the tree, plan, commands, and tools, and writes the shared orientation (subsystem map, HEAD, test baseline) | single |
| Test design | `test-designer`, one per slice | parallel, read-only |
| Implement | general-purpose subagent, one call per plan entry | serial; parallel only in separate worktrees |
| Verify live | `live-verifier`, after every commit lands | single, serialized |
| Review | pr-review's pipeline: `concern-reviewer` per slice of the diff maps and reviews concerns, `review-verifier` validates every finding; the report is compiled mechanically | slices in parallel, then validate, all as siblings |
| Describe | the pr-description skill in the session | single |

The orientation is written by an agent, not the walkthrough skill, because its readers are other agents, not a person. Where a named agent isn't available, give a general-purpose subagent the agent file's body as its prompt. Skip a stage another already covers: a test-first implementer makes a separate test-design pass redundant for that entry. Agent counts and caps are in [references/loops.md](references/loops.md).

## Rules

- **Every stage is a direct child of the orchestrator**, never a grandchild. A stage handles in-run recoveries (fix, retry, rescope) itself by the four-action rule, without starting a subagent; only a blocker it can't recover from returns `blocked`, and the orchestrator's decision agent decides it. Review's agents run as siblings under the orchestrator.
- **Every result is branched on.** The orchestrator maps each stage's raw return to `{status: pass | pass-with-gap | blocked | halt, gaps, reason}` by the table in [references/briefs.md](references/briefs.md), and has an `if` for every value. A field nothing reads is a label, not a gate; delete it.
- **Blocked is a correct result.** A pass the stage didn't observe is the only wrong answer.
- **Check the goal, not the tests.** The verifier checks the result against the plan entry or spec, not only that tests pass.
- **Every agent runs on the model of the session that invoked the skill.** The run plan doesn't pick models per stage. A fix is checked by a separate agent that didn't write it and doesn't see its reasoning (loops.md).

Tests read-only to fixers, the skeptic verifier, loop caps, and exclusive resources are in loops.md; cheap fact checks and never cleaning up are in briefs.md.

## Steps

```
- [ ] 1 Read settings and the goal
- [ ] 2 Decide: one agent or a run
- [ ] 3 Pick the runtime mode
- [ ] 4 Plan the run
- [ ] 5 Pre-flight
- [ ] 6 Run the stages
- [ ] 7 Report
```

1. **Read settings and the goal.** Settings first, then the plan or spec. Compute the shared context once (the diff, the plan entries verbatim, the changed files) so no agent re-derives it.
2. **Decide whether to run at all.** Use one agent when the work is one tightly coupled change, a sequence where each step needs the last one's full context, or small enough that one agent does it well; say so and end with a `next:` line whose first words name the stage for that work: `implement` in this session, or a stage skill (design-tests, live-verify, pr-review). Use a run when the work splits into independent pieces, needs an independent check, or is too big for one context; size it by loops.md.
3. **Pick the runtime mode**, per [references/runtime.md](references/runtime.md).
4. **Plan the run.** For each stage: its agent, inputs, return mapping, isolation, and the exclusive resources it holds. Show the plan in this shape, then **STOP — WAIT** for a go, unless the user passed `go`; the cost is the reason.

   ```
   Run plan (mode <n>: <why>)
   - <Stage>: <agent name> x<count>, <parallel | serial | worktree>
   - <Stage>: held (<why: settings, user, or no input>)
   Agents: <total> of a cap of <cap>   (review's own agents counted separately)
   Loop caps: <n> fix rounds per entry, <n> review fix rounds
   Reply `go` to start, or name stages to drop.
   ```

   Name each agent (`test-designer`, `review-verifier`, a general-purpose implementer); a held stage gets its stage name only. If the plan won't fit the cap, say how it splits into runs. If step 2 already chose one agent, don't show a run plan.
5. **Pre-flight**, before any expensive agent: the tree and HEAD are what the plan assumes, the plan isn't landed or closed, stage commands and tools exist, and the orientation is written. A failure ends the run as `blocked` with its reason.
6. **Run the stages** with [references/briefs.md](references/briefs.md) and loops.md. Verify live runs once, after every commit lands. In modes 2 and 3, append one line to `STATUS.md` at each stage transition (briefs.md); in mode 1, only when the settings name a status path.
7. **Report**: one line per stage with its status, commits landed, open gaps, blocked lanes, stages held or not run, and the agent count. Pushing, merging, and opening a pull request are **HUMAN TRIGGER**: the run drafts the description and stops.

Steps are agent-owned unless marked.

## Handoff

`next:` a clean run goes to the describe stage (pr-description) if it didn't run; a blocked or halted run goes back to the user with the blocker and the run's trail.
