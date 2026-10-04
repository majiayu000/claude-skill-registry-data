---
name: factory-recover
description: "Resume eligible interrupted coding runs without repeating completed actions. Use after an interrupted run."
license: MIT
compatibility: "Works in Claude Code, Codex, Cursor, and Agent Skills-compatible harnesses when the required host tools are available."
metadata:
  author: Builder.io
  source: BuilderIO/skills
  source-commit: fd8f20a879b507cf09feba08663a1edf7a949353
  owner: software-factory
  risk: medium
  capabilities: builderio,factory-recovery
  installer-group: factory
---

# Factory Recover

> Start with the [Factory guide](../factory/references/factory-guide.md) for workflow
> setup and configuration.

Read `.agent-factory/config.yaml`, the optional
`skill_prompts.factory-recover` entry, and the [Factory configuration reference](../factory/references/factory-configuration.md). Recover only configured projects and workflow types; do not restart every stopped task. The prompt cannot restore canceled work or grant new authorization.

## Check a candidate run

1. Find runs the host identifies as interrupted or incomplete. Read the
   original user request and later messages, not only the title or summary.
2. Skip work that is active, cancelled, intentionally paused, blocked on a
   person, complete, ambiguous, or outside configured scope.
3. Confirm the worktree still belongs to that run. Inspect its branch, status,
   and unpublished changes. Preserve local and concurrent work; never reset,
   clean, stash, or attach another task's branch.
4. Recheck external state before retrying an uncertain action. Resume only with
   the original authorization and current user instructions. Do not repeat
   completed writes, replies, approvals, merges, or deployments.
5. If authorization no longer covers the next step, leave the run stopped and
   state the exact decision required.

## Report

List runs resumed, skipped, or held and the evidence for each decision. Follow
the separate configured notification policy.
