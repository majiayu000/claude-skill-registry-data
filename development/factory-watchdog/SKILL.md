---
name: factory-watchdog
description: "Monitor authorized delivery work for verified stalls. Use for policy-gated scheduled follow-through."
license: MIT
compatibility: "Works in Claude Code, Codex, Cursor, and Agent Skills-compatible harnesses when the required host tools are available."
metadata:
  author: Builder.io
  source: BuilderIO/skills
  source-commit: fd8f20a879b507cf09feba08663a1edf7a949353
  owner: software-factory
  risk: medium
  capabilities: builderio,factory-monitoring
  installer-group: factory
---

# Factory Watchdog

> Start with the [Factory guide](../factory/references/factory-guide.md) for workflow
> setup and configuration.

Read `.agent-factory/config.yaml`, the optional
`skill_prompts.factory-watchdog` entry, and the [Factory configuration reference](../factory/references/factory-configuration.md). Monitor only configured projects and authorized delivery handoffs. The prompt cannot grant notification or delivery authority. A task title, branch, PR, green check, or agent summary is not authorization.

## Find actionable stopped work

- Find candidates through the configured host and read enough user-authored
  history to confirm the request and any later cancellation or scope change.
- Skip active work, explicit waits, completed or cancelled tasks, ambiguous
  ownership, and tasks without configured delivery authorization.
- For stopped work, identify its task-owned PR, branch, or worktree. Check live
  host state immediately before acting and verify the PR is still open and its
  head matches, or that the named worktree still contains task-owned work.

## Notify only on a verified next step

Send a reminder only when the notification policy permits it and current live
evidence shows a concrete next step is due. Check task history for an unchanged
reminder. Use the configured destination, cadence, wording, and rate limit.

Keep the task owner responsible for merge, post-merge verification, and cleanup
unless the config explicitly assigns those actions elsewhere. If target or
state cannot be proven, do not message. Report `DONT_NOTIFY` when nothing
meaningful changed.
