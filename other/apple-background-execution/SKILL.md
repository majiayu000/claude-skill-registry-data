---
name: apple-background-execution
description: "Design Apple background refresh, processing, background transfers, and expiration-safe work with durable progress, bounded execution, and truthful scheduling state."
---

# Background execution and resumable work

## Inputs

Identify the actual background mechanism, supported platform, required capabilities, launch registration, user benefit, durable operation state, and resource constraints.

## Rules

- **BG-001 — Scheduling is not a timer.** Submission or earliest-begin metadata is not a promise of execution time or successful delivery.
- **BG-002 — Persist resumable intent.** Store operation identity and checkpoints before relying on a process surviving suspension or termination.
- **BG-003 — Own expiration.** Install expiration handling promptly, cancel bounded work, checkpoint safely, and complete the task exactly once.
- **BG-004 — Use the right mechanism.** Choose refresh, processing, background transfer, or a permitted active-session mode for its documented purpose, not to keep the app alive indefinitely.
- **BG-005 — Test the real boundary.** Debugger-triggered launches and simulator success do not prove production scheduling or energy behavior.

## Workflow

1. Map foreground initiation to durable background state.
2. Register handlers and capabilities for the actual target.
3. Implement success, retry, expiration, and relaunch reconciliation.
4. Exercise interruption and report scheduling separately from completion.

## Verify

Test expiration during I/O and commit, duplicate launch, account revocation, restart, network loss, and low-resource conditions relevant to the mechanism.

## Output

Return the state machine, persisted checkpoints, completion policy, and actual scheduling/device evidence.

## References

- [Expiration, transfer, and recovery contracts](references/lifetimes-and-recovery.md).
