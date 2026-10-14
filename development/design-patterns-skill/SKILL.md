---
name: design-patterns-skill
description: Apply GoF design patterns (Creational, Structural, Behavioral) appropriately without over-engineering - language-agnostic with practical examples
license: Apache-2.0
compatibility: opencode
category: Code Quality
---

## What I do

Apply design patterns where they fit — and refuse to force them. Patterns solve problems you HAVE, not problems you MIGHT have; let them emerge from refactoring, not upfront design.

## When to use me

- A design problem you recognize (repeated type-switching, behavior addable without modification, complex object construction)
- You're tempted to add a pattern and want a second opinion on whether it's warranted

## House Learnings

#### Learning: `zai-client-class`
Instead of per-endpoint adapters, wrap all API endpoints in a single client class handling key resolution, base URL config, and error mapping centrally (combined Adapter + Facade): one `ZaiClient` with `_headers()`/`_request()` internals and typed endpoint methods (`search`, `summarize`, `analyze`); missing `ZAI_API_KEY` raises at construction.

#### Learning: `enum-strategy-resolution`
Dispatch via `str` + `Enum` with a default member: one dispatch point, Open/Closed-compliant (new strategies need no dispatcher edit), callers pass raw strings or enum members interchangeably. Unknown values fall through to the `UNKNOWN` member's handler instead of raising.

### Learning: `atomic-sql-update-race-free-transition`
Use a single `UPDATE ... WHERE expected_state RETURNING cols` as an optimistic lock — the `WHERE` guards the transition, `RETURNING` fetches columns in one round-trip, losers re-read and reconcile idempotently. Never read-then-write state transitions (two workers both commit, duplicate side effects).
Detection: `rg 'get_.*\(|fetch_.*\(' --type py -A 10 | rg 'status|state' | rg 'commit|save|update'`

### Learning: `double-checked-locking-async-refresh`
Async token/cache refresh must use double-checked locking (unlocked check → acquire lock → RE-CHECK → refresh only if still invalid) so exactly ONE caller hits the upstream provider per expiry window; hot path stays lock-free. Pair with `time.monotonic()` (NTP-immune) and proactive refresh at 80% of TTL.
Detection: `rg 'async with self\._lock|async with.*Lock' --type py -A 15 | rg 'await.*refresh|await.*fetch' | rg -v 'if.*stale|if.*expired'`

#### Learning: `zai-node-mixin`
Prefer mixins over deep inheritance for selectively adopted behaviors: a `CacheMixin`/`RetryMixin` composing into `DataPipeline` respects `__init_subclass__`, avoids fragile-base-class coupling, and subclasses pick only what they need.

> Removed 2026-09: GoF catalog with per-pattern code examples (Singleton/Factory/Builder/Adapter/Decorator/Proxy/Strategy/Observer/Template Method/Command), pattern-selection table, anti-pattern table, steps/best-practices/verification ceremony — textbook the model knows; the five codified learnings above are this config's real additions.
