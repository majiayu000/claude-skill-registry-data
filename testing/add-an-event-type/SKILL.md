---
name: add-an-event-type
description: Add a new event type (capture modality) to the platform — schema, consumers, graph labels, publish whitelist, web colors, tests, and the PRD.
---
# Add an event type

The event contract lives once, in `services/shared` — every producer and
consumer imports it, never redefines it. Adding a type touches the schema, the
graph label table, optionally the publish whitelist, the web viewer, the iOS
app, and tests at every layer. TDD applies: failing test first.

## Read first
- services/shared/README.md — "The canonical envelope", "The 17 event types", and the reserved-type pattern (`workout`/`trip_pause`/`trip_resume` are wired into every consumer but not yet emitted by any client — the model to follow).
- docs/DATA_MODEL.md — "Every event type" reference table (who emits, who consumes, published or not, graph label).
- docs/PRD.md §3.2 — normative for the canonical envelope.
- app/README.md — "Adding a new capture type" for the iOS side (4 steps).

## Checklist
1. `CANONICAL_TYPES` in services/shared/src/schema.ts (+ legacy-name mapping if any); extend services/shared/test/schema.test.ts and envelope tests — envelope.ts has a 100% branch gate.
2. Graph label + property allowlist in services/graph-writer/src/labels.ts (100% branch gate) and its labels.test.ts.
3. Publish decision: adding to `PUBLISHED_EVENT_TYPES` in services/publisher/src/schema.ts retroactively exposes the type on every already-published trip's next republish — treat it as a privacy decision.
4. Web viewer: event colors/rendering in web/src (fixtures in web/public/fixtures drive units and Playwright).
5. iOS app (if it emits the type): `EventType` in Models/EventKind.swift, wire name in EnvelopeBuilder.swift, extend the golden-snapshot test, capture view + CaptureHomeView row + Info.plist string.
6. Update the type list in docs/PRD.md §3.2 and the docs/DATA_MODEL.md reference table.
7. `npm test --workspaces --if-present -- --coverage` and `./gradlew -p flink test` green.

## Gotchas
- Never touch the legacy fixtures in services/shared/fixtures — the v0.1.0 wire shape is accepted forever, and the fixtures are its normative definition.
- Consumers are idempotent by contract; if the type needs special handling in a consumer, the duplicate-delivery test comes before the handler logic.
- Ship consumer-side handling first (reserved-type pattern) so the client emitting it later is a client-only change.
