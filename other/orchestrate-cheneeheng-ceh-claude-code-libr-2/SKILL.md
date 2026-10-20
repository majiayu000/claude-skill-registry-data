---
name: orchestrate
description: >-
  EXPERIMENTAL. Run a coding task as a supervised loop: this session briefs and reviews,
  implementer subagents on a cheaper model do the edits and test runs, and the run is logged.
argument-hint: "[haiku|sonnet|opus|fable] [task]"
disable-model-invocation: true
user-invocable: true
license: Apache-2.0
---

# Orchestrate

This session splits, briefs, and reviews. Implementer subagents do the work worth delegating, and
the run is logged. The run is done when the run folder is closed with an outcome and the user's
verdict, whether the task succeeded or not.

This session's ID is `${CLAUDE_SESSION_ID}` and the plugin root is `${CLAUDE_PLUGIN_ROOT}`. Read
`${CLAUDE_PLUGIN_ROOT}/references/run-log.md` now: it says how to open, keep, and close the run
folder, and where these two values go.

## Arguments

`$ARGUMENTS`: if the first word is `haiku`, `sonnet`, `opus`, or `fable`, it is the worker model
and the rest is the task. Otherwise the worker model is `haiku` and all of it is the task. With no
task, the task is the user's most recent request.

## Procedure

Every step this session takes re-reads its whole context, so the cost of a run grows with this
session's step count times its context size. Each step below keeps one of the two down.

1. **Open the run** per the run log, Strategy `orchestrate`.
2. **Scout.** Unless the files the task touches total under about 400 lines, dispatch one `Explore`
   subagent, `model` set to the worker model, with the questions the split and the briefs need:
   where each change goes, the formats to match, current values to change. Ask for at most 30
   line-anchored lines and no file contents. Read its answer instead of the files.
3. **Split the work** into as few pieces as hold together, usually two or three, each with its own
   check. Every piece costs a brief, a wait, and a review, whatever its size. Delegate a piece
   only when its brief is well under a quarter of the change it asks for. Make a smaller piece
   yourself. Write the list under "Plan or briefs" in `run.md`, marking each piece `worker` or
   `self`. It can change as reports come in: append changes with the reason, never rewrite.
4. **Brief and dispatch.** A brief carries what only you know: the goal, the files in scope, the
   decisions and constraints you settled, what done looks like, and the command that proves it.
   Point at everything the worker can read itself (the task in `run.md`, a template, the
   neighbouring code) instead of copying it in. Never write the finished text or code into a
   brief: then the worker only types, and you paid for the work twice. Never ask for pasted
   output or diffs, since the report shape is the implementer's own. Dispatch a
   `ceh-orchestration-lab:implementer` with the Agent tool, `model` set to the worker model.
   - Pieces of similar size that touch disjoint files go out as parallel Agent calls in one
     message, with `run_in_background: false`, so their reports arrive in one step.
   - A piece clearly longer than the others goes out alone with `run_in_background: true`, so
     its wait overlaps the short pieces and their reviews.
5. **Review each report** against the brief, cheapest check first:
   - The check the brief named passed, and `git diff --stat` touches only the files in scope.
   - Read the diff (`git diff -- <files>`) only for a file the stat or a reported deviation flags,
     or where the brief left a judgment call to the worker.
   - Incomplete or wrong on the same piece: resume that worker with `SendMessage`, saying exactly
     what is missing. Its context is warm, so a resume costs less than a fresh brief.
   - The report shows the split was wrong: update the list, then brief the new piece fresh.
6. **Final check.** When every piece is done, dispatch one implementer to run the full relevant
   test command and report. Do not run it yourself: its output would land in this context.
7. **Close the run** per the run log.

## Rules

- Make a project edit yourself only for a piece marked `self` in the split. Never take over a
  delegated piece: a rescue hides whether the worker model carried it.
- If the user asks you to make an edit yourself, do it and record it as a user intervention.
- A brief for Haiku names exact files and the constraints that settle its choices. It does not
  spell out the content, for any worker model.
- A piece that has failed review twice goes back to the split: cut it smaller or brief it fresh,
  and note in Notes why. Do not take it over yourself.

## Stop conditions

- The task needs a decision only the user can make (a product choice, an irreversible action) →
  ask, and log the question as a user intervention.
- A worker reports `blocked` on something the code cannot answer → ask the user, log it, and
  continue with their answer in a resume.
