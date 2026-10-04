---
name: offline-sync
category: mobile
description: Use when a screen must work without network or a mutation must survive a lost connection - local storage choice, the outbox pattern with idempotency keys, background replay, and how to test it with a fake clock and fake network.
---
# Offline and Sync

## Overview

Treat "offline" as a normal state, not an error condition: a screen that only works with a live connection is a defect on mobile. The hard part isn't detecting offline — it's making a queued mutation replay exactly once and keeping the UI honest about what's actually saved.

## Local store

Follow the repo's existing choice (drift/sqflite for Flutter, Room for Android, SwiftData/Core Data for iOS) — don't introduce a second local-storage mechanism alongside one that's already there.

## Outbox pattern

- Queue mutations in a local outbox table when offline; replay on reconnect.
- Every queued mutation carries a **client-generated idempotency key**, sent with the eventual request, so a retried replay (after a crash mid-sync, or a flaky connection that "succeeded" without the ack arriving) is deduplicated server-side instead of double-applied.
- Connectivity plugins (`connectivity_plus` and equivalents) report the state of the network *interface*, not whether the server is actually reachable — treat the server's response as the source of truth for whether a request succeeded, not the interface state alone.

## Background replay

- Android: `WorkManager` (native) or the `workmanager` plugin (Flutter) for replay that must survive the app being backgrounded or killed.
- iOS: `BGTaskScheduler` for background replay — register and schedule it, and test on-device since the simulator's background scheduling is unreliable.

## UI honesty

Show sync status explicitly per item — `pending` / `syncing` / `failed` — never render an unsynced change as if it were already saved. A spinner that never resolves is worse than an honest "failed, tap to retry."

## Conflicts

Pick **one** conflict rule per data type (last-write-wins, or an explicit user choice when both sides changed) and write it down in the task — don't leave it implicit in the code for the next person to infer.

## Reads degrade gracefully

Cached data with a staleness indicator beats a spinner that never resolves — show what you have, mark it as possibly stale, and update when the network returns.

## Testing

- Unit tests: a fake clock and a fake network/repository to drive queue → replay → ack deterministically, including the "replay happens twice" case to prove the idempotency key actually dedupes.
- On a local emulator: `adb shell cmd connectivity airplane-mode enable` / `disable` to exercise a real reconnect, not just a mocked one.

## Common Mistakes

- A screen that shows a blank/error state the instant the network drops, instead of cached data.
- A queued mutation with no idempotency key — a retried replay double-applies it.
- Trusting the connectivity plugin's "online" state as proof a request will succeed.
- A sync-status UI that doesn't distinguish `pending` from `failed`.
- Only testing airplane-mode-on; never testing the reconnect/replay path.

## Red Flags

- A mutation sent to the server with no client-generated key the server can dedupe on.
- "It works offline" verified only by reading the code, not by actually toggling airplane mode or a fake network.
- No written conflict rule for a data type that can be edited from two places.
