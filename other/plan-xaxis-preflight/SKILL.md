---
name: plan
description: Turn a goal into an approved, phased implementation plan where every phase ends at a real test checkpoint. Use before implementing anything non-trivial, or when a task has several viable approaches.
argument-hint: [what you want built]
---

Produce a phased plan for: $ARGUMENTS

No edits until the human approves. Planning is the cheapest place to be wrong — a bad assumption costs one paragraph here and three phases of rework later.

## Steps

1. **Enter plan mode** (EnterPlanMode) if you aren't already in it. It makes "no edits yet" a guarantee rather than an intention.

2. **Know the ground first.** If the target area is unfamiliar, run `/preflight:research` before planning. Planning against a guessed codebase produces a plan that dies on contact. Skip only if you already have the map.

3. **Delegate the plan** to the `planner` subagent, passing the goal, the research map, and any constraints the human gave. Its plan is a proposal to you, not a verdict — check it against what you know before endorsing it.

4. **Resolve the real forks.** If a decision genuinely changes what gets built and you can't settle it from the code, ask (AskUserQuestion). Don't ask what a sensible default already answers, and don't ask for approval — that's what step 5 is for.

5. **Present for approval** (ExitPlanMode). One recommended approach with phases, not a survey.

## What a phase must have

- **Goal** — one sentence.
- **Changes** — specific files and what happens in each.
- **Checkpoint** — the exact command and the observable result that proves it worked.

A checkpoint is a command with an expected result: `npm test -- auth.spec.ts passes`. "Tests pass" isn't one. "It compiles" isn't one — compiling is not evidence of behavior. If a phase has no honest checkpoint, it's drawn wrong: reslice it into something that runs end-to-end.

Prefer thin vertical slices that work over horizontal layers that can't be verified until three phases later.

## Execute

After approval, work the phases in order and stop at each checkpoint. Delegate checkpoint runs to `test-runner` so test output stays out of this conversation.

If a phase reveals the plan was wrong, stop and say so. Re-plan the remainder rather than improvising past a broken assumption — the plan was approved on premises that no longer hold, so silently continuing means shipping something the human never agreed to.
