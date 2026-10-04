---
name: apple-authoritative-game-systems
description: Design or review server-authoritative Apple games. Use when implementing deterministic state, Game Center, App Attest, StoreKit, offline play, or anti-cheat.
license: MIT
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-30"
  last-reviewed: "2026-08-30"
  apple-docs-reviewed: "2026-08-30"
---

# Apple Authoritative Game Systems

## Invariants

- The server alone commits currency, inventory, ownership, progression, time, rankings, and entitlements. Client state, clocks, pushes, and generated output are untrusted.
- Commands are typed, authorized, transactional, and idempotent: identical ID/semantics returns its stored result; changed semantics conflict.
- Simulation is deterministic, versioned, replayable, and explainable from recorded inputs, named randomness, and server time.
- An LLM or Foundation Model may phrase facts or propose bounded typed intent; it never writes state, chooses unbounded rewards, or joins financial transactions.
- StoreKit purchase, verified server grant, and spend are separate. Bind signed transaction evidence to the authenticated internal player with `appAccountToken` or an equally strong server-verified account correlation. Server-catalog rewards grant once; spending awaits the receipt.
- Game Center maps to an internal player/session. App Attest uses fresh challenges, binds actor and command semantics, and atomically serializes each key counter.
- Apple services add evidence, not authority; failure, replay, unsupported service, and account change need explicit policy.
- Offline/background execution is opportunistic, interruptible, and may never run. Persist immutable intent, not results; make retries duplicate-safe and reconcile server receipts in the foreground.

## Route only what applies

| Task | Read |
| --- | --- |
| Authority, simulation, settlement, or model narration | [authority-and-simulation.md](references/authority-and-simulation.md) |
| Commands, identity, App Attest, networking, or offline reconciliation | [contracts-and-integrity.md](references/contracts-and-integrity.md) |
| StoreKit purchase followed by valuable spending | [purchase-and-spend.md](references/purchase-and-spend.md) plus contracts and integrity |
| Test or release evidence | [test-strategy.md](references/test-strategy.md) |
| Apple API behavior or availability | [apple-documentation.md](references/apple-documentation.md), then Xcode DocumentationSearch |

Do not load unrelated references.

## Apply and verify

Map each fact to one writer. Keep external calls outside locks. Test replay, conflicting retries, contention, process death, invalid evidence, account changes, purchase ordering, and relaunch. Report trust violations and the smallest verified fix.

Before changing `apple-docs-reviewed`, rerun Xcode DocumentationSearch and follow [the date rules](references/apple-documentation.md).

## Review

- Last updated: `2026-08-30`
- Last reviewed: `2026-08-30`
- Apple documentation reviewed: `2026-08-30`

Game Center, App Attest, StoreKit, and authoritative game-system integration guidance were reviewed using Xcode MCP `DocumentationSearch`.

[Apple documentation evidence](references/apple-documentation.md)
