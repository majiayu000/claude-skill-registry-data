---
name: clarila-session
description: "Bind, inspect or continue the existing Codex session responsible for an issue. Use for native session status, queued and running turns, late events after a stop, and resuming work with its original context and ownership."
---

# Preserve the native session identity

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Resolve the shared workflow and current bound host/session/workspace. Inspect actual native session state before routing.
2. Bind the current Codex chat only using its real session identity. If another implementation session is active, deliver the requested follow-up there or retain the conflict.
3. For a verified owner instruction explicitly requesting a separate new Codex chat, use an available native creation tool with the registered project/worktree. Otherwise continue in the current chat. The Clarila control service owns the Codex contexts it starts for issues; route follow-ups to it with `@Clarila continue <message>` in the issue thread rather than opening a second context, and verify its actual native identity before reporting state. Retain existing workflows and unknown operations without replacement.
4. Continue the exact session through supported native messaging or resume. Queue acceptance and command exit zero do not prove execution; codex queue --resume may warn without resuming.
5. Expose working, waiting, idle, finished and unknown honestly. Pause/stop only through a supported exact-target control and confirm it. Never edit native session databases or silently transfer ownership.

PR-card actions route through the same coordinator and registered issue context. An assessment request invokes its actual separate Verify/Review context; a repair continues the existing implementation writer. Manual needs an owner continuation after a run settles. Automatic review follow-ups require an explicit, separate repository setting; ordinary Auto does not enable them. Preserve the durable repair-round budget and any unresolved PR action or workflow fence.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. Use the current host’s native tools during the invoked workflow.

## Deliverable

Return the bound native session, observed execution state, delivery receipt and any handoff/control limitation.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.

Read the [operation-specific reference](references/resume.md) when performing this responsibility.

When reconstructing local issue/worktree context, use the read-only resume/list helpers in the [local issue workflow](../clarila/local-workflow/guide.md). Native session identity and resume controls remain separate from Git context.
