---
name: start-child
description: >-
  Use when a manager session is asked to start a child session for part of its
  task — writes the child's task file, a row in the manager's task file and a
  self-contained brief, then starts it. Not for the state of running children
  (children-status).
---

# Start a Child Session

## Overview

A manager session hands one part of its task to a child session. Before the
child exists, its assignment is on disk: a task file of its own and a row in
the manager's task file. Then the child gets a self-contained brief and is
started with the host's session tool — or, where the host has none, the brief
is printed for the operator to start it by hand.

## Context

<context>
A swarm is one manager session and the child sessions it starts. Its ledger is
the manager's own task file (the `tasks` role from the project instructions):

- `## Swarm` — one plain bullet per child with links: title, session
  reference, the child's task file, branch and worktree, the manager's
  Definition-of-Done item it serves. The child's state is NOT copied here; it
  is read from the child's file every time.
- `## Decisions` — dated facts and decisions sent to children, with recipients.
- `## Follow-ups` — where the children's follow-ups end up when they are closed.

The manager forgets: a long session compacts its context, and what survives is
what is in the file. A child starts with a fresh context and knows only its
brief and its task file. Children that share one checkout overwrite each
other's work unless each knows exactly which files are its own.
</context>

## Rules & Constraints

<rules>
1. **Files first, session second.** The child's task file and the manager's
   row are written and committed before the session is started. A worktree is
   cut from a commit: an uncommitted task file does not exist in it.
2. **Commit by explicit paths.** The commit holds the child's task file and
   the manager's task file and nothing else. Never `git add -A` or `git add .`:
   the checkout may carry other sessions' work. Never stash.
3. **The manager does not do the child's work.** The manager's own turns are
   for planning, the ledger and decisions. Work, reviews and checks go to
   children. Do not start on the child's task "to save time".
4. **One child, one owner of each file.** A child either gets its own worktree
   and branch, or — in a shared checkout — an exact list of the files it owns.
   If two children would own the same file, say so and ask before starting.
5. **Start only on the operator's word.** A child is started on a turn the
   operator began, for a part the operator asked to delegate. Do not start
   children on your own initiative, and do not let a child start children.
6. **Never answer for the operator.** A child's question that needs the
   operator goes to the operator, not into an answer invented by the manager.
7. **A host tool that refuses is reported verbatim.** Leave the files as they
   are and say what the host answered.
</rules>

## Instructions

<step_by_step>

1. **Read or create the manager's task file**
   - Read the task file this manager session works on, from disk. It may come from a planning or an epic workflow.
   - The manager has none → write one in the project's accepted task format: the swarm's goal and one Definition-of-Done item per outcome. Use the task-format skill of the project if there is one.

2. **Write the child's task file**
   - A new file under the `tasks` role, in the accepted task format: the child's goal; the acceptance criteria as Definition-of-Done items, each with an evidence command where one exists; the constraints (owned files or own worktree); an empty `## Follow-ups` section.
   - Frontmatter `related_tasks:` points at the manager's task file.
   - Do not reuse the manager's file or another child's file.

3. **Update the manager's task file**
   - First child only — create `## Swarm` and open it with this rule line:
     `Rule: every decision or fact sent to children is appended to ## Decisions with its date and recipients; a changed assignment is also written into that child's task file.`
     Create empty `## Decisions` and `## Follow-ups` sections if they are missing.
   - First child only — add an unticked Definition-of-Done item: `Swarm closed: every child row is marked closed and nothing is lost` with the evidence "no open row under `## Swarm`; the closing skill's nothing-lost list is empty". With it the manager session cannot be finished while a child is still open.
   - Add one plain bullet (not a checkbox) for the child: title — session reference (`not started yet` for now); the child's task file path; `shared checkout` with the branch, or its own branch and worktree path; the manager's Definition-of-Done item it serves.

4. **Commit both files, by explicit paths**
   - Run `git status --porcelain` and look at it: everything other than your two files belongs to someone else.
   - `git add <child task file> <manager task file>`, then in a separate step check `git diff --cached --name-only`, then `git commit <child task file> <manager task file> -m "docs(tasks): add child <title> to the swarm"`.

5. **Build the brief**
   - The child knows nothing of this conversation. The brief is self-contained and carries every item of this checklist:
     - the goal in one or two sentences, and the path of the child's task file — "read it first; it is your contract";
     - where it works: its own worktree and branch, or the shared checkout with the exact list of files it owns — and that it edits no other file and commits only by explicit paths;
     - what it may not do: merge, push to the main branch, start sessions of its own, answer a question on the operator's behalf;
     - do not end a turn while background work it started is still running; do not end a turn only to report progress;
     - before the end of every turn run `session-status`, and begin the last message of the turn with its three opening lines;
     - in its own worktree: commit the task file by explicit path each time `session-status` updates it;
     - a decision or an instruction it gets directly from the operator is written into its task file under `Told directly by the operator`;
     - when every Definition-of-Done item is ticked: write the state `done` and end the work with `finish-session` — it checks the goals against the task file, commits, pushes the child's branch and archives the session.

6. **Start the session**
   - Look at the tools of this session for one that starts another session (e.g. a start-session tool in the Claude desktop app). Decide from the tool list alone.
   - A tool that runs a subagent inside THIS session is not one: a subagent has no session the operator can open, message or archive. Do not hand the child's work to a subagent instead.
   - Such a tool exists → start the child with the brief, a title that names the part of the task, a fresh context, and its own worktree when step 2 assigned one. Write the returned session reference into the child's bullet and commit the manager's file by explicit path.
   - No such tool → print the brief as one ready block, and say in one line that this host cannot start a session from here and the operator starts the child by hand with that brief. The files are already written and committed; that part is done.

7. **Report and stop**
   - Say: the child's task file, the row added, the commit, and whether the session was started or is left to the operator.
   - Do not begin the child's work. For the state of the children later, the status skill of this pack (`children-status`) builds the board from these files.

</step_by_step>

## Verification

<verification>
- [ ] The child has its own task file with a goal, Definition-of-Done items and `related_tasks` pointing at the manager's file.
- [ ] The manager's file has `## Swarm` with the rule line and a plain bullet for the child, and the `Swarm closed` Definition-of-Done item.
- [ ] One commit holds exactly the two task files; nothing foreign was staged or stashed.
- [ ] The brief carries every item of the checklist in step 5, `session-status` and `finish-session` included.
- [ ] The session was started with the host's tool and its reference recorded, or the brief was printed with the one-line notice.
- [ ] The manager did none of the child's work.
</verification>
