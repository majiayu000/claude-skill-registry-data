---
name: plan-then-implement
description: >-
  EXPERIMENTAL. Run a coding task as one plan and one handoff: this session writes a complete
  plan, one implementer subagent on a cheaper model carries it out, and the run is logged.
argument-hint: "[haiku|sonnet|opus|fable] [task]"
disable-model-invocation: true
user-invocable: true
license: Apache-2.0
---

# Plan then implement

This session plans, one implementer carries out the plan, and the run is logged. The run is done
when the run folder is closed with an outcome and the user's verdict, whether the task succeeded
or not.

This session's ID is `${CLAUDE_SESSION_ID}` and the plugin root is `${CLAUDE_PLUGIN_ROOT}`. Read
`${CLAUDE_PLUGIN_ROOT}/references/run-log.md` now: it says how to open, keep, and close the run
folder, and where these two values go.

## Arguments

`$ARGUMENTS`: if the first word is `haiku`, `sonnet`, `opus`, or `fable`, it is the worker model
and the rest is the task. Otherwise the worker model is `sonnet` and all of it is the task. With
no task, the task is the user's most recent request.

## Procedure

1. **Open the run** per the run log, Strategy `plan-then-implement`.
2. **Plan.** Read the code yourself until you could make the change without guessing, then write
   the plan under "Plan or briefs" in `run.md`: numbered steps naming the files and functions to
   change, the exact behavior of each change, the edge cases, and the command that proves it
   works. The implementer sees only what you send it, so the plan must stand alone: no "as
   discussed", no pointers into this conversation.
3. **Hand off.** Dispatch one `ceh-orchestration-lab:implementer` with the Agent tool, `model`
   set to the worker model. Its prompt is the task verbatim, then the plan, then this line:
   "Follow the plan, but trust the code and the task over the plan where they disagree, and
   report every disagreement."
4. **Check.** When it reports, run the plan's proving command yourself and
   read `git diff --stat`. Passing means the command passes and the diff touches what the plan
   named.
5. **Fix up once, at most.** If the check fails, resume the same implementer with `SendMessage`,
   giving it the failing output and what the plan required. Its context is still warm, so this
   costs less than a fresh dispatch. Check again. A second failure ends the run as `failed` or
   `partial`.
6. **Close the run** per the run log.

## Rules

- Never edit a project file yourself, even to fix a one-character slip. The run measures whether
  the plan carries the cheaper model, and a rescue by this session hides the answer. If the user
  asks you to fix it, do so and record it as a user intervention.
- One plan, one implementer, one fix-up. A second implementer or a revised plan turns this run
  into the `orchestrate` strategy, so end the run instead and say so in Notes.
- Keep the plan at the level of detail the worker model needs: exact names and values for Haiku,
  intent and constraints for Sonnet or Opus. Your plan text is the most expensive output of the
  run.

## Stop conditions

- The task needs a decision only the user can make (a product choice, an irreversible action) →
  ask before planning, and log the question as a user intervention.
- The implementer reports `blocked` → log it, ask the user whether to end the run or answer the
  blocker in a resume, and record their choice.
