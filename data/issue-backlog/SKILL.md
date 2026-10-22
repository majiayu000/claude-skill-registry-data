---
name: issue-backlog
description: >-
  Works a tracker's open issues from new to fixed, one stage at a time: triage, maintainer
  decisions, investigation, then fixes. Shows how many issues sit in each state and runs the
  next stage. Use for "work through the backlog" or "what's next on the tracker". For one
  known issue, use `issue-triage`, `investigate-bug` or `issue-resolve`.
user-invocable: true
argument-hint: [stage to start at: triage | decisions | investigate | fix, optional]
---

# issue-backlog

The front door for getting a tracker from "a pile of issues" to "fixed." It doesn't triage,
decide, investigate, or fix anything itself. It shows where every open issue stands, picks
the next stage, and hands that stage to the skill that owns it.

## Scope

- IN: count issues by state, suggest the next stage, run it through its owning skill, run
  investigations in parallel and gather their results, apply the tracker updates the user
  approves, start fixes one at a time.
- OUT: triage judgments (`issue-triage`), proving a cause (`investigate-bug`), the fix itself
  and its tracker updates (`issue-resolve`), and any tracker write the user hasn't
  approved.

## Preflight

1. Read `CLAUDE.md`'s `## Issue tracker` section. If it's missing, run `issue-triage` first;
   it owns that setup.
2. Use `issue-triage`'s State labels for the label names and what each one means.

## The board

Count open issues in each of these, and show the counts:

| Row | What it holds |
|---|---|
| To triage | No state label, plus anything `issue-triage`'s no-argument run would pick up again (a reporter reply, a needs-info timeout, a closed blocker) |
| Needs decision | `state/needs-decision` |
| Needs investigation | `state/needs-investigation` |
| Waiting | `state/needs-info` and `state/blocked` not yet due for another look |
| Ready | `state/ready` |
| In progress | `state/in-progress` |

## Pick the next stage

The first row with anything in it, in this order, unless the argument names a stage:

1. **To triage** → invoke `issue-triage` (Skill tool) with no argument. Triage goes first
   because it's quick and it feeds every other row.
2. **Needs decision** → invoke `issue-triage` with `decisions`. It's quick, and it needs the
   user, who is here now.
3. **Needs investigation** → the investigation stage below. It's slower, so it comes after
   the quick stages.
4. **Ready** → the fix stage below. Fixing comes last because every stage above feeds it.
5. **Nothing left** → everything is in progress or waiting on someone else. Say so.

Say which stage is next and why in one line, and run it on the user's yes. When it finishes,
show the board again and pick again, until the user stops or nothing is left to act on.

## The investigation stage

1. **Order the queue.** Sort `state/needs-investigation` issues by how bad the bug is (data
   loss or a security-adjacent fault, then a crash or a broken screen, then something
   cosmetic), then by demand (duplicates and reactions), then oldest first. Show the order;
   the user can reorder it or pick a few.
2. **Check parallel is safe.** Investigations run in parallel only when the demo site, if
   there is one, can run in several worktrees at once:
   - Its `.csproj` references `Umbraco.Community.WorktreeDevPort`, so each worktree gets its
     own port. If it doesn't, suggest `project-init`'s "Demo site ports" step.
   - Its database lives inside the worktree (such as SQLite under the site folder), not on a
     shared server. A shared database would mix one investigation's data into another's.

   If either fails, run them one at a time instead: invoke `investigate-bug` in this session
   for each issue, in order.
3. **Dispatch.** Up to three at a time, unless the user asks for a different number. Each
   one is an Agent tool call with `isolation: "worktree"`, told to invoke `investigate-bug`
   (Skill tool) with the issue ID and `--unattended`. Send a batch as parallel calls in one message.
4. **Gather.** Pull any security flag into its own list, handled as `issue-triage`'s
   Security reports section says. Show one table for the rest: issue, outcome
   (`state/ready`, `state/needs-info`, `state/blocked`, or a close), the cause in one line,
   and the drafted comment.
5. **Apply** exactly the updates the user approves, as `issue-triage`'s Aggregating and
   reporting section does.

## The fix stage

1. Sort the `state/ready` issues the same way as the investigation queue, and show the order.
   The user can pick a different one.
2. Invoke `issue-resolve` (Skill tool) for the first one. One at a time: a fix leaves real changes for the user to review, so it
   never runs in parallel.
3. When `issue-resolve` hands back, show the board again and offer the next ready issue.

## Rules

- Never write to the tracker without the user's yes, as `issue-triage`'s Rules say.
- Never fix anything itself. Ready issues go to `issue-resolve`, one at a time.
- Never run the next stage without saying what it is and getting a yes. A stage can mean
  dozens of subagents.

## Hand off

The board, and what's still open: issues in progress, and issues waiting on a reporter or
an upstream fix.
