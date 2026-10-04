---
name: dota-gsi
description: >
  Expert guidance for Dota 2 Game State Integration in this project.
  Use whenever implementing, modifying, debugging, testing, or discussing
  GSI configuration, the HTTP listener, payload parsing, PlayingGameState,
  SpectatingGameState, Map/Player/Hero/Items/Abilities/Buildings state,
  MatchState, domain events, partial payloads, state diffing, stale state,
  reconnections, fixtures, or the GSI replay simulator.
---

# Dota 2 Game State Integration

Apply this skill whenever working with Dota 2 GSI — configuration,
ingestion, parsing, normalization, or testing.

## Ground truth warning

Valve has never published an official GSI spec. Every field name in this
skill and its reference files is reverse-engineered from community
libraries and observed payloads, not a Valve contract. That means:

- **Never invent GSI fields.** If a field isn't documented in
  `references/payload-structure.md` or confirmed in a captured fixture,
  don't assume it exists or guess its shape.
- **Verify uncertain fields** against current community GSI documentation
  (e.g. actively-maintained GSI client libraries) or, better, an actual
  captured payload, before relying on them. `references/payload-structure.md`
  flags which sections are solid vs. which need per-project verification
  (`events`, `roshan_state` enum values, and `draft` fields are the
  weakest-verified areas as of this skill's writing).
- Treat GSI as an inherently unreliable feed (see "Known reliability
  issues" in `references/payload-structure.md`) — connections can be
  delayed, drop, or silently stop sending updates. Design ingestion code
  assuming this will happen, not as an edge case.

## Architecture

```
Raw GSI JSON (HTTP POST)
→ GsiListener              (HTTP endpoint, request validation)
→ GsiPayloadParser         (JSON → typed payload, Playing vs Spectating)
→ GsiNormalizer            (typed payload + diff → MatchState mutation)
→ MatchState                (canonical, current, normalized game state)
→ DomainEvents              (derived signals: hero died, item purchased...)
```

Each stage has a narrow job. Don't let normalization logic leak into the
listener, and don't let strategic reasoning leak into the normalizer —
see "Responsibilities" below and `dota-domain`/`dota-fairplay` for what
belongs above this layer.

## Responsibilities

The GSI layer may:

- listen for and receive HTTP POST payloads;
- validate payload structure/auth token;
- parse JSON into typed `PlayingGameState` / `SpectatingGameState` models;
- diff incoming payloads against current `MatchState` (using the payload's
  own `previously`/`added` blocks, see `references/state-diffing.md`);
- normalize/merge partial payloads into the canonical `MatchState`;
- detect state transitions and produce `DomainEvents`;
- detect stale/disconnected state and surface that as a signal.

The GSI layer must NOT:

- recommend items or strategy (that's `dota-domain` / recommendation layers);
- decide what's fair to use live (that's `dota-fairplay` — GSI ingestion
  exposes raw state; FairPlay classification happens at the boundary
  where that state is consumed, and `SpectatingGameState` fields must
  never be wired into a live player-facing feature — see
  `references/spectator-vs-playing.md`);
- call the UI directly;
- access OpenDota or other external match APIs;
- access hidden/fog-of-war game information (not exposed by GSI at all
  for a playing client — see `references/spectator-vs-playing.md` for why
  this matters more for spectator mode).

GSI is infrastructure. It answers "what does the game currently say," not
"what should the player do about it."

## Where to go next

This file stays intentionally short — the following reference files carry
the substance. Read the one relevant to the task at hand:

- **`references/configuration.md`** — writing/modifying the `.cfg` file:
  `uri`, `timeout`, `buffer`, `throttle`, `heartbeat`, the `data` section
  flags, and the optional `auth` token.
- **`references/payload-structure.md`** — the JSON payload shape: top-level
  sections (`provider`, `map`, `player`, `hero`, `abilities`, `items`,
  `buildings`, `draft`, `wearables`, `events`), what's solidly verified vs.
  needs fixture confirmation, and known reliability issues.
- **`references/spectator-vs-playing.md`** — how `PlayingGameState` and
  `SpectatingGameState` differ structurally, why spectator payloads expose
  materially more information, and the fair-play implication of that gap.
- **`references/state-diffing.md`** — how the `previously`/`added` blocks
  work, why payloads are partial by design, and how to normalize a partial
  payload into a persistent `MatchState` without losing unrelated fields.
- **`references/stale-state-and-reconnection.md`** — detecting a stalled
  feed via `heartbeat`, handling reconnects, and what `MatchState` should
  do while data is stale (don't silently keep serving last-known-good state
  as if it were current).
- **`references/fixtures-and-testing.md`** — required fixture format,
  where fixtures live, what every GSI change must test, and the GSI
  replay simulator (feeding a sequence of captured/fixture payloads
  through the pipeline at controlled pace to reproduce real match flow
  for tests and manual debugging).

## Testing requirement

Every GSI change — new field, new normalization rule, new domain event —
requires:
1. a fixture (captured or hand-built) demonstrating the payload shape
   involved, see `references/fixtures-and-testing.md`;
2. a test exercising the parser/normalizer against that fixture;
3. `dotnet test` passing before the change is considered complete.

A change without a fixture is a change nobody can verify still works when
the next person touches this code — GSI's own unreliability (see
`references/payload-structure.md`) makes this more important here than in
most code, not less.
