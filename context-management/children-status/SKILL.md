---
name: children-status
description: >-
  Use when a manager session is asked for the state of its child sessions —
  builds one board from the children's task files, branches and the host's
  session list, with the operator's next steps. Not for one session's own report
  (session-status).
---

# Children Status

## Overview

Answers "what state are my children in?" in one pass over files: the manager's
task file lists the children, each child's task file says what is done, what
is left and what it needs, and git says where its branch stands. The answer is
a board grouped by state, closed by a short block of what the operator must do
next. Nothing is edited.

## Context

<context>
A swarm is one manager session and the child sessions it started. Its ledger
is the manager's task file: `## Swarm` holds one bullet per child with the
child's task file, branch and worktree. Each child keeps a `## Status` section
in its own task file — `State:` (`working`, `blocked on operator`, `done`,
`failed`), `Needs from the operator:`, `Not verified:`, `Branch:`,
`Told directly by the operator:`, `Updated:` — and ticks its Definition-of-Done
items as it delivers them.

The host's own word for a session ("idle", "running") cannot answer the
question: idle covers finished, waiting for an answer and abandoned. And the
manager's memory of the conversation is not a source: it is cut by context
compaction, and the operator talks to children directly, behind the manager's
back.
</context>

## Rules & Constraints

<rules>
1. **Files, not memory.** Start from the manager's task file on disk. Do not
   answer from what you remember of the conversation, even when it seems
   fresh.
2. **Read-only.** Edit no file, tick nothing, commit nothing, merge nothing,
   message no child. This skill reports.
3. **A child with its own worktree is read from its branch.** The copy of its
   task file in the manager's checkout is the state at start. Read
   `git show <branch>:<task file path>`, or the file inside its worktree when
   that is newer and uncommitted.
4. **A child's report is a claim.** What you checked yourself (git state) is
   stated as fact. What you took from the child's file without checking is
   marked `by the child's report`.
5. **Git beats the `Branch:` line.** When the child's file says "pushed" or
   "merged" and git says otherwise, the board shows what git says and names
   the contradiction.
6. **The host's state wins where it says more.** A session the host reports as
   waiting for the user is `blocked on operator`, and one it reports as failed
   is `failed`, whatever the child wrote.
7. **Never a silent skip.** A missing or unreadable child task file is a row
   `state unknown` with the reason.
8. **Never answer a child's question for the operator.** An open question goes
   to the operator in the closing block.
</rules>

## Instructions

<step_by_step>

1. **Read the manager's task file**
   - The task file this manager session works on (the one the user names, else the one the session has been working on). Read it from disk now.
   - No `## Swarm` section → say in one line that this task has no children recorded, and stop.
   - Find the main branch: `git symbolic-ref --short refs/remotes/origin/HEAD` when there is a remote, else the branch the manager's checkout is on.

2. **Read every child** (independent reads go together where the tool allows)
   - For each bullet of `## Swarm` not marked `closed`:
     - **Task file**: shared checkout → read the file in the working tree. Own branch → `git show <branch>:<path>`; if its worktree exists, also `git -C <worktree> status --porcelain`, and read the file there when it is modified.
     - **Done and left**: count ticked and total Definition-of-Done items; note the unticked ones.
     - **Status section**: state, needs from the operator, not verified, told directly by the operator, updated. No `## Status` section → state `unknown — the child has not reported yet`.
     - **Follow-ups**: the bullets under `## Follow-ups`.
     - **Branch, checked by git, for a child with its own branch**: commits the main branch lacks (`git rev-list --count <main>..<branch>`); merged or not (`git branch --merged <main>`); pushed or not (`git rev-parse --verify --quiet refs/remotes/origin/<branch>`, or "no remote" when `git remote` prints nothing); uncommitted files in its worktree.
   - Closed children are counted, not re-read.

3. **Take the host's state, where the host has one**
   - Look at the tools of this session for one that lists sessions or returns a session's state (e.g. a session-list tool in the Claude desktop app). Decide from the tool list alone.
   - A tool that lists the subagents or teammates of THIS session is not one: a child session is a separate session, not a subagent. If a list you get does not contain the session references written in `## Swarm`, that tool cannot see the children — treat it as no tool. Never read "not in the list" as "not running".
   - Such a tool exists → one call for the list, not one call per child. Apply rule 6. A child whose written state is `working` while its session is not running, with no turn in progress, is `stalled`.
   - No such tool → say in one line that sessions cannot be listed from here, so the states come from the task files and git, and a stalled child cannot be told from a working one.

4. **Print the board**
   - One line first: how many children, and how many in each state.
   - Then the children grouped by state, in this order: `blocked on operator`, `failed`, `stalled`, `unknown`, `working`, `done`, and last the closed ones as a count.
   - Per child: title and session reference; state; done / total items and the items left; what it needs from the operator; not verified; told directly by the operator (when not "nothing"); branch state from git; follow-ups; when it was updated.
   - Mark with `by the child's report` everything not checked by you: the state, the ticked items, the unverified list.
   - Where git contradicts the child's `Branch:` line, say both.

5. **Close with the operator's next steps**
   - A block titled `You next`, at most three items, most urgent first. Each item is a concrete action and the session it belongs to: answer this question (with the options) in that child; decide about that failed child; merge that finished branch.
   - Nothing needs the operator → `You next: nothing — the children are working.`
   - This block is the last thing in the message. Then stop: closing children is the closing skill of this pack (`close-swarm`), and it runs only when the operator asks.

</step_by_step>

## Verification

<verification>
- [ ] Every bullet of `## Swarm` appears on the board, or in the closed count; none was skipped silently.
- [ ] A child with its own branch was read from that branch or its worktree, not from the manager's checkout.
- [ ] Branch state on the board comes from git commands run now.
- [ ] Unchecked claims carry `by the child's report`.
- [ ] The message ends with the `You next` block of at most three items.
- [ ] Nothing was edited, committed, merged or sent.
</verification>
