---
name: ho
description: Hand off the current work to a fresh agent in an Orca worktree or an adjacent terminal. Use when Prateek asks to hand off, or a skill's step says to run /ho.
argument-hint: "[--here | --host <name>] [--agent <id>] [--base <ref> | --stack] [--name <slug>] [--attach <path>]... [--] [<subject>] [; <instructions>]"
---

# Hand off to Orca

Write a handoff brief for a fresh agent, launch that agent through Orca, point it
at the brief, and stop. The receiving agent owns the work from then on; this
session neither supervises nor waits.

## Parse the invocation

| Argument | Default | Meaning |
| --- | --- | --- |
| `<subject>` | inferred from the conversation | What the next agent works on. |
| `; <instructions>` | none | Everything after the first `;`, passed verbatim to the receiver. |
| `--here` | off | Adjacent terminal in the current worktree. No new checkout. |
| `--host <name>` | this machine | Orca host by name or id, from `orca host list --json`. |
| `--agent <id>` | `claude` | Orca agent id (`claude`, `codex`, `pi`, ...). |
| `--base <ref>` | repo default base | Git base for the new worktree. |
| `--stack` | off | Branch from the current branch. |
| `--name <slug>` | slug of the subject | Worktree name. |
| `--attach <path>` | none | Extra file the brief references. Repeatable. |

`--here` excludes `--host`, `--base`, and `--stack`, and `--base` excludes
`--stack`. Resolve a conflict with the user before doing anything else. Without
`--base` or `--stack`, the handoff is independent: no parent lineage, repo
default base. The brief carries the current branch's context.

The handoff **id** is `<name>-<UTC yyyymmddThhmmss>`. It names the brief
directory and, on remote, the transport branch, so repeated handoffs never
collide.

## Resolve the target

Invoke the `orca-cli` skill and load its full guide. Take every Orca command and
flag from that guide or from `--help`. The guide's Full Handoffs section governs
launch and delivery. This skill decides only what it leaves open.

Classify the target as exactly one of the following:

- **here**: `--here`. The receiver runs as a new terminal in the current
  Orca-managed worktree. If the current directory is not one, stop and say so.
- **local**: a new worktree on this machine. `--stack` sets the current worktree
  as parent and the current branch as base.
- **remote**: a new worktree on another host. Find `--host` in `host list`,
  which reports two kinds. A paired Orca server resolves to
  `runtime:<environment id>` (the id from `orca environment list`, never the
  name). An SSH target resolves to `ssh:<id>`. Pass that host id as `--host` to
  the commands whose `--help` lists it (`project setups`, `worktree create`). For
  commands without `--host`, such as `terminal wait` and `terminal send`, route
  a paired server with the `--environment` selector `host list` reports. An SSH
  target's terminals belong to this machine's runtime and need no routing flag;
  that path is untested. The project needs a `ready` setup on the host. If it has
  none, stop with that blocker, before pushing anything, and name the setup
  commands `project --help` offers.

A remote `--stack` has no parent lineage, because the parent lives on another
host. Its base is `origin/<branch>`, which the transport step pushes after its
secret scan.

The step is complete when the target class, host id, repo or project selector,
lineage, and base are all resolved, or a blocker is reported.

## Write the brief

Save a handoff brief to `${XDG_STATE_HOME:-$HOME/.local/state}/ho/<id>/brief.md`.
Resolve the directory to an absolute path once and use it for retries. The brief
must give a fresh agent enough context to take over:

- State the subject, the next action, completed work, open questions, and blockers.
  Put the user's instructions verbatim under their own heading.
- Name the source worktree, branch, and HEAD commit. Say which work is unpushed
  or uncommitted and how the receiver can access it.
- Under `Transfer files`, list each file the receiver needs by absolute path
  and purpose. Include `--attach` files and relevant screenshots, logs, or
  traces. Point to existing plans, specs, commits, and diffs instead of
  repeating them.
- Name useful skills the receiver can invoke. Redact keys, passwords, tokens,
  and personal information from the brief.

A local receiver can read the source worktree directly. For a remote receiver,
the transport step copies needed files and rewrites the brief's paths. The brief
is complete when the next action and every needed artifact are identified.

## Choose the transport

The **transport** gets the brief and its files to where the receiver can read
them. Try these routes in order. Use the first one that works; each later route
shares the work more widely.

1. **In place**: here and local targets. The receiver reads the brief directory
   and source paths directly.
2. **Direct copy**: a remote host this machine reaches over SSH. Copy the bundle
   into the same state directory on that host.
3. **Transport branch**: an orphan branch `ho/<id>` on `origin`, after a
   secret scan.
4. **Ask the user**: when every route has failed and there are files to move.

If the receiver needs nothing but the brief, send its text in the prompt and
skip the transport. For routes 2 through 4, follow
[remote transport](references/remote-transport.md). Finish this step only after
the chosen route has delivered the brief or made a pinned transport commit
fetchable. If the route needs the user's choice, stop and resume after the
choice and delivery. Launch only when the brief is ready for the receiver.

## Launch

Keep the prompt short. Point it at the brief's absolute path on the receiving
machine, or give the transport branch's bootstrap line. Then:

1. Start the agent without a prompt. For **here**, create a terminal in the
   active worktree running `--agent`. For **local** and **remote**, use
   agent-first worktree creation with `--name` and `--agent`, plus the resolved
   host, lineage, and base.
2. Take the agent handle the guide names, and wait for `tui-idle`.
3. Send the prompt to that handle once. Never resend on silence; a receipt
   warning that no turn start was observed still counts as delivered.

The handoff is complete when the send receipt reports `accepted: true`. Then
report the following and stop:

- The worktree id (or, for here, the current worktree).
- The agent terminal handle.
- The transport route, the brief path, and for the transport branch, its pinned
  commit.
- Whether the brief carries unpushed or uncommitted work, and how.
- For local and here: the brief points into the source worktree, so that
  worktree stays in place until the receiver has read what it needs.
- For the transport branch: the secret-scan result.

## Retry

Record each confirmed stage as it happens: the id, the pushed commit, the
worktree id, the agent handle, and the send request id. A retry resumes after
the last confirmed stage with the same id, reusing everything already created.
It never creates a second worktree or agent, and never replaces a pushed
transport commit. For an ambiguous send, follow the guide's `--retry-request`
procedure. If the receiver never reaches a ready state, report the handoff as
not started and keep everything for the retry.

## Authorization

`/ho` authorizes these actions and nothing more:

- Creating the worktree or terminal.
- Writing `${XDG_STATE_HOME:-$HOME/.local/state}/ho/<id>/`.
- On remote only: copying the bundle into the receiving host's
  `${XDG_STATE_HOME:-$HOME/.local/state}/ho/<id>/` over SSH, pushing
  `ho/<id>`, and with `--stack`, fast-forward-pushing the current branch after
  its secret scan.
- The receiver deleting exactly `ho/<id>` after verifying its extraction.

It authorizes no commits to the working branch, no merges, and no cleanup of the
source worktree.
