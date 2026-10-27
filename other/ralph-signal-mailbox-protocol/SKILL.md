---
name: ralph-signal-mailbox-protocol
description: Ralph-v2 live signal mailbox protocol for polling, ack handling, broadcast quorum, and signal routing. Use when a Ralph agent needs to process `signals/inputs`, write ack files, route target-specific signals, or finalize broadcast signals safely.
---

# Ralph Signal Mailbox Protocol

This skill contains the authoritative live-signal mailbox rules for Ralph-v2 agents.

## Signal Artifacts

- Inputs: `.ralph-sessions/<SESSION_ID>/signals/inputs/`
- Acks: `.ralph-sessions/<SESSION_ID>/signals/acks/`
- Processed: `.ralph-sessions/<SESSION_ID>/signals/processed/`

## Recognized Signal Types

- `STEER`
- `PAUSE`
- `ABORT`
- `INFO`

## Target Namespace

- `ALL`
- `Orchestrator`
- `Executor`
- `Planner`
- `Questioner`
- `Reviewer`
- `Librarian`

Never encode runtime or version in `target`.

## Poll-Signals Routine

1. Ensure `signals/acks/` exists.
2. Read `signals/inputs/` in timestamp order.
3. For each candidate signal, inspect `type` and `target` before moving it.
4. Handle `target: ALL` by writing or refreshing `signals/acks/<SIGNAL_ID>/<Agent>.ack.yaml` and leaving the source signal in place.
5. Archive a broadcast signal only after ack quorum is satisfied for all required recipients.
6. For targeted signals:
   - `ABORT` blocks work immediately.
   - `PAUSE` waits.
   - `STEER` changes execution context.
   - `INFO` injects additional context.
7. Route target-specific signals to the named subagent by buffering context and moving the original file to `signals/processed/`.

## Broadcast Invariant

- The first agent that reads `target: ALL` never archives it.
- Every recipient writes exactly one ack file per signal ID.
- Only the Orchestrator archives the broadcast signal after quorum is met.

## Completion Hygiene

Before a session ends, the Orchestrator should sweep remaining `target: ALL` signals and archive them with either:

- `delivery_status: delivered`
- `delivery_status: partial` plus `unacked_agents`