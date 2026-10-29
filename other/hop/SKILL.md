---
name: hop
description: Pause current work and hand it to a fresh Orca agent with a durable resume point.
argument-hint: "[--here | --host <name>] [--agent <id>] [--base <ref> | --stack] [--name <slug>] [--attach <path>]... [--] [<subject>] [; <instructions>]"
disable-model-invocation: true
---

# Hop to Orca

Stop the current work at a safe boundary, record a checkpoint, and hand it to a
fresh agent through Orca. The receiver resumes the work; this session stops
after Orca accepts the prompt.

Read [ho](../../../utils-agent/skills/ho/SKILL.md) for argument parsing, target selection, transport,
launch, and retry. Follow those sections in order. Replace its "Write the brief"
and "Authorization" sections with the instructions below. Use its `ho/<id>`
state directory and transport branch so both skills share one delivery method.
Read [remote transport](../../../utils-agent/skills/ho/references/remote-transport.md) only for a remote
target.

This skill requires `utils-agent:ho`. If your client caches plugins separately,
locate that skill in its catalog and resolve its references from its directory.

## Pause and checkpoint

Finish the current atomic step or back out of it. Start no new work, and stop
nested agents that belong to this task. Inspect the source worktree before
committing. Make one `wip:` commit containing only this task's uncommitted
changes, if any. Record unrelated dirty paths in the note. If task-owned and
unrelated changes cannot be separated safely, stop and report the blocker. Do
not push merely to pause.

For a remote target with unrelated dirty paths, create a detached checkout at
the checkpoint HEAD outside the handoff bundle, under
`${XDG_STATE_HOME:-$HOME/.local/state}/hop-staging/<id>`. Use `git worktree add
--detach` and confirm that its HEAD matches the checkpoint and its tree is
clean. On a retry, reuse it only if both checks still pass. Run `ho`'s Git
transport commands from this checkout and copy repo-relative files from it.
Copy explicit `--attach` artifacts from their named paths after inspection.
Keep the original worktree and its unrelated dirty paths unchanged. Record the
staging path as sender-side retry state in the note and final handoff report.

Write the resume note to the `brief.md` path from `ho`. Include:

- The subject and the user's instructions verbatim under their own heading.
- The goal, decisions already made, completed work, current state, open
  questions, and blockers. Name the next work action after any transport
  restoration.
- The source worktree, branch, HEAD, checkpoint commit if made, and any dirty
  or unpushed work. Say what has been verified and what remains unverified.
- Under `Transfer files`, list only the artifacts the receiver needs, including
  `--attach` files. Give each path and its purpose. Keep unrelated dirty paths
  under `Sender state`; they are metadata, not files to send. Point to an
  available transcript or decision trail. For a remote receiver, put a local
  trail in `Transfer files` if it needs a copy. Do not repeat a plan, diff, or
  transcript in the note.

Redact keys, passwords, tokens, and personal information. Name useful skills
the receiver can invoke. The checkpoint is ready when a cold-start agent can
identify the current state and the first next action from the note and its
referenced artifacts.

## Resume on the receiving side

Prepare a short prompt that points to the note or gives the transport branch's
bootstrap command. Tell the receiver to read the note and any prior trail,
restore remote source state when the note requires it, inspect its worktree and
branch, compare completed work with pending work, and then start the recorded
work action. It must verify inherited claims on the real
artifact before treating the task as done. Ask it to report what it inherited,
what it had to redo, and the outcome.

Use `ho`'s transport and launch steps to deliver this prompt. Include the
checkpoint commit and any remaining dirty work in the final handoff report.
The handoff is complete only when Orca's send receipt reports `accepted: true`.

## Authorization

`/hop` authorizes one checkpoint commit containing only task-owned changes,
writing the handoff directory and clean staging checkout, and the Orca creation
and transport actions in `ho`. A remote transport may push only the refs
`ho` permits, after its secret scan. It authorizes no merge, PR, or cleanup
of the source worktree.
