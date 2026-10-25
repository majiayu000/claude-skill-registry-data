---
name: ls-herdr-task-routing
description: "Start here for Herdr (Herder) pane, task, remote machine, deployment, upgrade, or connection work. Resolve context and provenance, then load the relevant Herdr specialist."
metadata:
  version: "1.1"
  compatibility: "LocalSetup, Python 3.12+, reviewed Herdr v0.9.5 API; Linux, macOS, and WSL2."
---

# Herdr: start here

Use this master skill when the task calls for Herdr control, a Herdr-managed
terminal, or Herdr remote setup. Being inside Herdr alone does not authorize
opening terminals, starting agents, changing machines, or running commands.
Honor the active client's mode and the target repository's restrictions.

## Resolve once, then work

Use `localsetup herdr --help` for the installed LocalSetup interface and
`herdr --help` for native syntax. Never run bare `herdr` to discover commands;
it launches the interface. Do not probe mutating subcommands with missing args.

For pane work, bind the calling pane's inherited Herdr context or an explicitly
selected existing socket/session. Never select a target from UI focus, terminal
title, example IDs, or another client's current selection. Remote setup may
start outside Herdr when the user named the target and requested setup; it must
not inspect an unrelated focused session.

Read only the needed specialist:

- Create, size, move, or clean up panes: [layout](localsetup://package/ls-herdr-pane-layout/SKILL.md).
- Run commands, inspect logs, wait, cancel, or coordinate a requested agent:
  [tasks](localsetup://package/ls-herdr-command-tasks/SKILL.md).
- Connect, tunnel, deploy, configure, upgrade, or restart a remote:
  [remote](localsetup://package/ls-herdr-remote-connect/SKILL.md).
- Check upstream changes, compatibility, or refresh the suite:
  [provenance maintenance](localsetup://package/ls-herdr-provenance-drift/SKILL.md).

Use the shared tool through `localsetup herdr` or
`localsetup://tool/herdr_ops.py`; specialists do not implement their own
targeting, resizing, transport, or retry logic.

For repository work, pass the existing task's absolute private state directory
with `--state-dir`. Reuse its returned owner and operation handles across
substeps and resumes instead of creating a parallel per-agent state tree.

## Keep it smooth

The user's task authorizes ordinary necessary owned-pane work. Preserve focus,
reuse verified context and existing authorization, and proceed to the outcome.
Do not ask permission again for routine reads, waits, owned-pane allocation,
approved connections, or reconnects. A prerequisite deployment needs one scoped
decision only when deployment was not already requested. Ask again only for a
new target/scope, real authentication, or interruption beyond existing authority.

Only the controller may access a reserved operations pane (`<repo>-sudo` or
`<repo>-<exact-host-alias>-sudo`, with the legacy `sudo` label still protected).
Selection includes the native parent, endpoint and live controller binding;
identical labels under other agents are distinct resources. Do not pass pane
output to workers or treat a command-line option as controller authority. Honor
stronger repository-specific controller restrictions for other panes as well.

## Provenance and compatibility

The canonical [source manifest](references/upstream/provenance.json) records the
release and its immutable commit separately from the independently reviewed
`source_watch.commit` baseline and watched-file hashes, alongside licensing and
specialist coverage. `source.commit` remains the release pin; it does not advance
when a different source revision is reviewed.
[Upstream guidance](references/upstream/SKILL.source.md) and
[bundled schema](references/upstream/schema.json) are preserved evidence, not a
second workflow owner. Upstream retains its [Apache-2.0 license](references/upstream/LICENSE).

Distinguish the reviewed watched-source baseline, tagged release, installed
client, client-bundled schema, and live server. Compatible versions need not be
identical. An available newer release does not invalidate working supported
operations or authorize a host upgrade. Do not claim a client's schema proves
remote capabilities.

Submission is not completion. On a lost mutation response, reconcile the
original operation read-only; do not resend it or create a replacement pane.
Use the returned operation record and specific next action.
