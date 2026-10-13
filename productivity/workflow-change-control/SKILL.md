---
name: workflow-change-control
description: Protect a running multi-agent workflow when requirements change mid-run. Use before stopping, editing, resuming or relaunching a running Workflow; use orchestrate-pass to design a new pass.
---

# Changing requirements while a workflow runs

A running workflow holds agent context that no file preserves. Stopping it
destroys the context of every agent in flight; only their commits and file edits
survive. Resuming replays from cache only the longest unchanged prefix of
`agent()` calls, in the order the script issued them. In a parallel multi-lane
script every lane issues its first call at start, so changing one early prompt
re-runs every later call, finished ones included, even when their own prompt is
byte-identical.

This happened on 2026-09-23. Three stop-edit-resume cycles, each done to inject
one new user request, killed agents that had been working for 20 to 77 minutes.
The operator believed they had run "a few minutes", having counted conversation
turns instead of reading timestamps. Each resume also re-ran implementation
steps that had already finished.

## Default: never stop a run to inject a change

When the user adds or amends a requirement while a workflow runs:

1. Acknowledge it and record it in the plan or task list.
2. Route it without touching the run:
   - An independent task becomes a separate workflow on its own branch and
     worktree. Launch it now if it cannot conflict with the running lanes,
     otherwise after the run.
   - A correction to a task that has not started yet, or that is in progress,
     becomes a follow-up task that runs after the lane finishes. It amends the
     result, and the integrator reconciles it.
3. Tell the user where the change will land and when.

## The only reasons to stop

Stop only when the run is doing damage: destroying data, pushing, spending on
work the user cancelled, or building something the user reversed that is
expensive to undo. Even then:

1. Measure, never estimate. For every agent in flight, read the first and last
   timestamps of its transcript (`agent-<id>.jsonl` in the workflow transcript
   directory) and compare them with the current UTC time. Conversation turns are
   not a clock: the user may have been away for an hour between two messages.
2. List the finished calls that the stop will make run again.
3. Give the user the concrete cost (agents × minutes of context lost, steps that
   will re-run) and wait for an explicit go.

## Resuming after an interruption

- Resume with the script unchanged. Any edit to a prompt issued early,
  including a shared note or a hint appended for recovery, invalidates the
  cache from that call onward.
- Design for this up front: every implementation prompt must say from the
  first run that the agent starts by inspecting its worktree (`git log`,
  `git status`) and continues existing work. A plain resume is then safe
  without edits.
- Right after a resume, read `journal.jsonl`. A cached call replays without a
  new `started` line. If a finished step shows a new `started` line, it is
  running live: tell the user at once.

## Design runs that absorb change

- Prefer several shorter workflows chained through branches over one long
  monolithic run, so a new requirement becomes a new run instead of a restart.
- Keep shared decision text stable. Record later decisions in later runs.
- Guard each lane: retry a failed agent once, then stop the lane, so a quota
  or API outage cannot cascade through every remaining task.
- Keep temporary worktrees off a nearly full disk, and remove their junctions
  before removing the worktree.
