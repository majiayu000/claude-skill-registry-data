---
name: swarm
description: "Use when a person asks to swarm, delegate or parallelize work without a plan ('swarm this', 'run a swarm on…', 'get a few agents on it'), or when a task in front of you splits into independent parts or is long enough to hand off: then propose a swarm in one line, workers and why, and open it only on a yes. Runs a task swarm on the board: this session orchestrates, N swarm-worker agents take the tasks posted to them, report, and take the next, for as long as the person keeps giving work, on call or under a protocol (build-verify: builders, then verifiers walking the running product, looped until it holds). Produces the run on the board and the workers' results and merges. Not for work an approved plan covers (execute-plan), a discussion of seats (brainswarm), or a task small enough to do yourself."
---

# Swarm

**You orchestrate; the workers do the work.** The `orchestrate` skill holds the protocols, the
run's proposal, dispatch, briefs and how findings are weighed; the `swarm-board` skill holds the board, its orchestrator side in its
`references/orchestrator.md`, read before opening. Here: what a task swarm adds. There is no
plan behind it: **a task is a post on the board** (the `orchestrate` skill's `references/tasks.md`), whatever the task is.

## Proposing one

Not asked, but the work splits into parts or must be seen working: offer it as the `next-step`
skill says, the protocol filled in. On a no, do it yourself.

## Setting it up

**Propose the run as the `orchestrate` skill's *Propose the run* says**, built on the closest example
(build-verify when the work must be seen working; none for workers on call), with: how many
workers (3 to start from, reconsidered against the estimate of the work as *Propose the run* says) and each one's area; under
build-verify, the verifiers (sized from the verify's steps), their focus, source and port range, whether only one instance can run; the loop; each seat's model and effort (Opus; builders `low`, verifiers `medium`);
**the branch** their work merges into, a new `swarm/<topic>` off the current branch by default.

## Open and dispatch

1. Create the branch, push it, and leave it checked out nowhere (detach the main checkout): a
   worker fast-forwards it from its own worktree.
2. A seats file, one row per worker, `w1` … `w<n>`, titled `worker`, and under build-verify one
   per verifier, `v1` … `v<m>`, titled `verifier · <focus>`, with `"busyMax": 300000` (a browser or
   other non-shell call hung 5 min is told to you) and its own port range in its brief; then `$S open --kind task
   --group <topic> --title "<what the swarm is for>" --seats <file>` with `--protocol <the
   charter's base>` when it runs one, or `--protocol none` for a swarm with no phases on purpose,
   and start your link as it prints; under a protocol, open its first phase before the first
   task post. Give the person the board's URL.
3. **Every worker at once** on the plugin's `swarm-worker` agent (`subagent_type:
   "swarmstorm:swarm-worker"`), each with `isolation: "worktree"`, as the `orchestrate` skill
   dispatches. The brief holds no task:

   ```markdown
   You are worker `<wN>` of task swarm run `<run id>` on `<repository>`. Your worktree is based on `<branch>`; merge into `<branch>`. **Prepare**: `<the command, install included>`. Join now, then wait for the tasks posted to you.
   ```

   Under build-verify, every verifier at once too, on the plugin's `verifier` agent
   (`subagent_type: "swarmstorm:verifier"`), no `isolation`:

   ```markdown
   You are verifier `<vN>` of task swarm run `<run id>` on `<repository>`, protocol build-verify, focus `<focus>`, ports `<range>` for your own instance<, one instance only: lock `app:<name>`>. **Source**: <the `verify-<app>-<focus>` skill | instructed: each verify phase's message gives your steps>. Join now; each verify phase's message scopes your pass.
   ```

## Giving work

- **One post per task, to one worker**: `$S post "@w2 <the task>" --as <topic>/orchestrator`. A
  task says what to do, the context the worker lacks (the files, the decisions already taken,
  what not to touch), and **done when** (a command that exits 0, or what is observed).
- **Split so workers do not collide**: different files where you can; two tasks on one file are
  one task, or the workers settle it on the board.
- **The person keeps giving work**: each request becomes tasks for the workers waiting; a
  worker's report frees it for the next.

## A report

Read it; re-run its done-when yourself on the merged branch before you tell the person it is
done. A finding is weighed as the `orchestrate` skill's *Findings* says. Tell the person, in a
few lines, what landed.

## Under build-verify

The phases, the verify message, the judged table and the loop are the protocol's: the
`orchestrate` skill's `references/protocols/build-verify/protocol.md`, read before the first
phase. A task is posted as above; build 1 holds the work asked, every later build the judged
table's rows that stand.

## Closing

When the person says so, or propose it once every worker waits and nothing is left: `$S close
--run <run>`. Then the summary: what each task delivered, the branch and its commits, and the
choice that is the person's, a pull request or a merge into their branch. Never delete a branch.
